from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, TypeAdapter


class TurnOnDeviceIntent(BaseModel):
    intent: Literal["TurnOnDevice"] = "TurnOnDevice"
    device_type: Optional[str] = Field(
        default=None,
        description="Type of device to control, e.g., 'light', 'fan', 'thermostat'",
    )
    room: Optional[str] = Field(
        default=None, description="Room or area name, e.g., 'kitchen', 'bedroom'"
    )


class TurnOffDeviceIntent(BaseModel):
    intent: Literal["TurnOffDevice"] = "TurnOffDevice"
    device_type: Optional[str] = Field(default=None)
    room: Optional[str] = Field(default=None)


class SetTimerIntent(BaseModel):
    intent: Literal["SetTimer"] = "SetTimer"
    duration_seconds: int = Field(
        description="Timer duration in seconds; parse human input upstream"
    )
    label: Optional[str] = Field(default=None, description="Optional timer label")


class SetThermostatIntent(BaseModel):
    intent: Literal["SetThermostat"] = "SetThermostat"
    temperature_c: float = Field(description="Target temperature in Celsius")
    room: Optional[str] = Field(default=None)


class PlayMusicIntent(BaseModel):
    intent: Literal["PlayMusic"] = "PlayMusic"
    query: Optional[str] = Field(default=None, description="Song/artist/playlist")
    provider: Optional[str] = Field(
        default=None, description="Music provider (spotify, yt, local)"
    )
    room: Optional[str] = Field(default=None)


class GeneralQuestionIntent(BaseModel):
    intent: Literal["GeneralQuestion"] = "GeneralQuestion"
    question: str


Intent = Union[
    TurnOnDeviceIntent,
    TurnOffDeviceIntent,
    SetTimerIntent,
    SetThermostatIntent,
    PlayMusicIntent,
    GeneralQuestionIntent,
]


_intent_adapter: TypeAdapter[Intent] = TypeAdapter(Union[
    TurnOnDeviceIntent,
    TurnOffDeviceIntent,
    SetTimerIntent,
    SetThermostatIntent,
    PlayMusicIntent,
    GeneralQuestionIntent,
])


def parse_intent(payload: dict) -> Intent:
    """Validate and coerce a dict payload into a concrete Intent model.

    Raises pydantic.ValidationError on invalid payloads.
    """
    return _intent_adapter.validate_python(payload)


__all__ = [
    "TurnOnDeviceIntent",
    "TurnOffDeviceIntent",
    "SetTimerIntent",
    "SetThermostatIntent",
    "PlayMusicIntent",
    "GeneralQuestionIntent",
    "Intent",
    "parse_intent",
]


