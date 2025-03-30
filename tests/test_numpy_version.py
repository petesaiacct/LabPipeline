import numpy as np

def test_numpy_version():
    """Ensure the installed NumPy version meets minimum requirement."""
    major, minor, *_ = map(int, np.__version__.split("."))
    assert (major, minor) >= (1, 24), f"NumPy version is too old: {np.__version__}"
