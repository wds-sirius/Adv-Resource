import requests
import json
import os

WDS_Env_Url = os.environ.get("WDS_ENV_URL")
WDS_Env_Req = requests.post(WDS_Env_Url)
WDS_Env = (WDS_Env_Req.json())['result']

masterlistUrl = os.environ.get("WDS_MASTERLIST_URL")

out_json = []

comicFolder = '../comic/'
if not os.path.exists(comicFolder):
    os.makedirs(comicFolder)

comic_master = requests.get(f'{masterlistUrl}/ComicMaster.json')
if comic_master.status_code == 200:
    comic_data = comic_master.json()

    for comiclist in comic_data:
        id = (comiclist['Id'] - 1) * 10
        for comic in comiclist['Episodes']:
            try:
                epid = id + comic['Order']
                filename = comic["Body"].split("\"")[5]
                assetsReq = requests.get(f'{WDS_Env["assetUrl"]}/static-assets/Resources/Textures/Comic/{filename}.png')
                if assetsReq.status_code == 200:
                    open(os.path.join(comicFolder, f'{filename}.png'), "wb").write(assetsReq.content)
                    out_json.append({"id": epid, "title": comic['Title'], "filename": filename})
            except:
                print(epid)
  
    out_json.sort(key = lambda x: x["id"] )
    with open('../manifest/Comic.json', 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=4)