"""A tiny Semantic Kernel plugin that exposes the current time."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from semantic_kernel.functions import kernel_function


class TimePlugin:
    """Plugin containing time-related kernel functions."""

    def __init__(self, default_timezone: str = "UTC") -> None:
        self.default_timezone = default_timezone

    @kernel_function(
        name="now",
        description=(
            "Gets the current date and time. Provide an IANA timezone such as "
            "UTC, America/Phoenix, Europe/London, or Asia/Kolkata when needed."
        ),
    )
    def now(
        self,
        timezone: Annotated[
            str,
            "Optional IANA timezone. Use an empty value to use the configured default timezone.",
        ] = "",
    ) -> str:
        """Return the current date and time for the requested timezone."""

        selected_timezone = timezone.strip() or self.default_timezone

        try:
            zone = ZoneInfo(selected_timezone)
        except ZoneInfoNotFoundError:
            return (
                f"Unknown timezone: {selected_timezone}. "
                "Please use an IANA timezone like UTC or America/Phoenix."
            )

        current = datetime.now(zone)
        return current.strftime("%Y-%m-%d %H:%M:%S %Z%z")

