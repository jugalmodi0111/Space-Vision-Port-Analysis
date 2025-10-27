# Usage Guide & Examples

## Table of Contents
1. [Basic Usage](#basic-usage)
2. [Core Functions](#core-functions)
3. [Advanced Examples](#advanced-examples)
4. [Batch Processing](#batch-processing)
5. [Configuration & Parameters](#configuration--parameters)
6. [Output Interpretation](#output-interpretation)

## Basic Usage

### Quick Start: Detect Rotation

```python
from src.pipeline import detect_satellite_port_rotation

# Simple detection on a single image
result = detect_satellite_port_rotation(
    image_path="path/to/satellite_image.png",
    visualize=True
)

# Print results
print(f"Rotation Angle: {result.angle_deg:.2f}°")
print(f"Direction: {result.direction}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Circle Center: {result.circle_center}")
print(f"Circle Radius: {result.circle_radius} px")
print(f"Squares Detected: {len(result.squares)}")
```

### Step-by-Step Pipeline

```python
from src.preprocessor import preprocess_image
from src.detectors import detect_circle, detect_squares
from src.rotation_calculator import compute_rotation
import cv2

# 1. Load image
image = cv2.imread("satellite_image.png")

# 2. Preprocess
preprocessed = preprocess_image(image)

# 3. Detect circle
circle = detect_circle(preprocessed)
print(f"Circle: center={circle[:2]}, radius={circle[2]}")

# 4. Detect squares
squares = detect_squares(preprocessed)
print(f"Found {len(squares)} squares")

# 5. Calculate rotation
angle, confidence, direction = compute_rotation(
    circle=circle,
    squares=squares,
    image_shape=image.shape
)
print(f"Rotation: {angle:.2f}° ({direction})")
print(f"Confidence: {confidence:.2f}")
```

## Core Functions

### 1. `detect_satellite_port_rotation()`

Main entry point for complete pipeline.

```python
from src.pipeline import detect_satellite_port_rotation

result = detect_satellite_port_rotation(
    image_path: str,                    # Path to input image
    visualize: bool = False,            # Display results
    save_output: Optional[str] = None   # Save visualization to file
)
```

**Returns**: `RotationResult` object with:
- `angle_deg`: Rotation angle (0-360°)
- `confidence`: Score (0-1)
- `circle_center`: (x, y) tuple
- `circle_radius`: Integer pixels
- `squares`: List of detected squares
- `direction`: "clockwise" or "counterclockwise"

**Example**:
```python
result = detect_satellite_port_rotation("port.png", visualize=True)
if result.confidence > 0.8:
    print(f"High confidence detection: {result.angle_deg}°")
else:
    print(f"Low confidence ({result.confidence:.2f}). Check image quality.")
```

### 2. `detect_circle()`

Detect circular marker using multi-method fusion.

```python
from src.detectors import detect_circle

circle = detect_circle(preprocessed_image)
# Returns: (x, y, radius) or None
```

**Example**:
```python
if circle:
    x, y, radius = circle
    print(f"Circle at ({x}, {y}) with radius {radius}px")
else:
    print("No circle detected")
```

### 3. `detect_squares()`

Detect nested square structures.

```python
from src.detectors import detect_squares

squares = detect_squares(preprocessed_image)
# Returns: List of square corner arrays
```

**Example**:
```python
for i, square in enumerate(squares):
    print(f"Square {i+1}: {len(square)} corners")
    area = cv2.contourArea(square.astype(np.int32))
    print(f"  Area: {area:.0f} px²")
```

### 4. `rectify_image()`

Perspective correction using detected squares.

```python
from src.homography import rectify_image

rectified_dict = rectify_image(
    image=image,
    squares=squares,
    target_size=400
)

if rectified_dict:
    rectified_image = rectified_dict['rectified']
    H = rectified_dict['homography_matrix']
    print("Image rectified successfully")
```

### 5. `synthesize_angled_view()`

Generate synthetic 22.5° angled view.

```python
from src.homography import synthesize_angled_view

angled_dict = synthesize_angled_view(
    image=image,
    yaw_deg=22.5,      # Rotation angle
    hfov_deg=60.0      # Horizontal field of view
)

angled_view = angled_dict['angled_view']
cv2.imwrite("angled_22_5deg.png", angled_view)
```

### 6. `plan_camera_movements()`

Calculate camera pan/tilt/zoom for crop recovery.

```python
from src.pipeline import plan_camera_movements

plan = plan_camera_movements(
    crop_image=crop,
    reference_image=reference,
    expected_circle_diameter=40,
    intrinsics=camera_intrinsics
)

for step_num, (pan, tilt, zoom) in enumerate(plan.steps, 1):
    print(f"Step {step_num}: Pan {pan:.2f}°, Tilt {tilt:.2f}°, Zoom {zoom:.2f}x")
```

## Advanced Examples

### Example 1: Batch Processing Multiple Images

```python
from pathlib import Path
from src.pipeline import detect_satellite_port_rotation
import json

image_dir = Path("data/test_images")
results = []

for image_path in sorted(image_dir.glob("*.png")):
    print(f"Processing {image_path.name}...", end=" ")
    
    result = detect_satellite_port_rotation(str(image_path))
    
    if result and result.confidence > 0.7:
        results.append({
            "filename": image_path.name,
            "angle_deg": result.angle_deg,
            "confidence": result.confidence,
            "direction": result.direction,
            "circle_center": result.circle_center,
            "circle_radius": result.circle_radius
        })
        print(f"✓ {result.angle_deg:.1f}° ({result.direction})")
    else:
        print("✗ Failed")

# Save results
with open("results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nProcessed {len(results)}/{len(list(image_dir.glob('*.png')))} images successfully")
```

### Example 2: Rotation Analysis with Visualization

```python
import matplotlib.pyplot as plt
import numpy as np
from src.pipeline import detect_satellite_port_rotation
from src.visualizer import show_binary_and_final

image_path = "satellite_image.png"
result = detect_satellite_port_rotation(image_path, visualize=True)

if result:
    # Create analysis visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Subplot 1: Angle dial
    ax = axes[0, 0]
    angle = result.angle_deg
    ax.add_patch(plt.Circle((0, 0), 1, color='lightgray', alpha=0.3))
    # Draw needle
    ax.arrow(0, 0, np.cos(np.radians(angle-90)), 
             np.sin(np.radians(angle-90)), 
             head_width=0.1, head_length=0.1, fc='red', ec='red')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.set_title(f'Rotation Angle: {angle:.2f}°\n{result.direction}')
    ax.axis('off')
    
    # Subplot 2: Confidence gauge
    ax = axes[0, 1]
    confidence = result.confidence * 100
    ax.barh(0, confidence, color='green' if confidence > 80 else 'orange', height=0.3)
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel('Confidence (%)')
    ax.set_title(f'Confidence Score: {confidence:.1f}%')
    ax.set_yticks([])
    ax.grid(axis='x', alpha=0.3)
    
    # Subplot 3: Detection metrics
    ax = axes[1, 0]
    metrics = [
        f"Circle Center: ({result.circle_center[0]}, {result.circle_center[1]})",
        f"Circle Radius: {result.circle_radius} px",
        f"Squares Found: {len(result.squares)}",
        f"Angle: {result.angle_deg:.2f}°",
        f"Direction: {result.direction}",
        f"Confidence: {result.confidence:.2f}"
    ]
    ax.text(0.1, 0.9, "\n".join(metrics), transform=ax.transAxes,
            fontfamily='monospace', fontsize=10, verticalalignment='top')
    ax.axis('off')
    
    # Subplot 4: Image with overlay
    ax = axes[1, 1]
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    x, y, r = result.circle_center[0], result.circle_center[1], result.circle_radius
    cv2.circle(image_rgb, (x, y), r, (0, 255, 0), 3)
    cv2.circle(image_rgb, (x, y), 2, (255, 0, 0), 3)
    ax.imshow(image_rgb)
    ax.set_title('Detection Result')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig("analysis.png", dpi=150, bbox_inches='tight')
    plt.show()
```

### Example 3: Perspective Rectification Workflow

```python
import cv2
from src.pipeline import detect_satellite_port_rotation
from src.homography import rectify_image
from src.visualizer import visualize_rectification

image_path = "satellite_image.png"
image = cv2.imread(image_path)

# 1. Detect rotation and squares
result = detect_satellite_port_rotation(image_path)

if result and result.squares:
    # 2. Rectify image
    rectified_dict = rectify_image(image, result.squares)
    
    if rectified_dict:
        rectified = rectified_dict['rectified']
        
        # 3. Visualize before/after
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        
        axes[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        axes[0].set_title('Original (Rotated)')
        axes[0].axis('off')
        
        axes[1].imshow(cv2.cvtColor(rectified, cv2.COLOR_BGR2RGB))
        axes[1].set_title('Rectified (Front-Facing)')
        axes[1].axis('off')
        
        plt.tight_layout()
        plt.savefig("rectification_comparison.png")
        plt.show()
        
        # 4. Save rectified image
        cv2.imwrite("rectified_image.png", rectified)
        print("Rectification complete!")
else:
    print("Could not detect squares for rectification")
```

### Example 4: Generate Angled View

```python
from src.homography import synthesize_angled_view
import cv2

image = cv2.imread("front_view.png")

# Generate multiple angled views
angles = [0, 11.25, 22.5, 33.75, 45]

for angle in angles:
    result = synthesize_angled_view(image, yaw_deg=angle)
    
    if result:
        angled = result['angled_view']
        output_path = f"angled_{angle:.1f}deg.png"
        cv2.imwrite(output_path, angled)
        print(f"Saved: {output_path}")
```

## Batch Processing

### Process Directory of Images

```python
from pathlib import Path
from src.pipeline import detect_satellite_port_rotation
import pandas as pd

def batch_process_images(input_dir, output_csv=None):
    """
    Process all images in directory and save results to CSV.
    """
    results = []
    input_path = Path(input_dir)
    
    image_files = list(input_path.glob("*.png")) + list(input_path.glob("*.jpg"))
    
    for i, image_file in enumerate(image_files, 1):
        print(f"[{i}/{len(image_files)}] Processing {image_file.name}...", end=" ")
        
        try:
            result = detect_satellite_port_rotation(str(image_file))
            
            if result:
                results.append({
                    'filename': image_file.name,
                    'angle_deg': result.angle_deg,
                    'direction': result.direction,
                    'confidence': result.confidence,
                    'circle_x': result.circle_center[0],
                    'circle_y': result.circle_center[1],
                    'circle_radius': result.circle_radius,
                    'squares_found': len(result.squares),
                    'status': 'success'
                })
                print("✓")
            else:
                results.append({
                    'filename': image_file.name,
                    'status': 'failed_detection'
                })
                print("✗ (detection failed)")
                
        except Exception as e:
            results.append({
                'filename': image_file.name,
                'status': f'error: {str(e)}'
            })
            print(f"✗ (error: {e})")
    
    # Save to CSV
    df = pd.DataFrame(results)
    if output_csv:
        df.to_csv(output_csv, index=False)
        print(f"\nResults saved to {output_csv}")
    
    return df

# Usage
results_df = batch_process_images("data/images", "results.csv")
print(results_df.describe())
```

## Configuration & Parameters

### Adjust Detection Sensitivity

```python
from src.detectors import detect_circle, BlobParams, ContourParams

# Make circle detection more sensitive (lower threshold)
blob_params = BlobParams(
    min_sigma=3.0,      # Smaller circles
    max_sigma=40.0,     # Larger circles  
    threshold=0.05      # Lower = more detections
)

# Make contour detection stricter
contour_params = ContourParams(
    min_area=200,           # Larger minimum
    max_area=4000,          # Smaller maximum
    min_circularity=0.7     # More circular
)

circle = detect_circle(
    preprocessed_image,
    blob_params=blob_params,
    contour_params=contour_params
)
```

### Adjust Physical Parameters

```python
from src.pipeline import SatellitePortParams, detect_satellite_port_rotation

# Custom parameters for different setup
custom_params = SatellitePortParams(
    outer_square_size=40.0,
    inner_square_size=30.0,
    square_spacing=2.5,
    camera_distance=100.0,     # 1 meter
    min_circle_radius_px=8,
    max_circle_radius_px=60
)

# Use in detection
result = detect_satellite_port_rotation("image.png")
```

## Output Interpretation

### Understanding Results

```python
result = detect_satellite_port_rotation("image.png")

# Rotation Angle
print(f"Angle: {result.angle_deg}°")  # 0-360°
# 0° = original orientation (circle at top-left)
# 90° = 90° rotation
# Direction: clockwise or counterclockwise

# Confidence Score
print(f"Confidence: {result.confidence}")  # 0.0 to 1.0
# > 0.9:  Very high confidence
# 0.7-0.9: Good confidence
# 0.5-0.7: Moderate confidence (review results)
# < 0.5:  Low confidence (check image quality)

# Circle Detection
print(f"Circle: center={result.circle_center}, radius={result.circle_radius}")
# Pixel coordinates in image
# Useful for debugging and visualization

# Squares
print(f"Squares: {len(result.squares)}")
# 3 = all nested squares detected
# < 3 = partial detection (may impact confidence)
```

---

For more information, see [API.md](API.md) and [examples/](../examples/) folder.
