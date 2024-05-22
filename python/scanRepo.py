from git import Repo
import os


def is_file_in_git(git, file_path: str):
    try:
        return git.ls_files(file_path) == file_path
    except:
        return False


def walk_through_repo(repo):
    git = repo.git
    repo_path = git.working_dir
    for dirpath, dirnames, filenames in os.walk(repo_path):
        for file_name in filenames:
            full_path = os.path.join(dirpath, file_name)
            relative_path = os.path.relpath(str(full_path), repo_path)
            if is_file_in_git(git, relative_path):
                print(relative_path)
                commits_touching_path = list(repo.iter_commits(paths=relative_path))
                for commit in commits_touching_path:
                    print(f"{commit.hexsha}: {commit.message}")


if '__main__' == __name__:
    repo = Repo(os.getenv('REPO_PATH'))
    walk_through_repo(repo)
