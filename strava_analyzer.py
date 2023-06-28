import json
import os


cumulative = 0
milestone = 100
milestone_date = None

files = sorted(os.listdir("strava-runs"))
files.reverse()
print("first run on 11/20/2021")
for f in files:
    if not f.endswith("json"):
        continue
    with open(f'strava-runs/{f}', 'r') as file_reader:
        file_page = f.split(".")[0][4:]
        file_content = file_reader.readlines()[0]
        json_runs = json.loads(file_content)
        seen_page = json_runs["page"]
        if seen_page != int(file_page):
            raise Exception("oh no")
        runs = reversed(json_runs["models"])
        for run in runs:
            cumulative += float(run["distance"])
            if cumulative > milestone:
                milestone += 100
                milestone_date = run["start_date"]
                print(f"Cumulative of {cumulative} reached on {milestone_date}")

print(cumulative)
print(run["start_date"])

print("done")