#!/usr/bin/env python3
"""
Monitor network traffic when clicking NEXT button on Google Groups members page.

Uses ggroups_auth module for authentication (DRY principle).

This script:
1. Authenticates to Google Groups
2. Navigates to members page
3. Monitors network requests
4. Waits for you to click NEXT button
5. Shows what network requests were made

Usage:
    python monitor_next_button.py
"""

from pathlib import Path
from ggroups_auth import authenticate_ggroups, verify_authentication

# Configuration
SCRIPT_DIR = Path(__file__).parent
GROUP_URL = "https://groups.google.com/g/ecorestoration-alliance/members"

def monitor_next_button():
    """Monitor network traffic when NEXT button is clicked."""
    print("=" * 80)
    print("NETWORK MONITOR - Google Groups NEXT Button")
    print("=" * 80)
    print()
    
    # Track network requests
    requests = []
    
    def log_request(request):
        """Log all requests."""
        requests.append({
            'method': request.method,
            'url': request.url,
            'headers': dict(request.headers),
            'post_data': request.post_data
        })
    
    def log_response(response):
        """Log responses and highlight interesting ones."""
        print(f"📡 {response.request.method} {response.status} {response.url}")
        
        # Highlight potentially interesting requests
        url_lower = response.url.lower()
        if any(keyword in url_lower for keyword in ['member', 'page', 'next', 'list', 'data']):
            print(f"   ⭐ POTENTIALLY RELEVANT!")
            print(f"   Method: {response.request.method}")
            print(f"   Status: {response.status}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            if response.request.post_data:
                print(f"   POST data: {response.request.post_data[:200]}")
            print()
    
    # Authenticate using the reusable module
    with authenticate_ggroups() as page:
        print("✅ Authenticated with Microsoft Edge")
        print()
        
        # Set up network monitoring
        page.on('request', log_request)
        page.on('response', log_response)
        
        # Navigate to members page
        print(f"📍 Navigating to: {GROUP_URL}")
        page.goto(GROUP_URL, wait_until='networkidle')
        
        # Give page time to load
        page.wait_for_timeout(3000)
        print("✅ Page loaded - ready to monitor")
        print()
        
        # Clear initial requests
        requests.clear()
        
        print("=" * 80)
        print("✋ MANUAL ACTION REQUIRED")
        print("=" * 80)
        print()
        print("Please click the NEXT button (>) in the browser window.")
        print("I'll monitor the network traffic and show you what happens.")
        print()
        print("Watching for 60 seconds...")
        print()
        
        # Wait for user to click NEXT
        page.wait_for_timeout(60000)
        
        print()
        print("=" * 80)
        print("📊 NETWORK ANALYSIS")
        print("=" * 80)
        print()
        
        # Analyze requests
        if requests:
            print(f"Total requests captured: {len(requests)}")
            print()
            
            # Filter for interesting requests
            interesting = [r for r in requests if 
                         any(keyword in r['url'].lower() for keyword in 
                             ['member', 'page', 'next', 'list', 'data', 'api'])]
            
            if interesting:
                print(f"Found {len(interesting)} potentially relevant requests:")
                print()
                for i, req in enumerate(interesting, 1):
                    print(f"{i}. {req['method']} {req['url']}")
                    if req['post_data']:
                        print(f"   POST data: {req['post_data'][:300]}")
                    print()
            else:
                print("No obviously relevant requests detected.")
                print()
                print("All requests made:")
                for req in requests:
                    print(f"  {req['method']} {req['url']}")
        else:
            print("No requests captured. Did you click the NEXT button?")
        
        print()
        print("=" * 80)
        print("Analysis complete. Check output above for API endpoints.")
        print("=" * 80)

if __name__ == "__main__":
    monitor_next_button()
