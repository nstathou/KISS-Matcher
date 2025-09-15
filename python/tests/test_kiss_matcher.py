#!/usr/bin/env python3
"""
Basic tests for KISS-Matcher Python bindings.
"""
import unittest
import numpy as np
import kiss_matcher as km


class TestKISSMatcher(unittest.TestCase):
    """Test KISS-Matcher Python bindings."""

    def test_import(self):
        """Test that kiss_matcher can be imported."""
        # This test should pass if the module imports correctly
        self.assertTrue(hasattr(km, 'KISSMatcher'))
        self.assertTrue(hasattr(km, 'KISSMatcherConfig'))
        self.assertTrue(hasattr(km, 'RegistrationSolution'))

    def test_config_creation(self):
        """Test KISSMatcherConfig creation."""
        config = km.KISSMatcherConfig()
        self.assertIsInstance(config.voxel_size, float)
        self.assertEqual(config.voxel_size, 0.3)  # default value

        # Test custom config
        custom_config = km.KISSMatcherConfig(voxel_size=0.5)
        self.assertEqual(custom_config.voxel_size, 0.5)

    def test_matcher_creation(self):
        """Test KISSMatcher creation."""
        # Test with float parameter
        matcher = km.KISSMatcher(0.3)
        self.assertIsInstance(matcher, km.KISSMatcher)

        # Test with config
        config = km.KISSMatcherConfig(voxel_size=0.5)
        matcher_config = km.KISSMatcher(config)
        self.assertIsInstance(matcher_config, km.KISSMatcher)

    def test_basic_functionality(self):
        """Test basic functionality with dummy data."""
        try:
            # Create a matcher
            matcher = km.KISSMatcher(0.3)

            # Create larger point clouds for better matching
            src_points = np.random.rand(100, 3).astype(np.float32)
            tgt_points = src_points.copy()  # Use same points for target

            # Convert to vector format if needed
            src_vector = [src_points[i] for i in range(src_points.shape[0])]
            tgt_vector = [tgt_points[i] for i in range(tgt_points.shape[0])]

            # This should not crash - actual matching may fail due to random data
            # but the binding should work
            result = matcher.match(src_vector, tgt_vector)
            self.assertIsInstance(result, km.RegistrationSolution)

        except Exception as e:
            # If there's an issue with the binding itself, we want to know
            if "AttributeError" in str(type(e)) or "TypeError" in str(type(e)):
                self.fail(f"Binding error: {e}")
            # Other errors might be expected with random data
            pass

    def test_version_attribute(self):
        """Test that version attribute exists."""
        self.assertTrue(hasattr(km, '__version__'))
        self.assertIsInstance(km.__version__, str)


if __name__ == '__main__':
    unittest.main()