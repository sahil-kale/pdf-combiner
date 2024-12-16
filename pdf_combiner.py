from input import process_inputs, PdfInputData
from image_to_pdf import image_to_pdf
import pikepdf
import os


class PdfCombiner:
    def __init__(self, input_data: PdfInputData):
        self.input_paths = input_data.input_files
        self.output_path = input_data.output_path
        self.tmp_paths = []

        for i in range(len(self.input_paths)):
            if self.input_paths[i].endswith((".png", ".jpg", ".jpeg")):
                tmp_path = self.input_paths[i]
                # strip the extension
                tmp_path = tmp_path[: tmp_path.rfind(".")]
                tmp_path += "_TMP.pdf"
                image_to_pdf(self.input_paths[i], tmp_path)
                self.input_paths[i] = tmp_path

        self.combine_pdfs()

        for tmp_path in self.tmp_paths:
            os.remove(tmp_path)

    def combine_pdfs(self):
        pdf = pikepdf.Pdf.new()
        for path in self.input_paths:
            pdf_page = pikepdf.open(path)
            pdf.pages.extend(pdf_page.pages)
        pdf.save(self.output_path)


if __name__ == "__main__":
    input_data = process_inputs()
    PdfCombiner(input_data)
