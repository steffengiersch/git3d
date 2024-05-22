from git import Repo
import os


def is_file_in_git(git, file_path: str):
    """Check if file is tracked by git."""
    try:
        # If git returns a filename then file is tracked
        return git.ls_files(file_path) == file_path
    except:
        return False


def walk_through_repo(git):
    repo_path = git.working_dir
    for dirpath, dirnames, filenames in os.walk(repo_path):
        for file_name in filenames:
            full_path = os.path.join(dirpath, file_name)
            relative_path = os.path.relpath(str(full_path), repo_path)
            if is_file_in_git(git, relative_path):
                print(relative_path)


if '__main__' == __name__:
    repo = Repo(os.getenv('REPO_PATH'))
    git = repo.git
    walk_through_repo(git)
