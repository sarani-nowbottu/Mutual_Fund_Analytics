import os

for folder in ["data/raw", "data/processed", "notebooks", "sql", "dashboard", "reports"]:
    os.makedirs(folder, exist_ok=True)
    open(f"{folder}/.gitkeep", "w").close()  # lets Git track empty folders
print("Directory structure successfully initialized.")
