import os, random
import json
from PIL import Image

nftArray = []

jsonData = open("config.json")
jsonData = json.load(jsonData)

def init():
    thingsexist = True
    if not os.path.exists("results"):
        os.makedirs("results")
    for layer in jsonData["layers"]:
        if not os.path.exists(layer["folder_name"]):
            thingsexist = False
            os.makedirs(layer["folder_name"])
            print("generated the folder", layer["folder_name"], ", because it didn't exist.")
    if not thingsexist:
        print("add files to those folders, change the config.json, run this file.")
        exit()

def generateNFT():
    layersInOrder = []

    for layer in jsonData["layers"]:
        layersInOrder.append(None)

    for layer in jsonData["layers"]:
        layersInOrder[int(layer["id"])] = layer

    nftImage = Image.new(size=(jsonData["image"][0]["width"], jsonData["image"][0]["height"]), mode=jsonData["image"][0]["mode"])
    nftSeed = ""

    for layer in layersInOrder:
        currentLayerImage = random.choice(os.listdir(layer["folder_name"]))
        nftSeed+=currentLayerImage
        currentLayerImage = Image.open(layer["folder_name"] + "/" + currentLayerImage)
        currentLayerImage = currentLayerImage.convert(jsonData["image"][0]["mode"])
        nftImage.paste(currentLayerImage, (0, 0), currentLayerImage)

    if nftSeed in nftArray:
        generateNFT()
    else:
        nftArray.append(nftSeed)
        nftImage.save(f"results/{len(nftArray)}.png", "PNG")
        print(f"created NFT #{len(nftArray)}")

init()
for i in range(jsonData["image"][0]["nft_amount"]):
    generateNFT()