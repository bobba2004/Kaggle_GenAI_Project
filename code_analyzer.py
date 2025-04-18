import ast

def analyze_python_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    tree = ast.parse(code)
    functions, classes, imports = [], [], []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            for n in node.names:
                imports.append(n.name)
    return {"functions": functions, "classes": classes, "imports": imports}
