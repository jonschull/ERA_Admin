from fathom_ops.browser import sanitize_cookies


def test_sanitize_cookies_enforces_same_site_and_partition_key():
    cookies = [
        {"name": "a", "value": "1", "sameSite": "Bogus", "partitionKey": 123},
        {"name": "b", "value": "2", "sameSite": "Lax"},
        {"name": "c", "value": "3", "sameSite": "None", "partitionKey": "ok"},
    ]

    out = sanitize_cookies(cookies)

    # cookie[0]: sameSite corrected to Lax, partitionKey removed
    assert out[0]["sameSite"] == "Lax"
    assert "partitionKey" not in out[0]

    # cookie[1]: unchanged
    assert out[1]["sameSite"] == "Lax"

    # cookie[2]: unchanged (partitionKey is a string)
    assert out[2]["sameSite"] == "None"
    assert out[2]["partitionKey"] == "ok"
