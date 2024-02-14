'''file handling like extracting an archive'''
import gzip
import os


def extract_all_files(file_paths: list[str]) -> list[str]:
    '''
    Extracts given files and returns the location of the extracted files.
    '''
    return [extract_file(path) for path in file_paths]


def extract_file(file_path: str) -> str:
    '''
    Extracts a single file and removes the archive.
    '''
    base_path = os.path.split(file_path)[0]
    file_name = os.path.split(file_path)[1]
    target_file_path = os.path.join(base_path, file_name.removesuffix('.gz'))
    with gzip.open(file_path, 'rb') as archive_handle, \
            open(target_file_path, 'wb') as file_handle:
        file_handle.write(archive_handle.read())
    os.remove(file_path)
    return target_file_path


def read_file_formatted(file_path) -> list[list]:
    '''
    Reads the file content and returnes a formatted list of lists.
    '''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    split_rows = []
    for line_number in range(1, len(file_content), 1):
        line_content = file_content[line_number].split(';')
        split_rows.append([content.strip() for content in line_content])
    return split_rows
