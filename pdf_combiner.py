from input import process_inputs, PdfInputData
import pikepdf


class PdfCombiner:
    def __init__(self, input_data: PdfInputData):
        self.input_paths = input_data.input_files
        self.output_path = input_data.output_path

    def combine_pdfs(self):
        pdf = pikepdf.Pdf.new()
        for path in self.input_paths:
            pdf_page = pikepdf.open(path)
            pdf.pages.extend(pdf_page.pages)
        pdf.save(self.output_path)


if __name__ == "__main__":
    input_data = process_inputs()
