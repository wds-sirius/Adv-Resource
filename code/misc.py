import os
import json
import requests
import UnityPy

WDS_Env_Url = os.environ.get("WDS_ENV_URL")
WDS_Env_Req = requests.post(WDS_Env_Url)
WDS_Env = (WDS_Env_Req.json())['result']

manifest_dir = './manifest'

# spine setting
spinePathIndex = -1
spineFolder = './spine'
spinemaster = json.load(open(os.path.join(manifest_dir, 'Spine.json'), 'rb'))
if not os.path.exists(spineFolder):
    os.makedirs(spineFolder)

# cards setting
# cardsPathIndex = -1
cardsFolder = './card'
if not os.path.exists(cardsFolder):
    os.makedirs(cardsFolder)

# background setting
bgPathIndex = -1
bgFolder = './background'
bgmaster = json.load(open(os.path.join(manifest_dir, 'Background.json'), 'rb'))
if not os.path.exists(bgFolder):
    os.makedirs(bgFolder)

# # load temp list
tempList = json.load(open(os.path.join('./_temp', 'Temp.json'), 'rb'))

# load catalog
catalog_json = json.load(open(os.path.join('./_temp', '2dcatalog.json'), 'rb'))

# get pathId from catalog
for index, value in enumerate(catalog_json['m_InternalIdPrefixes']):
    if value.endswith('adventurecharacterstand_assets_adventurecharacterstands'):
        spinePathIndex = index
    # elif value.endswith('charactercards_assets_charactercard'):
    #     cardsPathIndex = index
    elif value.endswith('adventurebackground_assets_adventurebackgrounds'):
        bgPathIndex = index


for asset in catalog_json['m_InternalIds']:

    # spine
    if asset.startswith(f'{spinePathIndex}#'):
        filename = asset.split('/')[-1]
        spineId = filename.split('.')[0]

        # check the spine data isexit
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
                        if spineId in tempList['spine']:
                            tempList['spine'].remove(spineId)
                        spinemaster.append({
                            "Id" : int(spineId),
                            "CharacterId" : int(spineId[0 : 3]),
                            "CompanyId" : int(spineId[0]),
                        })
            except:
                print(spineId)
        else:
            if spineId in tempList['spine']:
                tempList['spine'].remove(spineId)
    
    # backgorund
    if asset.startswith(f'{bgPathIndex}#'):
        filename = asset.split('/')[-1]
        bgId = filename.split('.')[0]

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
                                if bgId in tempList['background']:
                                    tempList['background'].remove(bgId)
            except:
                print(bgId)
        else:
            if bgId in tempList['background']:
                tempList['background'].remove(bgId)


# save spine list
spinemaster.sort(key = lambda x: x["Id"] )
json_data = json.dumps(spinemaster, indent=4, ensure_ascii=False)
open(os.path.join(manifest_dir, 'Spine.json'), "w", encoding='utf8').write(json_data)

# save background list
bgmaster.sort()
bg_json_data = json.dumps(bgmaster, indent=4, ensure_ascii=False)
open(os.path.join(manifest_dir, 'Background.json'), "w", encoding='utf8').write(bg_json_data)


# card
for cardId in tempList['card'][:]:
    try:
        fullurl = f'{WDS_Env["assetUrl"]}/2d-assets/Android/{WDS_Env["assetVersion"]}/charactercards_assets_charactercard/{cardId}.bundle'
        assetsReq = requests.get(fullurl)
        if assetsReq.status_code == 200:
            assetsbundle = UnityPy.load(assetsReq.content)
            for obj in assetsbundle.objects:
                if obj.type.name == "Sprite":
                    data = obj.read()
                    if data.name == cardId:
                        data.image.save(os.path.join(cardsFolder, f'{data.name}.png'))
                        # clear the id 
                        tempList['card'].remove(cardId)
    except:
        print(cardId)

############ save temp json
tempList_data = json.dumps(tempList, indent=4, ensure_ascii=False)
open(os.path.join('./_temp', 'Temp.json'), "w", encoding='utf8').write(tempList_data)