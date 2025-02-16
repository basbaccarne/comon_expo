# This script takes a folder of PNG images and stitches them together into a single spritesheet image.

import os
import math
from PIL import Image

image_path = "tests/img"  # Change this to your input folder path

def create_spritesheet(image_folder, output_path, images_per_row=None):
    # Get all PNG files in the folder
    images = [f for f in os.listdir(image_folder) if f.endswith('.png')]
    images.sort()  # Ensure order
    
    if not images:
        print("No PNG images found in the folder.")
        return
    
    # Open images to get their dimensions
    image_objects = [Image.open(os.path.join(image_folder, img)) for img in images]
    img_width, img_height = image_objects[0].size # uncomment if you don't want to resize the images

    # calculate the number of rows and columns
    num_images = len(image_objects)
    images_per_row = images_per_row or math.ceil(math.sqrt(num_images))
    num_rows = math.ceil(num_images / images_per_row)
    print(f"Creating a spritesheet with {images_per_row} columns and {num_rows} rows. Total images: {num_images}")
    print(f"Each image will be resized to {img_width}x{img_height} pixels.")
    
    # Calculate spritesheet dimensions
    sheet_width = images_per_row * img_width
    sheet_height = num_rows * img_height
    
    # Create a blank spritesheet
    spritesheet = Image.new("RGBA", (sheet_width, sheet_height))
    
    # Paste images onto the spritesheet
    for index, img in enumerate(image_objects):
        x = (index % images_per_row) * img_width
        y = (index // images_per_row) * img_height
        spritesheet.paste(img, (x, y))
    
    # Save the spritesheet
    spritesheet.save(output_path)
    print(f"Spritesheet saved to {output_path}")

# Example usage
if __name__ == "__main__":
    input_folder = image_path  # Change this to your input folder path
    output_file = "spritesheet.png"  # Change this to your desired output file name
    create_spritesheet(input_folder, output_file)