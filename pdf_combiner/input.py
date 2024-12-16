import argparse
from pdf_combiner import util
import os
import click

INPUT_EXTENSIONS = (
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".PDF",
)


class PdfInputError(Exception):
    pass


class PdfInputData:
    def __init__(self, args):
        self.recursive = args.recursive

        if self.recursive:
            self.input_files = []
            for path in args.input_paths:
                if os.path.isdir(path):
                    files_with_extensions = util.get_files_with_extensions(
                        INPUT_EXTENSIONS, [], path
                    )
                    # Sort by filename (basename) before extending the list
                    files_with_extensions.sort(key=os.path.basename)

                    self.input_files.extend(files_with_extensions)
                else:
                    self.input_files.append(path)
        else:
            self.input_files = args.input_paths
            for path in self.input_files:
                if os.path.isdir(path):
                    raise PdfInputError(
                        f"Invalid input path - is directory! Use -r option: {path}"
                    )
                elif not os.path.exists(path):
                    raise PdfInputError(f"Invalid input path - does not exist: {path}")

        if args.output_path:
            self.output_path = args.output_path
            # get the output path extension
            _, output_extension = os.path.splitext(self.output_path)
            if output_extension != ".pdf":
                raise PdfInputError("Output file must be a PDF.")
        else:
            self.output_path = os.path.join(os.getcwd(), "converted_output")

            for path in self.input_files:
                file_name = os.path.basename(path)
                # remove the extension
                file_name = file_name[: file_name.rfind(".")]
                self.output_path += f"_{file_name}"

            self.output_path += ".pdf"

        if os.path.exists(self.output_path) and not (args.override_output_path):
            raise PdfInputError(
                f"Output file already exists: {self.output_path}. Use --override_output_path to overwrite."
            )

        input_files_printable = ", ".join(self.input_files)
        click.secho(f"Collected input files: {input_files_printable}", fg="green")


def process_inputs():
    parser = argparse.ArgumentParser(description="Combine multiple PDFs into one.")
    parser.add_argument("-o", "--output_path", help="Path to the output PDF.")
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively search directories for input files.",
    )
    parser.add_argument("input_paths", nargs="+", help="Paths to the input PDFs.")
    parser.add_argument(
        "--override_output_path",
        action="store_true",
        help="Override the output file if it exists",
    )

    args = parser.parse_args()

    # make the output path absolute
    if args.output_path:
        args.output_path = os.path.abspath(args.output_path)

    # make the input paths absolute
    args.input_paths = [os.path.abspath(path) for path in args.input_paths]

    return PdfInputData(args)
