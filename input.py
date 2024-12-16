import argparse
import util
import os

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
        else:
            self.output_path = f'combined_output_{"_".join(self.input_files)}.pdf'

        if os.path.exists(self.output_path):
            raise PdfInputError(f"Output file already exists: {self.output_path}")


def process_inputs():
    parser = argparse.ArgumentParser(description="Combine multiple PDFs into one.")
    parser.add_argument("--output_path", help="Path to the output PDF.")
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively search directories for input files.",
    )
    parser.add_argument("input_paths", nargs="+", help="Paths to the input PDFs.")

    args = parser.parse_args()

    return PdfInputData(args)
