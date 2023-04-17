import pysrt

# 读取SRT字幕文件
srt_file = 'tts\out\绝世娇媚.srt'
subs = pysrt.open(srt_file)

# 定义一个时间间隔阈值
time_threshold = 500  # 毫秒

# 遍历所有字幕对象，并将时间间隔小于指定阈值的相邻字幕对象合并为一个字幕对象
merged_subs = [subs[0]]
for i in range(1, len(subs)):
    prev_sub = merged_subs[-1]
    curr_sub = subs[i]
    if curr_sub.start - prev_sub.end <= time_threshold:
        prev_sub.text += '\n' + curr_sub.text
        prev_sub.end = curr_sub.end
    else:
        merged_subs.append(curr_sub)
    print(curr_sub)
print(merged_subs)
# 将合并后的字幕对象列表保存为SRT字幕文件
subrip = pysrt.SubRipFile(merged_subs)
subrip.save('merged_subtitle.srt', encoding='utf-8')