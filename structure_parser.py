import os

def get_file_structure(repo_path):
    structure = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            rel_dir = os.path.relpath(root, repo_path)
            rel_file = os.path.join(rel_dir, file)
            structure.append(rel_file)
    return structure
