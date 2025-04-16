import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from pathlib import Path


def plot_spectra(file_paths=None):
    if file_paths is None:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_paths = filedialog.askopenfilenames(
            title="Select Spectrum CSV files (multiple files possible)",
            filetypes=[("CSV files", "*.csv")],
        )

        if not file_paths:  # If user cancels
            print("No files selected")
            return

    if isinstance(file_paths, (str, Path)):
        file_paths = [file_paths]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle("Spectrum Analysis - Multiple Overlay", fontsize=14)

    colors = plt.cm.rainbow(np.linspace(0, 1, len(file_paths)))

    all_stats = []

    for file_path, color in zip(file_paths, colors):
        try:
            df = pd.read_csv(file_path)
            filename = Path(file_path).stem

            ax1.plot(
                df["Wavelength"],
                df["Intensity"],
                "-",
                linewidth=1.5,
                color=color,
                label=filename,
            )

            ax2.plot(
                df["Wavenumber"],
                df["Intensity"],
                "-",
                linewidth=1.5,
                color=color,
                label=filename,
            )

            stats = {
                "filename": filename,
                "max_intensity": df["Intensity"].max(),
                "min_intensity": df["Intensity"].min(),
                "mean_intensity": df["Intensity"].mean(),
                "wavelength_range": (df["Wavelength"].min(), df["Wavelength"].max()),
                "wavenumber_range": (df["Wavenumber"].min(), df["Wavenumber"].max()),
            }
            all_stats.append(stats)

        except Exception as e:
            print(f"Error reading or plotting file {file_path}: {e}")

    ax1.set_xlabel("Wavelength (nm)")
    ax1.set_ylabel("Intensity (arb.)")
    ax1.set_title("Wavelength Domain")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper left")

    ax2.set_xlabel("Wavenumber (1/cm)")
    ax2.set_ylabel("Intensity (arb.)")
    ax2.set_title("Wavenumber Domain")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="upper left")

    plt.tight_layout()
    # plt.yscale('log')
    print("\nSpectrum Statistics:")
    for stats in all_stats:
        print(f"\nFile: {stats['filename']}")
        print(f"Maximum intensity: {stats['max_intensity']:.2f}")
        print(f"Minimum intensity: {stats['min_intensity']:.2f}")
        print(f"Mean intensity: {stats['mean_intensity']:.2f}")
        print(
            f"Wavelength range: {stats['wavelength_range'][0]:.1f} - {stats['wavelength_range'][1]:.1f} nm"
        )
        print(
            f"Wavenumber range: {stats['wavenumber_range'][0]:.1f} - {stats['wavenumber_range'][1]:.1f} cm⁻¹"
        )

    plt.show()


def normalize_spectrum(intensity):
    """Normalize spectrum to range [0,1]"""
    return (intensity - intensity.min()) / (intensity.max() - intensity.min())


if __name__ == "__main__":
    plot_spectra()
