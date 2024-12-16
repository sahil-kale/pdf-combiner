from pdf_combiner.image_to_pdf import image_to_pdf
from pdf_combiner.input import process_inputs, PdfInputData
import pikepdf
import os
import click


class PdfCombiner:
    def __init__(self, input_data: PdfInputData):
        self.input_paths = input_data.input_files
        self.output_path = input_data.output_path
        self.tmp_paths = []

        for i in range(len(self.input_paths)):
            click.secho(f"Processing {self.input_paths[i]}", fg="cyan")
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
        click.secho(f"Removing temporary files", fg="cyan")
        for path in self.tmp_paths:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

    def combine_pdfs(self):
        pdf = pikepdf.Pdf.new()
        click.secho("Combining PDFs", fg="cyan")
        for path in self.input_paths:
            pdf_page = pikepdf.open(path)
            pdf.pages.extend(pdf_page.pages)
        pdf.save(self.output_path)

        click.secho(f"PDFs combined into {self.output_path}", fg="green")


def main():
    input_data = process_inputs()
    PdfCombiner(input_data)
    click.secho("Finished Execution", fg="green")
    click.secho(
        "Consider giving the project a star on GitHub if you found it useful!\nhttps://github.com/sahil-kale/pdf-combiner/ ✨",
        fg="magenta",
    )


if __name__ == "__main__":
    main()
