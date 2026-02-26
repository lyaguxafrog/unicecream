from pathlib import Path
import sys

from unicecream.cli.parser import build_parser
from unicecream.core.config import load_config
from unicecream.core.utils import process_file
from unicecream.rules import (
    IC001_CallRule,
    IC002_ImportRule,
    IC003_FromImportRule,
)


RULES = {
    "IC001": IC001_CallRule,
    "IC002": IC002_ImportRule,
    "IC003": IC003_FromImportRule,
}


def is_excluded(path: Path, exclude):
    return any(part in exclude for part in path.parts)


def collect_rules(select, ignore):
    if select:
        rules = [RULES[c] for c in select if c in RULES]
    else:
        rules = list(RULES.values())

    if ignore:
        ignore_set = set(ignore)
        rules = [
            r for code, r in RULES.items()
            if code not in ignore_set
        ]

    return rules

def main():
    parser = build_parser()
    args = parser.parse_args()

    config = load_config()

    select = args.select or config["select"]
    ignore = args.ignore or config["ignore"]
    exclude = config["exclude"]

    rules = collect_rules(select, ignore)

    changed = False

    # pre-commit
    if args.files:
        for file_path in args.files:
            path = Path(file_path)

            if not path.exists() or path.suffix != ".py":
                continue

            changed |= process_file(
                path,
                args.check,
                rules,
                select,
                ignore,
            )

    else:
        target = Path(args.path)

        if target.is_dir():
            for file in target.rglob("*.py"):
                if is_excluded(file, exclude):
                    continue

                changed |= process_file(
                    file,
                    args.check,
                    rules,
                    select,
                    ignore,
                )

        elif target.is_file():
            changed |= process_file(
                target,
                args.check,
                rules,
                select,
                ignore,
            )

        else:
            print("No python files found")
            sys.exit(1)

    if args.check and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
