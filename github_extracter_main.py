from extractor.github_downloader import clone_repo
from extractor.structure_parser import get_file_structure
from extractor.code_analyzer import analyze_python_file
from extractor.utils import get_file_type
import os

# 1. Clone repo
repo_url = "https://github.com/someone/someproject.git"
repo_path = clone_repo(repo_url)
print(f"Cloned to: {repo_path}")

# 2. Get file structure
files = get_file_structure(repo_path)
print(f"Files found:\n{files}")

# 3. Analyze files
for file in files:
    abs_path = os.path.join(repo_path, file)
    file_type = get_file_type(file)

    if file_type == 'py':
        result = analyze_python_file(abs_path)
        print(f"\n{file}")
        print(f"Functions: {result['functions']}")
        print(f"Classes: {result['classes']}")
        print(f"Imports: {result['imports']}")
    else:
        print(f"\n{file} (Not analyzed)")
