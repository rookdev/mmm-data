import os
import json
from pathlib import Path

errors = []
bail = False

dbDir = os.path.join(".","dbs")
for dbFilename in os.listdir(dbDir):
    dbFilepath = os.path.join(dbDir, dbFilename)
    if os.path.isfile(dbFilepath):
        if dbFilename.endswith(".json"):
            with open(dbFilepath, "r", encoding="utf-8") as dbFile:
                print(f"Validating {dbFilepath}")
                try:
                    dbJSON = json.load(dbFile)
                except json.JSONDecodeError as e:
                    jsonFile.seek(0)
                    errorLine = ""
                    errorCol = 0
                    pattern = r"^(?:\D+)(\d+)(?:\D+)(\d+)(?:\D+)(\d+)(?:\D+)$"
                    match = re.match(pattern, str(e))
                    if match:
                        line_num = int(match.group(1))
                        for i,line in enumerate(jsonFile):
                            if i == (line_num - 1):
                                errorLine = line
                            if i > line_num:
                                break
                        errorCol = int(match.group(2))
                    errors.append([
                        f"🔴ERROR: Connection data '{region}/{subregion}' is malformed!",
                        e,
                        errorLine.replace("\n",""),
                        ("-" * (errorCol - 3)) + "^"
                    ])

if bail:
    for errorSet in errors:
        for error in errorSet:
            print(error)
    print("🔴Something fucked up! Bailing!")
    exit(1)
