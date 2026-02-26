# -*- coding: utf-8 -*-

import libcst as cst

from unicecream.rules.base import RuleViolation


class IC001_CallRule(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)

    def __init__(self):
        self.violations = []

    def visit_Call(self, node):
        if isinstance(node.func, cst.Name) and node.func.value == "ic":
            pos = self.get_metadata(
                cst.metadata.PositionProvider,
                node
            )

            self.violations.append(
                RuleViolation(
                    pos.start.line,
                    pos.start.column + 1,
                    "IC001",
                    "remove icecream call",
                )
            )


class IcecreamFixTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (
        cst.metadata.ParentNodeProvider,
    )

    def leave_Import(self, original_node, updated_node):
        names = [
            n for n in updated_node.names
            if not (
                isinstance(n.name, cst.Name)
                and n.name.value == "icecream"
            )
        ]

        if not names:
            return cst.RemoveFromParent()

        return updated_node.with_changes(names=names)

    def leave_ImportFrom(self, original_node, updated_node):
        if (
            original_node.module
            and isinstance(original_node.module, cst.Name)
            and original_node.module.value == "icecream"
        ):
            return cst.RemoveFromParent()

        return updated_node

    def leave_Call(self, original_node, updated_node):
        if isinstance(updated_node.func, cst.Name) and updated_node.func.value == "ic":

            # ic(expr) → expr
            if len(updated_node.args) == 1:
                return updated_node.args[0].value

            parent = self.get_metadata(
                cst.metadata.ParentNodeProvider,
                original_node
            )

            if isinstance(parent, cst.Expr):
                return cst.RemoveFromParent()

        return updated_node
