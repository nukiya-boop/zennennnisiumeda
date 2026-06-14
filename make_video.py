from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip, TextClip
from PIL import Image
import numpy as np
import os

IMG_DIR = "/home/user/zennennnisiumeda/images"
OUT = "/home/user/zennennnisiumeda/output.mp4"
W, H = 1080, 1920
DURATION = 3.5  # seconds per image
FADE = 0.5

# テロップ定義（画像順）
images_order = [
    "DSC00477.jpg",
    "DSC00732.jpg",
    "DSC00741.jpg",
    "DSC02075.jpg",
    "内部 (11).jpg",
    "1P3J1082.jpg",
    "1P3J1095.jpg",
    "西梅田QR文字入り.jpg",
]

captions = [
    "開放感あふれる\nオープンフロア",
    "ゆったりと寛げる\n贅沢な空間",
    "広々としたホールで\n特別なひとときを",
    "大切な方々と\n心ゆくまでお楽しみください",
    "少人数から大人数まで\n柔軟にご対応",
    "様々なシーンの会食に\nご利用いただけます",
    "上質な空間で\n忘れられない宴を",
    "ご予約・お問い合わせは\nこちらから",
]

def fit_image(path, w, h):
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    img = img.crop((left, top, left + w, top + h))
    return np.array(img)

clips = []
for fname, caption in zip(images_order, captions):
    path = os.path.join(IMG_DIR, fname)
    if not os.path.exists(path):
        print(f"Skip: {fname}")
        continue

    arr = fit_image(path, W, H)
    base = ImageClip(arr, duration=DURATION)

    txt = TextClip(
        text=caption,
        font_size=62,
        color="white",
        font="/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
        stroke_color="black",
        stroke_width=3,
        text_align="center",
        method="caption",
        size=(W - 80, None),
    ).with_position(("center", H - 340)).with_duration(DURATION)

    clip = CompositeVideoClip([base, txt])
    clip = clip.with_effects([__import__("moviepy").video.fx.FadeIn(FADE),
                               __import__("moviepy").video.fx.FadeOut(FADE)])
    clips.append(clip)

final = concatenate_videoclips(clips, method="compose")
final.write_videofile(OUT, fps=30, codec="libx264", audio=False,
                      ffmpeg_params=["-crf", "20"])
print("Done:", OUT)
