import base64
import io
from PIL import Image, ImageDraw, ImageFont

def generate_dynamic_ad(generated_image_path, logo_path, punchline, punchline_color, button_text, button_color):
    try:
        logo_image = Image.open(io.BytesIO(logo_path))
        buffer = io.BytesIO()
        logo_image.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        logo_image = io.BytesIO(base64.decodebytes(bytes(img_str, "utf-8")))
        img = io.BytesIO(base64.decodebytes(bytes(generated_image_path, "utf-8")))
        generated_image = Image.open(img).convert("RGBA")
        generated_image = generated_image.resize((300, 300))

        ad_template = Image.new("RGBA", (800, 600), (255, 255, 255, 255))  # Beyaz arka plan
        logo = Image.open(logo_image).convert("RGBA").resize((80, 80))
        logo_position = ((ad_template.width - logo.width) // 2, 30)
        ad_template.paste(logo, logo_position)

        vertical_padding = 24

        generated_image_position = ((ad_template.width - generated_image.width) // 2, logo_position[1] + logo.height + vertical_padding)
        ad_template.paste(generated_image, generated_image_position, mask=generated_image)

        draw = ImageDraw.Draw(ad_template)
        font = ImageFont.load_default()

        font_size_text = 20
        font_size_button = 16
        font_text = ImageFont.truetype("arial.ttf", font_size_text)
        font_button = ImageFont.truetype("arial.ttf", font_size_button)

        punchline_position = ((ad_template.width - draw.textbbox((0, 0), punchline, font=font_text)[2]) // 2, generated_image_position[1] + generated_image.height + vertical_padding)
        draw.text(punchline_position, punchline, font=font_text, fill=punchline_color)

        # Ayarlanabilir buton boyutları
        button_text_bbox = draw.textbbox((0, 0), button_text, font=font)
        button_height = button_text_bbox[3] + 30  # 10 piksellik bir ek yükseklik
        button_width = max(button_text_bbox[2] + 20, 160)  # Min. genişlik 160 piksel

        button_radius = 5  # Increased radius for more rounded corners
        button_height = button_height + 2 * button_radius  # Increase height to account for rounded corners

        button_position = (
            (ad_template.width - button_width) // 2,
            punchline_position[1] + button_text_bbox[3] + vertical_padding + 10  # 10 piksel aşağı kaydır
        )

        # Yuvarlak köşeli buton çizimi
        draw_rounded_rectangle(draw, button_position, (button_width, button_height), button_color, button_radius)

        # Düzeltme: Text'in yatay ve dikey olarak butonun tam ortasında olması
        button_text_position = (
            button_position[0] + (button_width - button_text_bbox[2]) // 2 - 5,
            button_position[1] + (button_height - button_text_bbox[3]) // 2
        )

        draw.text(button_text_position, button_text, font=font_button, fill="white")

        buffer = io.BytesIO()
        ad_template.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return {"success": True, "message": "Ad template created successfully.", "output_path": img_str}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}", "output_path": None}

def draw_rounded_rectangle(draw, xy, size, fill, radius):
    upper_left_point = xy
    lower_right_point = (xy[0] + size[0], xy[1] + size[1])

    draw.rectangle([upper_left_point, lower_right_point], fill=fill)

    # Artan kavis açıları için değerleri 30'a çıkartabilirsiniz (isteğe bağlı)
    draw.pieslice([upper_left_point, (upper_left_point[0] + 2 * radius, upper_left_point[1] + 2 * radius)],
                  180, 270, fill=fill)
    draw.pieslice([(lower_right_point[0] - 2 * radius, upper_left_point[1]),
                   (lower_right_point[0], upper_left_point[1] + 2 * radius)], 270, 0, fill=fill)
    draw.pieslice([(upper_left_point[0], lower_right_point[1] - 2 * radius),
                   (upper_left_point[0] + 2 * radius, lower_right_point[1])], 90, 180, fill=fill)

    # Alt kısmındaki padding'i artırarak daha iyi bir görsel denge sağla
    draw.rectangle([upper_left_point, (lower_right_point[0], lower_right_point[1] + 10)], fill=fill)
