from __future__ import annotations

from typing import Any, Dict

from packages.shared import Intent, parse_intent, load_config
from services.llm.client import get_llm_client


SYSTEM_PROMPT = (
    "You are a function calling NLU. Extract the user's intent as strict JSON only. "
    "No extra text. Allowed intents: TurnOnDevice, TurnOffDevice, SetTimer, "
    "SetThermostat, PlayMusic, GeneralQuestion. Include an 'intent' field and the relevant fields."
)


def _build_user_instruction(user_text: str) -> str:
    return (
        "Given the command, produce a JSON object for the intent.\n"
        "Fields by intent:\n"
        "- TurnOnDevice/TurnOffDevice: device_type (str?), room (str?)\n"
        "- SetTimer: duration_seconds (int), label (str?)\n"
        "- SetThermostat: temperature_c (number), room (str?)\n"
        "- PlayMusic: query (str?), provider (str?), room (str?)\n"
        "- GeneralQuestion: question (str)\n\n"
        f"User: {user_text}"
    )


def extract_intent_from_text(text: str) -> Intent:
    config = load_config()
    llm = get_llm_client(config)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_instruction(text)},
    ]
    payload: Dict[str, Any] = llm.generate_structured_intent(messages)
    return parse_intent(payload)


__all__ = ["extract_intent_from_text"]


