import os
import requests
import shutil
from pydub import AudioSegment
import json
import UnityPy

WDS_Env_Url = os.environ.get("WDS_ENV_URL")
WDS_Env_Req = requests.post(WDS_Env_Url)
WDS_Env = (WDS_Env_Req.json())['result']

manifest_dir = './manifest'

# spine setting
spineFolder = './spine'
spinemaster = json.load(open(os.path.join(manifest_dir, 'Spine.json'), 'rb'))
if not os.path.exists(spineFolder):
    os.makedirs(spineFolder)

# cards setting
cardsFolder = './card'
if not os.path.exists(cardsFolder):
    os.makedirs(cardsFolder)

# background setting
bgFolder = './background'
bgmaster = json.load(open(os.path.join(manifest_dir, 'Background.json'), 'rb'))
if not os.path.exists(bgFolder):
    os.makedirs(bgFolder)

# load temp list
tempList = json.load(open(os.path.join('./_temp', 'Temp.json'), 'rb'))

############# spine
for spineId in tempList['spine'][:]:
    # check is file not exist
    isExist = [item for item in spinemaster if item.get('Id') == int(spineId)]
    IsExitImg = False
    IsExitMeta = False
    if len(isExist) == 0:
        try:
            fullurl = f'{WDS_Env["assetUrl"]}/2d-assets/Android/{WDS_Env["assetVersion"]}/adventurecharacterstand_assets_adventurecharacterstands/{spineId}.prefab.bundle'
            assetsReq = requests.get(fullurl)
            if assetsReq.status_code == 200:
                assetsbundle = UnityPy.load(assetsReq.content)
                for obj in assetsbundle.objects:
                    if obj.type.name == "Texture2D":
                        data = obj.read()
                        data.image.save(os.path.join(spineFolder, f'{spineId}.png'))
                        IsExitImg = True

                    if obj.type.name == "TextAsset":
                        data = obj.read()
                        ext = data.name.split('.')[-1]
                        open(os.path.join(spineFolder, f'{spineId}.{ext}'), "wb").write(bytes(data.script))
                        IsExitMeta = True

                if IsExitImg and IsExitMeta:
                    tempList['spine'].remove(spineId)
                    spinemaster.append({
                        "Id" : int(spineId),
                        "CharacterId" : int(spineId[0 : 3]),
                        "CompanyId" : int(spineId[0]),
                    })
        except:
            print(spineId)
    else:
        tempList['spine'].remove(spineId)

# save spine list
spinemaster.sort(key = lambda x: x["Id"] )
json_data = json.dumps(spinemaster, indent=4, ensure_ascii=False)
open(os.path.join(manifest_dir, 'Spine.json'), "w", encoding='utf8').write(json_data)

############# card
for cardId in tempList['card'][:]:
    try:
        fullurl = f'{WDS_Env["assetUrl"]}/2d-assets/Android/{WDS_Env["assetVersion"]}/charactercardtextures_assets_charactercardtextures/{cardId}.bundle'
        assetsReq = requests.get(fullurl)
        if assetsReq.status_code == 200:
            assetsbundle = UnityPy.load(assetsReq.content)
            for path, obj in assetsbundle.container.items():
                if obj.type.name == "Sprite" and path.endswith('.jpg'):
                    data = obj.read()
                    if data.name == cardId:
                        data.image.save(os.path.join(cardsFolder, f'{data.name}.png'))
            # clear the id 
            tempList['card'].remove(cardId)
    except:
        print(cardId)

############# backgorund
for bgId in tempList['background'][:]:
    if bgId not in bgmaster:
        try:
            fullurl = f'{WDS_Env["assetUrl"]}/2d-assets/Android/{WDS_Env["assetVersion"]}/adventurebackground_assets_adventurebackgrounds/{bgId}.bundle'
            assetsReq = requests.get(fullurl)
            if assetsReq.status_code == 200:
                assetsbundle = UnityPy.load(assetsReq.content)
                for obj in assetsbundle.objects:
                    if obj.type.name == "Texture2D":
                        data = obj.read()
                        if data.name == bgId:
                            data.image.save(os.path.join(bgFolder, f'{data.name}.png'))
                            bgmaster.append(data.name)
                            tempList['background'].remove(bgId)
        except:
            print(bgId)
    else:
        tempList['background'].remove(bgId)

# save background list
bgmaster.sort()
bg_json_data = json.dumps(bgmaster, indent=4, ensure_ascii=False)
open(os.path.join(manifest_dir, 'Background.json'), "w", encoding='utf8').write(bg_json_data)

############ save temp json
tempList_data = json.dumps(tempList, indent=4, ensure_ascii=False)
open(os.path.join('./_temp', 'Temp.json'), "w", encoding='utf8').write(tempList_data)