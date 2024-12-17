# PDF Utility
A simple command-line utility to combine multiple PDF/image files into a single PDF.

## Features
- Combine individual PDF files or entire folders of PDFs.
- Support for recursive folder traversal.
- Specify custom output file paths.
- Works as a CLI tool for seamless integration into your workflows.
- File Size Reduction.

## Installation
Using pip: `pip install pdf_utility`

*Note: the shortcut `pdf_utility` can be directly used, but sometimes pip shortcuts do not work on windows. In this case, the module can be run with `python -m pdf_utility <args>`.*

Using executable:
- Download the executable artifact from the latest `Build Windows Executable` job
- Execute the executable, ex: `path/to/pdf_utility.exe --help`

## Usage
Combine Specific Files
To combine specific PDF files into a single output: `pdf_utility --operation combine path/to/file1.pdf path/to/file2.png --output_path output.pdf`

Combine All PDFs in a Folder
To combine all PDF files in a specific folder: `pdf_utility --operation combine -r path/to/folder --output_path output.pdf`

Compressing PDF
`pdf_utility <args> --compress`

Note: images (.png, .jpg) are supported as file input
