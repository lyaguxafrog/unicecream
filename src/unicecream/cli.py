# -*- coding: utf-8 -*-

import ast
import sys
from pathlib import Path


class IcecreamRemover(ast.NodeTransformer):
    def visit_Import(self, node):
        node.names = [n for n in node.names if n.name != "icecream"]
        if not node.names:
            return None
        return node

    def visit_ImportFrom(self, node):
        if node.module == "icecream":
            node.names = [n for n in node.names if n.name != "ic"]
            if not node.names:
                return None
        return node

    def visit_Expr(self, node):
        # ic(...)
        if isinstance(node.value, ast.Call):
            if self._is_ic_call(node.value):
                if len(node.value.args) == 1 and not node.value.keywords:
                    return ast.Expr(value=node.value.args[0])
                return None
        return self.generic_visit(node)

    def visit_Call(self, node):
        # x = ic(...)
        if self._is_ic_call(node):
            if len(node.args) == 1 and not node.keywords:
                return self.visit(node.args[0])
        return self.generic_visit(node)

    @staticmethod
    def _is_ic_call(node):
        return (
            isinstance(node.func, ast.Name)
            and node.func.id == "ic"
        )


def clean_code(code: str) -> str:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code

    transformer = IcecreamRemover()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    return ast.unparse(new_tree) + "\n"


def process_file(path: Path, check: bool = False) -> bool:
    original = path.read_text(encoding="utf-8")
    cleaned = clean_code(original)

    if cleaned != original:
        if check:
            print(f"would clean: {path}")
            return True
        else:
            path.write_text(cleaned, encoding="utf-8")
            print(f"cleaned: {path}")
            return False
    else:
        print(f"unchanged: {path}")
        return False


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: unicecream [--check] <file_or_directory>")
        sys.exit(1)

    check = False
    if "--check" in args:
        check = True
        args.remove("--check")

    target = Path(args[0])
    changed = False

    if target.is_file() and target.suffix == ".py":
        changed |= process_file(target, check)
    elif target.is_dir():
        for file in target.rglob("*.py"):
            changed |= process_file(file, check)
    else:
        print("No Python files found.")
        sys.exit(1)

    if check and changed:
        sys.exit(1)
