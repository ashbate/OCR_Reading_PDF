import os
import re
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance
from pdf2image import convert_from_path, convert_from_bytes

def adjust(image):
    #cut the pages for blank spaces
    width, height = image.size
    left = 0.01 * width
    top = 0.01 * height
    right = 0.99 * width
    bottom = 0.95 * height
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image

def get_cutpoints(image):
    #get the cutpoints from reading black and white pixels of the pages
    cut_points = []
    mean_array_rgb = []
    gray_image = image.convert('L')
    contrast = ImageEnhance.Contrast(gray_image)
    enhanced_image = contrast.enhance(10)
    image_array = np.array(enhanced_image)
    height, width = image_array.shape

    for k in range(width):
        mean_array_rgb.append(image_array[:, k].mean())

    mean_array_rgb = np.array(mean_array_rgb)
    mean_pointer = np.where(mean_array_rgb > 250)[0]
    a = 0
    for z in range(len(mean_pointer) - 1):
        if mean_pointer[z + 1] - mean_pointer[z] > 150:
            cut_points.append(mean_pointer[a:z + 1].mean().round())
            a = z
    cut_points.append(mean_pointer[-1].mean().round())

    return cut_points

def snippet_cut_points(image):
    #create snippet cut points by horizontally reading black and white pixels
    cut_points = []
    mean_array_rgb = []
    gray_image = image.convert('L')
    contrast = ImageEnhance.Contrast(gray_image)
    enhanced_image = contrast.enhance(5)
    image_array = np.array(enhanced_image)
    height, width = image_array.shape
    mean_array_rgb = image_array.mean(axis=1)
    mean_pointer = np.where(mean_array_rgb < 40)[0]

    a = 0
    for z in range(len(mean_pointer) - 1):
        if mean_pointer[z + 1] - mean_pointer[z] > 2:
            cut_points.append(mean_pointer[a:z + 1].mean().round())
            a = z
                
    cut_points.append(mean_pointer[a:len(mean_pointer)].mean().round())
    cut_points.append(height)
    cut_points = np.array(cut_points)
    cut_points = cut_points[cut_points > 0]

    return cut_points, mean_array_rgb, mean_pointer
    
def snippet_cut(image, cut_points, path=None):
    #method for creating snippets from file
    width, height = image.size
    for i in range(len(cut_points) - 1):
        left = 0
        top = cut_points[i]
        right = width
        bottom = cut_points[i + 1]
        cropped_image = image.crop((left, top, right, bottom))
        if path is not None:
            cropped_image.save(f"{path}company{i}.jpg", 'JPEG')
        
def cut(image, cut_points, path=None):
    #method for creating column-wise cuts from file
    gray_image = image.convert('L')
    contrast = ImageEnhance.Contrast(gray_image)
    enhanced_image = contrast.enhance(3)
    image_array = np.array(enhanced_image)
    height, width = image_array.shape

    if len(cut_points) != 4:
        cut_points.append(width)

    crops = [image.crop((cut_points[i], 0, cut_points[i + 1], height)) for i in range(len(cut_points) - 1)]
    new_image = Image.new('RGB', (crops[0].size[0], sum(crop.size[1] for crop in crops)), (250, 250, 250))
    y_offset = 0
    for crop in crops:
        new_image.paste(crop, (0, y_offset))
        y_offset += crop.size[1]
    if path is not None:
        new_image.save(f"{path}page.jpg", 'JPEG')
    
    return crops

def horizontal_adjust(image):
    #Adjusting for horizontal lines using the mean rgb values 
    gray_image = image.convert('L')
    contrast = ImageEnhance.Contrast(gray_image)
    enhanced_image = contrast.enhance(10)
    image_array = np.array(enhanced_image)
    height, width = image_array.shape
    mean_array_rgb = image_array.mean(axis=1)
    mean_pointer = np.where(mean_array_rgb < 200)[0]

    for i in range(len(mean_pointer) + 2):
        if mean_pointer[i] >= 20 and mean_pointer[i + 1] - mean_pointer[i] > 3:
            cut_point = mean_pointer[i] + 5
            break

    cropped_image = image.crop((0, cut_point, width, height))
    return cropped_image

def missing(images, path):
    #Debugging method to check if there are any missing files after the execution
    missing_files = []
    dir_list = os.listdir(path)

    for j, _ in enumerate(images):
        for i in range(3):
            name = f"page{j}sub{i + 1}.jpg"
            if name not in dir_list:
                missing_files.append(name)
            
    return missing_files

def pdf_concat(image_list):
    #Using the created files concatenate to its final form
    concatenated_images = []
    for i in range(0, len(image_list) - len(image_list) % 2, 2):
        width = max(image.size[0] for image in image_list[i:i + 2])
        height_sum = sum(image.size[1] for image in image_list[i:i + 2])
        new_image = Image.new('RGB', (width, height_sum), (250, 250, 250))
        new_image.paste(image_list[i], (0, 0))
        new_image.paste(image_list[i + 1], (0, image_list[i].size[1]))
        concatenated_images.append(new_image)

    if len(image_list) % 2 != 0:
        concatenated_images.append(image_list[-1])

    return concatenated_images


def preprocess_text(text, patterns):
    # Compile the regex patterns for efficiency
    compiled_patterns = {key: re.compile(pattern, re.IGNORECASE) for key, pattern in patterns.items()}
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Filter out lines that match any of the provided patterns
    filtered_lines = []
    for line in lines:
        if not any(compiled_patterns[key].search(line) for key in compiled_patterns):
            filtered_lines.append(line)
    
    # Reassemble the text from the filtered lines
    return '\n'.join(filtered_lines)

# Define the regex patterns for irrelevant details
irrelevant_patterns = {
    "po_box": r"p\.o\.",
    "vice": r"vice",
    "president": r"president",
    "officer": r"officer",
    "acronym": r"company acronym",
    "director": r"director",
    "landline": r"(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}",
    "fax": r"fax",
    "telex": r"telex",
    "formerly": r"formerly",
    "privately": r"privately",
    "single_letter": r"^\b[A-Z]\b$",
    "ticker": r"ticker",
    "manager": r"manager",
    "single": r"^[A-Z]$|^[a-z]$|^'[A-Z]$|^'[a-z]$",
    "exchange": r"exchange",
    "chief": r"chief",
    "securities": r"securities",
    "secretary": r"secretary",
    "marketing": r"marketing",
    "division": r"division",
    "dot": r"^\.$",
    "owner": r"owner",  # Corrected the case to match your pattern keys
}

# Load the OCR text

def replace_commas_with_tildes(file_path):
    # Open the file and read its content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Use regex to replace all commas with tildes
    modified_content = re.sub(r',', '', content)
    
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)
    