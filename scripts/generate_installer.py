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

    subprocess.run(["pyinstaller", *pyinstaller_args, "pdf_utility/pdf_utility.py"])


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
    parser.add_argument(
        "--upload_test", action="store_true", help="Upload the wheel to TestPyPI."
    )
    parser.add_argument("--upload_dry_run", action="store_true", help="Dry run upload.")

    args = parser.parse_args()

    # remove the dist directory if it exists
    shutil.rmtree(DEST_DIR, ignore_errors=True)

    if not args.skip_installer:
        generate_installer()

    if not args.skip_wheel:
        generate_python_wheel(args)

        upload_args = [
            "twine",
            "check" if args.upload_dry_run else "upload",
            f"{DEST_DIR}/*",
        ]

        if not args.upload_dry_run:
            upload_args.append("--verbose")

        if args.upload_test:
            upload_args.append("--repository")
            upload_args.append("testpypi")

        if args.upload or args.upload_test:
            subprocess.run(upload_args)
        else:
            print("To upload the wheel to PyPI, use the --upload flag.")
            print("To upload the wheel to TestPyPI, use the --upload_test flag.")
            print("To perform a dry run upload, use the --upload_dry_run flag.")
            print("To skip the upload, use the --skip_upload flag.")
            print("To skip generating the wheel, use the --skip_wheel flag.")
            print("To skip generating the installer, use the --skip_installer flag.")
            print("To test the installation of the wheel, use the --test_install flag.")
            print("To see this message again, use the --help flag.")
