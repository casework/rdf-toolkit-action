import argparse
import filecmp
import hashlib
import subprocess
import sys
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
            opener = urllib.request.build_opener()
            # Set the user agent to avoid HTTP/406 error codes
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve('https://files.caseontology.org/rdf-toolkit-1.11.0.jar', 'rdf-toolkit.jar')
            # Validate the hash
            if not check_filehash('rdf-toolkit.jar', 'cff74ca5835cb6c4935c613c901e064b7d166fdcc874e49da5104cf783036b99'):
                raise Exception('Invalid hash value')
        except Exception as e:
            print(f'Error downloading rdf-toolkit.jar: {e}')


def check_filehash(filename: str, expected_hash: str) -> bool:
    """
    Checks the hash of a file against an expected value
    Source: https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
    """
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest() == expected_hash


def is_normalized(filename: str, autofix: bool = False) -> bool:
    """
    Determines if the provided ttl file is normalized as defined by rdf-toolkit.jar.
    """
    # Run the normalization in place 
    output_filename = filename + '.check'
    result = subprocess.run(['java', '-jar', 'rdf-toolkit.jar', 
                                '--inline-blank-nodes',
                                '--source', filename,
                                '--source-format', 'turtle',
                                '--target', output_filename,
                                '--target-format', 'turtle'], 
                                stdout=subprocess.PIPE)    

    # Determine if the process ran successfully
    if result.returncode == 0:
        # Determine if the files are the same
        retval = filecmp.cmp(filename, output_filename, shallow=False)
        
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
    

def main():
    """
    The entrypoint for the pre-commit hook. Accepts 1 -> n filenames as positional arguments
    and returns 0 if all are normalized as defined by rdf-toolkit.jar and 1 if any are not.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--autofix', action='store_true', help='Whether to automatically format the input file')
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args()

    # Ensure the library is available
    ensure_library()

    if len(args.filenames) == 0:
        print('Warning: no files found')

    retval = 0
    # Loop through the provided filenames and return 1 if any of them are not normalized
    for filename in args.filenames:
        if filename.endswith('.ttl'):
            if not is_normalized(filename, args.autofix):
                print(f'Error: {filename} is not normalized')
                retval = 1
        else:
            print(f'File is not a ttl file and was skipped: {filename}')

    sys.exit(retval)


if __name__ == '__main__':
    raise main()