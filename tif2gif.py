"""
TIF to PNG Converter and GIF Creator
------------------------------------
This Python script converts TIF images in a specified directory to PNG format and then combines 
these PNG images into a GIF with a progress bar overlay. The GIF is created with an optional 
duration setting for frame display.

Dependencies:
- os
- numpy
- PIL (Pillow)
- tifffile
- imageio
- loguru


Example:
    Run `main()` with the required folder paths and duration.

Author: Mohamed Yasser 
Date: 30-09-2023
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tifffile as tiff
import imageio
from loguru import logger

logger.add("conversion_and_gif_creation.log", rotation="1 MB", level="DEBUG")

def convert_tif_to_png(input_folder, output_folder, nodata_value=None):
    """
    Convert TIF images in the input folder to PNG format, with optional no-data masking.
    
    Args:
        input_folder (str): Path to the folder containing input TIF images.
        output_folder (str): Path to the folder where output PNG images will be saved.
        nodata_value (int, optional): No-data value to mask in the images. Defaults to None.
    """
    logger.info("Starting TIF to PNG conversion.")
    tif_files = []

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".tif"):
                tif_files.append(os.path.join(root, file))

    tif_files.sort()
    logger.info(f"Found {len(tif_files)} TIF files.")

    png_files = []
    for tif_file in tif_files:
        logger.debug(f"Converting {tif_file} to PNG...")
        try:
            img = tiff.imread(tif_file)
            if img.ndim == 3 and img.shape[2] == 3:
                red, green, blue = img[:, :, 0], img[:, :, 1], img[:, :, 2]

                if nodata_value is not None:
                    red[red == nodata_value] = 0
                    green[green == nodata_value] = 0
                    blue[blue == nodata_value] = 0

                min_red, max_red = np.percentile(red, [1, 98])
                min_green, max_green = np.percentile(green, [1, 98])
                min_blue, max_blue = np.percentile(blue, [1, 98])

                red_scaled = (np.clip(red, min_red, max_red) - min_red) / (max_red - min_red)
                green_scaled = (np.clip(green, min_green, max_green) - min_green) / (max_green - min_green)
                blue_scaled = (np.clip(blue, min_blue, max_blue) - min_blue) / (max_blue - min_blue)

                scaled_red = (red_scaled * 255).astype('uint8')
                scaled_green = (green_scaled * 255).astype('uint8')
                scaled_blue = (blue_scaled * 255).astype('uint8')

                img_scaled = np.stack([scaled_red, scaled_green, scaled_blue], axis=-1)
            else:
                img_scaled = img

                if nodata_value is not None:
                    img_scaled[img_scaled == nodata_value] = 0

            img_pil = Image.fromarray(img_scaled)
            filename = os.path.basename(tif_file).replace(".tif", ".png")
            output_path = os.path.join(output_folder, filename)
            img_pil.save(output_path)
            png_files.append(output_path)

        except Exception as e:
            logger.error(f"Error converting {tif_file} to PNG: {e}")

def create_gif_from_png(input_folder, output_gif, duration):
    """
    Create a GIF from PNG images in the specified folder, with a progress bar overlay.
    
    Args:
        input_folder (str): Path to the folder containing PNG images.
        output_gif (str): Path for saving the output GIF.
        duration (int): Duration in milliseconds for each GIF frame.
    """
    logger.info("Starting GIF creation from PNG images.")
    png_files = []

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".png"):
                png_files.append(os.path.join(root, file))

    png_files.sort()
    logger.info(f"Found {len(png_files)} PNG files for GIF creation.")

    images = []
    try:
        font_size = 35
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    total_frames = len(png_files)

    for i, png_file in enumerate(png_files):
        logger.debug(f"Processing {png_file} for GIF.")
        try:
            img = Image.open(png_file)
            filename = os.path.basename(png_file)
            date = filename.split(".")[0]

            img_width, img_height = img.size
            bar_height = 20
            bar_y = img_height + 10
            bar_x0 = 10
            bar_x1 = img_width - 10
            bar_width = bar_x1 - bar_x0

            new_img_height = img_height + bar_height + 20
            new_img = Image.new('RGB', (img_width, new_img_height))
            new_img.paste(img, (0, 0))

            draw = ImageDraw.Draw(new_img)
            draw.text((10, 10), date, fill="white", font=font)

            progress = (i + 1) / total_frames
            progress_width = int(progress * bar_width)
            draw.rectangle([bar_x0, bar_y, bar_x0 + progress_width, bar_y + bar_height], fill="white")

            images.append(new_img)

        except Exception as e:
            logger.error(f"Error processing {png_file}: {e}")

    if images:
        imageio.mimsave(output_gif, images, duration=duration)
        logger.info(f"Successfully created GIF: {output_gif}")
    else:
        logger.warning("No valid images found to create GIF.")

def main(input_tif, output_png, output_gif, duration=300):
    """
    Main function to convert TIF images to PNG and create a GIF from the resulting PNG files.
    
    Args:
        input_tif (str): Path to the folder containing TIF images.
        output_png (str): Path to the folder for storing converted PNG images.
        output_gif (str): Path for saving the output GIF.
        duration (int, optional): Duration for each frame in the GIF. Defaults to 300 ms.
    """
    logger.info("Starting the entire process of conversion and GIF creation.")
    convert_tif_to_png(input_tif, output_png)
    create_gif_from_png(output_png, output_gif, duration)





# File paths and parameters
input_tif = r"F:\create_gif\input_tif"
output_png = r"F:\create_gif\output_png"
output_gif = r"F:\create_gif\test_gif.gif"

main(input_tif, output_png, output_gif, duration=300)