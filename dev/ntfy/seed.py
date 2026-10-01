"""Publishes sample notifications to the dev ntfy server: every priority,
tags (some rendered as emoji), a click link, action buttons, markdown and a
long message. Topics: themepark-alerts and themepark-updates."""
import json
import time
import urllib.request

BASE = "http://ntfy:80"
MESSAGES = [
    ("themepark-alerts", {"title": "Backup finished", "message": "Nightly backup of 3 volumes took 4 min 12 s.",
                          "tags": ["white_check_mark", "backup"], "priority": 2}),
    ("themepark-alerts", {"title": "Disk almost full", "message": "/data is at 92% (1.84 of 2 TB).",
                          "tags": ["warning", "storage"], "priority": 4, "click": "https://theme-park.dev"}),
    ("themepark-alerts", {"title": "Service down", "message": "web-02 has not answered for 5 minutes.",
                          "tags": ["rotating_light"], "priority": 5,
                          "actions": [{"action": "view", "label": "Open dashboard", "url": "https://theme-park.dev"}]}),
    ("themepark-updates", {"title": "Update available", "markdown": True,
                           "message": "**Grafana 13.2.3** is out.\n\n- faster dashboards\n- [release notes](https://grafana.com)"}),
    ("themepark-updates", {"message": "A plain message without a title, at default priority.", "priority": 3}),
    ("themepark-updates", {"title": "A long one", "tags": ["memo"], "message": ("This message is long enough to wrap "
                           "over several lines, so the card's line height, text colour and padding are visible. ") * 3}),
]

for _ in range(60):                                  # wait for the server
    try:
        urllib.request.urlopen(f"{BASE}/v1/health", timeout=2).read()
        break
    except OSError:
        time.sleep(1)
for topic, msg in MESSAGES:
    body = json.dumps(dict(msg, topic=topic)).encode()
    urllib.request.urlopen(urllib.request.Request(BASE, data=body, method="POST",
                                                  headers={"Content-Type": "application/json"}), timeout=5).read()
    time.sleep(0.3)
print(f"published {len(MESSAGES)} sample notifications")
