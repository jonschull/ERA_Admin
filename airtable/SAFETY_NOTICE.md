# 🔒 AIRTABLE SAFETY NOTICE

## READ-ONLY MODE ENFORCED

**IMPORTANT**: This Airtable integration is configured for **READ-ONLY** access only.

### What This Means:
- ✅ **Safe to run**: All scripts only READ data from Airtable
- ✅ **No modifications**: Your Airtable database will NOT be changed
- ✅ **Export only**: Scripts create local CSV files for analysis
- ✅ **Cross-correlation safe**: Matching analysis uses local data only

### Scripts Confirmed Read-Only:
- `export_people.py` - ✅ Export only
- `export_for_fathom_matching.py` - ✅ Export only  
- `cross_correlate.py` - ✅ Uses local CSV files only
- `update_all.sh` - ✅ Runs export scripts only

### Database Protection:
- No CREATE operations
- No UPDATE operations  
- No DELETE operations
- No WRITE operations of any kind

### Future Modifications:
Any scripts that would modify Airtable will require explicit approval and will include prominent warnings.

---
**Last Updated**: 2025-09-23  
**Status**: All operations verified as read-only
