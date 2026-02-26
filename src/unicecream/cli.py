# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import libcst as cst
from libcst import RemovalSentinel


class IcecreamRemover(cst.CSTTransformer):
    def leave_Import(self, original_node, updated_node):
        # import icecream
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
        # from icecream import ic
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
        # ic(...)
        if isinstance(updated_node.func, cst.Name) and updated_node.func.value == "ic":
            if len(updated_node.args) == 1 and updated_node.args[0].keyword is None:
                return updated_node.args[0].value

            parent = self.get_metadata(cst.metadata.ParentNodeProvider, original_node)
            if isinstance(parent, cst.Expr):
                return RemovalSentinel.REMOVE

        return updated_node


def clean_code(code: str) -> str:
    try:
        wrapper = cst.MetadataWrapper(cst.parse_module(code))
        tree = wrapper.visit(IcecreamRemover())
        return tree.code
    except Exception:
        return code


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

if __name__ == "__main__":
    main()
