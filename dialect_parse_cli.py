#!/usr/bin/env python3
"""Run dialect parser inference from the command line."""

import argparse
import os
import sys
import tempfile
from contextlib import contextmanager, nullcontext
from pathlib import Path
from typing import Iterator, List, Optional

from dialect_models import available_aliases, download_model, format_models, get_model


ROOT_DIR = Path(__file__).resolve().parent
CAMEL_PARSER_DIR = ROOT_DIR / "camel_parser"
MODEL_DIR = ROOT_DIR / "models"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Parse Arabic dialect text or CoNLL files with CAMeL-Lab dialect parser models."
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("-i", "--input", help="Input text or CoNLL file.")
    input_group.add_argument("-s", "--string", help="Input string to parse.")
    parser.add_argument(
        "-f",
        "--file_type",
        choices=("conll", "text", "preprocessed_text", "tokenized", "tokenized_tagged"),
        help="Input format.",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="msa-egy-glf",
        choices=available_aliases(),
        help="Dialect parser model alias. Defaults to msa-egy-glf.",
    )
    parser.add_argument(
        "-b",
        "--morphology_db_type",
        default="r13",
        help="CAMeL Tools morphology DB for text/preprocessed_text input. Defaults to r13.",
    )
    parser.add_argument(
        "-d",
        "--disambiguator",
        default="bert",
        choices=("bert", "mle"),
        help="Disambiguator for text/preprocessed_text input. Defaults to bert.",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available dialect parser model aliases and exit.",
    )
    args = parser.parse_args()

    if args.list_models:
        return args
    if args.file_type is None:
        parser.error("-f/--file_type is required unless --list-models is used")
    if args.input is None and args.string is None:
        parser.error("one of -i/--input or -s/--string is required")
    if args.file_type == "conll" and args.string is not None:
        parser.error("-f conll requires -i/--input")
    return args


def ensure_camel_parser_submodule() -> None:
    if not (CAMEL_PARSER_DIR / "src").is_dir():
        raise SystemExit(
            "Cannot find the camel_parser submodule. Run:\n"
            "  git submodule update --init --recursive"
        )
    sys.path.insert(0, str(CAMEL_PARSER_DIR))


def read_input_lines(input_path: Optional[str], string_text: Optional[str]) -> List[str]:
    if string_text is not None:
        return [string_text]
    if input_path is None:
        return []
    with open(input_path, "r", encoding="utf-8") as input_file:
        return [line for line in input_file.readlines() if line.strip()]


@contextmanager
def normalized_conll_path(input_path: str) -> Iterator[str]:
    with open(input_path, "rb") as input_file:
        data = input_file.read().rstrip(b"\n") + b"\n\n"

    suffix = Path(input_path).suffix or ".conllx"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        with tmp:
            tmp.write(data)
        yield tmp.name
    finally:
        try:
            os.unlink(tmp.name)
        except FileNotFoundError:
            pass


def main() -> None:
    args = parse_args()
    if args.list_models:
        print(format_models())
        return

    ensure_camel_parser_submodule()
    model = get_model(args.model)
    try:
        model_path = download_model(args.model, MODEL_DIR)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc

    try:
        from camel_tools.utils.charmap import CharMapper
        from pandas import read_csv
        from transformers.utils import logging

        from src.conll_output import print_to_conll, text_tuples_to_string
        from src.data_preparation import get_file_type_params, parse_text
    except ModuleNotFoundError as exc:
        raise SystemExit(
            f"Missing dependency '{exc.name}'. Install dependencies with: "
            "pip install -r camel_parser/requirements.txt"
        ) from exc

    logging.set_verbosity_error()

    arclean = CharMapper.builtin_mapper("arclean")
    clitic_feats_df = read_csv(CAMEL_PARSER_DIR / "data/clitic_feats.csv")
    clitic_feats_df = clitic_feats_df.astype(str).astype(object)

    lines = read_input_lines(args.input, args.string)
    parse_input_path = args.input
    conll_context = (
        normalized_conll_path(args.input)
        if args.file_type == "conll" and args.input is not None
        else nullcontext(args.input)
    )

    with conll_context as normalized_path:
        if args.file_type == "conll":
            parse_input_path = normalized_path

        file_type_params = get_file_type_params(
            lines,
            args.file_type,
            parse_input_path,
            str(model_path),
            arclean,
            args.disambiguator,
            clitic_feats_df,
            model.tagset,
            args.morphology_db_type,
        )
        try:
            parsed_text_tuples = parse_text(args.file_type, file_type_params)
        except FileNotFoundError as exc:
            if ".camel_tools" in str(exc) or "CAMELTOOLS_DATA" in str(exc):
                raise SystemExit(
                    "Missing CAMeL Tools data. For text/preprocessed_text input, install the "
                    "default morphology DB and BERT disambiguator data:\n"
                    "  camel_data -i morphology-db-msa-r13\n"
                    "  camel_data -i disambig-bert-unfactored-msa"
                ) from exc
            raise

    string_lines = text_tuples_to_string(
        parsed_text_tuples,
        args.file_type,
        sentences=lines,
    )
    print_to_conll(string_lines)


if __name__ == "__main__":
    main()
