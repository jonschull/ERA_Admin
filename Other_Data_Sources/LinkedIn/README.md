# Other_Data_Sources/LinkedIn/README.md

### 1. Overview

**Purpose:** Fetch LinkedIn profiles for ERA members to enrich member bios

This component provides authenticated browser-based LinkedIn profile scraping using Playwright. It handles LinkedIn's anti-bot measures gracefully and extracts profile data including names, headlines, and full profile text.

**What this component does:**
- Fetches LinkedIn profiles using authenticated browser sessions
- Handles navigation timeouts and rate limiting gracefully
- Extracts name, headline, and complete profile text
- Saves structured JSON data for each profile
- Maintains cookie persistence across sessions

**Key insight:** LinkedIn's HTML structure changes frequently, making CSS selector-based extraction unreliable. This implementation extracts raw text from the page and parses it, which is more resilient to structural changes.

### 2. Orientation - Where to Find What

**You are at:** Other_Data_Sources/LinkedIn component

**What you might need:**
- **Parent** → [/README.md](../../README.md) - Overall ERA Admin architecture
- **Other_Data_Sources** → [../README.md](../README.md) - Data source overview
- **Integration** → [../../integration_scripts/member_enrichment/](../../integration_scripts/member_enrichment/) - Member bio enrichment
- **Reference pattern** → [../BROWSER_COOKIE_AUTH_PATTERN.md](../BROWSER_COOKIE_AUTH_PATTERN.md) - Cookie-based auth pattern

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md)

**LinkedIn-specific:**

**1. Resilient Extraction**
- Don't rely on CSS selectors (LinkedIn changes them frequently)
- Parse text content directly from main element
- Extract data even if navigation times out (page usually loads anyway)
- Graceful degradation: try multiple strategies

**2. Respect Rate Limits**
- 5-second delays between profiles
- Use visible browser (headless=False) - LinkedIn blocks headless
- Maintain authenticated sessions via cookies
- Don't scrape too many profiles at once

**3. Cookie Management**
- Cookies expire and need periodic refresh
- Load cookies at start, save at end of session
- Manual login in browser if authentication fails
- Follow BROWSER_COOKIE_AUTH_PATTERN.md for cookie export

**4. Data Quality**
- Always save full_text (contains About, Experience, etc.)
- Name and headline are parsed heuristically - verify output
- Some profiles may have location instead of headline (parse accordingly)
- Check saved JSON files to verify extraction quality

### 4. Specialized Topics

#### Quick Start

**Run the fetcher:**
```bash
cd /Users/admin/ERA_Admin/Other_Data_Sources/LinkedIn
/Users/admin/ERA_Admin_venv/bin/python linkedin_profile_fetcher.py
```

**Expected output:**
```
Scraping 12 LinkedIn profiles...
✅ Loaded cookies

[1/12] Penny Heiple
   https://www.linkedin.com/in/pennyheiple
   ✅ Saved: pennyheiple.json
   Name: Penny L. Heiple
   Headline: Co-Founder Design School for Regenerating Earth

...

✅ Complete!
   Success: 12/12
```

**Output location:** `profiles/*.json`

#### Files

**Scripts:**
- `linkedin_profile_fetcher.py` - Main scraper (use this one)
- `read_linkedin_profiles.py` - Alternative scraper with different defaults
- `test_linkedin_extraction.py` - Diagnostic tool (if needed for debugging)

**Data:**
- `linkedin_cookies.json` - Authentication cookies (kept up to date automatically)
- `profiles/*.json` - Extracted profile data

**Configuration:**
- Edit `URLs` list in `linkedin_profile_fetcher.py` to add members to scrape

#### How It Works

**Authentication:**
1. Load cookies from `linkedin_cookies.json`
2. Use Microsoft Edge browser (via Playwright)
3. Browser window visible (LinkedIn blocks headless browsers)
4. Cookies automatically saved at end of session

**Extraction Process:**
1. Navigate to profile URL
2. Wait for page to load (networkidle, fallback to domcontentloaded)
3. Give page 3 seconds to fully render
4. Extract all text from `<main>` element
5. Parse first few lines for name/headline
6. Save complete data as JSON

**Extraction Logic (Oct 30, 2025 fix):**
```python
# LinkedIn structure: First line is usually name, then pronouns, then headline
# We parse the text directly instead of using CSS selectors
lines = full_text.split('\n')

# Skip pronouns (She/Her, He/Him) and connection indicators (· 1st)
# First substantial line = name
# Second substantial line = headline (job title)
```

#### Updating URLs to Scrape

Edit `linkedin_profile_fetcher.py` and update the `URLs` list:

```python
URLs = [
    ("Member Name", "https://www.linkedin.com/in/username"),
    ("Another Member", "https://www.linkedin.com/in/another-username"),
    # Add more...
]
```

#### Cookie Refresh

**When to refresh:** If you get authentication errors or no data extracted

**How to refresh:**
1. Open Microsoft Edge
2. Log into LinkedIn manually
3. Navigate to any LinkedIn profile
4. Open DevTools (F12) → Application → Cookies → https://www.linkedin.com
5. Export cookies to `linkedin_cookies.json`

**See:** [../BROWSER_COOKIE_AUTH_PATTERN.md](../BROWSER_COOKIE_AUTH_PATTERN.md) for detailed cookie export instructions

Or use the reference script:
```bash
# From FathomInventory - adapt for LinkedIn
cp ../REFERENCE_convert_edge_cookies.py ./convert_edge_cookies.py
# Edit to target LinkedIn cookies
python convert_edge_cookies.py
```

#### Output Format

Each profile is saved as JSON:

```json
{
  "url": "https://www.linkedin.com/in/username/",
  "scraped_at": "2025-10-30T11:45:37.231513",
  "extracted": {
    "name": "Full Name",
    "headline": "Job Title or Description",
    "full_text": "Complete profile text including About, Experience, Education..."
  }
}
```

**Using the data:**
- `name` - Person's name (parsed from first line)
- `headline` - Job title/description (parsed from second line)
- `full_text` - Complete profile (use this for bio enrichment)

**Note:** Some profiles may have location as "headline" if LinkedIn shows it before the actual headline. Check the full_text for accurate information.

#### Troubleshooting

**Problem: "No meaningful data extracted"**
- Solution: Cookies expired - refresh them (see Cookie Refresh section)
- Or: LinkedIn detected automation - wait a few hours and try again

**Problem: Browser doesn't open**
- Solution: Check Playwright installation: `/Users/admin/ERA_Admin_venv/bin/python -m playwright install`
- Or: Check Microsoft Edge is installed

**Problem: Navigation timeout**
- Solution: This is normal! Script continues and extracts anyway
- LinkedIn is slow, but data usually loads despite timeout

**Problem: Wrong name/headline extracted**
- Solution: Check `profiles/*.json` - the full_text has everything
- LinkedIn profile structure varies by person
- Parse full_text manually if needed

#### Integration with Member Enrichment

**Current usage:**
```bash
# 1. Fetch profiles
cd /Users/admin/ERA_Admin/Other_Data_Sources/LinkedIn
python linkedin_profile_fetcher.py

# 2. Use in member enrichment
cd /Users/admin/ERA_Admin/integration_scripts/member_enrichment
python aggregate_member_info.py
# (Script reads LinkedIn profiles and includes in member data)
```

**Data flow:**
```
LinkedIn → profiles/*.json → member_enrichment → Airtable bios
```

#### Testing & Validation

**Test with one profile:**
```python
# Edit linkedin_profile_fetcher.py
URLs = [
    ("Test Person", "https://www.linkedin.com/in/test-profile"),
]
```

**Diagnostic script:**
```bash
# If extraction fails, use diagnostic tool
python test_linkedin_extraction.py
# Saves screenshot, HTML, and extraction analysis to test_output/
```

**Validate output:**
```bash
# Check profiles were saved
ls -lh profiles/*.json

# Verify content of one profile
cat profiles/username.json | jq '.extracted'
```

#### Common Patterns

**Pattern 1: Bulk scraping members**
```bash
# 1. Get LinkedIn URLs from Airtable or Google contacts
# 2. Add to URLs list in linkedin_profile_fetcher.py
# 3. Run scraper in batches of 10-20 (avoid rate limiting)
# 4. Save profiles to profiles/
# 5. Use in member enrichment workflow
```

**Pattern 2: Single profile quick check**
```bash
# Edit URLs list with one profile
# Run script
# Check profiles/username.json
# Copy relevant text to bio
```

**Pattern 3: Cookie refresh cycle**
```bash
# Every few weeks:
# 1. Log into LinkedIn in Edge
# 2. Export cookies
# 3. Replace linkedin_cookies.json
# 4. Test with one profile
# 5. Resume bulk scraping
```

#### Known Limitations

**Rate Limits:**
- LinkedIn may block after ~50-100 profiles in one session
- Use 5-second delays between profiles (built into script)
- If blocked, wait several hours before resuming

**Profile Visibility:**
- Can only scrape profiles visible to logged-in user
- Private profiles may have limited data
- "Out of network" profiles may require LinkedIn Premium

**Data Accuracy:**
- Name/headline parsing is heuristic (based on position in text)
- Some profiles have location before headline
- Always verify critical data against full_text

**Authentication:**
- Cookies expire (typically after 2-4 weeks)
- Manual re-login required when expired
- Can't be fully automated due to LinkedIn's security

#### Future Enhancements

**Planned:**
- Batch processing with automatic retry on failure
- Better headline extraction (handle location vs. job title)
- Integration with Airtable to auto-populate LinkedIn URLs
- Automated cookie refresh detection

**Possible:**
- Parallel scraping (multiple browser instances)
- Profile change detection (rescrape if updated)
- API integration if LinkedIn provides member API access

### Related Components

**Upstream (data sources):**
- LinkedIn profiles (via authenticated browser)
- Airtable LinkedIn URLs (member records)

**Downstream (consumers):**
- [../../integration_scripts/member_enrichment/](../../integration_scripts/member_enrichment/) - Uses profiles for bio generation
- [../../airtable/](../../airtable/) - Updated with LinkedIn data

**Reference:**
- [../BROWSER_COOKIE_AUTH_PATTERN.md](../BROWSER_COOKIE_AUTH_PATTERN.md) - Cookie authentication pattern
- [../REFERENCE_convert_edge_cookies.py](../REFERENCE_convert_edge_cookies.py) - Cookie conversion utility

**Back to:** [../README.md](../README.md)
