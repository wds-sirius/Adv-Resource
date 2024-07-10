import os
import shutil
from pydub import AudioSegment
import json

input_dir = '../_temp/voice_temp'
temp_dir = '../_temp/wav_voice_temp'
output_dir = '../voice'

#acb -> wav -> mp3
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
        mp3_output_dir = os.path.join(output_dir, story_id)
        if not os.path.exists(mp3_output_dir):
            os.makedirs(mp3_output_dir)

        # run command and save to temp dir
        os.system(f'./vgmstream-cli -S 0 -o {wav_temp_dir}/?n.wav -i {acb_full_path}')

        # manifest list
        manifest = []

        # exchange to mp3 format 
        for wavfile in os.listdir(wav_temp_dir):
            if wavfile.endswith(".wav"):
                full_wav_path = os.path.join(wav_temp_dir, wavfile)
                sound = AudioSegment.from_wav(full_wav_path)
                sound.export(os.path.join(mp3_output_dir, wavfile.replace('.wav', '.mp3')), format="mp3")
                # add file name in manifest list
                manifest.append(wavfile.split('.wav')[0])

        # save manifest list as json
        manifest_data = json.dumps(manifest, indent=4, ensure_ascii=False)
        open(os.path.join(mp3_output_dir,'manifest.json'), "w", encoding='utf8').write(manifest_data)

        # del file
        if os.path.exists(wav_temp_dir):
            shutil.rmtree(wav_temp_dir)
        
        
    # del input_dir
    shutil.rmtree(input_dir)

    # del temp_dir
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)