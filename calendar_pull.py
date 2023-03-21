import os
import requests
import urllib.parse
from datetime import datetime, timedelta
from ics import Calendar, Event

ORG_ID = os.environ.get('SLING_ORD_ID')
USER_ID = os.environ.get('SLING_USER_ID')
AUTH_CODE = os.environ.get('SLING_AUTH_CODE')

print(ORG_ID)
print(USER_ID)
print(AUTH_CODE)

today = datetime.today()
end_date = today + timedelta(days=55)
date_str = urllib.parse.quote(f'{today.isoformat()}/{end_date.isoformat()}', safe='')

request_url = f'https://api.getsling.com/v1/calendar/{ORG_ID}/users/{USER_ID}?dates={date_str}'

headers = {
    'authorization': AUTH_CODE
}

r = requests.get(request_url, headers=headers)
r.raise_for_status()

response_json = r.json()

cal = Calendar()

for event_obj in response_json:
    if event_obj['status'] != 'published' \
    or event_obj['type'] != 'shift' \
    or event_obj['user']['id'] != int(USER_ID):
        continue
    
    event = Event()
    event.name = 'work'
    event.begin = event_obj['dtstart']
    event.end = event_obj['dtend']
    cal.events.add(event)


with open('osterhaus.ics', 'w') as f:
    f.writelines(cal.serialize_iter())
