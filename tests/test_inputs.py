from pdf_combiner.input import PdfInputData, PdfInputError
import shutil
import os

CURRENT_DIR = os.path.dirname(__file__)

TEST_PLAYGROUND = f"{CURRENT_DIR}/test_playground"
TEST_IMG = f"{CURRENT_DIR}/samples/test_img.png"


def make_fake_dir(dir_name, files_to_fake_create=None):
    shutil.rmtree(f"{TEST_PLAYGROUND}/{dir_name}", ignore_errors=True)
    os.makedirs(f"{TEST_PLAYGROUND}/{dir_name}")

    if files_to_fake_create:
        for name in files_to_fake_create:
            with open(f"{TEST_PLAYGROUND}/{dir_name}/{name}", "w") as f:
                f.write("")


def delete_fake_dir(dir_name):
    shutil.rmtree(f"{TEST_PLAYGROUND}/{dir_name}", ignore_errors=True)


def test_no_output_file_means_current_dir_is_output_file():
    # create fake args object
    input_names = [TEST_IMG]

    class FakeArgs:
        input_paths = input_names
        output_path = None
        recursive = False
        override_output_path = False

    input_data = PdfInputData(FakeArgs)

    substring = (
        f"converted_output_{os.path.basename(TEST_IMG[:TEST_IMG.rfind('.')])}.pdf"
    )

    assert substring in input_data.output_path


def test_recursive_dir_filtering():
    # create fake args object
    input_names = ["input1.pdf", "input2.PDF", "input3.png"]
    # create a fake directory with 2 files
    fake_dir = f"{TEST_PLAYGROUND}/recursive_dir"
    shutil.rmtree(fake_dir, ignore_errors=True)

    os.makedirs(fake_dir)

    for name in input_names:
        with open(f"{fake_dir}/{name}", "w") as f:
            f.write("")

    class FakeArgs:
        input_paths = [fake_dir]
        output_path = "output.pdf"
        recursive = True
        override_output_path = False

    input_data = PdfInputData(FakeArgs)

    assert input_data.input_files == [f"{fake_dir}/{name}" for name in input_names]

    shutil.rmtree(fake_dir, ignore_errors=True)


def test_passing_in_dir_without_recursive():
    fake_dir = f"{TEST_PLAYGROUND}/non_recursive_dir"
    shutil.rmtree(fake_dir, ignore_errors=True)

    os.makedirs(fake_dir)

    class FakeArgs:
        input_paths = [fake_dir]
        output_path = "output.pdf"
        recursive = False
        override_output_path = False

    # should raise a PdfInputError
    try:
        input_data = PdfInputData(FakeArgs)
        assert False
    except PdfInputError:
        assert True


def test_file_not_existing():
    class FakeArgs:
        input_paths = ["non_existing_file.pdf"]
        output_path = "output.pdf"
        recursive = False

    # should raise a PdfInputError
    try:
        input_data = PdfInputData(FakeArgs)
        assert False
    except PdfInputError:
        assert True


def test_already_existing_output_file():
    # create fake args object
    input_names = [TEST_IMG]
    fake_output_path = f"{TEST_PLAYGROUND}/output.pdf"
    with open(fake_output_path, "w") as f:
        f.write("")

    class FakeArgs:
        input_paths = input_names
        output_path = fake_output_path
        recursive = False
        override_output_path = False

    try:
        input_data = PdfInputData(FakeArgs)
        assert False
    except PdfInputError:
        assert True

    os.remove(fake_output_path)


def test_output_path_is_not_pdf():
    # create fake args object
    input_names = [TEST_IMG]
    fake_output_path = f"{TEST_PLAYGROUND}/output.txt"

    class FakeArgs:
        input_paths = input_names
        output_path = fake_output_path
        recursive = False
        override_output_path = False

    try:
        input_data = PdfInputData(FakeArgs)
        assert False
    except PdfInputError:
        assert True


def test_arg_override_for_output_path():
    # create fake args object
    input_names = [TEST_IMG]
    fake_output_path = f"{TEST_PLAYGROUND}/output.pdf"

    # make the output file
    with open(fake_output_path, "w") as f:
        f.write("")

    class FakeArgs:
        input_paths = input_names
        output_path = fake_output_path
        recursive = False
        override_output_path = True

    input_data = PdfInputData(FakeArgs)

    assert input_data.output_path == fake_output_path
