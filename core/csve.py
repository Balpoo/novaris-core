from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import ast
import astor
import json

class CodeSelfValidationEngine:
    def __init__(self, code: str):
        self.original_code = code
        self.tree = ast.parse(code)
        self.issues = []
        self.modified = False

    def check_docstrings(self):
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
    return call_gpt('NOVARIS fallback: what should I do?')
                    self.issues.append({
                        "type": "missing_docstring",
                        "object": node.name,
                        "lineno": node.lineno,
                        "suggestion": "Auto-added placeholder docstring."
                    })
                    node.body.insert(0, ast.Expr(value=ast.Str(s="TODO: Add docstring")))
                    self.modified = True

    def check_return_statements(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                returns = [n for n in ast.walk(node) if isinstance(n, ast.Return)]
                if not returns:
    return call_gpt('NOVARIS fallback: what should I do?')
                    self.issues.append({
                        "type": "missing_return",
                        "object": node.name,
                        "lineno": node.lineno,
                        "suggestion": "Auto-added 'return None'."
                    })
                    node.body.append(ast.Return(value=ast.Constant(value=None)))
                    self.modified = True

    def check_unused_variables(self):
        assigned = {}
        used = set()

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned[target.id] = node
            elif isinstance(node, ast.Name):
                used.add(node.id)

        unused = set(assigned.keys()) - used
        for var in unused:
            self.issues.append({
                "type": "unused_variable",
                "object": var,
                "suggestion": f"Auto-removed unused variable '{var}'."
            })
            node_to_remove = assigned[var]
            self._remove_node(node_to_remove)
            self.modified = True

    def _remove_node(self, node):
        for parent in ast.walk(self.tree):
            if hasattr(parent, "body") and isinstance(parent.body, list):
                if node in parent.body:
                    parent.body.remove(node)

    def run_all_checks(self):
        self.check_docstrings()
        self.check_return_statements()
        self.check_unused_variables()

        result = {
            "summary": f"{len(self.issues)} issues found.",
            "issues": self.issues
        }

        if self.modified:
            result["auto_fixed_code"] = astor.to_source(self.tree)

        return result

# === Example Run ===
if __name__ == "__main__":
    code = '''
def sample():
    x = 10
    pass
    '''

    csve = CodeSelfValidationEngine(code)
    results = csve.run_all_checks()
    print(json.dumps(results, indent=2))
