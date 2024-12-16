from PIL import Image


def image_to_pdf(image_path, pdf_path):
    image = Image.open(image_path)
    pdf_bytes = image.convert("RGB")
    pdf_bytes.save(pdf_path)
