# Installation & Setup Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Dependency Management](#dependency-management)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [Docker Setup (Optional)](#docker-setup-optional)

## System Requirements

### Operating System
- **Linux**: Ubuntu 18.04+ (recommended)
- **macOS**: 10.14+
- **Windows**: 10/11 with WSL2 (recommended) or native Python

### Hardware
- **Processor**: Intel i5/i7 or ARM64 (Apple Silicon supported)
- **RAM**: 4GB minimum, 8GB+ recommended
- **Storage**: 2GB for installation + dependencies
- **GPU**: Optional (NVIDIA with CUDA for acceleration)

### Python Version
- **Python 3.8** or higher
- **pip** package manager
- **virtualenv** (recommended)

## Installation Steps

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/aule-space-vision.git
cd aule-space-vision
```

### Step 2: Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Upgrade pip

```bash
pip install --upgrade pip setuptools wheel
```

### Step 4: Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install with development tools
pip install -r requirements-dev.txt
```

### Step 5: Verify Installation

```bash
# Check Python version
python --version

# Check pip packages
pip list

# Run verification script
python scripts/verify_installation.py
```

## Dependency Management

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | >=1.19.0 | Numerical computing |
| opencv-python | >=4.5.0 | Computer vision algorithms |
| scikit-image | >=0.18.0 | Image processing & blob detection |
| matplotlib | >=3.3.0 | Visualization & plotting |
| scipy | >=1.5.0 | Scientific computing |

### Optional Dependencies

| Package | Version | Purpose | Install With |
|---------|---------|---------|---|
| jupyter | >=1.0.0 | Interactive notebooks | `-dev` |
| pytest | >=6.0.0 | Unit testing | `-dev` |
| black | >=21.0 | Code formatting | `-dev` |
| flake8 | >=3.9.0 | Linting | `-dev` |
| sphinx | >=4.0.0 | Documentation | `-dev` |

### GPU Acceleration (Optional)

For NVIDIA GPU support:

```bash
# Install CUDA-compatible OpenCV
pip install opencv-contrib-python

# Install CUDA toolkit
# Follow: https://developer.nvidia.com/cuda-downloads
```

## Verification

### Quick Test

```python
import cv2
import numpy as np
from src.pipeline import detect_satellite_port_rotation

print(f"OpenCV version: {cv2.__version__}")
print(f"NumPy version: {np.__version__}")
print("All imports successful!")
```

### Run Example

```bash
# Run full pipeline on example image
python -c "
from src.pipeline import detect_satellite_port_rotation
result = detect_satellite_port_rotation('path/to/image.png')
print(f'Rotation: {result.angle_deg}° ({result.direction})')
print(f'Confidence: {result.confidence:.2f}')
"
```

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_detectors.py::test_circle_detection -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

## Troubleshooting

### Issue: "No module named 'cv2'"

**Solution**:
```bash
pip install --upgrade opencv-python
# Or with contrib modules:
pip install opencv-contrib-python
```

### Issue: "ImportError: cannot import name 'blob_dog'"

**Solution**:
```bash
pip install --upgrade scikit-image
```

### Issue: Virtual environment not activating (Windows)

**Solution**:
```bash
# Use full path
.\venv\Scripts\Activate.ps1

# Or if that fails, use cmd.exe instead of PowerShell
cmd.exe
venv\Scripts\activate.bat
```

### Issue: Slow performance on M1/M2 Mac

**Solution**:
```bash
# Install ARM-optimized OpenCV
pip install --upgrade opencv-python

# Or use conda instead
conda install -c conda-forge opencv numpy scipy
```

### Issue: Out of memory errors

**Solution**:
```bash
# Process smaller images or reduce batch size
# Adjust in src/pipeline.py:
MAX_IMAGE_DIMENSION = 2048  # Default: 4096
```

### Issue: CUDA not detected despite installation

**Solution**:
```bash
# Verify CUDA installation
nvidia-smi

# Reinstall with CUDA support
pip install --upgrade opencv-contrib-python

# For PyTorch (if using GPU):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Docker Setup (Optional)

### Build Docker Image

```dockerfile
# Dockerfile
FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-c", "from src.pipeline import detect_satellite_port_rotation; print('Ready!')"]
```

Build and run:
```bash
# Build image
docker build -t aule-space-vision .

# Run container
docker run -v $(pwd)/data:/app/data aule-space-vision

# Interactive shell
docker run -it aule-space-vision bash
```

### Docker Compose (for Jupyter)

```yaml
# docker-compose.yml
version: '3.8'
services:
  jupyter:
    image: aule-space-vision
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/app/notebooks
      - ./data:/app/data
    command: jupyter notebook --ip=0.0.0.0 --no-browser --allow-root
```

Run with:
```bash
docker-compose up
```

## Platform-Specific Notes

### macOS (Intel)

```bash
# Standard installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### macOS (Apple Silicon M1/M2/M3)

```bash
# Use native ARM64 Python
# Ensure Homebrew Python or Anaconda is used

# If using conda:
conda create -n aule python=3.9
conda activate aule
conda install -c conda-forge opencv numpy scipy matplotlib

# Or native pip (may require additional steps):
pip install --upgrade opencv-python
```

### Linux (Ubuntu/Debian)

```bash
# Install system dependencies first
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
sudo apt-get install -y libsm6 libxext6 libxrender-dev  # OpenCV dependencies

# Then follow standard installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows (Native)

```bash
# Use PowerShell as Administrator
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Windows (WSL2 - Recommended)

```bash
# In WSL2 terminal, follow Linux instructions
wsl --install

# Inside WSL2:
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

After successful installation:

1. **Read the documentation**: Check [docs/USAGE.md](../docs/USAGE.md)
2. **Run examples**: See `notebooks/` folder
3. **Explore API**: Review [docs/API.md](../docs/API.md)
4. **Contribute**: Read [CONTRIBUTING.md](../CONTRIBUTING.md)

## Support

For installation issues:
- Check [Troubleshooting](#troubleshooting) section
- Review GitHub Issues: https://github.com/yourusername/aule-space-vision/issues
- Check OpenCV documentation: https://docs.opencv.org/
- Check scikit-image docs: https://scikit-image.org/

---

**Last Updated**: October 2025  
**Python Version Tested**: 3.8, 3.9, 3.10, 3.11
