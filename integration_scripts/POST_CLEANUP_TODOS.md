# Post-Cleanup TODOs - Oct 23, 2025

## ⚠️ CRITICAL - Review Before Next Landscape Update

### **Concern: ERA_Landscape Sync Scripts May Be Disrupted**

During cleanup (Oct 23, 2025), we archived ~120 files including scripts with "export" in their names. Some of these may have been actively syncing the participant database to the ERA_Landscape visualization.

**Scripts that were moved to `archive/experimental/`:**
- `export_to_landscape_prototype.py`
- `export_townhalls_to_landscape.py`

**Initial findings:**
- README.md indicates landscape export is "Phase 5T - future" (after Phase 4B-2)
- May be prototype/experimental rather than production
- But still need to verify if actively used

**Action Items:**

1. **Verify landscape sync still works:**
   - Check if ERA_Landscape visualization is still updating
   - Test the sync process
   - Identify which script was actually being used

2. **If broken:**
   - Restore the active landscape sync script to main directory
   - Document it as a "keeper" in CLEANUP_SUMMARY.md
   - Add it to core scripts list

3. **Document the landscape sync workflow:**
   - Which script runs?
   - How often (manual vs automated)?
   - What triggers it?
   - Add to AI_ASSISTANT_CONTEXT_RECOVERY.md if needed

4. **Review other archived scripts for active dependencies:**
   - Check `archive/experimental/` for other scripts that may be in use
   - Look for cron jobs, launchd tasks, or manual workflows that reference archived scripts

---

## Other Post-Cleanup Items

### **Review archived experimental scripts for lessons**
Location: `archive/experimental/` (37 files)

These contain "important insights into what has and has not worked in imposing discipline and efficiency on this process" (user note).

Should be reviewed to extract:
- What approaches to forcing functions were tried?
- What worked vs what didn't?
- Any patterns we should incorporate?

### **Update documentation based on lessons**
After reviewing experimental scripts, update:
- AI_ASSISTANT_CONTEXT_RECOVERY.md with additional forcing functions that worked
- PAST_LEARNINGS.md with patterns discovered

---

## Status
- [ ] Verify landscape sync still works
- [ ] Restore any active scripts that were archived
- [ ] Review experimental scripts for lessons
- [ ] Update documentation with extracted lessons
- [ ] Test complete workflow end-to-end
