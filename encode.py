import math
import platform
import subprocess
import sys

from moviepy.editor import VideoFileClip, ImageClip, concatenate
from emojEncode import emojencoder
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm


def encode(video_filename):
    original_clip = VideoFileClip(video_filename)

    colors, emojis = emojencoder.read_emoji_file(path='emojEncode/emojiGamutPartitioned.json')
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X=colors, y=np.arange(len(colors)))

    downscaled_height = 60
    if platform.system() == 'Darwin':
        upscale_factor = 24
    elif platform.system() == 'Windows' or ('Linux' in platform.platform() and 'microsoft' in platform.platform()):
        upscale_factor = 8
    else:
        print('sorry linux users, you\'ll have to wait for the year of linux on the desktop')
        sys.exit(1)


    texts = []
    print('emojifying images')
    for frame in tqdm(original_clip.iter_frames(), total=int(original_clip.duration * original_clip.fps)):
      image = Image.fromarray(frame)
      width, height = image.size
      aspect_ratio = width / height
      
      downscaled_width = math.floor(downscaled_height * aspect_ratio)
      
      resized = image.resize((downscaled_width, downscaled_height))
      color_corrected = np.asarray(resized)[:, :, ::-1]  # least awful way to convert BGR to RGB
      texts.append(emojencoder.convertImage(knn, emojis, color_corrected))


    if platform.system() == 'Darwin':
        font = ImageFont.truetype('/System/Library/Fonts/Apple Color Emoji.ttc', size=20)
    elif platform.system() == 'Windows':
        font = ImageFont.truetype('c:/windows/fonts/seguiemj.ttf', size=5)
    elif 'Linux' in platform.platform() and 'microsoft' in platform.platform():
        font = ImageFont.truetype('/mnt/c/windows/fonts/seguiemj.ttf', size=5)

    images = []
    print('imagizing emojis')
    for i, text in tqdm(enumerate(texts), total=len(texts)):
        
        image = Image.new('RGB', (downscaled_width * upscale_factor, downscaled_height * upscale_factor))
        drawer = ImageDraw.Draw(image)
        drawer.text((0, 0), text, font=font, embedded_color=True)
        images.append(ImageClip(np.asarray(image), duration=1 / original_clip.fps))

    emoji_clip = concatenate(images)
    emoji_clip = emoji_clip.set_audio(original_clip.audio)
    emoji_clip.write_videofile('emoji_' + video_filename, fps=original_clip.fps)


if __name__ == '__main__':
    encode(sys.argv[1])
