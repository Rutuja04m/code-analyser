import ast

def parse_python_code(file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        source = f.read()
        tree = ast.parse(source)

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "docstring": ast.get_docstring(node),
            })
    return [{"file": file_path, "functions": functions}]
