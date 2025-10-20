# Fathom Inventory System - Overview

> **Quick Reference**: System architecture, data flow, and current status at a glance

## 🎯 System Purpose

Automatically capture, process, and organize Fathom meeting recordings with public share URLs for ERA organization analysis.

---

## 🔄 Data Flow (5 Steps)

```
1. DISCOVER                2. SHARE                 3. RECEIVE              4. PROCESS              5. REPORT
   ↓                          ↓                        ↓                       ↓                       ↓
┌─────────────┐          ┌─────────────┐         ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│  Fathom.video  │   →   │   Share to     │   →   │  Gmail Inbox   │   →   │  Extract &     │   →   │  Daily Email   │
│  jschull@      │       │  fathomizer@   │       │  fathomizer@   │       │  Normalize     │       │  Report        │
│  e-nable.org   │       │  ecorestor...  │       │  ecorestor...  │       │  to Database   │       │  jschull@      │
└─────────────┘          └─────────────┘         └─────────────┘        └─────────────┘        └─────────────┘

Scrape new calls          Auto-share via           Receive summary         Parse HTML →            Health check
from account              Fathom UI                emails with             Structured DB          + public URLs
                                                   /share/ URLs            ISO dates
```

**Key Principle**: Two separate accounts with distinct purposes
- **jschull@e-nable.org** (Fathom cookies): Source account for discovering calls
- **fathomizer@ecorestorationalliance.org** (Gmail OAuth): Receiver account for automated processing

---

## 📊 Current Status (Oct 9, 2025)

### System Health
| Metric | Value | Status |
|--------|-------|--------|
| **Total Calls Tracked** | 1,608 | ✅ |
| **Public Share URLs** | 1,603 (99.7%) | ✅ |
| **Emails Processed** | 1,855 | ✅ |
| **Date Format** | ISO (YYYY-MM-DD) | ✅ |
| **Automation** | Active (10:00 AM daily) | ✅ |
| **Configuration** | Correct accounts | ✅ |

### Data Quality
- ✅ **100% date normalization**: All calls and emails use ISO format
- ✅ **99.7% URL coverage**: Nearly all calls have public share URLs
- ✅ **Email parsing**: Full metadata extraction (title, date, duration, URLs, counts)
- ✅ **Linking accuracy**: Title + ISO date + duration matching works reliably
- ✅ **Duplicate handling**: Duration-based matching resolves multiple calls with same title

---

## 🏗️ Technical Architecture

### Core Components

```
/Users/admin/FathomInventory/
├── run_daily_share.py          # 1. Discover & Share (uses Fathom cookies)
├── scripts/
│   ├── download_emails.py      # 3. Receive & Process (uses Gmail OAuth)
│   └── send_daily_report.py    # 5. Report (email summary)
├── email_conversion/
│   └── fathom_email_2_md.py    # 4. Parse HTML → Markdown + metadata
├── fathom_emails.db            # SQLite database (calls + emails tables)
├── all_fathom_calls.tsv        # Master registry of discovered calls
└── docs/                       # Comprehensive documentation
```

### Authentication Files

| File | Purpose | Account | How to Refresh |
|------|---------|---------|----------------|
| `fathom_cookies.json` | Fathom.video web scraping | jschull@e-nable.org | `./scripts/refresh_fathom_auth.sh` (weekly) |
| `token.json` | Gmail API access | **fathomizer@ecorestorationalliance.org** | Delete + re-run `download_emails.py` |
| `credentials.json` | Google API project config | (project: fathomizer-email-analysis) | One-time setup |

**⚠️ CRITICAL**: `token.json` MUST be authenticated with `fathomizer@ecorestorationalliance.org`, not personal account

---

## 🔍 Data Model

### Calls Table
Primary record of discovered Fathom calls

| Field | Type | Example | Source |
|-------|------|---------|--------|
| `title` | TEXT | "ERA Steering Committee" | Fathom web scrape |
| `date` | TEXT | "2025-10-07" (ISO) | Fathom web scrape → normalized |
| `hyperlink` | TEXT | `https://fathom.video/calls/434777882` | Fathom web scrape |
| `public_share_url` | TEXT | `https://fathom.video/share/C_6-ddefN...` | Email → linked |
| `shareStatus` | TEXT | "success" / "failed" | Share operation result |

### Emails Table
Processed summary emails from Fathom

| Field | Type | Example | Source |
|-------|------|---------|--------|
| `message_id` | TEXT | "199c9f0832f88d35" | Gmail message ID |
| `meeting_title` | TEXT | "ERA Steering Committee" | Parsed from HTML |
| `meeting_date` | TEXT | "2025-10-07" (ISO) | Parsed → normalized |
| `meeting_url` | TEXT | `https://fathom.video/share/C_6-ddef...` | Extracted (prioritize /share/) |
| `action_items_count` | INT | 5 | Parsed from HTML |
| `body_md` | TEXT | Full markdown | HTML → Markdown conversion |

**Linking Logic**: Match by `calls.title` = `emails.meeting_title` AND `calls.date` = `emails.meeting_date` (both ISO format)

---

## 🚨 Known Issues & Solutions

### Issue: Wrong Gmail Account
**Symptom**: `/calls/` URLs instead of `/share/` URLs, date mismatches  
**Cause**: `token.json` authenticated with wrong account  
**Solution**: See [CONFIGURATION_ERRORS.md](CONFIGURATION_ERRORS.md)  
**Prevention**: Run verification command weekly

### Issue: Date Format Mismatch
**Symptom**: Emails not linking to calls  
**Cause**: Different date formats preventing matching  
**Solution**: ✅ **FIXED** - All dates normalized to ISO at entry points  
**Status**: Resolved Oct 9, 2025

### Issue: Cookie Expiration
**Symptom**: "Authentication failed" or "redirected to login"  
**Solution**: `./scripts/refresh_fathom_auth.sh` (weekly maintenance)  
**Prevention**: Set calendar reminder for weekly refresh

---

## 📚 Documentation Map

**For Quick Start:**
- [README.md](../README.md) - 5-minute setup guide

**For Understanding:**
- **This document** - System overview and data flow
- [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) - Complete technical details

**For Troubleshooting:**
- [CONFIGURATION_ERRORS.md](CONFIGURATION_ERRORS.md) - Critical configuration issues
- [AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md) - Auth setup and problems
- [IMPROVEMENTS_LOG.md](IMPROVEMENTS_LOG.md) - Change history and lessons learned

**For Operations:**
- [AUTOMATION_MONITORING_GUIDE.md](AUTOMATION_MONITORING_GUIDE.md) - Daily automation setup

---

## ✅ Verification Commands

**Check Gmail account (CRITICAL):**
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

**Check date formats:**
```bash
sqlite3 fathom_emails.db "SELECT COUNT(*) as iso_dates FROM calls WHERE date LIKE '____-__-__';"
# Expected: 1604 (all calls)
```

**Check URL coverage:**
```bash
sqlite3 fathom_emails.db "
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN public_share_url LIKE '%/share/%' THEN 1 ELSE 0 END) as share_urls,
  ROUND(100.0 * SUM(CASE WHEN public_share_url LIKE '%/share/%' THEN 1 ELSE 0 END) / COUNT(*), 1) as percent
FROM calls;
"
# Expected: ~99.8% share URLs
```

**Check Fathom cookies:**
```bash
python scripts/check_auth_health.py
```

---

## 🔄 Daily Workflow (Automated)

**10:00 AM Daily** (via macOS launchd):

1. **Discover** new calls from Fathom (2-3 minutes)
2. **Share** calls to fathomizer@ (1-2 minutes per call)
3. **Wait** 5 minutes for emails to arrive
4. **Download** and process new emails (1-2 minutes)
5. **Report** status via email to jschull@gmail.com

**Manual trigger:**
```bash
cd /Users/admin/FathomInventory
./run_all.sh
```

**Monitor progress:**
```bash
tail -f cron.log
```

---

## 📅 Maintenance Schedule

**Weekly** (every Sunday):
- [ ] Refresh Fathom cookies: `./scripts/refresh_fathom_auth.sh`
- [ ] Verify Gmail account configuration (see command above)
- [ ] Check URL coverage and data quality

**Monthly** (first Monday):
- [ ] Review system health metrics
- [ ] Check for authentication issues in logs
- [ ] Validate data accuracy with spot checks

**As Needed**:
- [ ] Re-authenticate Gmail if wrong account detected
- [ ] Update documentation after system changes
- [ ] Review and clear old cron logs

---

## 🎯 Success Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| **URL Coverage** | ≥ 95% | 99.8% | ✅ |
| **Date Consistency** | 100% | 100% | ✅ |
| **Automation Uptime** | ≥ 95% | ~100% | ✅ |
| **Data Quality** | No parsing errors | <1% errors | ✅ |
| **Configuration** | Correct accounts | Verified | ✅ |

---

*Last Updated: October 9, 2025*  
*System Status: **FULLY OPERATIONAL***
