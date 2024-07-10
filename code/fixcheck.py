import json
import os


temp = {
    "temp": "temp"
} 

tempList_data = json.dumps(temp, indent=4, ensure_ascii=False)
open(os.path.join('./_temp', 'Test.json'), "w", encoding='utf8').write(tempList_data)
