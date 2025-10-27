# Contributing Guidelines

Thank you for your interest in contributing to the Aule Space Vision Challenge project! This document provides guidelines for contributing code, documentation, and other improvements.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Commit Messages](#commit-messages)
6. [Pull Request Process](#pull-request-process)
7. [Testing Guidelines](#testing-guidelines)
8. [Documentation](#documentation)

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Report violations to project maintainers

## How to Contribute

### Types of Contributions

1. **Bug Reports**: Report issues with current functionality
2. **Feature Requests**: Suggest new capabilities
3. **Code Improvements**: Optimize existing code
4. **Documentation**: Improve guides and API docs
5. **Test Coverage**: Add new test cases
6. **Performance**: Optimize processing speed

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/aule-space-vision.git
   cd aule-space-vision
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original/aule-space-vision.git
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Install Development Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install all dependencies including dev tools
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks (recommended)
pre-commit install
```

### Verify Setup

```bash
# Run tests
pytest tests/ -v

# Check code quality
flake8 src/
black --check src/

# Run linting
pylint src/
```

## Coding Standards

### Python Style

We follow **PEP 8** with these specific rules:

- **Line length**: Maximum 100 characters
- **Indentation**: 4 spaces
- **Naming conventions**:
  - Functions: `lowercase_with_underscores()`
  - Classes: `PascalCase`
  - Constants: `UPPERCASE_WITH_UNDERSCORES`
  - Private methods: `_private_method()`

### Code Quality Tools

```bash
# Format code with Black
black src/ tests/

# Check with Flake8
flake8 src/ --max-line-length=100

# Type checking with mypy
mypy src/ --ignore-missing-imports

# Linting with pylint
pylint src/ --max-line-length=100
```

### Code Example

```python
"""Module docstring explaining purpose."""

from typing import Optional, Tuple
import numpy as np


class CircleDetector:
    """Detects circles using blob detection and contour analysis."""
    
    def __init__(self, min_radius: int = 10, max_radius: int = 50):
        """
        Initialize detector.
        
        Args:
            min_radius: Minimum circle radius in pixels
            max_radius: Maximum circle radius in pixels
        """
        self.min_radius = min_radius
        self.max_radius = max_radius
    
    def detect(self, image: np.ndarray) -> Optional[Tuple[int, int, int]]:
        """
        Detect circle in image.
        
        Args:
            image: Input image (numpy array)
            
        Returns:
            Tuple of (x, y, radius) or None if not detected
        """
        # Implementation here
        return None
```

### Documentation Requirements

Every function must include:

```python
def function_name(param1: type, param2: type = default) -> return_type:
    """
    Brief one-line description.
    
    Longer description if needed. Explain what the function does,
    any important behavior, and edge cases.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: value)
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When specific condition occurs
        
    Example:
        >>> result = function_name(42, "example")
        >>> print(result)
    """
```

## Commit Messages

Follow the **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, semicolons, etc.)
- **refactor**: Code refactoring without feature changes
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Build, dependencies, or configuration changes

### Examples

```bash
# Feature
git commit -m "feat(detectors): add SIFT-based circle detection

- Implements SIFT keypoint extraction
- Improves detection in low-light conditions
- Adds corresponding unit tests"

# Bug Fix
git commit -m "fix(preprocessor): handle edge case in CLAHE

Fixes #123 where CLAHE enhancement failed on all-black images"

# Documentation
git commit -m "docs(README): add installation instructions for ARM64"
```

## Pull Request Process

### Before Submitting

1. **Update your branch** with latest changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests locally**:
   ```bash
   pytest tests/ -v --cov=src
   ```

3. **Format code**:
   ```bash
   black src/ tests/
   flake8 src/ tests/
   ```

4. **Update documentation** if needed
5. **Add/update tests** for your changes

### Creating a PR

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub with:
   - Clear title describing changes
   - Description of what/why/how
   - Link to related issues (e.g., "Fixes #123")
   - Screenshot/results if applicable
   - Checklist items completed

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #(issue number)

## How to Test
Steps to verify the change works correctly

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No new warnings generated
- [ ] Changes tested locally
```

### PR Review Process

- Maintainers will review code, style, and tests
- Address feedback constructively
- Make requested changes in new commits (don't squash until approved)
- Once approved, maintainers will merge

## Testing Guidelines

### Test Structure

```
tests/
├── test_detectors.py
├── test_preprocessor.py
├── test_rotation.py
├── test_homography.py
├── fixtures/
│   ├── test_image_vga.png
│   ├── test_image_hd.png
│   └── test_data.json
└── conftest.py
```

### Writing Tests

```python
import pytest
from src.detectors import detect_circle
from src.preprocessor import preprocess_image


class TestCircleDetection:
    """Test suite for circle detection."""
    
    def setup_method(self):
        """Prepare test fixtures."""
        self.test_image = load_test_image()
    
    def test_detect_circle_basic(self):
        """Test basic circle detection on clear image."""
        prep = preprocess_image(self.test_image)
        circle = detect_circle(prep)
        
        assert circle is not None
        x, y, r = circle
        assert 0 <= x < self.test_image.shape[1]
        assert 0 <= y < self.test_image.shape[0]
        assert r > 0
    
    def test_detect_circle_no_detection(self):
        """Test handling when no circle present."""
        blank_image = np.zeros((480, 640, 3), dtype=np.uint8)
        prep = preprocess_image(blank_image)
        circle = detect_circle(prep)
        
        assert circle is None
    
    @pytest.mark.parametrize("threshold", [0.05, 0.08, 0.12])
    def test_detect_circle_with_thresholds(self, threshold):
        """Test circle detection with various thresholds."""
        # Test implementation
        pass
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_detectors.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_detectors.py::TestCircleDetection::test_detect_circle_basic

# Run with markers
pytest -m "not slow" tests/
```

### Test Coverage Requirements

- Minimum 80% code coverage
- All public functions tested
- Edge cases covered
- Error conditions handled

## Documentation

### Types of Documentation

1. **Docstrings**: Function/class-level documentation
2. **Comments**: Complex logic explanation
3. **README/Guides**: User-facing documentation
4. **API Docs**: Complete API reference
5. **Examples**: Jupyter notebooks and scripts

### Documentation Checklist

- [ ] Function/class has docstring
- [ ] Parameters documented with types
- [ ] Return value documented
- [ ] Exceptions documented
- [ ] Usage example provided
- [ ] Links to related functions added

### Building Documentation

```bash
# Build Sphinx documentation
cd docs/
make html
open _build/html/index.html
```

## Performance Optimization

When proposing performance improvements:

1. **Profile before/after**:
   ```bash
   python -m cProfile -s cumulative script.py > profile.txt
   ```

2. **Include benchmarks** in PR description
3. **Avoid premature optimization** - profile first
4. **Document trade-offs** (speed vs accuracy, memory, etc.)

## Release Process

- Maintainers create releases following **Semantic Versioning**
- Format: `v{major}.{minor}.{patch}` (e.g., v1.2.3)
- Changelog updated for each release
- GitHub releases page maintained

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: File an Issue with clear reproduction steps
- **Suggestions**: Post a Feature Request
- **Contact**: Email project maintainers

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- GitHub contributors page
- Release notes for significant contributions

---

**Thank you for contributing to Aule Space Vision Challenge!** 🚀

Questions? Feel free to open an issue or discussion.
