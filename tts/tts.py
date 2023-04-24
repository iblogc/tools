import os
import re
import fnmatch
import asyncio
import edge_tts

VOICE = 'zh-CN-XiaoxiaoNeural'

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TXT_PATH = os.path.join(CURRENT_DIR, 'txt')
OUT_PATH = os.path.join(CURRENT_DIR, 'out')
if not os.path.isdir(OUT_PATH):
    os.mkdir(OUT_PATH)
PATTERN = '0*.txt'
VOICE_RATE='+70%'



async def _main(txt) -> None:
    print(txt)
    f = open(txt, encoding='utf-8')
    lines = f.readlines()
    # 去掉第一行链接
    content = ''
    for line in lines[1:]:
        content += re.sub(r'^ *\d+.? *$', '', line)
    # content = ''.join(lines[1:])
    content = re.sub(r'[。！？……!?]', ',', content)
    print('总计约', len(content), '字')
    communicate = edge_tts.Communicate(content, VOICE, rate=VOICE_RATE)
    submaker = edge_tts.SubMaker()
    file_name_with_no_suffix = re.split(r'[\/]', txt)[-1].split('.')[0].replace('0-', '')
    # print(file_name_with_no_suffix)
    mp3_file = os.path.join(OUT_PATH, file_name_with_no_suffix + '.mp3')
    # vtt_sub_file = os.path.join(OUT_PATH, file_name_with_no_suffix + '.vtt')
    # srt_sub_file = os.path.join(OUT_PATH, file_name_with_no_suffix + '.srt')
    with open(mp3_file, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
        print('音频生成完成')

    # with open(vtt_sub_file, 'w', encoding="utf-8") as vtt_file:
    #     vtt_file.write(submaker.generate_subs())
    #     print('字幕生成完成')
    # vvt_2_srt(vtt_sub_file)
 
def vvt_2_srt(vvt_file):
    idx = 1  # 字幕序号
    srt_file = re.sub(r'\.vtt$', '.srt', vvt_file)
    with open(srt_file, 'w', encoding='utf-8') as srt:
        for line in open(vvt_file, encoding='utf-8'):
            if '-->' in line:
                srt.write("%d\n" % idx)
                idx += 1
                # 这行不是必须的，srt也能识别'.'
                line = line.replace('.', ',') 
            # 跳过header部分
            if idx > 1: 
                line
                srt.write(line)


if __name__ == "__main__":
    for root, dirs, files in os.walk(TXT_PATH):
        for filename in fnmatch.filter(files, PATTERN):
            file_path = os.path.join(root, filename)
            asyncio.run(_main(file_path))
            # os.rename(file_path , os.path.join(root, filename.replace('0-', '1-')))



