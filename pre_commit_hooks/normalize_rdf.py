import argparse
import filecmp
import subprocess
import urllib.request

from os import remove
from os.path import exists
from shutil import copy


def ensure_library() -> None:
    """
    Ensures the rdf-toolkit.jar is available locally and downloads it if it doesn't exist.
    """
    if not exists('rdf-toolkit.jar'):
        # Download the file
        try:
            urllib.request.urlretrieve("https://github.com/trypuz/openfibo/blob/1f9ab415e8ebd131eadcc9b0fc46241adeeb0384/etc/serialization/rdf-toolkit.jar?raw=true", "rdf-toolkit.jar")
        except Exception as e:
            print(f"Error downloading rdf-toolkit.jar: {e}")

def is_normalized(filename: str, autofix: bool = False) -> bool:
    """
    Determines if the provided ttl file is normalized as defined by rdf-toolkit.jar.
    """
    # Run the normalization in place 
    output_filename = filename + '.check'
    result = subprocess.run(['java', '-jar', 'rdf-toolkit.jar', 
                                '--infer-base-iri', 
                                '--inline-blank-nodes',
                                '--source', filename,
                                '--source-format', 'turtle',
                                '--target', output_filename,
                                '--target-format', 'turtle'], 
                                stdout=subprocess.PIPE)    

    # Determine if the process ran successfully
    if result.returncode == 0:
        # Determine if the files are the same
        if filecmp.cmp(filename, output_filename, shallow=False):
            retval = True
        
        # Determine if "autofix" is set and copy the normalized file to the 
        if autofix:
            copy(output_filename, filename)
    else:
        # There was an error normalizing the file contents
        retval = False

    # Cleanup check file if it exists
    if exists(output_filename):
        remove(output_filename)

    return retval
    

def main(argv: list = []) -> int:
    """
    The entrypoint for the pre-commit hook. Accepts 1 -> n filenames as positional arguments
    and returns 0 if all are normalized as defined by rdf-toolkit.jar and 1 if any are not.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument('-a', '--autofix', action="store_true", default=False, help="Whether to automatically format the input file")
    args = parser.parse_args(argv)

    # Ensure the library is available
    ensure_library()

    retval = 0
    # Loop through the provided filenames and return 1 if any of them are not normalized
    for filename in args.filenames:
        if not is_normalized(filename, args.autofix):
            print(f"Error: {filename} is not normalized")
            retval = 1

    return retval


if __name__ == '__main__':
    raise SystemExit(main())