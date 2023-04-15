# import requests
# import json

# url = 'http://t.weather.sojson.com/api/weather/city/101030100'
# response = requests.get(url)

# if response.status_code == 200:
#     data = json.loads(response.text)
#     city = data['cityInfo']['city']
#     temperature = data['data']['wendu']
#     print(f"城市：{city}，温度：{temperature}℃")
# else:
#     print("请求失败")
# Is6iZUs66dVQKHUMToaxN6eEnzy1apI8VLZbGHHP3Q8=

# aiohttp==3.8.4
# aiosignal==1.3.1
# async-timeout==4.0.2
# attrs==22.2.0
# certifi==2022.12.7
# charset-normalizer==3.1.0
# edge-tts==6.1.3
# frozenlist==1.3.3
# idna==3.4
# multidict==6.0.4
# requests==2.28.2
# urllib3==1.26.15
# yapf==0.32.0
# yarl==1.8.2
import sys
sys.path.append('D:\Program Files\Tesseract-OCR')
print(sys.path)
import requests
import pytesseract
from PIL import Image
import io

url = 'https://hplus-sandbox-3.healthcareyun.com/hplus/platform/auth/captcha'

# 发送 GET 请求，获取验证码图片
response = requests.get(url, stream=True)

# 使用 Pillow 库打开图片
image = Image.open(io.BytesIO(response.content))

# 识别验证码
captcha = pytesseract.image_to_string(image).strip()
print("验证码为：", captcha)




# import requests

# url = 'http://t.weather.sojson.com/api/weather/city/101030100'

# # 发送 GET 请求，获取天气信息
# response = requests.get(url)

# # 提取城市、温度、PM25 值
# if response.status_code == 200:
#     data = response.json()
#     city = data['cityInfo']['city']
#     wendu = data['data']['wendu']
#     pm25 = data['data']['pm25']
#     print("城市：{}".format(city))
#     print("温度：{}℃".format(wendu))
#     print("PM25：{}".format(pm25))
# else:
#     print("请求失败")

# # 提取未来 3 天的温度信息
# if response.status_code == 200:
#     data = response.json()
#     forecast = data['data']['forecast']
#     for i in range(3):
#         date = forecast[i]['date']
#         high = forecast[i]['high']
#         low = forecast[i]['low']
#         print("{}：{} ~ {}".format(date, low, high))
# else:
#     print("请求失败")