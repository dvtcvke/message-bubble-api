from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_chat_image(text: str, output_path="chat_output.jpg"):
    # Couleurs et styles
    outer_padding = 30  # marge autour de la bulle (dans l'image)
    inner_padding = 30  # marge entre le texte et le bord de la bulle
    line_spacing = 10
    font_size = 36

    bg_color = (255, 255, 255)        # fond de l'image (blanc)
    bubble_color = (230, 235, 239)    # couleur de la bulle #E6EBEF
    text_color = (0, 0, 0)            # texte noir
    radius = 40                       # coins arrondis

    # Chargement police
    try:
        font = ImageFont.truetype("Arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Traitement du texte
    paragraphs = text.split('\n')
    wrapped_lines = []
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    max_line_width = 0

    for idx, paragraph in enumerate(paragraphs):
        lines = textwrap.wrap(paragraph, width=40) or ['']
        wrapped_lines.extend(lines)

        # Ajout de saut de ligne entre paragraphes (mais pas après le dernier)
        if idx < len(paragraphs) - 1:
            wrapped_lines.append('')

        for line in lines:
            bbox = dummy_draw.textbbox((0, 0), line, font=font)
            max_line_width = max(max_line_width, bbox[2])

    # Dimensions
    line_height = font.getbbox("Ag")[3] + line_spacing
    bubble_width = max_line_width + inner_padding * 2
    bubble_height = inner_padding * 2 + line_height * len(wrapped_lines)

    image_width = bubble_width + outer_padding * 2
    image_height = bubble_height + outer_padding * 2

    # Création image et bulle
    image = Image.new("RGB", (image_width, image_height), bg_color)
    bubble = Image.new("RGB", (bubble_width, bubble_height), bubble_color)
    draw = ImageDraw.Draw(bubble)

    # Placement du texte
    y = inner_padding
    for line in wrapped_lines:
        draw.text((inner_padding, y), line, fill=text_color, font=font)
        y += line_height

    # Coins arrondis
    mask = Image.new("L", bubble.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, bubble_width, bubble_height], radius=radius, fill=255)

    # Collage de la bulle sur fond
    image.paste(bubble, (outer_padding, outer_padding), mask)

    # Sauvegarde
    image.save(output_path, "JPEG")
    return output_path
