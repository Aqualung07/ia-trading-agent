import analysis.decision_engine as de

def test_empty_fundamentals():
    # When fundamentals are missing and no technical signal,
    # the engine should indicate insufficient data, not just a generic watch.
    result = de.generate_recommendation({}, "", None)
    assert "insufficient fundamental data" in result
