# Imports
import os
import time
from datetime import datetime

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.ndimage import minimum_filter1d

# Variables

length = 1920
height = 1080
laser_wavelength = 532  # Used to perform wavenumber conversion
crop_y1, crop_y2 = 0.53, 0.64  # What vertical space to average
rolling = 1  # How many temporal frames to average
baselineRemoval = False  # remove fluorescence baseline
cameraNumber = 0  # Adjust this to whatever your camera is numbered

calibrate = [
    0.5378783977636364,
    251.83884117409121,
]  # Input your own calibration values, mx+b for pixel (x) to wavelength (nm)

# Less important variables

display_width = 960  # Half the original width
display_height = 540  # Half the original height

# Code
print("\n\033[1m[RAMAN SPECTROMETER TERMINAL]\033[0m")

print("Loading camera...")
t0 = time.perf_counter()
cap = cv2.VideoCapture(
    cameraNumber, cv2.CAP_V4L2
)  # V4L2 has minimal compression and latency

cap.set(cv2.CAP_PROP_FRAME_WIDTH, length)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

print("Loaded Camera:", int(1e3 * (time.perf_counter() - t0)), "ms\n")

wavelengths = (length / length) * np.arange(length) * calibrate[0] + calibrate[1]
laser_wavenumber = 1e7 / laser_wavelength
wavenumbers = (1e7 / wavelengths) - laser_wavenumber

y1, y2 = int(crop_y1 * height), int(crop_y2 * height)
roll = np.zeros((length, rolling))
roll_i = 0

# Load dark frame
dark_intensities = np.zeros((length, height))
if os.path.exists("dark_frame.csv"):
    dark_frame = pd.read_csv("dark_frame.csv")
    dark_intensities = dark_frame["Intensity"].values

plt.ion()
fig, ax = plt.subplots(figsize=(8, 6))
(line,) = ax.plot([], [], "k")
(nocorrect,) = ax.plot([], [], "k", alpha=0.5)

ax.set_title("Spectrometer Output")
ax.set_ylim(0, 255)
ax.set_xlim(np.min(wavenumbers), np.max(wavenumbers))
ax.set_xlabel("Wavenumber (1/cm)")
ax.set_ylabel("Intensity (arb.)")
plt.tight_layout()


def save_spectrum(wavelengths, intensities):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"spectrum_{timestamp}.csv"

    # Create DataFrame with wavelength and intensity data
    df = pd.DataFrame(
        {"Wavelength": wavelengths, "Wavenumber": wavenumbers, "Intensity": intensities}
    )

    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Spectrum saved to {filename}")
    return filename


def removeFluor(intensities, window_size=10):
    baseline = minimum_filter1d(intensities, window_size, mode="reflect")
    corrected = intensities - baseline
    return np.clip(corrected, 0, None)  # Ensure non-negative values


while True:
    _, frame = cap.read()
    frame = cv2.line(frame, (0, y1), (frame.shape[1], y1), (0, 255, 0), 1)
    frame = cv2.line(frame, (0, y2), (frame.shape[1], y2), (0, 255, 0), 1)
    frame = cv2.flip(frame, 1)
    display_frame = cv2.resize(frame, (display_width, display_height))
    cv2.imshow("Image", display_frame)

    frame = np.array(frame)
    spectrum = np.mean(frame[y1:y2], axis=(0, 2))
    roll[:, roll_i % rolling] = spectrum

    data = np.average(roll, axis=1)

    # Subtract dark frame
    data = data - dark_intensities
    data_noremove = data - np.min(data)

    if baselineRemoval:
        data = removeFluor(data)
        line.set_data(wavelengths, data)
    nocorrect.set_data(wavelengths, data_noremove)

    plt.pause(0.1)

    roll_i += 1

    key = cv2.waitKey(10) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("s"):
        filename = save_spectrum(wavelengths, data_noremove)


cap.release()
cv2.destroyAllWindows()
plt.close("all")
