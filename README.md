
# TIFF to PNG and GIF Converter

## Description

This project provides a Python-based utility for converting TIFF files to PNG format and creating animated GIFs from the resulting PNG images. It utilizes several libraries, including `numpy`, `PIL`, `tifffile`, and `imageio`, to handle image processing efficiently.

## Features

- **Batch Conversion**: Convert multiple TIFF files in a specified input directory to PNG format.
- **NoData Handling**: Optionally specify a NoData value to handle pixels that should be treated as transparent or ignored during conversion.
- **GIF Creation**: Create an animated GIF from the converted PNG images, with progress visualization overlaid on each frame.

## Installation

To run this project, ensure you have the required libraries installed. You can install them using pip:

```bash
pip install numpy pillow tifffile imageio
```

## Usage

To use the converter, follow these steps:

1. **Set Input and Output Paths**: Modify the `input_tif`, `output_png`, and `output_gif` variables in the `main` function to point to your desired directories.
2. **Run the Script**: Execute the script to start the conversion and GIF creation process:

```bash
python tif2gif.py
```
