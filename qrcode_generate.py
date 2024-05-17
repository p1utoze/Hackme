from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
import cv2
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv


load_dotenv()
conn = create_engine("TO BE FILLED WITH DATABASE URL")

host_url = "https://hackme.hackaventus.com"
if os.environ["HOSTNAME_URL"]:
    host_url = os.environ["HOSTNAME_URL"]

# df = pd.read_csv("app/data/temp.csv")
# df.to_sql("participants", con=conn, if_exists="replace", index=False)
# with conn.connect() as connection:
#     query = text("SELECT * FROM participants")
#     result = connection.execute(query).fetchall()


def generate_qr(uid, name, host_url="http://127.0.0.1:5000", track=None):
    # name = name.split()
    # fname = name[0]
    q = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=5,
    )
    q.add_data(f"{host_url}/qr_scan/{uid}")
    q.make(fit=True)
    img = q.make_image(fill_color="black", back_color="white").convert("RGB")
    draw = ImageDraw.Draw(img)
    qr_width, qr_height = img.size
    font_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "assets",
        )
    )
    font_path = "assets/Lucidity-Expand.ttf"
    font = ImageFont.truetype(font=font_path, size=60)

    draw.text(
        (qr_width / 2, qr_height - (qr_height * 0.05)),
        "{0}".format(uid),
        font=font,
        anchor="mm",
        fill=(0, 0, 0, 1),
    )
    print(f"{uid}")
    img.save(f"qrcodes/{track}/{name}.png")


def fill_names(f_name, l_name, t_name):
    img = Image.open("Aventus 2.0 - ID Cards.jpg")
    width, height = img.size
    font_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "assets/mokoto-mokoto-regular-400.ttf",
        )
    )
    draw = ImageDraw.Draw(img)
    bxlen = 300
    tsize = cv2.getTextSize(t_name, cv2.FONT_HERSHEY_DUPLEX, 1, 2)
    print(tsize)
    if bxlen > tsize[0][0]:
        font = ImageFont.truetype(font=font_path, size=110 - 0.15 * tsize[1])
    else:
        font = ImageFont.truetype(font=font_path, size=110 + 0.55 * tsize[1])
    draw.text(
        ((width / 2), (height / 2) - (height * 0.12)),
        t_name,
        anchor="mm",
        font=font,
        fill=(216, 233, 168),
    )
    tsize = cv2.getTextSize(
        f_name + " " + l_name, cv2.FONT_HERSHEY_DUPLEX, 2, 3
    )
    bxlen = 550
    if tsize[0][0] > bxlen:
        font = ImageFont.truetype(font=font_path, size=110 - 0.1 * tsize[1])
        draw.text(
            ((width / 2), (height / 2) + (height * 0.37)),
            f"{f_name}",
            font=font,
            anchor="mm",
            fill=(216, 233, 168),
        )
        draw.text(
            ((width / 2), (height / 2) + (height * 0.42)),
            f"{l_name}",
            font=font,
            anchor="mm",
            fill=(216, 233, 168),
        )
    else:
        font = ImageFont.truetype(font=font_path, size=110 + 0.1 * tsize[1])
        draw.text(
            ((width / 2), (height / 2) + (height * 0.37)),
            f"{f_name} {l_name}",
            font=font,
            anchor="mm",
            fill=(216, 233, 168),
        )

    img.save(f"id_cards/{f_name} {l_name}.jpg")
    # img = cv2.imread("random.png")
    # height, width, depth = img.shape
    # desired_height = 512
    # aspect_ratio = desired_height / width
    # dimension = (desired_height, int(height * aspect_ratio))
    # img_resized = cv2.resize(img, dimension)
    # cv2.imshow("Resized", img_resized)
    # cv2.waitKey(0)


# THIS IS FOR THE QR CODES
df = pd.read_sql_table("participants", con=conn)
for track in df["track"].unique().tolist():
    data = df.loc[df.track == track, :]
    for uid, f_name, l_name in zip(
        data["member_id"], data["f_name"], data["l_name"]
    ):
        generate_qr(uid, " ".join([f_name, l_name]), host_url, track)


# THIS IS FOR THE ID CARDS
# for f_name, l_name, t_name in zip(df["f_name"], df["l_name"], df["team_name"]):
#     fill_names(f_name, l_name, t_name)
