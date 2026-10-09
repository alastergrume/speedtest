"""Data models: the result of a single request and the summary of all requests."""

from dataclasses import dataclass
from typing import List

BYTES_IN_MB = 1_000_000


@dataclass(frozen=True)
class Measurement:
    """Result of a single successful request."""

    size_bytes: int
    duration_s: float

    @property
    def speed_mb_per_s(self) -> float:
        if self.duration_s <= 0:
            return 0.0
        return self.size_bytes / self.duration_s / BYTES_IN_MB


@dataclass(frozen=True)
class Summary:
    """Summary of all requests."""

    measurements: List[Measurement]
    failed: int

    @property
    def successful(self) -> int:
        return len(self.measurements)

    @property
    def total_bytes(self) -> int:
        return sum(m.size_bytes for m in self.measurements)

    @property
    def total_time_s(self) -> float:
        return sum(m.duration_s for m in self.measurements)

    @property
    def average_time_s(self) -> float:
        return self.total_time_s / self.successful if self.successful else 0.0

    @property
    def speed_mb_per_s(self) -> float:
        """Average speed: total downloaded bytes / total download time."""
        if self.total_time_s <= 0:
            return 0.0
        return self.total_bytes / self.total_time_s / BYTES_IN_MB
