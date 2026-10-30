from PIL import Image

# ---- 내가 바꾸는 값 ----
PHOTO = "cat.jpg"
N = 5                           # 가로 N 픽셀 × 세로 N 픽셀을 한 칸으로 합친다 (클수록 거칠다)

img = Image.open(PHOTO)
small = img.resize((img.width // N, img.height // N))          # 픽셀의 개수를 1/N으로 줄인다
print("줄인 크기", small.width, "x", small.height, "= 픽셀", small.width * small.height, "개 (원래", img.width * img.height, "개)")
big = small.resize(img.size, Image.NEAREST)                    # 같은 크기로 다시 키운다. NEAREST = 가장 가까운 칸의 숫자를 그대로 쓴다 (네모 칸이 보인다)
big.save("mosaic.jpg")
print("mosaic.jpg 로 저장했다")
big.show()
