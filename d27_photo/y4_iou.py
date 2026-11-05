from ultralytics import YOLO

# ---- 내가 바꾸는 값 ----
PHOTO = "moto.jpg"
CONF = 0.1
IOU = 0.95

model = YOLO("yolo26n.pt")
results = model(PHOTO, conf=CONF, iou=IOU)
result = results[0]


print("겹침 기준", IOU, "→ 찾은 물체의 개수 :", len(result.boxes))

# ------- [물체 종류별 개수 출력 v1] -------

# obj_cnts = {}                                  # 검출된 물체의 종류별 숫자를 담을 딕셔너리

# for box in result.boxes:
#     name = result.names[int(box.cls[0])]        # 이름 번호(정수)를 이름 목록에서 찾아 글자로 바꾼다
#     confidence = float(box.conf[0])             # 이 네모의 자신감 (0 ~ 1 사이 소수)
#     print("   ", name, round(confidence, 2))    # 이름과 자신감을 소수 둘째 자리까지 쓴다
#
#     if name in obj_cnts:
#         obj_cnts[name] += 1                 # 딕셔너리에 이름이 있으면 숫자를 더하고
#     else:
#         obj_cnts[name] = 1                  # 이름이 없으면 추가한다.
#
# for name,count in obj_cnts.items():
#     print(f"{name}:{count}개")


# ------- [물체 종류별 개수 출력 v2] -------

names_list = [result.names[int(box.cls[0])] for box in result.boxes]
                                                   # 모든 박스의 이름들을 리스트로 추출

for box in result.boxes:
    name = result.names[int(box.cls[0])]
    confidence = float(box.conf[0])
    print("   ", name, round(confidence, 2))

object_counts = Counter(names_list)                # Counter를 이용해 개수 세기

for name, count in object_counts.items():
    print(f"   {name}: {count}개")


result.save("yolo_iou_95.jpg")
print("yolo_iou.jpg 로 저장했다")
