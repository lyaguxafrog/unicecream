# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import libcst as cst
from libcst import RemovalSentinel


class IcecreamFinder(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (
        cst.metadata.PositionProvider,
    )

    def __init__(self):
        self.violations = []

    def visit_Call(self, node):
        if isinstance(node.func, cst.Name) and node.func.value == "ic":
            pos = self.get_metadata(cst.metadata.PositionProvider, node)
            self.violations.append(
                (
                    pos.start.line,
                    pos.start.column + 1,
                    "IC001",
                    "remove icecream call",
                )
            )

    def visit_Import(self, node):
        for alias in node.names:
            if (
                isinstance(alias.name, cst.Name)
                and alias.name.value == "icecream"
            ):
                pos = self.get_metadata(cst.metadata.PositionProvider, node)
                self.violations.append(
                    (
                        pos.start.line,
                        pos.start.column + 1,
                        "IC002",
                        "remove icecream import",
                    )
                )

    def visit_ImportFrom(self, node):
        if (
            node.module
            and isinstance(node.module, cst.Name)
            and node.module.value == "icecream"
        ):
            pos = self.get_metadata(cst.metadata.PositionProvider, node)
            self.violations.append(
                (
                    pos.start.line,
                    pos.start.column + 1,
                    "IC003",
                    "remove icecream from-import",
                )
            )

class IcecreamRemover(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (
        cst.metadata.ParentNodeProvider,
    )

    def leave_Import(self, original_node, updated_node):
        names = [
            name for name in updated_node.names
            if not (
                isinstance(name.name, cst.Name)
                and name.name.value == "icecream"
            )
        ]

        if not names:
            return RemovalSentinel.REMOVE

        return updated_node.with_changes(names=names)

    def leave_ImportFrom(self, original_node, updated_node):
        if (
            original_node.module
            and isinstance(original_node.module, cst.Name)
            and original_node.module.value == "icecream"
        ):
            names = [
                name for name in updated_node.names
                if not (
                    isinstance(name, cst.ImportAlias)
                    and isinstance(name.name, cst.Name)
                    and name.name.value == "ic"
                )
            ]

            if not names:
                return RemovalSentinel.REMOVE

            return updated_node.with_changes(names=names)

        return updated_node

    def leave_Call(self, original_node, updated_node):
        if isinstance(updated_node.func, cst.Name) and updated_node.func.value == "ic":
            if len(updated_node.args) == 1 and updated_node.args[0].keyword is None:
                return updated_node.args[0].value

            parent = self.get_metadata(cst.metadata.ParentNodeProvider, original_node)
            if isinstance(parent, cst.Expr):
                return RemovalSentinel.REMOVE

        return updated_node

def find_violations(code: str):
    try:
        wrapper = cst.MetadataWrapper(cst.parse_module(code))
        finder = IcecreamFinder()
        wrapper.visit(finder)
        return sorted(set(finder.violations))
    except Exception:
        return []


def clean_code(code: str) -> str:
    try:
        wrapper = cst.MetadataWrapper(cst.parse_module(code))
        tree = wrapper.visit(IcecreamRemover())
        return tree.code
    except Exception:
        return code


def process_file(path: Path, check: bool = False) -> bool:
    original = path.read_text(encoding="utf-8")

    if check:
        violations = find_violations(original)
        if violations:
            for line, col, code, message in violations:
                print(
                    f"{path}:{line}:{col}: {code} {message}"
                )
            return True
        return False

    cleaned = clean_code(original)

    if cleaned != original:
        path.write_text(cleaned, encoding="utf-8")
        print(f"cleaned: {path}")
        return True

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


if __name__ == "__main__":
    main()
