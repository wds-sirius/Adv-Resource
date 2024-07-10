import os
import requests
import shutil
import json
from pydub import AudioSegment

WDS_Env_Url = os.environ.get("WDS_ENV_URL")
WDS_Env_Req = requests.post(WDS_Env_Url)
WDS_Env = (WDS_Env_Req.json())['result']

manifest_dir = '../manifest'

# bgm dir
bgm_temp_dir = '../_temp/bgm_temp'
bgm_dir = './bgm'
bgm_temp_wav_dir = '../_temp/bgm_wav_temp'
bgmmaster = json.load(open(os.path.join(manifest_dir, 'BGM.json'), 'rb'))
if not os.path.exists(bgm_temp_dir):
    os.makedirs(bgm_temp_dir)

#se dir
se_temp_dir = '../_temp/se_temp'
se_dir = './se'
se_temp_wav_dir = '../_temp/se_wav_temp'
semaster = json.load(open(os.path.join(manifest_dir, 'SE.json'), 'rb'))
if not os.path.exists(se_temp_dir):
    os.makedirs(se_temp_dir)

#acb -> wav -> mp3
def acbToMp3(input_dir, temp_dir, output_dir):
    if os.path.exists(input_dir):

        for fname in os.listdir(input_dir):

            acb_full_path = os.path.join(input_dir, fname)

            # 生成wav的位置
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # 生成mp3的位置
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # run command and save to temp dir
            os.system(f'./vgmstream-cli -S 0 -o {temp_dir}/?n.wav -i {acb_full_path}')

            # exchange to mp3 format 
            for wavfile in os.listdir(temp_dir):
                if wavfile.endswith(".wav"):
                    full_wav_path = os.path.join(temp_dir, wavfile)
                    sound = AudioSegment.from_wav(full_wav_path)
                    sound.export(os.path.join(output_dir, wavfile.replace('.wav', '.mp3')), format="mp3")
            
            # del temp file
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        
        # del file
        if os.path.exists(input_dir):
            shutil.rmtree(input_dir)


# load temp list
templist = json.load(open(os.path.join('../_temp', 'Temp.json'), 'rb'))

############# SE
notExist = [se for se in templist['se'] if se not in semaster]
if len(notExist) > 0:
    voiceRes = requests.get(f'{WDS_Env["assetUrl"]}/cri-assets/Android/{WDS_Env["assetVersion"]}/cridata_remote_assets_criaddressables/adventurese.acb.bundle')
    if voiceRes.status_code == 200:
        open(os.path.join(se_temp_dir, 'adventurese.acb'), "wb").write(voiceRes.content)

############# BGM
for bgmId in templist['bgm'][:]:
    if not bgmId in bgmmaster:
        voiceRes = requests.get(f'{WDS_Env["assetUrl"]}/cri-assets/Android/{WDS_Env["assetVersion"]}/cridata_remote_assets_criaddressables/adventure_{bgmId}.acb.bundle')
        if voiceRes.status_code == 200:
            open(os.path.join(bgm_temp_dir, f'adventure_{bgmId}.acb'), "wb").write(voiceRes.content)
    else:
        templist['bgm'].remove(bgmId)

######## convert
# bgm
acbToMp3(bgm_temp_dir, bgm_temp_wav_dir, bgm_dir)
for mp3file in os.listdir(bgm_dir):
    if mp3file.endswith("mp3"):
        bgmmaster.append(mp3file.split('.mp3')[0])
bgm_data = json.dumps(bgmmaster, indent=4, ensure_ascii=False)
open(os.path.join(manifest_dir, 'BGM.json'), "w", encoding='utf8').write(bgm_data)

# se 
acbToMp3(se_temp_dir, se_temp_wav_dir, se_dir)
semaster = []
for mp3file in os.listdir(se_dir):
    if mp3file.endswith("mp3"):
        semaster.append(mp3file.split('.mp3')[0])
templist['se'] = [se for se in templist['se'] if se not in semaster]
se_data = json.dumps(semaster, indent=4, ensure_ascii=False)
open(os.path.join(manifest_dir, 'SE.json'), "w", encoding='utf8').write(se_data)

############ save temp json
tempList_data = json.dumps(templist, indent=4, ensure_ascii=False)
open(os.path.join('../_temp', 'Temp.json'), "w", encoding='utf8').write(tempList_data)