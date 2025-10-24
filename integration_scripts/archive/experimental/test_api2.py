import requests
import json

API_KEY = "sF9gLOLjqXECcReINyHCYw.C5u2TizRtq8kvaf7kL6XjkQ6KaAuhvrksUHGvIvlenY"
headers = {'X-Api-Key': API_KEY}

# Get meetings WITH transcript
response = requests.get(
    'https://api.fathom.ai/external/v1/meetings',
    headers=headers,
    params={
        'limit': 2,
        'include_transcript': 'true'
    }
)

data = response.json()
meeting = data['items'][0]

print(f"Meeting: {meeting['meeting_title']}")
print(f"\nCalendar invitees: {len(meeting.get('calendar_invitees', []))}")
for inv in meeting.get('calendar_invitees', []):
    print(f"  - {inv.get('name')} ({inv.get('email')})")

if meeting.get('transcript'):
    speakers = {}
    for entry in meeting['transcript']:
        speaker = entry['speaker']['display_name']
        email = entry['speaker'].get('matched_calendar_invitee_email', 'NO EMAIL')
        if speaker not in speakers:
            speakers[speaker] = email
    
    print(f"\nActual speakers in transcript: {len(speakers)}")
    for speaker, email in speakers.items():
        print(f"  - {speaker} ({email})")
else:
    print("\n❌ No transcript available")
