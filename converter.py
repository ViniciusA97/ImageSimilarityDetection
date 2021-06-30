import glob
import uuid as uuid4
import json

def createJsonData(termo:str):
    finaljson = []

    termo = termo.replace(" ", "_")

    path = './images/' + termo +"/"
    print("Paht: "+path)
    for filename in glob.glob(path+'*.jpg'): 
        uuid = generateUUID()
        finalFilename = filename[len(path):-4]
        print("FinalFilename: "+finalFilename)
        finaljson.append({"imageName": finalFilename, "uuid":uuid})

    print(finaljson)

    with open('output_images.json', 'w') as json_file:
        json.dump(finaljson, json_file)

def generateUUID():
    uuidGenerated = uuid4.uuid4()
    uuidString = str(uuidGenerated)
    return uuidString
