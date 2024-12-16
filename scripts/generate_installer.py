import subprocess
import shutil

DEST_DIR = "dist"

if __name__ == "__main__":
    pyinstaller_args = [
        "--onefile",
        f"--distpath={DEST_DIR}",
    ]

    # remove the dist directory if it exists
    shutil.rmtree(DEST_DIR, ignore_errors=True)

    subprocess.run(["pyinstaller", *pyinstaller_args, "pdf_combiner/pdf_combiner.py"])
