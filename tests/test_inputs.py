import input


def test_no_output_dir_means_current_dir_is_output_dir():
    # create fake args object
    input_names = ["input1.pdf", "input2.pdf"]

    class FakeArgs:
        input_paths = input_names
        output_path = None
        recursive = False

    PdfInputData = input.PdfInputData(FakeArgs)

    assert (
        PdfInputData.output_path
        == f"combined_output_{input_names[0]}_{input_names[1]}.pdf"
    )
