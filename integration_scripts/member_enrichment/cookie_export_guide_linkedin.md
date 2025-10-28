# Cookie Export Guide for LinkedIn

## Purpose

Export LinkedIn session cookies to enable automated profile reading without triggering bot detection.

## Method: Browser Developer Tools (Following Fathom pattern)

### Steps:

1. **Log into LinkedIn** in Chrome or Edge
2. **Navigate to** https://www.linkedin.com
3. **Open Developer Tools** (F12 or right-click → Inspect)
4. **Go to Application tab** (Chrome) or Storage tab (Firefox)
5. **Click on Cookies** in left sidebar
6. **Select https://www.linkedin.com**
7. **Right-click in cookie list** → "Select All"
8. **Copy all cookies** (Ctrl+C)
9. **Run the converter script** (see below)

## Using the Converter Script

```bash
cd integration_scripts/member_enrichment
python convert_linkedin_cookies.py
```

Then paste the copied cookie data when prompted.

## Testing Your Cookies

```bash
python read_linkedin_profiles.py
```

Should successfully access profiles without login prompts.

## Security Notes

- **Keep cookies private** - they provide full access to your LinkedIn account
- **Don't commit to git** - already in .gitignore
- **Rotate regularly** - export fresh cookies monthly
- **File permissions**: `chmod 600 linkedin_cookies.json`

## Troubleshooting

### "Authentication failed" or redirected to login

**Solution**: Export fresh cookies from browser (LinkedIn may have invalidated session)

### Bot detection / CAPTCHA

**Solution**: 
1. Increase pause between profiles (currently 5 seconds)
2. Don't run too frequently
3. Use fresh cookies from active browser session
