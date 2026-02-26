# -*- coding: utf-8 -*-


class RuleViolation:
    def __init__(self, line, col, code, message):
        self.line = line
        self.col = col
        self.code = code
        self.message = message

    def format(self, path):
        return f"{path}:{self.line}:{self.col}: {self.code} {self.message}"
