# -*- coding: utf-8 -*-

import libcst as cst

from unicecream.rules.base import RuleViolation


class IC002_ImportRule(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)

    def __init__(self):
        self.violations = []

    def visit_Import(self, node):
        for alias in node.names:
            if (
                isinstance(alias.name, cst.Name)
                and alias.name.value == "icecream"
            ):
                pos = self.get_metadata(
                    cst.metadata.PositionProvider,
                    node
                )

                self.violations.append(
                    RuleViolation(
                        pos.start.line,
                        pos.start.column + 1,
                        "IC002",
                        "remove icecream import",
                    )
                )


class IC003_FromImportRule(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)

    def __init__(self):
        self.violations = []

    def visit_ImportFrom(self, node):
        if (
            node.module
            and isinstance(node.module, cst.Name)
            and node.module.value == "icecream"
        ):
            pos = self.get_metadata(
                cst.metadata.PositionProvider,
                node
            )

            self.violations.append(
                RuleViolation(
                    pos.start.line,
                    pos.start.column + 1,
                    "IC003",
                    "remove icecream from-import",
                )
            )
