# Fathom Inventory System

> **🔧 Making changes?** Read [DEVELOPMENT.md](DEVELOPMENT.md) first (workflow, testing, constraints)  
> **🆘 Resuming work?** Read [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) first (project state, how to continue)

**Automatically downloads, processes, and analyzes Fathom meeting summaries**

## 🎯 System Status: ✅ FULLY OPERATIONAL (Oct 17, 2025)

**What This System Does:**
1. **Discovers** new Fathom calls from jschull@e-nable.org account
2. **Shares** calls to `fathomizer@ecorestorationalliance.org` (automated receiver)
3. **Downloads** summary emails with public `/share/` URLs (no login required)
4. **Processes** emails into structured database with normalized dates (ISO format)
5. **Reports** daily status with health checks and public URLs

**Current Health:**
- ✅ **1,616 calls** tracked with 99.7% URL coverage
- ✅ **3,229 emails** processed with full metadata extraction
- ✅ **Dates normalized** to ISO format (YYYY-MM-DD) at all entry points
- ✅ **Automation active** - Daily runs at 3:00 AM via macOS launchd
- ✅ **Enhanced failure detection** - Catches authentication failures immediately

**Recent Improvements (Oct 17, 2025):**
- ✅ **Pre-flight authentication checks** - Fails fast with clear error messages
- ✅ **Fixed bash pipeline exit codes** - No more silent failures
- ✅ **Enhanced daily reports** - Critical alerts separated from warnings with log analysis
- ✅ **Improved error messaging** - Actionable remediation steps provided
- 📋 **Full details**: [FAILURE_DETECTION_IMPROVEMENTS.md](docs/FAILURE_DETECTION_IMPROVEMENTS.md)

> **⚠️ Configuration Validation**: See [CONFIGURATION_ERRORS.md](docs/CONFIGURATION_ERRORS.md) for critical setup requirements and recovery procedures

---

As fully documented in [TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md),

* *This project provides a suite of tools to download, process, and analyze Fathom meeting summaries. It establishes a robust pipeline to convert unstructured Fathom summary emails into a structured, queryable SQLite database, enabling detailed analysis of meeting metadata and content.*

## Quick Start (5 minutes)

### 1. Setup Dependencies

```bash
# Create virtual environment (if not exists)
python3 -m venv ../ERA_Admin_venv
source ../ERA_Admin_venv/bin/activate

# Install requirements
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Authentication

**For Fathom.video access:**

```bash
./scripts/refresh_fathom_auth.sh
```

Follow the prompts to export cookies from your browser.

**For Gmail access (CRITICAL - must use correct account):**

**⚠️ IMPORTANT**: Authenticate with `fathomizer@ecorestorationalliance.org`, NOT your personal account

- Run `python scripts/download_emails.py`
- Complete OAuth flow in browser when prompted
- **Verify**: Sign in as `fathomizer@ecorestorationalliance.org`
- Credentials will be saved automatically

**Verify correct configuration:**
```bash
./venv/bin/python -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
creds = Credentials.from_authorized_user_file('token.json')
service = build('gmail', 'v1', credentials=creds)
profile = service.users().getProfile(userId='me').execute()
expected = 'fathomizer@ecorestorationalliance.org'
print(f'✅ Correct: {expected}' if profile['emailAddress'] == expected else f'❌ WRONG: {profile[\"emailAddress\"]}')
"
```

### 3. Run the System

```bash
./run_all.sh
```

**That's it!** The system will:

- Find new Fathom calls and share them
- Wait 5 minutes for emails to arrive
- Download and process the emails
- Update the database with structured data

**Advanced: Multi-Account Support**

Fathom account configuration is centralized in `../era_config.py`. Switch accounts using:

**Option 1: Environment variable (temporary)**
```bash
FATHOM_ACCOUNT=era python run_daily_share.py
# Uses ERA account (ecorestorationalliance@gmail.com)

FATHOM_ACCOUNT=enable python run_daily_share.py
# Uses e-NABLE account (jschull@e-nable.org) - default
```

**Option 2: Edit era_config.py (permanent)**
```python
# In /Users/admin/ERA_Admin/era_config.py
FATHOM_ACTIVE_ACCOUNT = 'era'  # Change from 'enable' to 'era'
```

**Option 3: Override at runtime (one-off)**
```bash
python run_daily_share.py --cookies fathom_cookies_alt.json --share-email other@example.com
# Still works for special cases
```

**Experimental: Database Mode**

Use database instead of TSV for call tracking:

```bash
# Enable database mode
python run_daily_share.py --use-db

# Or specify custom database
python run_daily_share.py --use-db --db custom.db
```

**Note:** TSV remains the default. Database mode is feature-flagged for testing.

## Daily Operation

The system runs automatically at **3:00 AM daily** via macOS scheduling.

**Monitor progress:**

```bash
tail -f cron.log
```

## Weekly Maintenance (Required)

**Refresh Fathom authentication:**

```bash
./scripts/refresh_fathom_auth.sh
```

Fathom cookies expire frequently (some daily), so weekly refresh prevents authentication failures.

## When Things Break

### "Authentication failed" or "redirected to login"

**Solution:** Refresh cookies

```bash
./scripts/refresh_fathom_auth.sh
```

### "No new emails found"

**Check:** Gmail authentication

```bash
python scripts/download_emails.py
```

### "Script hangs or times out"

**Solution:** Check authentication health

```bash
python scripts/check_auth_health.py
```

### "Permission denied" or file errors

**Solution:** Check file permissions

```bash
chmod 600 *.json
chmod +x *.sh
```

## Key Files

| File                     | Purpose               | When to Touch          |
| ------------------------ | --------------------- | ---------------------- |
| `fathom_cookies.json`  | Fathom authentication | Weekly refresh         |
| `credentials.json`     | Google API setup      | One-time setup         |
| `token.json`           | Gmail access          | Auto-managed           |
| `all_fathom_calls.tsv` | Master call registry  | **Never delete** |
| `fathom_emails.db`     | Processed data        | View-only              |
| `cron.log`             | System activity       | Monitor for errors     |
| `analysis/`            | AI analysis scripts   | See analysis/README.md |

## Data Output

**Structured database:** `fathom_emails.db`

- Meeting titles, dates, participants
- Action items and next steps counts
- Full email content and metadata

**Call registry:** `all_fathom_calls.tsv`

- Master list of all discovered calls
- Share status and timestamps

## Automation Status

**Check if automation is active:**

```bash
launchctl list | grep era
```

**Should show:** `com.era.admin.fathom` if running

## Getting Help

### Quick Health Check

```bash
python scripts/check_auth_health.py
```

### Detailed Documentation

- **[Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md)** - Complete system architecture, validation details, and workflows
- **[Authentication Guide](docs/AUTHENTICATION_GUIDE.md)** - All authentication methods and troubleshooting
- **[Automation Guide](docs/AUTOMATION_MONITORING_GUIDE.md)** - Scheduling and monitoring

### Test Individual Components

```bash
cd authentication
python test_all_auth.py        # Test all authentication
python test_fathom_cookies.py  # Test Fathom access only
python test_google_auth.py     # Test Gmail access only
```

## Project Status

✅ **Core pipeline validated** - 100% data accuracy confirmed
✅ **Automation active** - Daily runs at 3:00 AM
✅ **Authentication streamlined** - Weekly maintenance process
✅ **Error handling robust** - Graceful failure recovery

---

## Complete Documentation

- **[TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md)** - Complete system architecture, data pipeline validation, script dependencies, and all technical details
- **[AUTHENTICATION_GUIDE.md](docs/AUTHENTICATION_GUIDE.md)** - Comprehensive authentication setup, troubleshooting, and maintenance procedures

*This README provides essential user information. For complete technical documentation, architecture diagrams, and development details, see the links above.*
