from src.streaming import StreamingStateFilter, StreamingConfig


def test_hysteresis_transitions():
    f = StreamingStateFilter(StreamingConfig(alpha=1.0, high_threshold=0.6, low_threshold=0.4))

    assert f.update(0.2)["state"] == "relaxed"
    assert f.update(0.65)["state"] == "focused"
    # stays focused above low threshold
    assert f.update(0.45)["state"] == "focused"
    # flips back when below low threshold
    assert f.update(0.35)["state"] == "relaxed"
