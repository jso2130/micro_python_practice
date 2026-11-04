from ultralytics import YOLO

# ---- 내가 바꾸는 값 ----
PHOTO = "street.jpg"
CONF = 0.2                              # 물체 판단하는 신뢰도 최솟값 (0 ~ 1 사이)

model = YOLO("yolo26n.pt")              # 가장 작은 YOLO 파일을 불러와 model 이라는 이름을 붙인다
results = model(PHOTO, conf=CONF)       # conf는 위에서 정한 CONF 값으로 적용한다
result = results[0]                     # 가장 신뢰도가 높은 것을 가져옴

print("자신감 기준", CONF, "→ 찾은 물체의 개수 :", len(result.boxes))

for box in result.boxes:
    name = result.names[int(box.cls[0])]        # 결과에 맞는 이름을 목록(Tensor)에서 가져온다
    confidence = float(box.conf[0])
    print("   ", name, round(confidence, 2))    # 확률값은 소숫점 2자리까지

result.save("yolo_conf.jpg")
print("yolo_conf.jpg 로 저장했다")
