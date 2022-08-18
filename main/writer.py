import json,os

def write(data,name = "P1"):
    with open(f"Locals/{name}.json","w") as f:
        json.dump(data,f,indent=2)
    
def read(file_name):
    with open(file_name,"r") as f:
        data = json.load(f)

    return data

def reset():
    for path in os.listdir("Locals"):
        os.remove(f"Locals/{path}")