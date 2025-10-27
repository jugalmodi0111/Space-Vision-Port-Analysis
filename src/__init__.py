"""Aule Space Vision Challenge - Satellite Port Detection & Analysis.

Main package for rotation detection, rectification, and perspective synthesis.
"""

__version__ = "1.0.0"
__author__ = "Aule Space Vision Team"
__email__ = "team@aulespace.com"

from .pipeline import (
    detect_satellite_port_rotation,
    plan_camera_movements,
    solve_problem_part_c,
)
from .detectors import detect_circle, detect_squares
from .preprocessor import preprocess_image
from .rotation_calculator import _compute_rotation
from .homography import (
    rectify_image_with_homography,
    synthesize_angled_view,
)

__all__ = [
    "detect_satellite_port_rotation",
    "plan_camera_movements",
    "solve_problem_part_c",
    "detect_circle",
    "detect_squares",
    "preprocess_image",
    "_compute_rotation",
    "rectify_image_with_homography",
    "synthesize_angled_view",
]
