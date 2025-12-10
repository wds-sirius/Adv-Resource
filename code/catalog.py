import json
import requests
import os

WDS_Env_Url = os.environ.get("WDS_ENV_URL")
WDS_Env_Req = requests.post(WDS_Env_Url)
WDS_Env = (WDS_Env_Req.json())['result']

templist = json.load(open(os.path.join('./_temp', 'Temp.json'), 'rb'))
catalog_2d_hash = templist['2dhash']
catalog_cri_hash = templist['crihash']

# 獲取新的hash
new_catalog_2d_hash = requests.get(f'{WDS_Env["assetUrl"]}/2d-assets/Android/{WDS_Env["assetVersion"]}/catalog_{WDS_Env["assetVersion"]}.hash').text
new_catalog_cri_hash = requests.get(f'{WDS_Env["assetUrl"]}/cri-assets/Android/{WDS_Env["assetVersion"]}/catalog_{WDS_Env["assetVersion"]}.hash').text

# 如果有新的就更新(2d-assets)
if catalog_2d_hash != new_catalog_2d_hash:
    templist['2dhash'] = new_catalog_2d_hash
    catalog2d_data_raw = requests.get(f'{WDS_Env["assetUrl"]}/2d-assets/Android/{WDS_Env["assetVersion"]}/catalog_{WDS_Env["assetVersion"]}.json')
    catalog2d_data = catalog2d_data_raw.json()
    catalog2d_json = {
        'm_InternalIds' : catalog2d_data['m_InternalIds'],
        'm_InternalIdPrefixes' : catalog2d_data['m_InternalIdPrefixes'],
    }
    open(os.path.join('./_temp', '2dcatalog.json'), "w", encoding='utf8').write(json.dumps(catalog2d_json, indent=4, ensure_ascii=False))
    pass

# 如果有新的就更新(cri-assets)
if catalog_cri_hash != new_catalog_cri_hash:
    templist['crihash'] = new_catalog_cri_hash
    catalogcri_data_raw = requests.get(f'{WDS_Env["assetUrl"]}/cri-assets/Android/{WDS_Env["assetVersion"]}/catalog_{WDS_Env["assetVersion"]}.json')
    catalogcri_data = catalogcri_data_raw.json()
    catalogcri_json = {
        'm_InternalIds' : catalogcri_data['m_InternalIds'],
        'm_InternalIdPrefixes' : catalogcri_data['m_InternalIdPrefixes'],
    }
    open(os.path.join('./_temp', 'cricatalog.json'), "w", encoding='utf8').write(json.dumps(catalogcri_json, indent=4, ensure_ascii=False))
    pass

tempList_data = json.dumps(templist, indent=4, ensure_ascii=False)
open(os.path.join('./_temp', 'Temp.json'), "w", encoding='utf8').write(tempList_data)