# ERA Admin Airtable Integration

## Overview
Self-contained Airtable integration for ERA administrative functions. This folder provides easy, routine access to the current ERA membership database in Airtable.

## Base Configuration
- **Base ID**: `appe7aXupdvB4xXzu`
- **Primary Table**: `People` (membership database)
- **API Access**: Via pyairtable library

## Quick Start

### 1. Setup Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Current Data
```bash
# Export all People records to CSV
python export_people.py

# Get summary statistics
python airtable_summary.py

# Export for cross-correlation with Fathom data
python export_for_fathom_matching.py
```

## Files

### Core Scripts
- `export_people.py` - Export People table to CSV with all fields
- `airtable_summary.py` - Generate database statistics and health check
- `export_for_fathom_matching.py` - Export optimized for name matching
- `config.py` - Centralized configuration and credentials

### Data Files
- `people_export.csv` - Latest full export of People table
- `people_for_matching.csv` - Cleaned names for cross-correlation
- `airtable_summary.txt` - Latest database statistics

### Utilities
- `requirements.txt` - Python dependencies
- `update_all.sh` - Run all exports and updates
- `venv/` - Virtual environment (created on first setup)

## Routine Usage

### Daily/Weekly Updates
```bash
# Quick update - get latest data
./update_all.sh

# Check what changed
python compare_exports.py people_export.csv people_export_previous.csv
```

### Cross-Correlation with Fathom
```bash
# Prepare Airtable data for matching
python export_for_fathom_matching.py

# Run cross-correlation (from FathomInventory/analysis/)
python ../airtable/cross_correlate.py
```

## Integration Points

### With Fathom Analysis
- Name matching between Airtable People and Fathom participants
- Enrichment of Fathom data with membership status, donor flags
- Identification of active participants not yet in membership database

### With ERA Admin Workflows
- Member communication lists
- Donor identification and tracking
- Engagement pattern analysis
- Geographic distribution mapping

## Maintenance

### Keep Data Fresh
- Run `./update_all.sh` weekly or before major analysis
- Monitor API rate limits (5 requests/second for Airtable)
- Backup exports before major changes

### Security & Data Protection
- **READ-ONLY MODE**: All scripts are configured for data export only
- **NO WRITES TO AIRTABLE**: Database modifications are disabled
- API key stored in `config.py` (not version controlled)
- Regular key rotation recommended

## Future Enhancements
- [ ] Automated daily sync with ERA_Admin automation
- [ ] Real-time change detection
- [ ] Bidirectional sync capabilities
- [ ] Integration with email systems
- [ ] Advanced matching algorithms for name variations
