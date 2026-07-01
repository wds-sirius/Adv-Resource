import json
import requests
import os
import struct
import shutil
from pydub import AudioSegment

def packEpisodeVoice(input_folder, output_package_path):
    valid_extensions = ('.ogg', '.mp3', '.wav')
    audio_files = [f for f in os.listdir(input_folder) if f.endswith(valid_extensions)]
    audio_files.sort()

    index_table = {}
    current_offset = 0
    audio_bytes_list = []

    for file_name in audio_files:
        file_path = os.path.join(input_folder, file_name)
        with open(file_path, 'rb') as f:
            audio_data = f.read()
            
        data_length = len(audio_data)
        cue_name = os.path.splitext(file_name)[0]
        
        index_table[cue_name] = {
            "offset": current_offset,
            "length": data_length
        }
        
        audio_bytes_list.append(audio_data)
        current_offset += data_length
        
        padding_needed = (4 - (data_length % 4)) % 4
        if padding_needed > 0:
            audio_bytes_list.append(b'\x00' * padding_needed)
            current_offset += padding_needed

    json_bytes = json.dumps(index_table, ensure_ascii=False).encode('utf-8')
    json_length = len(json_bytes)

    with open(output_package_path, 'wb') as f:
        f.write(struct.pack('<I', json_length)) 
        
        f.write(json_bytes)
        
        for audio_data in audio_bytes_list:
            f.write(audio_data)

    print(f"資產包: {output_package_path}")


# Download acb File
WDS_Env_Url = os.environ.get("WDS_ENV_URL")
WDS_Env_Req = requests.post(WDS_Env_Url)
WDS_Env = (WDS_Env_Req.json())['result']

dl_temp_dir = './_temp/voice_temp'
if not os.path.exists(dl_temp_dir):
    os.makedirs(dl_temp_dir)

rePackEPList = json.load(open(os.path.join('./_temp', 'repack.json'), 'r'))
for EP in rePackEPList:
    voiceRes = requests.get(f'{WDS_Env["assetUrl"]}/cri-assets/Android/{WDS_Env["assetVersion"]}/cridata_remote_assets_criaddressables/{EP}.acb.bundle')
    if voiceRes.status_code == 200:
        open(os.path.join(dl_temp_dir, f'{EP}.acb'), "wb").write(voiceRes.content)


# rePack
input_dir = './_temp/voice_temp'
temp_dir = './_temp/wav_voice_temp'
temp2_dir = './_temp/mp3_voice_temp'
output_dir = './voice'

if os.path.exists(input_dir):
    for fname in os.listdir(input_dir):
        acb_full_path = os.path.join(input_dir, fname)

        # get story id
        story_id = fname.split('.acb')[0]

        # 生成wav的位置
        wav_temp_dir = os.path.join(temp_dir, story_id)
        if not os.path.exists(wav_temp_dir):
            os.makedirs(wav_temp_dir)
        
        # 生成mp3的位置
        mp3_temp_dir = os.path.join(temp2_dir, story_id)
        if not os.path.exists(mp3_temp_dir):
            os.makedirs(mp3_temp_dir)

        # run the command to export wav and save it to wav temp dir
        os.system(f'./code/vgmstream-cli -S 0 -o {wav_temp_dir}/?n.wav -i {acb_full_path}')

        for wavfile in os.listdir(wav_temp_dir):
            if wavfile.endswith(".wav"):
                full_wav_path = os.path.join(wav_temp_dir, wavfile)
                sound = AudioSegment.from_wav(full_wav_path)
                mono_sound = sound.set_channels(1)
                mono_sound.export(os.path.join(mp3_temp_dir, wavfile.replace('.wav', '.mp3')), format="mp3", codec="libmp3lame", bitrate="64k", parameters=["-ar", "48000"])

        packEpisodeVoice(mp3_temp_dir, os.path.join(output_dir, f'{story_id}.wds'))

        # del folder
        if os.path.exists(wav_temp_dir):
            shutil.rmtree(wav_temp_dir)
        
        if os.path.exists(mp3_temp_dir):
            shutil.rmtree(mp3_temp_dir)

        old_dir = os.path.join(output_dir, story_id)
        if os.path.exists(old_dir):
            shutil.rmtree(old_dir)
        

    # del input_dir
    shutil.rmtree(input_dir)

    # del temp_dir
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)