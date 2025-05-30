from PIL import Image, ImageDraw, ImageFont
import textwrap
from pathlib import Path

def create_chat_image(text: str, output_path="chat_output.png"):
    # 📐 Résolution haute
    scale = 2

    # 🎨 Styles
    outer_padding = 30 * scale
    inner_padding = 30 * scale
    line_spacing = 10 * scale
    font_size = 36 * scale
    radius = 40 * scale

    bg_color = (255, 255, 255)        # blanc
    bubble_color = (230, 235, 239)    # #E6EBEF
    text_color = (0, 0, 0)            # noir

    # 🖋️ Police locale embarquée
    font_path = Path(__file__).parent / "fonts" / "Inter-Regular.ttf"
    font = ImageFont.truetype(str(font_path), font_size)

    # 📦 Préparation du texte
    paragraphs = text.split('\n')
    wrapped_lines = []
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    max_line_width = 0

    for idx, paragraph in enumerate(paragraphs):
        lines = textwrap.wrap(paragraph, width=40) or ['']
        wrapped_lines.extend(lines)
        if idx < len(paragraphs) - 1:
            wrapped_lines.append('')

        for line in lines:
            bbox = dummy_draw.textbbox((0, 0), line, font=font)
            max_line_width = max(max_line_width, bbox[2])

    line_height = font.getbbox("Ag")[3] + line_spacing
    bubble_width = max_line_width + inner_padding * 2
    bubble_height = inner_padding * 2 + line_height * len(wrapped_lines)
    image_width = bubble_width + outer_padding * 2
    image_height = bubble_height + outer_padding * 2

    # 🖼 Création de l'image et de la bulle
    image = Image.new("RGB", (image_width, image_height), bg_color)
    bubble = Image.new("RGB", (bubble_width, bubble_height), bubble_color)
    draw = ImageDraw.Draw(bubble)

    y = inner_padding
    for line in wrapped_lines:
        draw.text((inner_padding, y), line, fill=text_color, font=font)
        y += line_height

    # 🧼 Coins arrondis
    mask = Image.new("L", bubble.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, bubble_width, bubble_height], radius=radius, fill=255)

    image.paste(bubble, (outer_padding, outer_padding), mask)

    # 💾 Sauvegarde PNG
    image.save(output_path, "PNG")
    return output_path
