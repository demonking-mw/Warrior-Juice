import requests

BASE = "http://127.0.0.1:5000"

response = requests.post(
    BASE + "/activity",
    json={
        "act_title": "Project Kickoff Meeting",
        "user_name": {
            "developers": {
                "frontend": "bob",
            }
        },
        "act_type": "Meeting",
        "due_date": "2025-02-02 14:30:00",
        "act_brief": "Initial meeting to discuss project goals and deliverables.",
        "aux_info": {
            "location": "Zoom",
            "duration": "1 hour",
            "agenda": ["Introductions", "Project Scope", "Timeline"]
        },
        "task_tree": {
        }
    },
    timeout=10,
)
print(response.json())
