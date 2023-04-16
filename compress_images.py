from PIL import Image
import os
from fpdf import FPDF


def compress_images(folder_path):
    """
    Compresses JPEG and PNG images in a folder using Pillow library.
    Converts PNG and WebP images to JPEG format and then compresses them.
    
    Args:
        folder_path (str): Path to the folder containing images.
    
    Returns:
        str: Path to the compressed folder.
    """
    # Create a new folder to store the compressed images
    compressed_folder_path = os.path.join(folder_path, "compressed")
    if not os.path.exists(compressed_folder_path):
        os.mkdir(compressed_folder_path)

    # Loop through all the files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            # Open the JPEG image using Pillow
            img = Image.open(file_path)
            
            # Compress the JPEG image and save it in the compressed folder
            compressed_img_path = os.path.join(compressed_folder_path, filename)
            img.save(compressed_img_path, "JPEG", quality=70)  # You can adjust the quality value for compression ratio
            
            # Close the JPEG image
            img.close()
            
        elif filename.endswith(".png") or filename.endswith(".webp"):
            # Open the PNG or WebP image using Pillow
            img = Image.open(file_path)
            
            # Convert PNG or WebP to RGB mode (JPEG supports RGB mode only)
            img = img.convert("RGB")
            
            # Compress the converted image and save it in the compressed folder
            compressed_img_path = os.path.join(compressed_folder_path, os.path.splitext(filename)[0] + ".jpg")
            img.save(compressed_img_path, "JPEG", quality=70)  # You can adjust the quality value for compression ratio
            
            # Close the converted image
            img.close()
    
    return compressed_folder_path


def rotate_landscape_images(directory):
    """
    Rotates landscape images to portrait orientation in a directory.

    Args:
        directory (str): Path to the directory containing JPEG images.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image_path = os.path.join(directory, filename)
            with Image.open(image_path) as image:
                width, height = image.size
                if width > height:
                    rotated_image = image.rotate(270, expand=True)
                    rotated_image.save(image_path)
                    print(f"Rotated '{filename}' to portrait orientation.")


def convert_images_to_pdf(directory_path):
    # Create a PDF object with portrait orientation, A4 size, and .5 inch border
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=5)

    # Define the effective page width and height after considering margins
    page_width = 210 - 2 * 5  # A4 width is 210mm, margin is .5 inch on each side
    page_height = 297 - 2 * 5  # A4 height is 297mm, margin is .5 inch on each side

    # Loop through all the files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            # Open the image and calculate its new size to fit the A4 page with a border of .5 inch
            image_path = os.path.join(directory_path, filename)
            image = Image.open(image_path)
            width, height = image.size
            max_width = page_width
            max_height = page_height
            if width > max_width:
                height = int(max_width * height / width)
                width = max_width
            if height > max_height:
                width = int(max_height * width / height)
                height = max_height

            # Add a page to the PDF with the calculated image size and .5 inch border
            pdf.add_page()
            pdf.set_margins(left=5, top=5, right=5)

            # Calculate the horizontal and vertical center positions for the image
            x = 5 + (page_width - width) / 2
            y = 5 + (page_height - height) / 2

            # Add the image to the PDF and center it on the page
            pdf.image(image_path, x, y, width, height)

    # Save the PDF in the same directory with the same name as the directory
    pdf_path = os.path.join(directory_path, f"{os.path.basename(directory_path)}.pdf")
    pdf.output(pdf_path)

    print(f"PDF created successfully at: {pdf_path}")


def images_to_pdf(main_path):
    path = compress_images(main_path)
    rotate_landscape_images(path)
    convert_images_to_pdf(path)