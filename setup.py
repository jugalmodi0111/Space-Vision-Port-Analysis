"""Setup configuration for Aule Space Vision Challenge package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="aule-space-vision",
    version="1.0.0",
    author="Aule Space Vision Team",
    author_email="team@aulespace.com",
    description="Satellite port detection and rotation analysis using advanced computer vision",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aule-space-vision",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/aule-space-vision/issues",
        "Documentation": "https://aule-space-vision.readthedocs.io",
        "Source Code": "https://github.com/yourusername/aule-space-vision",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.0",
        "opencv-python>=4.5.0",
        "opencv-contrib-python>=4.5.0",
        "scikit-image>=0.18.0",
        "matplotlib>=3.3.0",
        "scipy>=1.5.0",
        "Pillow>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0",
            "flake8>=3.9.0",
            "pylint>=2.8.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "sphinx-autodoc-typehints>=1.12.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "notebook>=6.0.0",
            "ipywidgets>=7.6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "aule-detect=src.cli:main",
        ],
    },
    keywords="computer-vision image-processing satellite detection rotation",
    zip_safe=False,
)
