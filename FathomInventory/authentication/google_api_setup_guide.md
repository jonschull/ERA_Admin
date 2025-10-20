# Google API Setup Guide

## When You Need This
- Setting up the system for the first time
- Moving to a new Google account
- Credentials have been revoked or compromised
- Setting up ERA_Admin project with different email

## Overview
The system needs Google API access to read emails from the Gmail account where Fathom sends meeting summaries. This requires:

1. **Google Cloud Project** with Gmail API enabled
2. **OAuth 2.0 Credentials** for desktop application
3. **User consent** for Gmail read access

## Step-by-Step Setup

### 1. Create Google Cloud Project

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Sign in** with the Google account that will be used for email access
3. **Create New Project**:
   - Click "Select a project" dropdown
   - Click "New Project"
   - Project name: `era-admin-fathom` (or similar)
   - Click "Create"

### 2. Enable Gmail API

1. **Navigate to APIs & Services** → **Library**
2. **Search for "Gmail API"**
3. **Click on Gmail API**
4. **Click "Enable"**
5. **Wait for activation** (may take a few minutes)

### 3. Create OAuth 2.0 Credentials

1. **Go to APIs & Services** → **Credentials**
2. **Click "Create Credentials"** → **OAuth client ID**
3. **Configure OAuth consent screen** (if prompted):
   - User Type: **External** (unless using Google Workspace)
   - App name: `ERA Admin Fathom Integration`
   - User support email: Your email
   - Developer contact: Your email
   - Scopes: Add `https://www.googleapis.com/auth/gmail.readonly`
   - Test users: Add your email address
4. **Create OAuth client ID**:
   - Application type: **Desktop application**
   - Name: `ERA Admin Desktop Client`
   - Click "Create"

### 4. Download Credentials

1. **Find your new OAuth client** in credentials list
2. **Click download icon** (⬇️) next to your client
3. **Save file as `credentials.json`** in project root
4. **Verify file contents** look like:

```json
{
  "installed": {
    "client_id": "your-client-id.apps.googleusercontent.com",
    "project_id": "era-admin-fathom",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your-client-secret",
    "redirect_uris": ["http://localhost"]
  }
}
```

### 5. Test Authentication

1. **Run authentication test**:
```bash
cd authentication
python test_google_auth.py
```

2. **Complete OAuth flow**:
   - Browser will open automatically
   - Sign in with your Google account
   - Grant permissions for Gmail read access
   - Return to terminal for confirmation

3. **Verify token creation**:
   - `token.json` file should be created
   - Test should show "Gmail API access successful"

## Understanding the Files

### credentials.json (Client Credentials)
- **Contains**: OAuth client ID and secret
- **Purpose**: Identifies your application to Google
- **Security**: Sensitive but not user-specific
- **Expiration**: Does not expire
- **Sharing**: Can be shared within your organization

### token.json (User Token)
- **Contains**: Access token and refresh token
- **Purpose**: Proves user has granted permission
- **Security**: Very sensitive, user-specific
- **Expiration**: Access token expires hourly, refresh token long-lived
- **Sharing**: Never share - specific to one user

## Scopes and Permissions

### Current Scope
```python
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
```

### What This Allows
- **Read email messages** and metadata
- **Search emails** by sender, subject, etc.
- **Access email attachments**
- **View email labels** and folders

### What This Does NOT Allow
- **Send emails**
- **Delete emails**
- **Modify emails**
- **Access other Google services**

## Troubleshooting

### "Project not found" Error
**Cause**: Wrong project selected in Cloud Console
**Solution**: Verify project name in dropdown matches your setup

### "Gmail API not enabled" Error
**Cause**: API not activated for project
**Solution**: Go to APIs & Services → Library → Enable Gmail API

### "Invalid client" Error
**Cause**: Wrong credentials file or corrupted download
**Solution**: Re-download credentials.json from Cloud Console

### "Access denied" Error
**Cause**: User hasn't granted permissions or consent screen not configured
**Solution**: 
1. Check OAuth consent screen configuration
2. Add your email as test user
3. Delete token.json and re-run OAuth flow

### "Quota exceeded" Error
**Cause**: Too many API requests (rare for this use case)
**Solution**: Wait and retry, or request quota increase

## Security Best Practices

### File Permissions
```bash
chmod 600 credentials.json token.json
```

### Version Control
Add to `.gitignore`:
```
credentials.json
token.json
```

### Backup Strategy
- **Keep secure backup** of credentials.json
- **Don't backup token.json** (can be regenerated)
- **Document project settings** for recreation if needed

### Access Review
- **Regularly review** OAuth consent screen
- **Monitor API usage** in Cloud Console
- **Revoke access** if no longer needed

## For ERA_Admin Project

### Account Considerations
- **Use dedicated service account** if possible
- **Or use shared organizational account** for ERA emails
- **Ensure account has access** to target Gmail inbox

### Project Naming
- Use descriptive project name: `era-admin-fathom-integration`
- Tag resources appropriately for cost tracking
- Document project purpose in description

### Monitoring
- **Enable audit logs** for security
- **Set up billing alerts** (though usage should be minimal)
- **Monitor API quotas** and usage patterns

## Testing Checklist

After setup, verify:
- [ ] credentials.json file exists and is valid JSON
- [ ] OAuth flow completes successfully
- [ ] token.json is created with proper expiry
- [ ] Gmail API returns user profile information
- [ ] Can search for Fathom emails specifically
- [ ] Token refresh works automatically
- [ ] No quota or permission errors

## Maintenance

### Monthly Tasks
- **Check token expiry** dates
- **Verify API access** still works
- **Review Cloud Console** for any alerts

### When Moving Environments
1. **Copy credentials.json** to new environment
2. **Don't copy token.json** (user-specific)
3. **Run OAuth flow** in new environment
4. **Test API access** before production use
