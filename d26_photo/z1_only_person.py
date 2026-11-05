from ultralytics import YOLO

# ---- 내가 바꾸는 값 ----
PHOTO = "street.jpg"
CONF = 0.25
ONLY = [0]                              # 0 = person (사람), 24 = backpack, 26 = handbag

model = YOLO("yolo26n.pt")
results = model(PHOTO, conf=CONF, classes=ONLY)     # 'ONLY' 물체만 가져온다
result = results[0]                                 # 답 묶음의 0번째 = 사진 한 장에 대한 답

print("번호", ONLY, "만 그렸다 → 남은 네모 :", len(result.boxes), "개")
result.save("yolo_only.jpg")
print("yolo_only.jpg 로 저장했다")
