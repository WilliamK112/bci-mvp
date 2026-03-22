# Space User Guide

Generated: 2026-03-22 16:01 UTC

## Access
- https://huggingface.co/spaces/williamKang112/bci-mvp-demo

## Modes
- **Single Prediction**: input 32-dim feature vector and get class probabilities.
- **Streaming (Simulated)**: view real-time probability curve with EMA+hysteresis stabilization.

## Runtime Indicator
- `REAL_MODEL`: using trained model file
- `MOCK_FALLBACK`: model not present; deterministic fallback for demo continuity

## Troubleshooting
- If blank or unavailable, wait for Space rebuild and refresh.
- If connection resets, retry both page URL and direct `hf.space` URL.
- Use project diagnostics docs: `docs/HF_SPACE_STATUS.md`, `docs/SPACE_SMOKE_TEST.md`.
