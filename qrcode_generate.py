from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

import pandas as pd
from dotenv import load_dotenv

df = pd.read_csv("app/data/Final_List.csv")
load_dotenv()

host_url = "http://127.0.0.1:5000"
if os.environ["HOSTNAME_URL"]:
    host_url = os.environ["HOSTNAME_URL"]


def generate_qr(uid, fname, host_url="http://127.0.0.1:5000"):
    name = fname.split()
    fname = name[0]
    q = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=3,
        border=5,
    )
    q.add_data(f"{host_url}/qr_scan/{uid}")
    q.make(fit=True)
    img = q.make_image(fill_color="black", back_color="white").convert("RGB")
    Image.open("../../Pictures/juice wrld/DoggoWRLD.jpeg")
    draw = ImageDraw.Draw(img)
    qr_width, qr_height = img.size
    font_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "app/static/Michroma/Michroma-Regular.ttf",
        )
    )
    font = ImageFont.truetype(font=font_path, size=9)

    draw.text(
        (qr_width - (qr_width * 0.875), qr_height - (qr_height * 0.10)),
        "{0}  {1}".format(uid, fname),
        font=font,
        fill=(0, 0, 0, 1),
    )
    print(f"{uid}")
    img.save(f"qrcodes/{uid}.png")


for uid, fname in zip(df["UID"].to_list(), df["firstName"].to_list()):
    generate_qr(uid, fname, host_url)
