# az snapshot list --query "[*].{name: name, time: timeCreated }" > data.json
import jmespath
import json
from dateutil import parser
from datetime import datetime, timezone
import subprocess
import os
import sys

FRESHNESS_INTERVAL = 0
dry_run = eval(sys.argv[1])


def image_age(target_date: datetime) -> int:
    duration = datetime.now(timezone.utc) - target_date
    days_difference = duration.days

    return days_difference

with open('data.json', 'r') as file:
    data = json.load(file)

query = "[*].{name: name, date: time}"
result = jmespath.search(query, data)

for snapshot in result:
    if image_age(target_date=parser.parse(snapshot["date"])) >= FRESHNESS_INTERVAL:
        print("delete snapshot:", snapshot["name"], snapshot["date"])
        if not dry_run:
            command = [
            "az", "snapshot", "delete",
            "--resource-group", os.getenv("RESOURCE_GROUP_NAME"),
            "--name", snapshot["name"]
            ]
            subprocess.run(command, check=True)
