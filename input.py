import argparse


class PdfInputData:
    def __init__(self, args):
        self.recursive = args.recursive
        self.input_files = args.input_paths

        if args.output_path:
            self.output_path = args.output_path
        else:
            self.output_path = f'combined_output_{"_".join(self.input_files)}.pdf'


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
