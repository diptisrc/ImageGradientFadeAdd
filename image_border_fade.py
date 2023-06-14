''' This Code was created by Diptis Chaudhari'''


# This Code is for job posted on upwork
# Job link: https://www.upwork.com/jobs/Create-python-script-for-adding-text-borders-image-using-Pillow_~01fe0e375e4211b2fb/

import os 
from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np

class ImageBorderFade():
    def __init__(self):
        pass

    def add_border(self, img_fname):
        # Function to add a border to the image
        if type(img_fname) == str:
            img = Image.open(img_fname)
        else:
            img = img_fname

        # Expand the image with a black border
        img = ImageOps.expand(img, border=4, fill='black')
        img = ImageOps.expand(img, border=15, fill='white')
        img = ImageOps.expand(img, border=8, fill='black')
        output = ImageOps.expand(img, border=40, fill='white')
        return output

    def gradient_fade_bottom(self, image_fname, fade_percentage, fade_color):
        # Function to apply a gradient fade effect to the bottom of the image
        img = Image.open(image_fname).convert("RGBA")
        width, height = img.size

        fade_start = int(height * (1 - fade_percentage))
        fade_range = height - fade_start

        # Create a gradient array for the alpha channel
        alpha_gradient = np.linspace(0, 255, fade_range, dtype=np.uint8)

        # Apply the gradient fade to the image
        pixels = np.array(img)
        alpha_channel = pixels[:, :, 3]
        alpha_channel[fade_start:, :] = np.tile(alpha_gradient, (width, 1)).T

        # Create a blank image with the same size as the original image
        fade_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        # Draw a gradient rectangle on the blank image
        for y in range(fade_start, height):
            alpha = alpha_gradient[y - fade_start]
            color = fade_color[:3] + (alpha,)
            fade_img.paste(color, (0, y, width, y + 1))

        # Combine the original image and the fade image
        faded_image = Image.alpha_composite(img, fade_img)
        return faded_image

    def add_text(self, static_image, lat, lon, width, height, city, state, base_dir):
        # Function to add text to the image
        print(f'{lat} {lon}')
        print(f'{width} {height}')
        print(f'{city} {state}')
        static_image_file = os.path.join(base_dir, f'{state}_{city}_{width}_{height}.jpeg')
        static_image_file_upd = os.path.join(base_dir, f'{state}_{city}_{width}_{height}_upd.jpeg')

        # static_image = Image.open(static_image_file)
        image_editable = ImageDraw.Draw(static_image)
        font_city = ImageFont.truetype("arial.ttf", 80)
        font_state = ImageFont.truetype("arial.ttf", 70)
        font_location = ImageFont.truetype("arial.ttf", 30)
        coord_letter_lat = ''
        if lat > 0:
            coord_letter_lat = 'N'
        else:
            coord_letter_lat = 'S'
        if lon > 0:
            coord_letter_lon = 'E'
        else:
            coord_letter_lon = 'W'
        location_text = f'{lat}°{coord_letter_lat} {lon}°{coord_letter_lon}'
        
        # Add text to the image at specific positions
        image_editable.text((width / 2, height - 300), city.upper(), (0, 0, 0), font=font_city, anchor="mm")
        image_editable.text((width / 2, height - 225), str(f"--- {state.upper()} ----"), (0, 0, 0), font=font_state, anchor="mm")
        image_editable.text((width / 2, height - 150), location_text, (0, 0, 0), font=font_location, anchor="mm")
        return static_image

    def run(self, in_fname, out_fname):
        # Function to run the entire process
        fade_percentage = 0.7
        fade_color = (255, 255, 255, 255)  # Color

        lat = 39.7420
        lon = -104.9915
        city = "Vail"
        state = "Colorado"
        base_dir = "."

        faded_image = self.gradient_fade_bottom(image_fname=in_fname, fade_percentage=fade_percentage, fade_color=fade_color)
        image_with_border = self.add_border(faded_image)
        width = image_with_border.size[0]
        height = image_with_border.size[1]
        image_with_text = self.add_text(image_with_border, lat, lon, width, height, city, state, ".")
        # image_with_text.show()
        image_with_text.save(out_fname)


if __name__ == "__main__":
    editor = ImageBorderFade()
    editor.run(in_fname="image.jpeg", out_fname="image_with_border_bottom_fade.png")
