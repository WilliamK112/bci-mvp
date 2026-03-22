"""
Streaming inference utilities for stable real-time BCI predictions.
- Exponential moving average (EMA) smoothing
- Hysteresis-based state transitions to reduce flicker
"""
from dataclasses import dataclass


@dataclass
class StreamingConfig:
    alpha: float = 0.25
    high_threshold: float = 0.60
    low_threshold: float = 0.40


class StreamingStateFilter:
    def __init__(self, config: StreamingConfig | None = None):
        self.cfg = config or StreamingConfig()
        self.ema = None
        self.state = "relaxed"

    def update(self, focused_prob: float) -> dict:
        p = max(0.0, min(1.0, float(focused_prob)))
        if self.ema is None:
            self.ema = p
        else:
            self.ema = self.cfg.alpha * p + (1 - self.cfg.alpha) * self.ema

        # Hysteresis state transition
        if self.state == "relaxed" and self.ema >= self.cfg.high_threshold:
            self.state = "focused"
        elif self.state == "focused" and self.ema <= self.cfg.low_threshold:
            self.state = "relaxed"

        return {
            "raw_focused_prob": p,
            "smoothed_focused_prob": self.ema,
            "state": self.state,
        }
