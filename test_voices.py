from app import get_api_key
from google import genai

client = genai.Client(api_key=get_api_key())
page_token = None
core_voices = []

for _ in range(20):
    kwargs = {"page_token": page_token} if page_token else {}
    resp = client.voices.list(**kwargs)
    if hasattr(resp, 'voices') and resp.voices:
        for v in resp.voices:
            if v.type == 'prebuilt' and not ('-' in (v.id or '')):
                core_voices.append((v.id, v.display_name, v.gender, v.description))
    if hasattr(resp, 'next_page_token') and resp.next_page_token:
        page_token = resp.next_page_token
    else:
        break

print(f"Total core voices found: {len(core_voices)}")
for cv in core_voices:
    print(cv)
