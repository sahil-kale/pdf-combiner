from pdf_combiner import image_to_pdf

# get the current directory
import os

CURRENT_DIR = os.path.dirname(__file__)

TEST_IMG = f"{CURRENT_DIR}/samples/test_img.png"


def test_image_to_pdf():
    pdf_path = f"{CURRENT_DIR}/test_img.pdf"
    image_to_pdf.image_to_pdf(TEST_IMG, pdf_path)
    assert os.path.exists(pdf_path)
    os.remove(pdf_path)
    assert not os.path.exists(pdf_path)
