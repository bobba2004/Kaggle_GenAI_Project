# main.py
import os
import argparse
from dotenv import load_dotenv
from repo_parser import clone_repository, parse_repository, chunk_documents
from vector_store import setup_vector_db, load_vector_db
from qa_engine import create_qa_engine, format_response_with_links

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Codebase QA Assistant")
    parser.add_argument("--repo", type=str, help="GitHub repository URL")
    parser.add_argument("--query", type=str, help="Question about the codebase")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the vector database")
    
    args = parser.parse_args()
    
    # Set up paths
    repo_path = "./temp_repo"
    db_path = "./chroma_db"
    
    # Clone and process repository if needed
    if args.repo or args.rebuild:
        if args.repo:
            print(f"Cloning repository: {args.repo}")
            clone_repository(args.repo, repo_path)
        
        print("Parsing repository files...")
        documents = parse_repository(repo_path)
        print(f"Found {len(documents)} files")
        
        print("Chunking documents...")
        chunks = chunk_documents(documents)
        print(f"Created {len(chunks)} chunks")
        
        print("Building vector database...")
        vector_db = setup_vector_db(chunks, db_path)
        print("Vector database built successfully")
    else:
        # Load existing vector database
        if not os.path.exists(db_path):
            print("Error: No existing database found. Please provide a repository URL.")
            return
        
        print("Loading existing vector database...")
        vector_db = load_vector_db(db_path)
    
    # Handle query if provided
    if args.query:
        print(f"\nQuestion: {args.query}")
        print("\nSearching for information...")
        
        # Create QA engine
        qa_engine = create_qa_engine(vector_db)
        
        # Get documents for context
        retrieved_docs = vector_db.similarity_search(args.query, k=5)
        
        # Get answer
        response = qa_engine.run(args.query)
        
        # Format response with links
        enhanced_response = format_response_with_links(response, retrieved_docs)
        
        print("\nAnswer:")
        print(enhanced_response)
    else:
        # Interactive mode
        print("\nEntering interactive mode. Type 'exit' to quit.")
        qa_engine = create_qa_engine(vector_db)
        
        while True:
            query = input("\nAsk a question about the codebase: ")
            if query.lower() in ["exit", "quit", "q"]:
                break
                
            retrieved_docs = vector_db.similarity_search(query, k=5)
            response = qa_engine.run(query)
            enhanced_response = format_response_with_links(response, retrieved_docs)
            
            print("\nAnswer:")
            print(enhanced_response)

if __name__ == "__main__":
    main()
