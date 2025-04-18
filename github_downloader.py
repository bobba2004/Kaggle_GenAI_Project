import subprocess
import os
import tempfile

def clone_repo(repo_url):
    temp_dir = tempfile.mkdtemp()
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    clone_path = os.path.join(temp_dir, repo_name)

    subprocess.run(["git", "clone", repo_url, clone_path], check=True)
    return clone_path
