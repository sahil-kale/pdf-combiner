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
            output_path_dir = os.path.dirname(self.output_path)
            if self.input_paths[i].endswith((".png", ".jpg", ".jpeg")):
                tmp_path = self.input_paths[i]
                tmp_path = os.path.basename(tmp_path)
                # get the filename without the extension
                tmp_path = tmp_path[: tmp_path.rfind(".")]

                # add the output path directory
                tmp_path = os.path.join(output_path_dir, tmp_path)

                # remove the extension and add _TMP.pdf
                tmp_path += "_TMP.pdf"
                image_to_pdf(self.input_paths[i], tmp_path)
                self.input_paths[i] = tmp_path
                self.tmp_paths.append(tmp_path)

        self.combine_pdfs()

    def __del__(self):
        for path in self.tmp_paths:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

    def combine_pdfs(self):
        pdf = pikepdf.Pdf.new()
        for path in self.input_paths:
            pdf_page = pikepdf.open(path)
            pdf.pages.extend(pdf_page.pages)
        pdf.save(self.output_path)

        print(f"Combined PDFs saved to: {self.output_path}")


def main():
    input_data = process_inputs()
    PdfCombiner(input_data)


if __name__ == "__main__":
    main()
