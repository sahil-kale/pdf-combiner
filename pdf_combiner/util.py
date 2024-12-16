import os


def get_files_with_extensions(extensions, exclude_dirs, base_path="."):
    # Convert the base path to an absolute path
    base_path = os.path.abspath(base_path)

    files = []
    for root, dirs, filenames in os.walk(base_path):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # All paths returned by os.walk will now be absolute because base_path is absolute
        files.extend(
            os.path.join(root, filename)
            for filename in filenames
            if filename.endswith(extensions)
        )
    return files
