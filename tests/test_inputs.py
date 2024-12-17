import os
import shutil
import pytest
from pdf_utility.input import PdfInputData, PdfInputError

# Constants
CURRENT_DIR = os.path.dirname(__file__)
TEST_PLAYGROUND = f"{CURRENT_DIR}/test_playground"
TEST_IMG = f"{CURRENT_DIR}/samples/test_img.png"


# Reusable FakeArgs class
class FakeArgs:
    def __init__(
        self,
        input_paths,
        output_path=None,
        recursive=False,
        override_output_path=False,
    ):
        self.input_paths = input_paths
        self.output_path = output_path
        self.recursive = recursive
        self.override_output_path = override_output_path


# Fixtures for setup and teardown
@pytest.fixture(autouse=True)
def clean_test_playground():
    """Fixture to create and clean the test_playground directory."""
    shutil.rmtree(TEST_PLAYGROUND, ignore_errors=True)
    os.makedirs(TEST_PLAYGROUND)
    yield
    shutil.rmtree(TEST_PLAYGROUND, ignore_errors=True)


# Utility Functions
def make_fake_dir(name, files=None):
    path = os.path.join(TEST_PLAYGROUND, name)
    os.makedirs(path, exist_ok=True)
    if files:
        for file in files:
            with open(os.path.join(path, file), "w") as f:
                f.write("")
    return path


# Tests
def test_no_output_file_means_current_dir_is_output_file():
    fake_args = FakeArgs(input_paths=[TEST_IMG])
    input_data = PdfInputData(fake_args)

    expected_substring = (
        f"converted_output_{os.path.basename(TEST_IMG).rsplit('.', 1)[0]}.pdf"
    )
    assert expected_substring in input_data.output_path


def test_recursive_dir_filtering():
    input_names = ["input1.pdf", "input2.PDF", "input3.png"]
    fake_dir = make_fake_dir("recursive_dir", input_names)

    fake_args = FakeArgs(
        input_paths=[fake_dir], output_path="output.pdf", recursive=True
    )
    input_data = PdfInputData(fake_args)

    expected_files = [os.path.join(fake_dir, name) for name in input_names]
    assert input_data.input_files == expected_files


def test_passing_in_dir_without_recursive():
    fake_dir = make_fake_dir("non_recursive_dir")

    fake_args = FakeArgs(
        input_paths=[fake_dir], output_path="output.pdf", recursive=False
    )

    with pytest.raises(PdfInputError):
        PdfInputData(fake_args)


def test_file_not_existing():
    fake_args = FakeArgs(
        input_paths=["non_existing_file.pdf"], output_path="output.pdf"
    )

    with pytest.raises(PdfInputError):
        PdfInputData(fake_args)


def test_already_existing_output_file():
    fake_output = os.path.join(TEST_PLAYGROUND, "output.pdf")
    with open(fake_output, "w") as f:
        f.write("")  # Create fake output file

    fake_args = FakeArgs(input_paths=[TEST_IMG], output_path=fake_output)

    with pytest.raises(PdfInputError):
        PdfInputData(fake_args)


def test_output_path_is_not_pdf():
    fake_output = os.path.join(TEST_PLAYGROUND, "output.txt")

    fake_args = FakeArgs(input_paths=[TEST_IMG], output_path=fake_output)

    with pytest.raises(PdfInputError):
        PdfInputData(fake_args)


def test_arg_override_for_output_path():
    fake_output = os.path.join(TEST_PLAYGROUND, "output.pdf")
    with open(fake_output, "w") as f:
        f.write("")  # Create fake output file

    fake_args = FakeArgs(
        input_paths=[TEST_IMG], output_path=fake_output, override_output_path=True
    )
    input_data = PdfInputData(fake_args)

    assert input_data.output_path == fake_output
