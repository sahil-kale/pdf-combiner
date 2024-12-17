# PDF Combiner
A simple command-line utility to combine multiple PDF/image files into a single PDF.

## Features
Combine individual PDF files or entire folders of PDFs.
Support for recursive folder traversal.
Specify custom output file paths.
Works as a CLI tool for seamless integration into your workflows.

## Installation
Using pip: `pip install pdf_combiner`

*Note: the shortcut `pdf_combiner` can be directly used, but sometimes pip shortcuts do not work on windows. In this case, the module can be run with `python -m pdf_combiner <args>`.*

Using executable:
- Download the executable artifact from the latest `Build Windows Executable` job
- Execute the executable, ex: `path/to/pdf_combiner.exe --help`

## Usage
Combine Specific Files
To combine specific PDF files into a single output: `pdf_combiner path/to/file1.pdf path/to/file2.pdf --output_path output.pdf`

Combine All PDFs in a Folder
To combine all PDF files in a specific folder: `pdf_combiner -r path/to/folder --output_path output.pdf`

Note: images (.png, .jpg) are supported as file input
