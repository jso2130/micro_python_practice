import numpy as np
from PIL import Image

# ---- 내가 바꾸는 값 ----
PHOTOS = ["street.jpg", "cat.jpg", "dog.jpg", "desk.jpg", "fruit.jpg", "moto.jpg", "drone.jpg", "zoo.jpg"]
LINE = 120                                              # 밝기 기준 (0 ~ 255 사이에서 고른다)

for name in PHOTOS:                                     # 사진 리스트에서 사진을 하나씩 꺼낸다.
    gray = np.array(Image.open(name).convert("L"))      # 사진을 흑백 숫자표로 바꾼다
    average = gray.mean()                               # 모든 픽셀의 평균 밝기 (0 ~ 255)
    if average > LINE:                                  # 평균이 정한 기준(LINE)보다 크면
        print(name, "평균 밝기", round(average, 1), "→ 밝은 사진")
    else:
        print(name, "평균 밝기", round(average, 1), "→ 어두운 사진")
