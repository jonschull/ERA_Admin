# Cookie Export Guide for Fathom.video

## When You Need This

- Setting up authentication for the first time
- Cookies have expired (authentication fails)
- Moving to a new environment
- Fathom access is being denied

Four methods are presented below.  If you are using Microsoft Edge, Method 4 is recommended.

## Method 1: Browser Developer Tools (Recommended)

### Chrome/Edge Steps:

1. **Log into Fathom.video** in your browser
2. **Navigate to** https://fathom.video/home
3. **Open Developer Tools** (F12 or right-click → Inspect)
4. **Go to Application tab** (or Storage in Firefox)
5. **Click on Cookies** in left sidebar
6. **Select https://fathom.video**
7. **Right-click in cookie list** → "Select All"
8. **Copy all cookies** (Ctrl+C)
9. **Paste into text editor** and format as JSON [this is not what we did.  

### Firefox Steps:

1. **Log into Fathom.video** in your browser
2. **Open Developer Tools** (F12)
3. **Go to Storage tab**
4. **Click on Cookies** → https://fathom.video
5. **Right-click** → "Select All"
6. **Copy** and format as JSON

## Method 2: Browser Extension (Easier)

### Recommended Extensions:

- **"Cookie-Editor"** (Chrome/Firefox)
- **"EditThisCookie"** (Chrome)
- **"Export Cookies"** (Firefox)

### Using Cookie-Editor:

1. **Install Cookie-Editor** from browser store
2. **Log into Fathom.video**
3. **Click Cookie-Editor icon**
4. **Click "Export"** button
5. **Choose "JSON format"**
6. **Copy the exported JSON**
7. **Save as fathom_cookies.json**

## Method 3: Manual Export Script

Save this as `export_cookies.js` and run in browser console:

```javascript
// Run this in browser console on fathom.video
function exportCookies() {
    const cookies = document.cookie.split(';').map(cookie => {
        const [name, value] = cookie.trim().split('=');
        return {
            name: name,
            value: value,
            domain: '.fathom.video',
            path: '/',
            secure: true,
            httpOnly: false,
            sameSite: 'Lax'
        };
    });
  
    console.log('Copy this JSON:');
    console.log(JSON.stringify(cookies, null, 2));
  
    // Also copy to clipboard if possible
    navigator.clipboard.writeText(JSON.stringify(cookies, null, 2));
}

exportCookies();
```

## Expected Cookie Format

Your `fathom_cookies.json` should look like this:

```json
[
  {
    "domain": ".fathom.video",
    "expirationDate": 1775094135,
    "hostOnly": false,
    "httpOnly": false,
    "name": "session_token",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "your_session_token_here"
  },
  {
    "domain": ".fathom.video",
    "expirationDate": 1775164697,
    "hostOnly": false,
    "httpOnly": false,
    "name": "user_id",
    "path": "/",
    "sameSite": "lax",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "your_user_id_here"
  }
]
```

## Important Cookie Fields

### Required Fields:

- **name**: Cookie name
- **value**: Cookie value
- **domain**: Usually ".fathom.video"
- **path**: Usually "/"

### Optional but Important:

- **expirationDate**: Unix timestamp (when cookie expires)
- **secure**: true/false
- **httpOnly**: true/false
- **sameSite**: "Strict", "Lax", or "None"

### Auto-Fixed by System:

- **sameSite**: System converts invalid values to "Lax"
- **partitionKey**: System removes if invalid

## Testing Your Cookies

After exporting cookies, test them:

```bash
cd authentication
python test_fathom_cookies.py
```

Expected output:

```
✅ fathom_cookies.json found with 25 cookies
✅ All cookies are current
✅ Successfully authenticated with Fathom
🎉 Fathom cookie authentication is fully functional!
```

## Troubleshooting

### "Cookies expired" Error

**Solution**: Export fresh cookies from browser

### "Invalid JSON" Error

**Solution**: Validate JSON format at jsonlint.com

### "Authentication failed" Error

**Possible causes**:

1. Cookies are from wrong domain
2. Session has been invalidated
3. Fathom.video changed authentication system

**Solution**: Log out and back into Fathom, export fresh cookies

### "sameSite" Errors

**Solution**: System automatically fixes these - no action needed

## Security Notes

- **Keep cookies private** - they provide full access to your Fathom account
- **Don't share cookie files** - they contain authentication tokens
- **Rotate regularly** - export fresh cookies monthly
- **Use secure storage** - set file permissions to 600

```bash
chmod 600 fathom_cookies.json
```

## Method 4: Edge Cookie Converter Script (Automated)

For Microsoft Edge users, there's an automated converter script:

### Using convert_edge_cookies.py:

1. **Log into Fathom.video** in Microsoft Edge
2. **Open Developer Tools** (F12) → Application tab → Cookies → https://fathom.video
3. **Select all cookies** (Ctrl+A) and **copy** (Ctrl+C)
4. **Run the converter**:
   ```bash
   python convert_edge_cookies.py
   ```
5. **Paste the copied cookie data** when prompted
6. **Press Enter twice** to finish
7. **Script automatically saves** as `fathom_cookies.json`

### Converter Features:

- ✅ Handles Edge's tab-separated cookie format
- ✅ Converts expiration dates to Unix timestamps
- ✅ Sets proper domain and security attributes
- ✅ Validates and formats JSON correctly

## Automation Tips

- **Set calendar reminder** to refresh cookies **weekly** (not monthly - some expire daily)
- **Monitor expiration dates** in cookie file
- **Test authentication** before important runs
- **Keep backup** of working cookie files
- **Use the Edge converter script** for quick updates
