import random
from PIL import Image, ImageDraw, ImageFont
import frappe
import io
import base64
from PIL import Image
import os

def generate_captcha():
    width = 150
    height = 27
    length = 6
    
    image = Image.new('RGB', (width, height), '#D3CCCC')
    draw = ImageDraw.Draw(image)


    characters = 'ABCDEFGHJKMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz234567890'


    captcha_text = ''.join(random.choices(characters, k=length))

    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'OpenSans-ExtraBold.ttf')  
    try:
        font = ImageFont.truetype(font_path, 20)
    except IOError:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), captcha_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calculate text position to center horizontally and vertically
    text_x = (width - text_width) / 2
    text_y = (height - text_height) /10

    draw.text((text_x, text_y), captcha_text, font=font, fill='black')

    for x in range(width):
        for y in range(height):
            if random.random() < 0.1:
                draw.point((x, y), fill='black')

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str, captcha_text

@frappe.whitelist(allow_guest=True)
def get_captcha():
    img, captcha_text = generate_captcha()
    return {
        'captcha_image': img,
        'captcha_text': captcha_text
    }