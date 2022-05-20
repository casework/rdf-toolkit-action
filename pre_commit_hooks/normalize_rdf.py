import argparse
import filecmp
import subprocess
import urllib.request

from typing import Sequence
from os.path import exists


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

def is_normalized(filename: str) -> bool:
    """
    Determines if the provided ttl file is normalized as defined by rdf-toolkit.jar.
    """
    result = subprocess.run(['java', '-jar', 'rdf-toolkit.jar', 
                                '--infer-base-iri', 
                                '--inline-blank-nodes',
                                '--source', filename,
                                '--source-format', 'turtle',
                                '--target', filename + '.check',
                                '--target-format', 'turtle'], 
                                stdout=subprocess.PIPE)
    
    # Compare the original and the output file
    return result.returncode == 0 and filecmp.cmp(filename, filename + '.check', shallow=False)

def main(argv: Sequence[str] | None = None) -> int:
    """
    The entrypoint for the pre-commit hook. Accepts 1 -> n filenames as positional arguments
    and returns 0 if all are normalized as defined by rdf-toolkit.jar and 1 if any are not.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    # Ensure the library is available
    ensure_library()

    retval = 0
    # Loop through the provided filenames and return 1 if any of them are not normalized
    for filename in args.filenames:
        if not is_normalized(filename):
            print(f"Error: {filename} is not normalized")
            retval = 1

    return retval


if __name__ == '__main__':
    raise SystemExit(main())