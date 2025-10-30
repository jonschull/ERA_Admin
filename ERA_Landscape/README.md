# ERA_Landscape/README.md

# ERA Landscape - Static Viewer

**Live Demo**: https://jonschull.github.io/ERA_Admin/ERA_Landscape/

**Historical repo (archived)**: https://github.com/jonschull/ERA_Landscape_Static

Interactive graph visualization for the climate/restoration landscape. Pure HTML/JavaScript, no server required.

---

## What Is This?

A **standalone HTML file** (20KB) that:
- Auto-loads fresh data from Google Sheets on page load
- Shows 350+ organizations and their relationships
- Allows editing (with Google sign-in)
- Requires NO server, NO Python, NO backend
- NO embedded data - always shows latest from Sheet

**Just open via HTTP server or GitHub Pages.**

---

## Quick Start

### View Locally (with Google Sheets API)

**Important:** Google Sheets API requires HTTP/HTTPS protocol. Use a local server:

```bash
# Clone the repo
git clone https://github.com/jonschull/ERA_Admin.git
cd ERA_Admin/ERA_Landscape

# Start local server
python3 -m http.server 8000

# Open in browser
open http://localhost:8000
```

**Note:** Opening `index.html` directly (file:// protocol) won't work - Google Sheets API requires HTTP/HTTPS. Use HTTP server locally or GitHub Pages for deployment.

### Deploy to GitHub Pages

Already configured! Merge PRs to main and GitHub Pages auto-deploys.

**URL**: https://jonschull.github.io/ERA_Admin/ERA_Landscape/

**Important**: Use branch-based workflow (see DEVELOPMENT.md)

---

## How It Works

### Data Flow
1. **Page loads** → Empty graph initialized
2. **Google Sheets API initializes** → API key authentication
3. **Data auto-loads** → Fetches nodes & edges from [ERA Climate Week Data](https://docs.google.com/spreadsheets/d/1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY/edit)
4. **Graph renders** → Shows ~350+ nodes with relationships
5. **Loading screen hides** → Interactive graph ready

**Zero embedded data** → Always shows fresh data from Sheet

### Authentication
- **Viewing**: No sign-in required (public read via API key)
- **Editing**: Click "Sign In" button, authenticate via Google OAuth
- **Saving**: Changes written directly back to Google Sheet

### Architecture
```
Browser loads index.html
  ↓
Calls Google Sheets API (API key)
  ↓
Fetches nodes & edges data
  ↓
Renders interactive graph (vis-network.js)
  ↓
User clicks "Sign In" (optional)
  ↓
OAuth popup → authenticated
  ↓
User can save edits back to Sheet
```

**No server. No backend. Pure client-side.**

---

## Documentation

**For Users:**
- [README.md](README.md) - This file (quick start, deployment)
- [KNOWN_ISSUES.md](../ERA_Landscape/KNOWN_ISSUES.md) - Current bugs and workarounds

**For Developers:**
- [NETWORK_ARCHITECTURE.md](../ERA_Landscape/NETWORK_ARCHITECTURE.md) - **Technical deep-dive:** Town Hall treatment, physics engine, node sizing, slider controls
- [DEVELOPMENT.md](../ERA_Landscape/DEVELOPMENT.md) - Development workflow and testing
- [AI_HANDOFF_GUIDE.md](../ERA_Landscape/AI_HANDOFF_GUIDE.md) - Context for AI assistants

## Files

```
ERA_Landscape_Static/
├── index.html                   # Main HTML file (UI, modals, event handlers)
├── graph.js                     # vis.js initialization and options
├── README.md                    # This file (quick start)
├── NETWORK_ARCHITECTURE.md      # Technical documentation (NEW!)
├── DEVELOPMENT.md               # Development workflow
├── KNOWN_ISSUES.md              # Bug tracking
└── tests/                       # Test scripts
    ├── test_load.py             # Basic load test
    ├── test_visual_nodesize.py  # Screenshot validation
    └── test_visual_centralgravity.py  # Screenshot validation
```

---

## Configuration

Google API credentials are embedded in `index.html`:

```javascript
const SHEET_ID = '1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY';
const API_KEY = 'AIzaSyBp23GwrTURmM3Z1ERZocotnu3Tn96TmUo';
const CLIENT_ID = '57881875374-flipnf45tc25cq7emcr9qhvq7unk16n5.apps.googleusercontent.com';
```

**Google Sheet Configuration:**
- **Sheet URL**: https://docs.google.com/spreadsheets/d/1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY/edit
- **Sheet Owner**: jschull@gmail.com
- **Access Policy**: Write access granted to trusted users only
- **Note**: Sheet URL not shared with end users (not ready for public editing)

**OAuth Configuration:**
- **OAuth App Name**: ERA Graph Browser Client
- **Google Cloud Account**: fathomizer@ecorestorationalliance.com
- **Console**: https://console.cloud.google.com/apis/credentials?project=57881875374
- **Status**: ✅ In production (anyone with Google account can sign in)

**To use your own Sheet:**
1. Copy the Google Sheet
2. Get API Key & OAuth Client ID from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
3. Update credentials in `index.html`
4. Make sure Sheet is publicly readable

---

## Development

### Edit the HTML/JavaScript

```bash
# Create feature branch
git checkout -b feat/feature-name

# Edit files
code index.html
code graph.js

# Test locally (MUST use HTTP server)
python3 -m http.server 8000
open http://localhost:8000

# Commit changes
git add .
git commit -m "feat: Update feature"
git push origin feat/feature-name

# Create PR on GitHub, then merge to main
```

**No build step. No compilation. Just edit and test.**

### Run Tests

```bash
# Install Playwright
pip install playwright
playwright install

# Run test
cd tests
python test_load.py
```

---

## Deployment

### GitHub Pages (Automatic)

Already configured! Every push to `main` auto-deploys in ~1-2 minutes.

**To update the live site:**
```bash
# 1. Create feature branch
git checkout -b feat/my-change

# 2. Make your changes
code index.html

# 3. Test locally (REQUIRED - needs HTTP server)
python3 -m http.server 8000
open http://localhost:8000

# 4. Commit and push branch
git add .
git commit -m "feat: Description of changes"
git push origin feat/my-change

# 5. Create PR and merge to main
# (via GitHub UI or gh pr create)

# 6. Wait for deployment (~1-2 minutes)
gh api repos/jonschull/ERA_Landscape_Static/pages/builds/latest | jq -r '.status'

# 7. Verify live site
open https://jonschull.github.io/ERA_Admin/ERA_Landscape/
```

**Settings → Pages:**
- Source: Deploy from branch
- Branch: `main`
- Folder: `/` (root)
- URL: https://jonschull.github.io/ERA_Landscape_Static/

**Build typically completes in:**
- First deploy: ~1-2 minutes
- Subsequent updates: ~30-60 seconds

### Other Hosting

Works on any static host:
- Netlify
- Vercel
- Amazon S3
- Your own web server
- Email attachment (yes, really!)
- Dropbox public link

**Just serve `index.html`.**

---

## Features

### Current
- ✅ Auto-loads fresh data from Google Sheets on page init
- ✅ Auto-fit graph after data loads
- ✅ Interactive graph (drag, zoom, pan)
- ✅ **Town Hall Integration** (65 events in fixed peripheral ring)
  - Grey edges with distance-based fading
  - See [NETWORK_ARCHITECTURE.md](../ERA_Landscape/NETWORK_ARCHITECTURE.md) for details
- ✅ **Network Settings Modal** (🌐 button)
  - Node Scaling (constant ↔ logarithmic)
  - Node Size (0.2-3.0x multiplier)
  - Edge Fading & Thickness
- ✅ **Physics Settings Modal** (⚙️ button)
  - Central Gravity, Node Spacing, Edge Springs
  - Real-time layout adjustment
  - ⚠️ Central Gravity has inverted behavior (see KNOWN_ISSUES.md)
- ✅ Node scaling by connection count with visual tests
- ✅ Quick Editor (add/remove connections)
  - Enter key triggers Add/Update
  - Yellow border highlights matching nodes
- ✅ Search filtering
- ✅ Hide/show nodes
- ✅ Save changes to Google Sheets (with sign-in)
- ✅ Re-Load button (re-fetch from Sheets with guardrail)
- ✅ Color-coded by type (person=blue, org=teal, project=purple, event=grey)
- ✅ Type parsed from ID prefix (person::, org::, project::, event::)
- ✅ **Progressive Node Selection Highlighting** (PR #39)
  - Click node → highlights 1st-order connections
  - Hold 3 seconds → expands to 2nd-order connections
  - Hold 6 seconds → expands to 3rd-order connections
  - Release & re-click → resumes expansion from current level
  - Highlighted edges: bright blue (#2B7CE9), width=2
  - Dimmed nodes/edges: 15% opacity, frozen in place
  - Cursor changes to 'progress' indicator while timer active
  - Auto-zoom to fit highlighted nodes in view
  - Works with search fields (qeFrom/qeTo)
- ✅ Hover tooltips on all buttons

### Planned
- [ ] Curation modal for organizations
- [ ] Batch operations
- [ ] Export to PNG/CSV
- [ ] Undo/redo

---

## Related Project

This project was extracted from [ERA_ClimateWeek](https://github.com/jonschull/ERA_ClimateWeek) and is now part of the ERA_Admin monorepo as a self-contained component.

**When to use each:**

**ERA_ClimateWeek** (Python):
- Data processing & transformation
- Importing from CSV
- Batch operations
- Development & testing

**ERA_Landscape_Static** (this project):
- Production viewer
- Public deployment
- No server needed
- Simple editing

---

## Browser Compatibility

Tested on:
- ✅ Chrome 118+
- ✅ Firefox 119+
- ✅ Safari 17+
- ✅ Edge 118+

Requires modern browser with ES6 support.

---

## License

MIT License - See parent project for details.

---

## Contact

**Repository**: https://github.com/jonschull/ERA_Admin (ERA_Landscape/ component)  
**Historical repo**: https://github.com/jonschull/ERA_Landscape_Static (archived)  
**Main Project**: https://github.com/jonschull/ERA_ClimateWeek  
**Developer**: Jon Schull