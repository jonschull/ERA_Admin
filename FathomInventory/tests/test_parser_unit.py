import pathlib
from run_daily_share import parse_for_new_calls

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def read_fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_parse_for_new_calls_extracts_records_from_sample_html():
    html = read_fixture("my_calls_sample.html")
    existing = set()
    records = parse_for_new_calls(html, existing)

    # Expect two records
    assert len(records) == 2

    # Validate fields for first record
    r0 = records[0]
    assert r0["Title"] == "Impromptu Zoom Meeting"
    assert r0["Date"] == "Sep 2, 2025"
    assert r0["Duration"] == "30 mins"
    assert r0["Hyperlink"] == "https://fathom.video/calls/123"

    # Validate fields for second record
    r1 = records[1]
    assert r1["Title"] == "ERA Town Hall Meeting"
    assert r1["Date"] == "Sep 3, 2025"
    assert r1["Duration"] == "125 mins"
    assert r1["Hyperlink"] == "https://fathom.video/calls/456"


def test_parse_for_new_calls_deduplicates_existing_links():
    html = read_fixture("my_calls_sample.html")
    existing = {"https://fathom.video/calls/123"}
    records = parse_for_new_calls(html, existing)

    # One of the two should be filtered out
    assert len(records) == 1
    assert records[0]["Hyperlink"] == "https://fathom.video/calls/456"
