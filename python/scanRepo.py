from git import Repo
import os
from datetime import datetime
from functools import reduce


def is_file_in_git(git, file_path: str):
    try:
        return git.ls_files(file_path) == file_path
    except:
        return False


def extract_author_list(repo, relative_path) -> list:
    authors = {}
    commits_touching_path = list(repo.iter_commits(paths=relative_path))
    for commit in commits_touching_path:
        points = 1 / (2 ** ((datetime.now() - datetime.fromtimestamp(commit.committed_date)).days + 1))
        authors[commit.author.name] = authors.get(commit.author.name, 0) + points
    authors_list = reduce(lambda al, a: [*al, {'author': a, 'knowledge': authors[a]}], authors.keys(), [])
    return authors_list


def walk_through_repo(repo):
    git = repo.git
    repo_path = git.working_dir
    for dirpath, dirnames, filenames in os.walk(repo_path):
        for file_name in filenames:
            full_path = os.path.join(dirpath, file_name)
            relative_path = os.path.relpath(str(full_path), repo_path)
            if is_file_in_git(git, relative_path):
                print(relative_path)
                author_list = extract_author_list(repo, relative_path)
                print(author_list)


if '__main__' == __name__:
    repo = Repo(os.getenv('REPO_PATH'))
    walk_through_repo(repo)
