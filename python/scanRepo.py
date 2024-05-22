from git import Repo
import os

REPO_PATH = os.getenv('REPO_PATH')


def is_file_in_git(git, file_path: str):
    """Check if file is tracked by git."""
    try:
        # If git returns a filename then file is tracked
        return git.ls_files(file_path) == file_path
    except:
        return False


def walk_through_repo(git, folder_path: str):
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file_name in filenames:
            full_path = os.path.join(dirpath, file_name)
            relative_path = os.path.relpath(str(full_path), folder_path)
            if is_file_in_git(git, relative_path):
                print(relative_path)


if '__main__' == __name__:
    repo = Repo(REPO_PATH)
    git = repo.git
    walk_through_repo(git, repo.working_dir)
