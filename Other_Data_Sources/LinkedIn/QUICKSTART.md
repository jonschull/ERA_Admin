# LinkedIn Profile Fetcher - Quick Start

## Run the Fetcher

```bash
cd /Users/admin/ERA_Admin/Other_Data_Sources/LinkedIn
/Users/admin/ERA_Admin_venv/bin/python linkedin_profile_fetcher.py
```

## What Happens

1. Loads cookies from `linkedin_cookies.json`
2. Opens Microsoft Edge browser (visible)
3. Visits each LinkedIn profile URL in the list
4. Extracts name, headline, and full profile text
5. Saves to `profiles/username.json`
6. 5-second pause between profiles

## Current URLs (12 profiles)

The script is currently configured to fetch 12 profiles. Check the `URLs` list in `linkedin_profile_fetcher.py` to see which ones.

## Add More Profiles

Edit `linkedin_profile_fetcher.py` and update the `URLs` list:

```python
URLs = [
    ("Member Name", "https://www.linkedin.com/in/username"),
    ("Another Member", "https://www.linkedin.com/in/another-username"),
    # Add more...
]
```

## Output Location

Profiles saved to: `/Users/admin/ERA_Admin/Other_Data_Sources/LinkedIn/profiles/`

Each file is named: `username.json`

## Troubleshooting

**No data extracted?**
- Cookies may have expired
- Refresh them: Log into LinkedIn in Edge, export cookies to `linkedin_cookies.json`
- See [README.md](README.md) section "Cookie Refresh" for details

**Browser doesn't open?**
- Check Playwright: `/Users/admin/ERA_Admin_venv/bin/python -m playwright install`

## Next Steps

Use the profiles in member enrichment:

```bash
cd /Users/admin/ERA_Admin/integration_scripts/member_enrichment
python aggregate_member_info.py
```

## Full Documentation

See [README.md](README.md) for complete usage, troubleshooting, and integration details.
