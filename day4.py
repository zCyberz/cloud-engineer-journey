import json 
data = {
    "employees":[
        {"name": "Alice", "role": "Developer", "active": True},
        {"name": "Bob", "role": "Designer", "active": False},
        {"name": "Charlie", "role": "DevOps", "active": True},
        {"name": "David", "role": "Manager", "active": False}
    ]
}

with open("employees.json","w") as f:
    json.dump(data,f)

print("--- Active employees ---")

with open("employees.json","r") as f:
    loaded = json.load(f)

for employee in loaded["employees"]:
    if employee["active"] == True:
        print(f"{employee['name']} - {employee['role']}")

loaded["employees"].append({"name":"Eve","role":"Cloud Engineer","active":True})

with open("employees.json","w") as f:
    json.dump(loaded,f,indent=4)

print("--- All employees ---")
for employee in loaded["employees"]:
    if employee["active"] == True:
        print(f"{employee['name']} - {employee['role']} - active")
    else:
        print(f"{employee['name']} - {employee['role']} - inactive")