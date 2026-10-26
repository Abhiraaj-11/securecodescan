import ast


class PythonVulnVisitor(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path
        self.findings = []

    # -------------------------
    # 1. Detect hardcoded secrets
    # -------------------------
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.lower()

                if var_name in ["password", "secret", "api_key", "apikey", "token"]:
                    self.findings.append({
                        "type": "Hardcoded Secret",
                        "severity": "HIGH",
                        "file": self.file_path,
                        "line": node.lineno
                    })

        self.generic_visit(node)

    # -------------------------
    # 2. Detect SQL Injection
    # -------------------------
    def visit_Call(self, node):
        try:
            func_name = ""

            if isinstance(node.func, ast.Attribute):
                func_name = node.func.attr

            # detect cursor.execute(...)
            if func_name == "execute":
                for arg in node.args:
                    if isinstance(arg, ast.BinOp):  # string concatenation
                        self.findings.append({
                            "type": "SQL Injection",
                            "severity": "CRITICAL",
                            "file": self.file_path,
                            "line": node.lineno
                        })

        except:
            pass

        self.generic_visit(node)

    # -------------------------
    # 3. Detect Command Injection
    # -------------------------
    def visit_Call(self, node):
        try:
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in ["system", "popen", "call", "run"]:
                    for arg in node.args:
                        if isinstance(arg, ast.BinOp):
                            self.findings.append({
                                "type": "Command Injection",
                                "severity": "CRITICAL",
                                "file": self.file_path,
                                "line": node.lineno
                            })

        except:
            pass

        self.generic_visit(node)


def scan_python_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read(), filename=file_path)

        visitor = PythonVulnVisitor(file_path)
        visitor.visit(tree)

        return visitor.findings

    except Exception:
        return []