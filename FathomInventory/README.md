# FathomInventory/README.md

### 1. Overview

**Purpose:** Automatically downloads, processes, and analyzes Fathom meeting summaries

FathomInventory is one of four components in ERA_Admin. It provides a robust pipeline to convert unstructured Fathom summary emails into a structured, queryable SQLite database, enabling detailed analysis of meeting metadata and content.

**System Status:** ✅ FULLY OPERATIONAL

**What This System Does:**
1. **Discovers** new Fathom calls from jschull@e-nable.org account
2. **Shares** calls to `fathomizer@ecorestorationalliance.org` (automated receiver)
3. **Downloads** summary emails with public `/share/` URLs (no login required)
4. **Processes** emails into structured database with normalized dates (ISO format)
5. **Reports** daily status with health checks and public URLs

**Current Health:**
- ✅ **682 participants** tracked (459 validated/67%, 223 new/unprocessed)
- ✅ **3,229+ emails** processed with full metadata extraction
- ✅ **Dates normalized** to ISO format (YYYY-MM-DD) at all entry points
- ✅ **Automation active** - Daily runs at 3:00 AM via macOS launchd
- ✅ **Enhanced failure detection** - Catches authentication failures immediately
- ✅ **Phase 4B-2 COMPLETE** - 459 participants validated (Oct 23, 2025)

**Recent Improvements:**
- ✅ Pre-flight authentication checks (fails fast with clear errors)
- ✅ Fixed bash pipeline exit codes (no more silent failures)
- ✅ Enhanced daily reports (critical alerts separated from warnings)
- ✅ Improved error messaging (actionable remediation steps)

**Key Features:**
- **Multi-account support** - Switch between ERA and e-NABLE accounts via config
- **Experimental database mode** - Use database instead of TSV for call tracking
- **Weekly maintenance** - Fathom cookies expire frequently, refresh weekly

### 2. Orientation - Where to Find What

**You are at:** FathomInventory component README

**First-time users:**
1. Read this Overview (Section 1)
2. Follow Quick Start in Section 4
3. Run `./run_all.sh` to test the system

**Resuming work:**
1. Read [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - Current component state
2. Check health: `python scripts/check_auth_health.py`
3. Continue from documented next steps

**Making changes:**
1. Read [DEVELOPMENT.md](../ERA_Landscape/DEVELOPMENT.md) - Workflow, testing, constraints
2. Follow component-specific development practices
3. Test before committing

**What you might need:**
- **Parent system** → [/README.md](../README.md) - Overall ERA Admin architecture
- **System-wide status** → [/CONTEXT_RECOVERY.md](../CONTEXT_RECOVERY.md) - Integration status
- **Component status** → [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - FathomInventory health
- **System principles** → [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) - Overall philosophy
- **Authentication** → [authentication/README.md](authentication/README.md) - Cookie and token management
- **Analysis** → analysis/README.md - AI analysis scripts for ERA meetings

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**FathomInventory-specific:**

**1. Authentication Health Checks**
- **Pre-flight validation** - Check auth before running pipeline (fails fast)
- **Weekly refresh required** - Fathom cookies expire frequently (some daily)
- **Correct account critical** - Gmail must use `fathomizer@ecorestorationalliance.org`
- **Health monitoring** - Run `check_auth_health.py` before manual runs

**2. Pipeline Reliability**
- **Fail-fast design** - Catch authentication failures immediately, don't proceed
- **Bash exit codes** - Fixed pipeline to respect script failures
- **5-minute wait** - After sharing, wait for emails to arrive before downloading
- **Daily automation** - Runs at 3:00 AM via launchd, monitor `cron.log`

**3. Data Normalization**
- **ISO date format** - All dates as YYYY-MM-DD (entry point normalization)
- **No assumptions** - Validate and normalize at data entry, not query time
- **Consistent schema** - SQLite database with normalized participant data

**4. Self-Contained Component**
- **Works standalone** - Can be understood without reading parent docs
- **Clear interfaces** - Exposes `fathom_emails.db` and `all_fathom_calls.tsv`
- **Minimal coupling** - Integration happens at integration_scripts/[type]/ level

### 4. Specialized Topics

#### Quick Start (5 minutes)

**1. Setup Dependencies**
```bash
# Create virtual environment (if not exists)
python3 -m venv ../ERA_Admin_venv
source ../ERA_Admin_venv/bin/activate

# Install requirements
pip install -r requirements.txt
playwright install chromium
```

**2. Configure Authentication**

*For Fathom.video access:*
```bash
./scripts/refresh_fathom_auth.sh
# Follow prompts to export cookies from browser
```

*For Gmail access (CRITICAL - correct account):*

⚠️ **IMPORTANT:** Authenticate with `fathomizer@ecorestorationalliance.org`, NOT personal account

```bash
python scripts/download_emails.py
# Complete OAuth flow in browser
# Verify: Sign in as fathomizer@ecorestorationalliance.org
```

*Verify correct configuration:*
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

**3. Run the System**
```bash
./run_all.sh
```

**That's it!** The system will:
- Find new Fathom calls and share them
- Wait 5 minutes for emails to arrive
- Download and process the emails
- Update the database with structured data

#### Advanced Configuration

**Multi-Account Support:**

Fathom account configuration centralized in `../era_config.py`. Switch accounts using:

*Option 1: Environment variable (temporary)*
```bash
FATHOM_ACCOUNT=era python run_daily_share.py
# Uses ERA account (ecorestorationalliance@gmail.com)

FATHOM_ACCOUNT=enable python run_daily_share.py
# Uses e-NABLE account (jschull@e-nable.org) - default
```

*Option 2: Edit era_config.py (permanent)*
```python
# In /Users/admin/ERA_Admin/era_config.py
FATHOM_ACTIVE_ACCOUNT = 'era'  # Change from 'enable' to 'era'
```

*Option 3: Override at runtime (one-off)*
```bash
python run_daily_share.py --cookies fathom_cookies_alt.json --share-email other@example.com
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

#### Daily Operation

The system runs automatically at **3:00 AM daily** via macOS scheduling.

**Monitor progress:**
```bash
tail -f cron.log
```

**Check automation status:**
```bash
launchctl list | grep era
# Should show: com.era.admin.fathom if running
```

#### Weekly Maintenance (Required)

**Refresh Fathom authentication:**
```bash
./scripts/refresh_fathom_auth.sh
```

Fathom cookies expire frequently (some daily), so weekly refresh prevents authentication failures.

#### Troubleshooting

**"Authentication failed" or "redirected to login"**

*Solution:* Refresh cookies
```bash
./scripts/refresh_fathom_auth.sh
```

**"No new emails found"**

*Check:* Gmail authentication
```bash
python scripts/download_emails.py
```

**"Script hangs or times out"**

*Solution:* Check authentication health
```bash
python scripts/check_auth_health.py
```

**"Permission denied" or file errors**

*Solution:* Check file permissions
```bash
chmod 600 *.json
chmod +x *.sh
```

#### Key Files

| File | Purpose | When to Touch |
|------|---------|---------------|
| `fathom_cookies.json` | Fathom authentication | Weekly refresh |
| `credentials.json` | Google API setup | One-time setup |
| `token.json` | Gmail access | Auto-managed |
| `all_fathom_calls.tsv` | Master call registry | **Never delete** |
| `fathom_emails.db` | Processed data | View-only |
| `cron.log` | System activity | Monitor for errors |
| `analysis/` | AI analysis scripts | See analysis/README.md |

#### Data Output

**Structured database:** `fathom_emails.db`
- Meeting titles, dates, participants
- Action items and next steps counts
- Full email content and metadata

**Call registry:** `all_fathom_calls.tsv`
- Master list of all discovered calls
- Share status and timestamps

#### Getting Help

**Quick Health Check:**
```bash
python scripts/check_auth_health.py
```

**Test Individual Components:**
```bash
cd authentication
python test_all_auth.py        # Test all authentication
python test_fathom_cookies.py  # Test Fathom access only
python test_google_auth.py     # Test Gmail access only
```

**Detailed Documentation:**
- [TECHNICAL_DOCUMENTATION.md](../FathomInventory/docs/TECHNICAL_DOCUMENTATION.md) - Complete architecture, validation, workflows
- [AUTHENTICATION_GUIDE.md](../FathomInventory/docs/AUTHENTICATION_GUIDE.md) - All auth methods and troubleshooting
- [AUTOMATION_MONITORING_GUIDE.md](../FathomInventory/docs/AUTOMATION_MONITORING_GUIDE.md) - Scheduling and monitoring
- [FAILURE_DETECTION_IMPROVEMENTS.md](../FathomInventory/docs/FAILURE_DETECTION_IMPROVEMENTS.md) - Recent reliability enhancements
- [CONFIGURATION_ERRORS.md](../FathomInventory/docs/CONFIGURATION_ERRORS.md) - Critical setup requirements and recovery

#### Component Organization

**Subdirectories:**
- [authentication/README.md](authentication/README.md) - Cookie and token management
- analysis/ - AI analysis scripts for ERA meetings (Phases 1-3)
- docs/ - Detailed technical documentation
- scripts/ - Pipeline automation scripts (30+ operational scripts)
- tests/ - Test suite (unit tests, smoke tests)

**Key Component Files:**
- [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - Current component state
- DEVELOPMENT.md - Development workflow, testing, constraints
- BACKUP_AND_RECOVERY.md - Data backup and recovery procedures

#### Internal Architecture

**Core Modules:**
- `data_access/` - Database abstraction layer
  - `db_io.py` - SQLite database operations
  - `tsv_io.py` - TSV file I/O (legacy format support)
- `fathom_ops/` - Browser automation internals
  - `browser.py` - Playwright-based web scraping
  - `parser.py` - HTML parsing and data extraction

**Analysis Scripts (Phases 1-3):**
Located in `analysis/`:
- `batch_analyze_calls.py` - Bulk call analysis
- `sync_era_meetings.py` - ERA meeting synchronization
- `import_participants.py` - Participant data import
- `mark_era_meetings.py` - Meeting classification
- `ask_fathom_ai.py` - AI-powered analysis
- See `analysis/README.md` for details

**Maintenance Scripts:**
Located in `scripts/`:
- **Health checks:** `database_health_check.sh` - Verify DB integrity
- **Backfilling:** `backfill_public_urls.py` - Add missing URLs
- **Migrations:** `fix_*.py` - Various data fixes and schema updates
- **Utilities:** `create_thumbnails.py`, `batch_database_converter.py`
- **Monitoring:** `check_auth_health.py` - Authentication status

**Testing:**
Test suite in `tests/` directory:
- `test_smoke.py` - Basic functionality tests
- `test_browser_sanitize.py` - Cookie sanitization tests
- `test_parser_unit.py` - Parser unit tests
- Run: `pytest` or `python -m pytest`

**Back to:** [/README.md](../README.md)