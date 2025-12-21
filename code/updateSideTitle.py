import json
import os

# folder paths
EPBase_dir = './episode'

sideTempList = json.load(open(os.path.join('./_temp', 'SideTitleTemp.json'), 'rb'))

for sideData in sideTempList:
    if sideData["Title"] != "":
        jsonData = json.load(open(os.path.join(EPBase_dir, f'{sideData["Id"]}.json'), 'rb'))
        jsonData["Chapter"] = sideData["CardName"]
        jsonData["Title"] = sideData["Title"]
        out_json_data = json.dumps(jsonData, indent=4, ensure_ascii=False)
        open(os.path.join(EPBase_dir, f'{sideData["Id"]}.json'), "w", encoding='utf8').write(out_json_data)