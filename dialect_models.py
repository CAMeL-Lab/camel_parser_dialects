"""Dialect parser model registry and Hugging Face download helpers."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple


@dataclass(frozen=True)
class DialectModel:
    alias: str
    repo_id: str
    filename: str
    tagset: str = "catib6"
    formalism: str = "catib"


_CANONICAL_MODELS: Tuple[DialectModel, ...] = (
    DialectModel(
        alias="msa",
        repo_id="CAMeL-Lab/camelparser-dialects-MSA",
        filename="MSA.PATB-CamelTB.CAMeLBERT-MIX.model",
    ),
    DialectModel(
        alias="egy",
        repo_id="CAMeL-Lab/camelparser-dialects-EGY",
        filename="EGY.ARZTB.CAMeLBERT-MIX.model",
    ),
    DialectModel(
        alias="glf",
        repo_id="CAMeL-Lab/camelparser-dialects-GLF",
        filename="GLF.GulfTB.CAMeLBERT-MIX.model",
    ),
    DialectModel(
        alias="msa-egy",
        repo_id="CAMeL-Lab/camelparser-dialects-MSA-EGY",
        filename="MSA-EGY.PATB-CamelTB-ARZTB.CAMeLBERT-MIX.model",
    ),
    DialectModel(
        alias="msa-glf",
        repo_id="CAMeL-Lab/camelparser-dialects-MSA-GLF",
        filename="MSA-GLF.PATB-CamelTB-GulfTB.CAMeLBERT-MIX.model",
    ),
    DialectModel(
        alias="egy-glf",
        repo_id="CAMeL-Lab/camelparser-dialects-EGY-GLF",
        filename="EGY-GLF.ARZTB-GulfTB.CAMeLBERT-MIX.model",
    ),
    DialectModel(
        alias="msa-egy-glf",
        repo_id="CAMeL-Lab/camelparser-dialects-MSA-EGY-GLF",
        filename="MSA-EGY-GLF.PATB-CamelTB-ARZTB-GulfTB.CAMeLBERT-MIX.model",
    ),
)


def _build_aliases() -> Dict[str, DialectModel]:
    aliases = {}
    for model in _CANONICAL_MODELS:
        aliases[model.alias] = model
        aliases[f"catib-{model.alias}"] = model
    return aliases


DIALECT_MODELS: Dict[str, DialectModel] = _build_aliases()


def iter_models() -> Iterable[DialectModel]:
    return _CANONICAL_MODELS


def available_aliases() -> Tuple[str, ...]:
    return tuple(sorted(DIALECT_MODELS))


def get_model(alias: str) -> DialectModel:
    model = DIALECT_MODELS.get(alias.lower())
    if model is None:
        raise ValueError(
            f"Unknown model alias '{alias}'. Available aliases: "
            f"{', '.join(available_aliases())}"
        )
    return model


def format_models() -> str:
    rows = [
        f"{model.alias:12} {model.repo_id:45} {model.filename}"
        for model in iter_models()
    ]
    return "\n".join(["Alias        Hugging Face repo                             Filename", *rows])


def download_model(alias: str, model_dir: Path) -> Path:
    model = get_model(alias)
    model_dir.mkdir(parents=True, exist_ok=True)
    target = model_dir / model.filename
    if target.exists():
        return target

    try:
        from huggingface_hub import hf_hub_download
    except ImportError as exc:
        raise RuntimeError(
            "huggingface_hub is required to download dialect parser models. "
            "Install dependencies with: pip install -r camel_parser/requirements.txt"
        ) from exc

    return Path(
        hf_hub_download(
            repo_id=model.repo_id,
            filename=model.filename,
            local_dir=str(model_dir),
            local_dir_use_symlinks=False,
        )
    )


def download_all_models(model_dir: Path) -> Tuple[Path, ...]:
    return tuple(download_model(model.alias, model_dir) for model in iter_models())
