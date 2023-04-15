import os
import re
import fnmatch
import asyncio
import edge_tts

VOICE = 'zh-CN-XiaoxiaoNeural'
TXT_PATH = 'txt'
OUT_PATH = 'out'

# 文件夹路径
PATTERN = '0*.txt'


async def _main(txt) -> None:
    print(txt)
    f = open(txt, encoding='utf-8')
    lines = f.read()
    lines = re.sub(r'[。！？……]', ',', lines)
    print('总计约', len(lines), '字')
    communicate = edge_tts.Communicate(lines, VOICE, rate='+70%')
    submaker = edge_tts.SubMaker()
    file_name_with_no_suffix = txt.split('\\')[-1].split('.')[0].replace('0-', '')
    print(file_name_with_no_suffix)
    mp3_file = os.path.join(OUT_PATH, file_name_with_no_suffix + '.mp3')
    sub_file = os.path.join(OUT_PATH, file_name_with_no_suffix + '.vtt')
    with open(mp3_file, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
        print('音频生成完成')

    with open(sub_file, "w", encoding="utf-8") as file:
        file.write(submaker.generate_subs())
        print('字幕生成完成')



if __name__ == "__main__":
    for root, dirs, files in os.walk(TXT_PATH):
        for filename in fnmatch.filter(files, PATTERN):
            file_path = os.path.join(root, filename)
            asyncio.run(_main(file_path))
            os.rename(file_path , os.path.join(root, filename.replace('0-', '1-')))



