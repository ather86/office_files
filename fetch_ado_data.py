import requests
import json
import pandas as pd
import base64
from datetime import datetime
import os

# Load config
with open('config.json') as f:
    config = json.load(f)

# ADO variables
org_url = config["organization"]
project = config["project"]
area_path = config["area_path"]
iteration_path = config["iteration_path"]
pat = config["pat"]

# Set up ADO auth
authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic '+authorization
}

# WIQL query using AreaPath and IterationPath
query = {
    "query": f"""
    SELECT
        [System.Id],
        [System.WorkItemType],
        [System.Title],
        [System.State],
        [Microsoft.VSTS.Scheduling.StoryPoints],
        [System.AssignedTo]
    FROM workitems
    WHERE
        [System.TeamProject] = '{project}'
        AND [System.AreaPath] UNDER '{area_path}'
        AND [System.IterationPath] UNDER '{iteration_path}'
    ORDER BY [System.ChangedDate] DESC
    """
}

# Run the WIQL query
wiql_url = f"{org_url}{project}/_apis/wit/wiql?api-version=7.0"
response = requests.post(wiql_url, headers=headers, json=query)
response.raise_for_status()
work_item_ids = [item["id"] for item in response.json()["workItems"]]

print(f"Found {len(work_item_ids)} work items")

# Batch get work item details
def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i+size]

all_items = []

for chunk in chunked(work_item_ids, 200):  # Max batch size = 200
    ids = ",".join(map(str, chunk))
    url = f"{org_url}_apis/wit/workitems?ids={ids}&$expand=fields&api-version=7.0"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    items = r.json()["value"]
    for item in items:
        fields = item["fields"]
        all_items.append({
            "ID": item["id"],
            "Type": fields.get("System.WorkItemType", ""),
            "Title": fields.get("System.Title", ""),
            "State": fields.get("System.State", ""),
            "Assignee": fields.get("System.AssignedTo", {}).get("displayName", "Unassigned"),
            "Story Points": fields.get("Microsoft.VSTS.Scheduling.StoryPoints", 0)
        })

# Save to CSV
df = pd.DataFrame(all_items)
os.makedirs("output", exist_ok=True)
df.to_csv("output/sprint_data.csv", index=False)
print("✅ Data saved to output/sprint_data.csv")
