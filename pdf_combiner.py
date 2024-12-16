from input import process_inputs
import pikepdf


class PdfCombiner:
    def __init__(self, input_paths, output_path):
        self.input_paths = input_paths
        self.output_path = output_path

    def combine_pdfs(self):
        pdf = pikepdf.Pdf.new()
        for path in self.input_paths:
            pdf_page = pikepdf.open(path)
            pdf.pages.extend(pdf_page.pages)
        pdf.save(self.output_path)


if __name__ == "__main__":
    process_inputs()
