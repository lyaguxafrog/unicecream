# -*- coding: utf-8 -*-

import argparse


def build_parser():
    parser = argparse.ArgumentParser(
        prog="unicecream",
        description="Remove icecream debug calls from Python files",
    )

    parser.add_argument("path")

    parser.add_argument(
        "--check",
        action="store_true",
    )

    parser.add_argument(
        "--select",
        action="append",
        metavar="CODE",
        help="Select rule code",
    )

    parser.add_argument(
        "--ignore",
        action="append",
        metavar="CODE",
        help="Ignore rule code",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="unicecream 0.1.0",
    )

    parser.add_argument(
        "files",
        nargs="*",
        help="Files passed from pre-commit",
    )

    return parser
