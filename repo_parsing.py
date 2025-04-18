# repo_parser.py
import os
import git
from langchain.text_splitter import RecursiveCharacterTextSplitter

def clone_repository(repo_url, local_path="./temp_repo"):
    """Clone a GitHub repository to a local directory."""
    if os.path.exists(local_path):
        import shutil
        shutil.rmtree(local_path)
    
    git.Repo.clone_from(repo_url, local_path)
    return local_path

def get_file_content(file_path):
    """Read and return file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def parse_repository(repo_path, exclude_dirs=None):
    """Parse all files in the repository and return a list of documents."""
    if exclude_dirs is None:
        exclude_dirs = ['.git', 'node_modules', 'venv', '.venv', '__pycache__']
    
    documents = []
    
    for root, dirs, files in os.walk(repo_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, repo_path)
            
            # Skip binary files and focus on text files (code, markdown, etc.)
            if file.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.h', '.c', '.html', '.css', 
                             '.md', '.txt', '.yml', '.yaml', '.json', '.xml', '.sh', '.bat', 
                             '.jsx', '.tsx', '.vue', '.go', '.rs', '.rb', '.php')):
                content = get_file_content(file_path)
                documents.append({
                    "content": content,
                    "metadata": {
                        "source": relative_path,
                        "file_path": file_path
                    }
                })
                
    return documents

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Split documents into chunks for embedding."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )
    
    chunks = []
    for doc in documents:
        doc_chunks = text_splitter.create_documents(
            [doc["content"]], 
            metadatas=[doc["metadata"]]
        )
        chunks.extend(doc_chunks)
    
    return chunks
