# MIT License
#
# Copyright (c) 2025 Hyungtae Lim and coauthors.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

include(FetchContent)

# Build FLANN as static library for easier wheel distribution
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)

FetchContent_Declare(
  flann
  GIT_REPOSITORY https://github.com/flann-lib/flann.git
  GIT_TAG master
  GIT_SHALLOW TRUE
)

# Configure FLANN options before FetchContent_MakeAvailable
set(BUILD_C_BINDINGS OFF CACHE BOOL "Build FLANN C bindings" FORCE)
set(BUILD_EXAMPLES OFF CACHE BOOL "Build FLANN examples" FORCE)
set(BUILD_TESTS OFF CACHE BOOL "Build FLANN tests" FORCE)
set(BUILD_DOC OFF CACHE BOOL "Build FLANN documentation" FORCE)
set(BUILD_MATLAB_BINDINGS OFF CACHE BOOL "Build MATLAB bindings" FORCE)
set(BUILD_PYTHON_BINDINGS OFF CACHE BOOL "Build Python bindings" FORCE)
set(USE_OPENMP ON CACHE BOOL "Use OpenMP" FORCE)

FetchContent_MakeAvailable(flann)

# Create alias for easier linking (FLANN creates flann_cpp_s for static)
if(TARGET flann_cpp_s)
  add_library(flann_cpp ALIAS flann_cpp_s)
  get_target_property(flann_include_dirs flann_cpp_s INTERFACE_INCLUDE_DIRECTORIES)
  set_target_properties(flann_cpp_s PROPERTIES INTERFACE_SYSTEM_INCLUDE_DIRECTORIES "${flann_include_dirs}")
elseif(TARGET flann_cpp)
  get_target_property(flann_include_dirs flann_cpp INTERFACE_INCLUDE_DIRECTORIES)
  set_target_properties(flann_cpp PROPERTIES INTERFACE_SYSTEM_INCLUDE_DIRECTORIES "${flann_include_dirs}")
elseif(TARGET flann)
  add_library(flann_cpp ALIAS flann)
  get_target_property(flann_include_dirs flann INTERFACE_INCLUDE_DIRECTORIES)
  set_target_properties(flann PROPERTIES INTERFACE_SYSTEM_INCLUDE_DIRECTORIES "${flann_include_dirs}")
endif()
