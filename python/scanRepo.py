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


global_author_list = []


def extract_author_list(commits_touching_path: list) -> list:
    authors = {}
    for commit in commits_touching_path:
        if commit.author.name not in global_author_list:
            global_author_list.append(commit.author.name)
        if commit.author.name not in authors:
            points = 1 / (((datetime.now() - datetime.fromtimestamp(commit.committed_date)).days // 30) + 1)
            authors[commit.author.name] = points
    author_list = reduce(lambda al, a: [*al, {'name': a, 'knowledge': authors[a]}], authors.keys(), [])
    return author_list


def merge_author_lists(target_list: list, source_list: list) -> list:
    target_dict = reduce(lambda td, a: {**td, a['name']: a['knowledge']}, target_list, {})
    for source_entry in source_list:
        if source_entry['name'] in target_dict:
            target_dict[source_entry['name']] += source_entry['knowledge']
        else:
            target_dict[source_entry['name']] = source_entry['knowledge']
    return reduce(lambda tl, a: [*tl, {'name': a, 'knowledge': target_dict[a]}], target_dict.keys(), [])


def normalize_author_list(author_list: list, number_of_files) -> list:
    return reduce(lambda al, a: [*al, {'name': a['name'], 'knowledge': a['knowledge'] / number_of_files}], author_list, [])

def recursive_walk_repo(repo, relative_path, current):
    print(f"scan: {relative_path}")
    git = repo.git
    repo_path = git.working_dir
    abs_path = os.path.join(repo_path, relative_path)
    if os.path.isfile(abs_path):
        if is_file_in_git(git, relative_path):
            commits_touching_path = list(repo.iter_commits(paths=relative_path))
            number_of_changes = len(commits_touching_path)
            author_list = extract_author_list(commits_touching_path)
            max_knowledge = reduce(lambda c, a: a['knowledge'] if a['knowledge'] > c else c, author_list, 0)
            criticality = 1 - max_knowledge
            size_in_bytes = os.path.getsize(abs_path)
            file_descriptor = {
                'type': 'file',
                'name': os.path.basename(relative_path),
                'extension': os.path.splitext(relative_path)[1],
                'changes': number_of_changes,
                'sizeInBytes': size_in_bytes,
                'contributors': author_list,
                'criticality': criticality,
            }
            current['children'].append(file_descriptor)
            return (number_of_changes, criticality, size_in_bytes, author_list, 1)
        else:
            return (0, 0, 0, [], 0)
    else:
        sum_number_of_changes = 0
        sum_criticality = 0
        sum_size_in_bytes = 0
        sum_author_list = []
        sum_number_of_files = 0
        folder_descriptor = {
            'type': 'folder',
            'name': os.path.basename(relative_path) if len(relative_path) > 0 else '.',
            'children': [],
        }
        for entry in os.listdir(str(abs_path)):
            abs_entry_path = os.path.join(str(abs_path), entry)
            if os.path.isfile(abs_entry_path) or not entry.startswith('.'):
                rel_entry_path = os.path.join(relative_path, entry)
                (number_of_changes, criticality, size_in_bytes, author_list, number_of_files) = recursive_walk_repo(repo=repo, relative_path=rel_entry_path, current=folder_descriptor)
                sum_number_of_changes += number_of_changes
                sum_criticality += criticality
                sum_size_in_bytes += size_in_bytes
                sum_number_of_files += number_of_files
                sum_author_list = merge_author_lists(sum_author_list, author_list)
        normalized_author_list = normalize_author_list(author_list=sum_author_list, number_of_files=sum_number_of_files)
        max_knowledge = reduce(lambda c, a: a['knowledge'] if a['knowledge'] > c else c, normalized_author_list, 0)
        criticality = 1 - max_knowledge
        folder_descriptor['criticality'] = criticality
        folder_descriptor['sizeInBytes'] = sum_size_in_bytes
        folder_descriptor['number_of_changes'] = sum_number_of_changes
        folder_descriptor['contributors'] = normalized_author_list
        current['children'].append(folder_descriptor)
        return (sum_number_of_changes, sum_criticality, sum_size_in_bytes, sum_author_list, sum_number_of_files)


def start(repo_path, out_file_path):
    repo = Repo(repo_path)
    _root = {'children': []}
    recursive_walk_repo(repo=repo, relative_path="", current=_root)
    root = {
        'repository': {
            'name': os.path.basename(repo_path),
            'url': repo.remotes.origin.url,
            'path': repo_path,
        },
        'contributors': global_author_list,
        'filetree': _root['children']
    }
    with open(out_file_path, 'w') as f:
        json.dump(root, f)


if '__main__' == __name__:
    start(os.getenv('REPO_PATH'), os.getenv('OUT_FILE_PATH'))
