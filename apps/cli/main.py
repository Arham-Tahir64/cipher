from __future__ import annotations

import json
from typing import Optional

import typer

from services.nlu import extract_intent_from_text


app = typer.Typer(add_completion=False, help="Text-only NLU CLI using local LM Studio")


@app.command()
def parse(text: str = typer.Argument(..., help="User command to parse as intent")):
    intent = extract_intent_from_text(text)
    print(json.dumps(intent.model_dump(), indent=2))


if __name__ == "__main__":
    app()


