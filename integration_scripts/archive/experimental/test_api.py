import requests
import json

API_KEY = "sF9gLOLjqXECcReINyHCYw.C5u2TizRtq8kvaf7kL6XjkQ6KaAuhvrksUHGvIvlenY"
headers = {'X-Api-Key': API_KEY}

# Get recent meetings
response = requests.get(
    'https://api.fathom.ai/external/v1/meetings',
    headers=headers,
    params={'limit': 5}
)

data = response.json()
print(f"Total meetings returned: {len(data.get('items', []))}")
print("\nFirst meeting structure:")
print(json.dumps(data['items'][0], indent=2))
