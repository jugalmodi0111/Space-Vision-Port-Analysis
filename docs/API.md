# API Reference

Complete documentation of all public functions and classes.

## Table of Contents
1. [Core Pipeline](#core-pipeline)
2. [Detectors Module](#detectors-module)
3. [Preprocessor Module](#preprocessor-module)
4. [Rotation Calculator](#rotation-calculator)
5. [Homography Module](#homography-module)
6. [Visualizer Module](#visualizer-module)
7. [Data Classes](#data-classes)

---

## Core Pipeline

### `detect_satellite_port_rotation()`

Main entry point for complete rotation detection pipeline.

```python
def detect_satellite_port_rotation(
    image_path: str,
    visualize: bool = False,
    save_output: Optional[str] = None,
    params: Optional[SatellitePortParams] = None
) -> Optional[RotationResult]
```

**Parameters:**
- `image_path` (str): Path to input image file
- `visualize` (bool): Display detection results (default: False)
- `save_output` (str, optional): Path to save visualization image
- `params` (SatellitePortParams, optional): Custom parameters

**Returns:**
- `RotationResult` object with detection results, or `None` if detection fails

**Example:**
```python
from src.pipeline import detect_satellite_port_rotation

result = detect_satellite_port_rotation("port.png", visualize=True)
if result:
    print(f"Angle: {result.angle_deg}°, Confidence: {result.confidence}")
```

---

### `plan_camera_movements()`

Generate camera movement plan for crop recovery.

```python
def plan_camera_movements(
    crop_image: np.ndarray,
    reference_image: np.ndarray,
    expected_circle_diameter: int,
    intrinsics: CameraIntrinsicsExtended
) -> MovementPlan
```

**Parameters:**
- `crop_image` (np.ndarray): Cropped/offset satellite image
- `reference_image` (np.ndarray): Full reference image
- `expected_circle_diameter` (int): Expected circle size in pixels
- `intrinsics` (CameraIntrinsicsExtended): Camera calibration parameters

**Returns:**
- `MovementPlan` object with:
  - `origin`: Method used for planning
  - `confidence`: Plan confidence score
  - `steps`: List of (pan_deg, tilt_deg, zoom) tuples

**Example:**
```python
from src.pipeline import plan_camera_movements, CameraIntrinsicsExtended

K = CameraIntrinsicsExtended.from_fov((1080, 1920), hfov_deg=60.0)
plan = plan_camera_movements(crop, reference, 40, K)
for pan, tilt, zoom in plan.steps:
    print(f"Move: Pan {pan:.2f}°, Tilt {tilt:.2f}°, Zoom {zoom:.2f}x")
```

---

### `solve_problem_part_c()`

Synthesize 22.5° angled view from front-view image.

```python
def solve_problem_part_c(
    front_view_image_path: str,
    output_path: str,
    yaw_deg: float = 22.5,
    hfov_deg: float = 60.0
) -> Optional[Dict]
```

**Parameters:**
- `front_view_image_path` (str): Path to front-view image
- `output_path` (str): Path to save angled view image
- `yaw_deg` (float): Rotation angle in degrees (default: 22.5)
- `hfov_deg` (float): Horizontal field of view (default: 60.0)

**Returns:**
- Dictionary with:
  - `angled_view`: Synthesized image (np.ndarray)
  - `homography_matrix`: 3×3 transformation matrix
  - `yaw_angle_deg`: Applied rotation angle
  - `distance_cm`: Camera distance
  - Or `None` if operation fails

**Example:**
```python
from src.pipeline import solve_problem_part_c

result = solve_problem_part_c("front.png", "angled.png", yaw_deg=22.5)
if result:
    print(f"Angled view saved with {result['yaw_angle_deg']}° rotation")
```

---

## Detectors Module

### `detect_circle()`

Multi-method circle detection using blob detection and contour analysis.

```python
def detect_circle(
    prep_dict: Dict,
    blob_params: BlobParams = BlobParams(),
    contour_params: ContourParams = ContourParams()
) -> Optional[Tuple[int, int, int]]
```

**Parameters:**
- `prep_dict` (dict): Preprocessed image dictionary from `preprocess_image()`
- `blob_params` (BlobParams): Blob detection parameters
- `contour_params` (ContourParams): Contour detection parameters

**Returns:**
- Tuple `(x, y, radius)` for detected circle, or `None`

**Example:**
```python
from src.preprocessor import preprocess_image
from src.detectors import detect_circle

prep = preprocess_image(image)
circle = detect_circle(prep)
if circle:
    x, y, r = circle
    print(f"Circle at ({x}, {y}) with radius {r}px")
```

---

### `detect_circles_blob()`

Blob-based circle detection using DoG and LoG.

```python
def detect_circles_blob(
    gray: np.ndarray,
    params: BlobParams = BlobParams()
) -> List[Tuple[int, int, int]]
```

**Parameters:**
- `gray` (np.ndarray): Grayscale image
- `params` (BlobParams): Detection parameters

**Returns:**
- List of `(x, y, radius)` tuples

---

### `detect_circles_contour()`

Contour-based circle detection with circularity filtering.

```python
def detect_circles_contour(
    binary: np.ndarray,
    params: ContourParams = ContourParams()
) -> List[Tuple[int, int, int]]
```

**Parameters:**
- `binary` (np.ndarray): Binary image (thresholded)
- `params` (ContourParams): Detection parameters

**Returns:**
- List of `(x, y, radius)` tuples filtered by circularity

---

### `detect_squares()`

Nested square detection using Hough line transform.

```python
def detect_squares(
    prep_dict: Dict,
    params: SatellitePortParams
) -> List[np.ndarray]
```

**Parameters:**
- `prep_dict` (dict): Preprocessed image dictionary
- `params` (SatellitePortParams): Physical parameters

**Returns:**
- List of detected squares (each as 4×2 array of corner coordinates)

**Example:**
```python
squares = detect_squares(prep, params)
for i, square in enumerate(squares):
    print(f"Square {i+1}: {square.shape[0]} corners")
```

---

### `merge_circle_detections()`

Merge nearby circle detections via spatial consensus.

```python
def merge_circle_detections(
    circles: List[Tuple[int, int, int]],
    proximity_threshold: int = 20
) -> List[Tuple[int, int, int]]
```

**Parameters:**
- `circles` (list): List of `(x, y, radius)` detections
- `proximity_threshold` (int): Maximum distance for merging (pixels)

**Returns:**
- Merged list of circles with at least 2 detections within threshold

---

## Preprocessor Module

### `preprocess_image()`

Comprehensive image preprocessing pipeline.

```python
def preprocess_image(image: np.ndarray) -> Dict[str, np.ndarray]
```

**Parameters:**
- `image` (np.ndarray): Input image (BGR or grayscale)

**Returns:**
- Dictionary with keys:
  - `gray`: Grayscale image
  - `enhanced`: CLAHE-enhanced image
  - `denoised`: Bilateral filtered image
  - `binary`: Thresholded & morphologically cleaned
  - `edges`: Canny edge detection output

**Example:**
```python
from src.preprocessor import preprocess_image
import cv2

image = cv2.imread("port.png")
prep = preprocess_image(image)

cv2.imshow("Binary", prep['binary'])
cv2.imshow("Edges", prep['edges'])
cv2.waitKey(0)
```

---

## Rotation Calculator

### `_compute_rotation()`

Calculate rotation angle from geometric features.

```python
def _compute_rotation(
    circle: Optional[Tuple[int, int, int]],
    squares: List[np.ndarray],
    image_shape: Tuple[int, int]
) -> Tuple[float, float, Optional[Dict], str]
```

**Parameters:**
- `circle` (tuple): Detected circle `(x, y, radius)` or None
- `squares` (list): Detected squares list
- `image_shape` (tuple): Image dimensions `(height, width)`

**Returns:**
- Tuple of:
  - `angle_deg` (float): Rotation angle (0-360°)
  - `confidence` (float): Score (0-1)
  - `metadata` (dict): Additional info or None
  - `direction` (str): "clockwise" or "counterclockwise"

---

## Homography Module

### `rectify_image_with_homography()`

Perspective correction using detected squares.

```python
def rectify_image_with_homography(
    image: np.ndarray,
    rotation_result: RotationResult,
    target_size: int = 400
) -> Optional[Dict]
```

**Parameters:**
- `image` (np.ndarray): Input image
- `rotation_result` (RotationResult): Detection result with squares
- `target_size` (int): Output image size (pixels)

**Returns:**
- Dictionary with:
  - `rectified`: Perspective-corrected image
  - `homography_matrix`: 3×3 transformation
  - `target_size`: Output dimensions
  - Or `None` if insufficient squares detected

---

### `synthesize_angled_view()`

Generate synthetic angled view using 3D rotation.

```python
def synthesize_angled_view(
    image: np.ndarray,
    yaw_deg: float = 22.5,
    hfov_deg: float = 60.0
) -> Optional[Dict]
```

**Parameters:**
- `image` (np.ndarray): Input image
- `yaw_deg` (float): Rotation angle (degrees)
- `hfov_deg` (float): Horizontal field of view

**Returns:**
- Dictionary with:
  - `angled_view`: Transformed image
  - `homography_matrix`: Transformation matrix
  - Or `None` if operation fails

---

### `_compute_intrinsics()`

Estimate camera intrinsic parameters.

```python
def _compute_intrinsics(
    image_shape: Tuple[int, int],
    hfov_deg: float = 60.0
) -> np.ndarray
```

**Parameters:**
- `image_shape` (tuple): Image dimensions `(height, width)`
- `hfov_deg` (float): Horizontal field of view (degrees)

**Returns:**
- 3×3 camera intrinsic matrix

---

## Visualizer Module

### `show_binary_and_final()`

Display two-panel visualization (binary mask + final detection).

```python
def show_binary_and_final(
    image: np.ndarray,
    prep: Dict,
    circle: Optional[Tuple[int, int, int]]
) -> None
```

**Parameters:**
- `image` (np.ndarray): Original image
- `prep` (dict): Preprocessed image dictionary
- `circle` (tuple): Detected circle or None

**Side Effects:**
- Displays matplotlib figure with two subplots

---

### `visualize_combined_detection()`

Overlay circles and squares on original image.

```python
def visualize_combined_detection(
    image: np.ndarray,
    circle: Optional[Tuple[int, int, int]],
    squares: List[np.ndarray]
) -> None
```

**Parameters:**
- `image` (np.ndarray): Original image
- `circle` (tuple): Detected circle or None
- `squares` (list): List of detected squares

---

### `visualize_circle_detection_stages()`

Multi-panel visualization of circle detection pipeline.

```python
def visualize_circle_detection_stages(
    image: np.ndarray,
    prep_dict: Dict,
    blob_params: BlobParams = BlobParams(),
    contour_params: ContourParams = ContourParams()
) -> None
```

---

### `visualize_square_detection()`

Display detected squares overlaid on image.

```python
def visualize_square_detection(
    image: np.ndarray,
    prep: Dict,
    squares: List[np.ndarray]
) -> None
```

---

### `visualize_homography_results()`

Before/after perspective rectification visualization.

```python
def visualize_homography_results(
    original_image: np.ndarray,
    rectified_dict: Dict,
    rotation_result: RotationResult
) -> None
```

---

## Data Classes

### `SatellitePortParams`

Physical parameters of the satellite port.

```python
@dataclass
class SatellitePortParams:
    outer_square_size: float = 40.0      # cm
    inner_square_size: float = 30.0      # cm
    square_spacing: float = 2.5          # cm
    camera_distance: float = 100.0       # cm
    circle_diameter_cm: float = 5.0      # cm
    min_circle_radius_px: int = 10
    max_circle_radius_px: int = 50
    min_square_size_px: int = 100
    max_square_size_px: int = 500
```

---

### `RotationResult`

Result object returned by `detect_satellite_port_rotation()`.

```python
@dataclass
class RotationResult:
    angle_deg: float                    # Rotation angle (0-360°)
    confidence: float                   # Score (0-1)
    circle_center: Tuple[int, int]     # (x, y) pixels
    circle_radius: int                  # Pixels
    squares: List[np.ndarray]          # Detected squares
    direction: str                      # "clockwise" or "counterclockwise"
```

---

### `BlobParams`

Parameters for blob-based circle detection.

```python
@dataclass
class BlobParams:
    min_sigma: float = 4.0
    max_sigma: float = 30.0
    num_sigma: int = 10
    threshold: float = 0.08
```

---

### `ContourParams`

Parameters for contour-based circle detection.

```python
@dataclass
class ContourParams:
    min_area: int = 100
    max_area: int = 5000
    min_circularity: float = 0.6       # 4π·area/perimeter² threshold
```

---

### `MovementPlan`

Camera movement planning result.

```python
@dataclass
class MovementPlan:
    origin: str                         # Method used ("geometry-offset", etc.)
    confidence: float                   # Plan confidence (0-1)
    steps: List[Tuple[float, float, float]]  # [(pan°, tilt°, zoom), ...]
```

---

### `CameraIntrinsicsExtended`

Camera calibration parameters.

```python
@dataclass
class CameraIntrinsicsExtended:
    fx: float                           # Focal length x
    fy: float                           # Focal length y
    cx: float                           # Principal point x
    cy: float                           # Principal point y
    fov_deg: float = 60.0              # Field of view (degrees)
    
    @classmethod
    def from_fov(cls, image_shape: tuple, hfov_deg: float = 60.0):
        """Create intrinsics from image dimensions and FOV."""
```

---

## Exception Handling

Common exceptions and how to handle them:

```python
from src.pipeline import detect_satellite_port_rotation

try:
    result = detect_satellite_port_rotation("nonexistent.png")
except FileNotFoundError:
    print("Image file not found")
except ValueError as e:
    print(f"Invalid parameter: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

**Last Updated**: October 2025  
**API Version**: 1.0  
**Python Version**: 3.8+
