# -*- coding: utf-8 -*-

import libcst as cst


def collect_violations(code, rules):
    violations = []

    wrapper = cst.MetadataWrapper(cst.parse_module(code))

    for rule_cls in rules:
        rule = rule_cls()
        wrapper.visit(rule)
        violations.extend(rule.violations)

    return violations
