import qrcode
import cv2
import numpy as np
from tkinter import Tk, filedialog
from PIL import Image, ImageDraw
import math
import random

def read_qr_code():
    """Prompt user to select an image file and decode the QR code."""
    Tk().withdraw()  # Hide Tkinter root window
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        print("No file selected.")
        return None

    # Decode QR using OpenCV
    img = cv2.imread(file_path)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)

    if data:
        print("Decoded Data:", data)
        return data
    else:
        print("No QR code found in the selected image.")
        return None

def get_input_data():
    """Retrieve data from image or prompt user input."""
    data = read_qr_code()
    if not data:
        data = input("Enter the data to encode in the QR code: ")
    return data

def draw_hexagon(draw, center_x, center_y, size, color, rotation):
    """Draw a rotated hexagon centered at (center_x, center_y) with a given size and rotation."""
    angle_step = math.pi / 3  # 60 degrees in radians
    points = [
        (
            center_x + size * math.cos(i * angle_step + rotation),
            center_y + size * math.sin(i * angle_step + rotation)
        )
        for i in range(6)
    ]
    draw.polygon(points, fill=color)

def get_alignment_positions(version, border):
    """Retrieve alignment pattern positions for a given QR code version."""
    if version == 1:
        return []

    num_align = (version // 7) + 2
    step = (version * 8 + num_align * 3 + 5) // (num_align * 4 - 4)
    step = step if step % 2 == 0 else step + 1  # Ensure even step size

    positions = [6 + border]
    for i in range(1, num_align - 1):
        positions.append(positions[-1] + step)
    positions.append(version * 4 + 6 + border)
    return positions

def is_in_corner(matrix_x, matrix_y, border, adjusted_matrix_size):
    """Check if the module is within the 7x7 corner areas."""
    if (0 <= matrix_x < 7 or adjusted_matrix_size - 7 <= matrix_x < adjusted_matrix_size) and \
       (0 <= matrix_y < 7 or adjusted_matrix_size - 7 <= matrix_y < adjusted_matrix_size):
        return True
    return False

def is_alignment_pattern(x, y, version, border, adjusted_matrix_size):
    """Check if the (x, y) position corresponds to an alignment pattern."""
    positions = get_alignment_positions(version, border)
    for px in positions:
        for py in positions:
            # Skip the finder pattern areas
            if (px == border and py == border) or \
               (px == border and py == adjusted_matrix_size - 1 - border) or \
               (px == adjusted_matrix_size - 1 - border and py == border):
                continue
            # Check if (x, y) is within the 5x5 area of the alignment pattern
            if px - 2 <= x <= px + 2 and py - 2 <= y <= py + 2:
                return True
    return False

def create_custom_qr(data, output_path="custom_qr.png"):
    """Generate a customized QR code based on the provided data."""
    # QR code configuration
    border_size = 4
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=border_size,
    )
    qr.add_data(data)
    qr.make(fit=True)

    matrix = qr.get_matrix()
    matrix_size = len(matrix)

    # Adjusted matrix size excluding borders
    adjusted_matrix_size = matrix_size - 2 * border_size

    # Image size calculations
    dot_size = 10  # Size of each module in pixels
    img_size = adjusted_matrix_size * dot_size  # Adjusted to exclude borders

    # Create a blank image with the specified background color
    background_color = (233, 233, 244)
    img = Image.new("RGB", (img_size, img_size), color=background_color)
    draw = ImageDraw.Draw(img)

    # Colors
    corner_color = (0, 60, 131)
    data_color = corner_color  # Use the same color for data modules

    # Draw the QR code
    for y in range(border_size, matrix_size - border_size):
        for x in range(border_size, matrix_size - border_size):
            if matrix[y][x]:  # True indicates a black module
                # Calculate pixel position
                top_left = ((x - border_size) * dot_size, (y - border_size) * dot_size)
                bottom_right = ((x - border_size + 1) * dot_size, (y - border_size + 1) * dot_size)

                adjusted_x = x - border_size
                adjusted_y = y - border_size

                if is_in_corner(adjusted_x, adjusted_y, border_size, adjusted_matrix_size):
                    # Draw corner boxes
                    draw.rectangle([top_left, bottom_right], fill=corner_color)
                elif is_alignment_pattern(adjusted_x, adjusted_y, qr.version, border_size, adjusted_matrix_size):
                    # Draw alignment pattern boxes
                    draw.rectangle([top_left, bottom_right], fill=corner_color)
                else:
                    center_x = (top_left[0] + bottom_right[0]) / 2
                    center_y = (top_left[1] + bottom_right[1]) / 2
                    hex_size = dot_size * 0.4
                    rotation_angle = random.uniform(0, 2 * math.pi)
                    draw_hexagon(draw, center_x, center_y, hex_size, data_color, rotation_angle)

    # Save the image
    img.save(output_path)
    print(f"QR Code saved as {output_path}")

def main():
    data = get_input_data()
    if data:
        create_custom_qr(data)

if __name__ == "__main__":
    main()