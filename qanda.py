# qa_engine.py
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def create_qa_engine(vector_db):
    """Create a QA engine using LangChain."""
    # Create language model
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    
    # Create custom prompt template
    template = """You are a technical assistant that helps developers understand codebases. 
    Answer the following question about the code repository:
    
    Question: {question}
    
    Use only the following context to answer the question. If you don't know the answer based on this context, say "I don't have enough information about that in the codebase."
    
    {context}
    
    When referring to code or files, include their relative paths. Format code snippets with markdown.
    """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": prompt}
    )
    
    return qa_chain

def format_response_with_links(response, retrieved_docs):
    """Format response with links to the original files."""
    enhanced_response = response
    
    # Add a section with links to relevant files
    enhanced_response += "\n\n**Relevant Files:**\n"
    
    seen_files = set()
    for doc in retrieved_docs:
        file_path = doc.metadata.get("source")
        start_index = doc.metadata.get("start_index", 0)
        
        if file_path and file_path not in seen_files:
            # For local development, you can use file:// links
            # In a web app, you might create links to GitHub
            line_number = count_lines_until_index(doc.metadata.get("file_path"), start_index)
            enhanced_response += f"- {file_path} (around line {line_number})\n"
            seen_files.add(file_path)
    
    return enhanced_response

def count_lines_until_index(file_path, char_index):
    """Count the number of lines until the given character index."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Count newlines up to the character index
            return content[:char_index].count('\n') + 1
    except Exception:
        return 1  # Default to line 1 if there's an error
