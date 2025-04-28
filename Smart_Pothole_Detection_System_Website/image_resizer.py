from PIL import Image
import os

def resize_image(input_path, output_path, max_width, max_height):
    """
    Resize the image while maintaining its aspect ratio.

    :param input_path: Path to the input image
    :param output_path: Path to save the resized image
    :param max_width: Maximum width for the resized image
    :param max_height: Maximum height for the resized image
    """
    with Image.open(input_path) as img:
        # Get current dimensions
        original_width, original_height = img.size

        # Calculate the scaling factor to maintain aspect ratio
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)

        # Resize the image
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Save the resized image
        resized_img.save(output_path)

        print(f"Image resized and saved to {output_path} - New size: {new_width}x{new_height}")

def resize_images_in_directory(input_dir, output_dir, max_width, max_height):
    """
    Resize all images in a directory while maintaining their aspect ratio.

    :param input_dir: Directory containing the images to resize
    :param output_dir: Directory to save the resized images
    :param max_width: Maximum width for the resized images
    :param max_height: Maximum height for the resized images
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            resize_image(input_path, output_path, max_width, max_height)

# Example usage
input_directory = './Website/static/images/Potholes'
output_directory = './testout'
max_width = 600
max_height = 600

resize_images_in_directory(input_directory, output_directory, max_width, max_height)
