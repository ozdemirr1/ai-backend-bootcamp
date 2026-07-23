import json
from pathlib import Path

current_directory = Path(__file__).parent
data_directory = current_directory / "data"
data_directory.mkdir(exist_ok=True)
summary_file_path = data_directory / "ticket_summary.txt"
ticket_json_file_path = data_directory / "ticket.json"
missing_ticket_file_path = data_directory / "missing_ticket.json"

ticket_data = {
    "id": 1001,
    "title": "Password reset email is not received",
    "priority": "high",
    "is_resolved": False,
    "assigned_user": None,
}

with ticket_json_file_path.open("w", encoding="utf-8") as ticket_json_file:
    json.dump(ticket_data, ticket_json_file, indent=2, ensure_ascii=False)
    ticket_json_file.write("\n")

with ticket_json_file_path.open("r", encoding="utf-8") as ticket_json_file:
    loaded_ticket = json.load(ticket_json_file)

with summary_file_path.open("w", encoding="utf-8") as summary_file:
    summary_file.write("Ticket ID: 1001\n")
    summary_file.write("Title: Password reset email is not received\n")
    summary_file.write("Priority: high\n")

with summary_file_path.open("a", encoding="utf-8") as summary_file:
    summary_file.write("Assigned user: Furkan\n")

with summary_file_path.open("r", encoding="utf-8") as summary_file:
    ticket_summary = summary_file.read().strip()

print(ticket_summary)
print(f"Loaded ticket title: {loaded_ticket['title']}")
print(f"Loaded ticket priority: {loaded_ticket['priority']}")

assert summary_file_path.exists()
assert ticket_json_file_path.exists()
assert loaded_ticket == ticket_data
assert isinstance(loaded_ticket["id"], int)
assert loaded_ticket["assigned_user"] is None
assert "Assigned user: Furkan" in ticket_summary

print("All file handling checks passed.")

try:
    with missing_ticket_file_path.open("r", encoding="utf-8") as missing_ticket_file:
        json.load(missing_ticket_file)
except FileNotFoundError:
    print(f"Ticket file not found: {missing_ticket_file_path.name}")