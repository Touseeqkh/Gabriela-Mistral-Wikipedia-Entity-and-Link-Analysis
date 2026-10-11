from src.analyze_wikipedia import clean_text, extract_biographical_attributes, is_probably_person


def test_clean_text_collapses_whitespace():
    assert clean_text("hello\n  world") == "hello world"


def test_person_candidate_filter():
    assert is_probably_person("Gabriela Mistral")
    assert is_probably_person("José Martí")
    assert not is_probably_person("Category:Poets")
    assert not is_probably_person("Chile")


def test_biographical_dates_are_extracted_when_pattern_matches():
    result = extract_biographical_attributes("She was born April 7, 1889. She died January 10, 1957.")
    assert result["Date of Birth"] == "April 7, 1889"
    assert result["Date of Death"] == "January 10, 1957"
