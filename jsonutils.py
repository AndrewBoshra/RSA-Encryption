import json

# function to add to JSON
def writeJson(new_data, filename='PublicKeys.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["publickeys"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)


# function to add to JSON
def getUserPU(receivername, filename='PublicKeys.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        for obj in file_data.get("publickeys"):
            if obj.get("name") == receivername:
                return obj.get("publicmod"), obj.get("publicexp")
        return False

def getJsonData(filename='CCAtestcases.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        return file_data.get("testcases")
