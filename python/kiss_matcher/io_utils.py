"""
Lightweight I/O utilities for point cloud files without heavy dependencies.
Replaces Open3D for basic file operations.
"""
import struct
import numpy as np


def read_pcd(pcd_path):
    """
    Read PCD file without Open3D dependency.
    Supports ASCII and binary PCD formats.
    """
    with open(pcd_path, 'r') as f:
        lines = f.readlines()

    # Parse header
    header_info = {}
    data_start_idx = 0

    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('VERSION'):
            header_info['version'] = line.split()[1]
        elif line.startswith('FIELDS'):
            header_info['fields'] = line.split()[1:]
        elif line.startswith('SIZE'):
            header_info['size'] = [int(x) for x in line.split()[1:]]
        elif line.startswith('TYPE'):
            header_info['type'] = line.split()[1:]
        elif line.startswith('COUNT'):
            header_info['count'] = [int(x) for x in line.split()[1:]]
        elif line.startswith('WIDTH'):
            header_info['width'] = int(line.split()[1])
        elif line.startswith('HEIGHT'):
            header_info['height'] = int(line.split()[1])
        elif line.startswith('VIEWPOINT'):
            header_info['viewpoint'] = [float(x) for x in line.split()[1:]]
        elif line.startswith('POINTS'):
            header_info['points'] = int(line.split()[1])
        elif line.startswith('DATA'):
            header_info['data'] = line.split()[1]
            data_start_idx = i + 1
            break

    # Read point data
    if header_info.get('data', '').upper() == 'ASCII':
        # ASCII format
        points = []
        for line in lines[data_start_idx:]:
            line = line.strip()
            if line:
                values = [float(x) for x in line.split()]
                # Extract x, y, z (first 3 coordinates)
                if len(values) >= 3:
                    points.append(values[:3])
        return np.array(points)

    elif header_info.get('data', '').upper() == 'BINARY':
        # Binary format - simplified implementation
        # Read remaining file as binary
        with open(pcd_path, 'rb') as f:
            # Skip to data section
            for _ in range(data_start_idx):
                f.readline()

            points = []
            num_points = header_info.get('points', 0)

            # Assuming float32 for x, y, z
            for _ in range(num_points):
                try:
                    x = struct.unpack('f', f.read(4))[0]
                    y = struct.unpack('f', f.read(4))[0]
                    z = struct.unpack('f', f.read(4))[0]
                    points.append([x, y, z])

                    # Skip additional fields if any
                    total_fields = len(header_info.get('fields', []))
                    if total_fields > 3:
                        f.read(4 * (total_fields - 3))

                except:
                    break

            return np.array(points)

    else:
        raise ValueError(f"Unsupported PCD data format: {header_info.get('data', 'unknown')}")


def read_bin(bin_path):
    """
    Read KITTI-style binary point cloud file.
    """
    scan = np.fromfile(bin_path, dtype=np.float32)
    scan = scan.reshape((-1, 4))
    return scan[:, :3]  # Return only x, y, z


def read_ply(ply_path):
    """
    Read PLY file without Open3D dependency.
    Supports ASCII and binary PLY formats.
    Only extracts x, y, z coordinates (ignores normals and other properties).
    """
    with open(ply_path, 'rb') as f:
        # Read header
        header_lines = []
        while True:
            line = f.readline()
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            line = line.strip()
            header_lines.append(line)

            if line == 'end_header':
                break

        # Parse header information
        vertex_count = 0
        format_type = 'ascii'
        properties = []

        for line in header_lines:
            if line.startswith('element vertex'):
                vertex_count = int(line.split()[-1])
            elif line.startswith('format'):
                format_type = line.split()[1]
            elif line.startswith('property float') or line.startswith('property double'):
                prop_name = line.split()[-1]
                properties.append(prop_name)

        # Find indices of x, y, z coordinates
        x_idx = properties.index('x') if 'x' in properties else None
        y_idx = properties.index('y') if 'y' in properties else None
        z_idx = properties.index('z') if 'z' in properties else None

        if x_idx is None or y_idx is None or z_idx is None:
            raise ValueError("PLY file must contain x, y, z coordinates")

        points = []

        if format_type == 'ascii':
            # ASCII format
            for _ in range(vertex_count):
                line = f.readline()
                if isinstance(line, bytes):
                    line = line.decode('utf-8')
                values = line.strip().split()
                if len(values) >= len(properties):
                    x = float(values[x_idx])
                    y = float(values[y_idx])
                    z = float(values[z_idx])
                    points.append([x, y, z])

        elif format_type == 'binary_little_endian':
            # Binary little endian format
            for _ in range(vertex_count):
                vertex_data = []
                for prop in properties:
                    # Assuming float32 for coordinates
                    value = struct.unpack('<f', f.read(4))[0]
                    vertex_data.append(value)

                x = vertex_data[x_idx]
                y = vertex_data[y_idx]
                z = vertex_data[z_idx]
                points.append([x, y, z])

        elif format_type == 'binary_big_endian':
            # Binary big endian format
            for _ in range(vertex_count):
                vertex_data = []
                for prop in properties:
                    # Assuming float32 for coordinates
                    value = struct.unpack('>f', f.read(4))[0]
                    vertex_data.append(value)

                x = vertex_data[x_idx]
                y = vertex_data[y_idx]
                z = vertex_data[z_idx]
                points.append([x, y, z])

        else:
            raise ValueError(f"Unsupported PLY format: {format_type}")

        return np.array(points)


def write_pcd(points, pcd_path):
    """
    Write points to PCD file in ASCII format.

    Args:
        points: numpy array of shape (N, 3) with x, y, z coordinates
        pcd_path: output file path
    """
    num_points = points.shape[0]

    header = f"""# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z
SIZE 4 4 4
TYPE F F F
COUNT 1 1 1
WIDTH {num_points}
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS {num_points}
DATA ascii
"""

    with open(pcd_path, 'w') as f:
        f.write(header)
        for point in points:
            f.write(f"{point[0]:.6f} {point[1]:.6f} {point[2]:.6f}\n")