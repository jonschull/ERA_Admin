# Fathom Analysis Module

## Overview

This module contains scripts for analyzing Fathom meeting data using AI-powered analysis. It provides automated batch processing capabilities and individual call analysis tools.

## Scripts

### `ask_fathom_ai.py`
**Purpose**: Query Fathom's AI for analysis of individual meeting calls

**Usage**:
```bash
python ask_fathom_ai.py <fathom_url> "<question>"
```

**Example**:
```bash
python ask_fathom_ai.py "https://fathom.video/calls/123456" "Who were the participants and what were the key topics?"
```

**Dependencies**:
- `../fathom_cookies.json` - Authentication cookies for Fathom.video
- Playwright browser automation
- BeautifulSoup for HTML parsing

### `batch_analyze_calls.py`
**Purpose**: Batch analysis of multiple Fathom calls from a TSV file

**Usage**:
```bash
python batch_analyze_calls.py
```

**Input**: `../era connections.tsv` - TSV file with call URLs and metadata  
**Output**: `../analysis_results.txt` - Structured analysis results

**Features**:
- Resumes from previous runs (tracks completed analyses)
- Processes calls marked for analysis in the input TSV
- Calls `ask_fathom_ai.py` for each individual analysis
- Structured output with participant and collaboration information

### `run_analysis_wrapper.py`
**Purpose**: Watchdog script to monitor and restart batch analysis

**Usage**:
```bash
python run_analysis_wrapper.py
```

**Features**:
- Monitors `batch_analyze_calls.py` for inactivity (5-minute timeout)
- Automatically restarts if the process hangs or becomes unresponsive
- Useful for long-running batch analysis jobs
- Provides process monitoring and logging

## Data Flow

```
era connections.tsv → batch_analyze_calls.py → ask_fathom_ai.py → analysis_results.txt
                           ↑
                    run_analysis_wrapper.py (monitors)
```

## Configuration

### Required Files (in parent directory)
- `fathom_cookies.json` - Fathom.video authentication cookies
- `era connections.tsv` - Input data with call URLs
- `analysis_results.txt` - Output file (created automatically)

### Authentication
All scripts require valid Fathom cookies. Refresh weekly using:
```bash
cd .. && ./scripts/refresh_fathom_auth.sh
```

## Usage Examples

### Single Call Analysis
```bash
cd analysis
python ask_fathom_ai.py "https://fathom.video/calls/416857010" "Summarize the key decisions made in this meeting"
```

### Batch Analysis
```bash
cd analysis
python batch_analyze_calls.py
```

### Monitored Batch Analysis
```bash
cd analysis
python run_analysis_wrapper.py
```

## Output Format

The analysis results follow a structured format:
```
Name: John Smith
Location: Unknown
Affiliation: ecorestoration alliance
Collaborating with People: <name>, <name>, <name>, etc.
Collaborating with Organizations: <organization>, <organization>, <organization>, etc.
```

## Error Handling

### Common Issues
- **Authentication failures**: Refresh cookies with `../scripts/refresh_fathom_auth.sh`
- **Missing input file**: Ensure `../era connections.tsv` exists
- **Browser automation errors**: Check Playwright installation
- **Process hangs**: Use `run_analysis_wrapper.py` for automatic recovery

### Debugging
- Check `../cron.log` for system-level errors
- Monitor console output for real-time status
- Verify authentication with `../scripts/check_auth_health.py`

## Integration

This module integrates with the main Fathom Inventory system:
- Uses shared authentication system (`../fathom_cookies.json`)
- Processes data from the main call registry (`../all_fathom_calls.tsv`)
- Can be called from main workflow scripts
- Follows the same error handling and logging patterns

## Future Enhancements

Potential improvements for this module:
- Parallel processing for faster batch analysis
- Enhanced error recovery and retry logic
- More sophisticated analysis questions and output formats
- Integration with database storage for analysis results
- Web dashboard for monitoring analysis progress
