import numpy as np
from PIL import Image

# ---- 내가 바꾸는 값 : 비교할 사진들 ----
PHOTOS = ["street.jpg", "cat.jpg", "dog.jpg", "desk.jpg", "fruit.jpg", "moto.jpg", "drone.jpg", "zoo.jpg"]

lo = 255
hi = 0

for name in PHOTOS:
    gray = np.array(Image.open(name).convert("L"))      # 흑백을 만들어주고 숫자표로 전환한다
    average = gray.mean()                               # 숫자표 전체의 평균 밝기 (0 ~ 255)
    print(f"{name:12s} 평균 밝기 {average:6.1f}  가장 어두운 픽셀 {gray.min():3d}  가장 밝은 픽셀 {gray.max():3d}")
            #문자12자      # 정수 6개, 소수점 아래 1자리까지           # 정수 3자

    # 과제 : 반복문으로 가장 작은 것, 가장 큰 것 알아보기
    if average < lo:  # 지금까지 본 것보다 더 작으면 최소를 바꾼다
        lo = average
    if average > hi:  # 지금까지 본 것보다 더 크면 최대를 바꾼다
        hi = average

print("밝기 범위 : 최소", lo, "최대", hi)


