import json
import requests
import os
import UnityPy

WDS_Env_Url = os.environ.get("WDS_ENV_URL")
WDS_Env_Req = requests.post(WDS_Env_Url)
WDS_Env = (WDS_Env_Req.json())['result']

masterlistUrl = os.environ.get("WDS_MASTERLIST_URL")

eventImage_dir = './image/eventLogo'
eventBanner_dir = './image/eventBanner'
sideImage_dir = './image/cardIcon'
posterImage_dir = './image/posterIcon'

if not os.path.exists(sideImage_dir):
    os.makedirs(sideImage_dir)

if not os.path.exists(eventImage_dir):
    os.makedirs(eventImage_dir)

if not os.path.exists(posterImage_dir):
    os.makedirs(posterImage_dir)

# 更新event照片
StoryEvent = requests.get(f'{masterlistUrl}/StoryEventMaster.json')
if StoryEvent.status_code == 200:
    for story in StoryEvent.json():
        try:
            assetsReq = requests.get(f'{WDS_Env["assetUrl"]}/2d-assets/Android/{WDS_Env["assetVersion"]}/eventslogo_assets_events/logo_{story["Id"]}.bundle')
            assetsbundle = UnityPy.load(assetsReq.content)
            for obj in assetsbundle.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()
                    data.image.save(os.path.join(eventImage_dir, f'logo_{story["Id"]}.png'))
        except:
            print(story["Id"])
# 更新event Banner照片
        try:
            bannerReq = requests.get(f'{WDS_Env["assetUrl"]}/static-assets/Resources/Textures/Banners/Event/{story["Id"]}.png')
            if bannerReq.status_code == 200:
                open(os.path.join(eventBanner_dir, f'{story["Id"]}.png'), "wb").write(bannerReq.content)
        except:
            print(story["Id"])

# 更新roulette event照片
StoryEvent = requests.get(f'{masterlistUrl}/RouletteEventMaster.json')
if StoryEvent.status_code == 200:
    for story in StoryEvent.json():
        try:
            assetsReq = requests.get(f'{WDS_Env["assetUrl"]}/2d-assets/Android/{WDS_Env["assetVersion"]}/eventslogo_assets_events/logo_{story["Id"]}.bundle')
            assetsbundle = UnityPy.load(assetsReq.content)
            for obj in assetsbundle.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()
                    data.image.save(os.path.join(eventImage_dir, f'logo_{story["Id"]}.png'))
        except:
            print(story["Id"])
# 更新roulette event Banner照片
        try:
            bannerReq = requests.get(f'{WDS_Env["assetUrl"]}/static-assets/Resources/Textures/Banners/Event/{story["Id"]}.png')
            if bannerReq.status_code == 200:
                open(os.path.join(eventBanner_dir, f'{story["Id"]}.png'), "wb").write(bannerReq.content)
        except:
            print(story["Id"])

# 更新卡片照片
try:
    assetsReq = requests.get(f'{WDS_Env["assetUrl"]}/2d-assets/Android/{WDS_Env["assetVersion"]}/spriteatlases_assets_spriteatlases/characters.bundle')
    assetsbundle = UnityPy.load(assetsReq.content)
    for obj in assetsbundle.objects:
        if obj.type.name == "Sprite":
            data = obj.read()
            data.image.save(os.path.join(sideImage_dir, f'{data.name}.png'))
except:
    print('Side images error')

# 更新Poster照片
try:
    assetsReq = requests.get(f'{WDS_Env["assetUrl"]}/2d-assets/Android/{WDS_Env["assetVersion"]}/spriteatlases_assets_spriteatlases/posters.bundle')
    assetsbundle = UnityPy.load(assetsReq.content)
    for obj in assetsbundle.objects:
        if obj.type.name == "Sprite":
            data = obj.read()
            data.image.save(os.path.join(posterImage_dir, f'{data.name}.png'))
except:
    print('Poster images error')