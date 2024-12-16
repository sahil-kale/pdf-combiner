import subprocess
import argparse
import os
import shutil

DEST_DIR = os.path.abspath("dist")


def generate_python_wheel(args):
    subprocess.run(["python", "-m", "build"])

    if args.test_install:
        # find the .whl file inside the dist directory
        whl_file = None
        for file in os.listdir(DEST_DIR):
            if file.endswith(".whl"):
                whl_file = DEST_DIR + f"/{file}"
                break

        if whl_file is None:
            raise FileNotFoundError("No wheel file found in the dist directory.")

        subprocess.run(["pip", "install", whl_file])


def generate_installer():
    pyinstaller_args = [
        "--onefile",
        f"--distpath={DEST_DIR}",
    ]

    subprocess.run(["pyinstaller", *pyinstaller_args, "pdf_combiner/pdf_combiner.py"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Python wheel.")
    parser.add_argument(
        "--test_install",
        action="store_true",
        help="Test the installation of the wheel.",
    )
    parser.add_argument(
        "--skip_installer", action="store_true", help="Skip generating the installer."
    )
    parser.add_argument(
        "--skip_wheel", action="store_true", help="Skip generating the wheel."
    )
    parser.add_argument(
        "--upload", action="store_true", help="Upload the wheel to PyPI."
    )

    args = parser.parse_args()

    # remove the dist directory if it exists
    shutil.rmtree(DEST_DIR, ignore_errors=True)

    if not args.skip_installer:
        generate_installer()

    if not args.skip_wheel:
        generate_python_wheel(args)

        if args.upload:
            subprocess.run(["twine", "upload", f"{DEST_DIR}/*", "--verbose"])
