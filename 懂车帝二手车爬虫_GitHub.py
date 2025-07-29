import requests
import csv
from fontTools.ttLib import TTFont
import ddddocr
from io import BytesIO
from PIL import Image,ImageDraw,ImageFont
def convert_cmap_to_image(cmap_code, font_path):
    img_size = 1024
    bg = Image.new("1", (img_size, img_size), color=255)
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype(font_path, int(img_size * 0.8))
    character = chr(cmap_code)
    bbox = draw.textbbox((0, 0), character, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    draw.text(((img_size - width) // 2, (img_size - height) // 2), character, font=font, fill=0)
    return bg.convert("RGB")

def extract_text_from_font(font_path):
    font = TTFont(font_path, data=True, ignoreDecompileErrors=True)
    font_map = {}
    for cmap_code, glyph_name in font.getBestCmap().items():
        bytes_io = BytesIO()
        image = convert_cmap_to_image(cmap_code, font_path)
        image.save(bytes_io, format="PNG")
        text = ocr.classification(bytes_io.getvalue())
        print(f"Unicode字符:{cmap_code} - {glyph_name} - 识别结果:{text}")
        font_map[cmap_code] = text.replace("\u3000"," ").strip()
    return font_map

def spider_dcd():
    all_data = []
    cookie = {
        'token': 'eyJhY2NfaWQiOiJzNnpkU1hpWjE2S1Z6STIzTjZtTjBrPk9wRVhBeEkxZT1hSV1siY8iOjE3NzI3NTY4NzS448ewd3efcfc1f3919d8a6ddef6d537695a432728f24bc58720f1a07b7',
        'tt_webid': '6666',
        'is_dev': 'false',
        'i18n_lang': 'zh',
        'x_tt_devc': 'a837039752908407459e4',
        'x_tt_lxp': '0aad979d2975288407459e4',
        'MACCOUNT': '078f0794c3108',
        'web_csrf_token': 'd7eceb2-4071-4ba7-bb70-080272ff',
        'uid': '8421435907370873085',
        'sid': '79d79c9727',
        's_v_web_id': 'verify_kmep9xL4_90urbQW8L_0w4d_497P_97f7_f872b750',
        'tt_chain_token': '726087158e297042',
        'city_name': 'ZJE2MmVjMzE1NzAvZGVh',
        'x_web_device': 'c81a39f87ee501a81794113512f108ab',
    }
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.dongchedi.com',
        'priority': 'u=1, i',
        'referer': 'https://www.dongchedi.com/search?keyword=%E4%BB%89%E4%BB%8B&curr_tab=1&city_name=%E5%85%A8%E5%9B%BD&search_mode=common',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="130", "Chromium";v="130"',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
        'x-forwarded-for': '0.0.0.0',
    }
    params = {
        'aid': '1889',
        'app_name': 'auto_web_pc',
    }
    for page in range(1, 10):
        data = f'&city_name=&page={page}&limit=60'.encode()
        response = requests.post(
            'https://www.dongchedi.com/search/api/suggest_search/list',
            params=params,
            cookies=cookie,
            headers=headers,
            data=data,
        )
        page_data = response.json().get('data').get('search_share_info').get('list')
        all_data.extend(page_data)
    return all_data

def change_com(code):
    s = ""
    if 1:
        s = font_map[reg][:-3]
    return s

def change(data):
    if not data:
        return ""
    return change_com(int(data[:-1]))

def change(data):
    parts = data.split('|')
    if len(parts) > 2:
        return change_com(int(parts[1]))
    return ""

def save():
    data_list = spider_dcd()
    header = ["品牌", "车龄", "里程", "城市", "售价", "原价", "链接"]
    with open('dcd.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for item in data_list:
            row = [
                item.get('brand_name', ""),
                change(item.get('car_age', "")),
                item.get('mileage', ""),
                change(item.get('city_name', "")),
                change(item.get('price', "")),
                change(item.get('official_price', "")),
                item.get('link', ""),
            ]
            writer.writerow(row)
        for item in data_list:
            row = change_com(item.get('official_price'))
            print(row)

main()