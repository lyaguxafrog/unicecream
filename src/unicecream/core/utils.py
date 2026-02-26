# -*- coding: utf-8 -*-

from pathlib import Path

import libcst as cst


def should_report(code, select, ignore):
    if select and code not in select:
        return False
    if ignore and code in ignore:
        return False
    return True

def process_file(path: Path, check: bool, rules, select, ignore):
    original_code = path.read_text(encoding="utf-8")

    wrapper = cst.MetadataWrapper(cst.parse_module(original_code))

    violations = []
    _transformer = None

    for rule_cls in rules:
        rule = rule_cls()

        if hasattr(rule, "transform"):
            _transformer = rule

        wrapper.visit(rule)
        violations.extend(rule.violations)

    violations = [
        v for v in violations
        if should_report(v.code, select, ignore)
    ]

    if check:
        for v in violations:
            print(v.format(path))
        return bool(violations)

    from unicecream.rules.ic_calls import IcecreamFixTransformer

    try:
        tree = cst.MetadataWrapper(
            cst.parse_module(original_code)
        ).visit(IcecreamFixTransformer())

        new_code = tree.code

        if new_code != original_code:
            path.write_text(new_code, encoding="utf-8")
            print(f"fixed: {path}")

        return False

    except Exception:
        return False
