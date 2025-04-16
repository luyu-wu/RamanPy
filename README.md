# RamanPy - Raman Spectrometer Data Acquisition and Analysis

RamanPy is a Python-based tool for capturing, visualizing, and analyzing USB-UVC Raman spectrometer data. It provides real-time spectrum visualization, dark frame correction, and spectrum overlay comparison.

It focuses on being easily configurable and editable. I found existing general UVC spectrometer implementations to be too obtuse.

## Features

- Real-time camera-based spectral data acquisition
- Wavelength and wavenumber calibration
- Fluorescence baseline removal option
- Dark frame subtraction for improved signal quality
- Spectrum saving with timestamp
- Multi-spectrum overlay visualization and comparison

## Requirements

- Python 3.6+
- Connected camera (webcam or spectrometer camera)
- Dependencies listed in `requirements.txt`
- Likely only works on Linux without modification (using V4L2 as it provides far less compressed data)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/RamanPy.git
   cd RamanPy
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Data Acquisition

Run the main script to start capturing spectral data:

```bash
python RamanPy/main.py
```

Controls:
- Press `s` to save the current spectrum
- Press `q` to quit the application

The script will show two windows:
1. The camera feed with the spectral region highlighted
2. A real-time plot of the spectrum

### Configuration

Adjust these parameters in `main.py` to configure your setup:

```python
# Camera settings
length = 1920         # Camera width resolution
height = 1080         # Camera height resolution

# Analysis settings
laser_wavelength = 532  # Excitation wavelength in nm
crop_y1, crop_y2 = 0.53, 0.64  # Vertical region to analyze (as fraction of height)
rolling = 1           # Number of frames to average
baselineRemoval = False  # Enable/disable fluorescence baseline removal

# Calibration (wavelength = m*pixel + b)
calibrate = [0.5378783977636364, 251.83884117409121]  # [m, b] coefficients
```

### Spectrum Analysis

After collecting spectra, use the drawing tool to visualize and compare multiple spectra:

```bash
python RamanPy/draw.py
```

This will open a file selection dialog where you can choose one or more spectrum files to visualize.

## File Format

Spectra are saved as CSV files with the following columns:
- Wavelength (nm)
- Wavenumber (cm⁻¹)
- Intensity (arbitrary units)

## Dark Frame Correction

The system will automatically use `dark_frame.csv` if present in the working directory to provide background subtraction.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
