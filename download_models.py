#!/usr/bin/env python3
"""Download dialect parser model checkpoints from Hugging Face."""

import argparse
from pathlib import Path

from dialect_models import available_aliases, download_all_models, download_model, format_models


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download dialect parser models from the CAMeL-Lab Hugging Face collection."
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=available_aliases(),
        help="Download one model alias instead of all canonical dialect models.",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available dialect parser model aliases and exit.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.list_models:
        print(format_models())
        return

    model_dir = Path(__file__).resolve().parent / "models"
    try:
        if args.model:
            path = download_model(args.model, model_dir)
            print(f"Downloaded {args.model}: {path}")
            return

        for path in download_all_models(model_dir):
            print(f"Downloaded: {path}")
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
