"""
Streaming inference utilities for stable real-time BCI predictions.
- Exponential moving average (EMA) smoothing
- Hysteresis-based state transitions to reduce flicker
- Optional confidence-weighted updates (Dynamic Alpha)
- Optional debounce filter (require N consecutive ticks)
"""
from dataclasses import dataclass
from collections import deque

@dataclass
class StreamingConfig:
    alpha: float = 0.25
    high_threshold: float = 0.60
    low_threshold: float = 0.40
    debounce_ticks: int = 1
    dynamic_alpha: bool = False

class StreamingStateFilter:
    def __init__(self, config: StreamingConfig | None = None):
        self.cfg = config or StreamingConfig()
        self.ema = None
        self.state = "relaxed"
        self._state_history = deque(maxlen=self.cfg.debounce_ticks)
        for _ in range(self.cfg.debounce_ticks):
            self._state_history.append("relaxed")

    def update(self, focused_prob: float) -> dict:
        p = max(0.0, min(1.0, float(focused_prob)))
        
        if self.cfg.dynamic_alpha:
            confidence = abs(p - 0.5) * 2.0
            current_alpha = self.cfg.alpha * (0.5 + 0.5 * confidence)
        else:
            current_alpha = self.cfg.alpha

        if self.ema is None:
            self.ema = p
        else:
            self.ema = current_alpha * p + (1 - current_alpha) * self.ema

        candidate_state = self.state
        if self.state == "relaxed" and self.ema >= self.cfg.high_threshold:
            candidate_state = "focused"
        elif self.state == "focused" and self.ema <= self.cfg.low_threshold:
            candidate_state = "relaxed"

        self._state_history.append(candidate_state)
        
        if all(s == "focused" for s in self._state_history):
            self.state = "focused"
        elif all(s == "relaxed" for s in self._state_history):
            self.state = "relaxed"

        return {
            "raw_focused_prob": p,
            "smoothed_focused_prob": self.ema,
            "state": self.state,
        }
