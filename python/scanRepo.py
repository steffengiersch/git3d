from git import Repo
import os
from datetime import datetime
from functools import reduce
import time
import json


def is_file_in_git(git, file_path: str):
    try:
        return git.ls_files(file_path) == file_path
    except:
        return False


def extract_author_list(commits_touching_path) -> list:
    authors = {}
    for commit in commits_touching_path:
        points = 1 / (((datetime.now() - datetime.fromtimestamp(commit.committed_date)).days // 7) + 1)
        authors[commit.author.name] = authors.get(commit.author.name, 0) + points
    authors_list = reduce(lambda al, a: [*al, {'author': a, 'knowledge': authors[a]}], authors.keys(), [])
    return authors_list


def recursive_walk_repo(repo, relative_path, current):
    git = repo.git
    repo_path = git.working_dir
    abs_path = os.path.join(repo_path, relative_path)
    if os.path.isfile(abs_path) and is_file_in_git(git, relative_path):
        commits_touching_path = list(repo.iter_commits(paths=relative_path))
        number_of_changes = len(commits_touching_path)
        author_list = extract_author_list(commits_touching_path)
        criticality = reduce(lambda c, a: c + a['knowledge'], author_list, 0)
        size_in_bytes = os.path.getsize(abs_path)
        file_descriptor = {
            'type': 'file',
            'name': os.path.basename(relative_path),
            'extension': os.path.splitext(relative_path)[1],
            'created': time.ctime(os.path.getctime(abs_path)),
            'last_modified': time.ctime(os.path.getmtime(abs_path)),
            'changes': number_of_changes,
            'sizeInBytes': size_in_bytes,
            'contributors': author_list,
            'criticality': criticality,
        }
        current['children'].append(file_descriptor)
        return (number_of_changes, criticality, size_in_bytes)
    else:
        sum_number_of_changes = 0
        sum_criticality = 0
        sum_size_in_bytes = 0
        folder_descriptor = {
            'type': 'folder',
            'name': os.path.basename(relative_path),
            'created': time.ctime(os.path.getctime(abs_path)),
            'last_modified': time.ctime(os.path.getmtime(abs_path)),
            'children': [],
        }
        for entry in os.listdir(str(abs_path)):
            abs_entry_path = os.path.join(str(abs_path), entry)
            if os.path.isfile(abs_entry_path) or not entry.startswith('.'):
                rel_entry_path = os.path.join(relative_path, entry)
                (criticality, number_of_changes, size_in_bytes) = recursive_walk_repo(repo=repo, relative_path=rel_entry_path, current=folder_descriptor)
                sum_number_of_changes += number_of_changes
                sum_criticality += criticality
                sum_size_in_bytes += size_in_bytes
        folder_descriptor['criticality'] = sum_criticality
        folder_descriptor['sizeInBytes'] = sum_size_in_bytes
        folder_descriptor['number_of_changes'] = sum_number_of_changes
        current['children'].append(folder_descriptor)
        return (sum_number_of_changes, sum_criticality, sum_size_in_bytes)


def start(repo_path, out_file_path):
    repo = Repo(repo_path)
    root = {'children': []}
    recursive_walk_repo(repo=repo, relative_path="", current=root)
    with open(out_file_path, 'w') as f:
        json.dump(root, f)


if '__main__' == __name__:
    start(os.getenv('REPO_PATH'), os.getenv('OUT_FILE_PATH'))
