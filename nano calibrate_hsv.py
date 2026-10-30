import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cv2.namedWindow('HSV Calibration')

# Создаём слайдеры
cv2.createTrackbar('Lower H', 'HSV Calibration', 0, 180, nothing)
cv2.createTrackbar('Lower S', 'HSV Calibration', 20, 255, nothing)
cv2.createTrackbar('Lower V', 'HSV Calibration', 70, 255, nothing)
cv2.createTrackbar('Upper H', 'HSV Calibration', 20, 180, nothing)
cv2.createTrackbar('Upper S', 'HSV Calibration', 255, 255, nothing)
cv2.createTrackbar('Upper V', 'HSV Calibration', 255, 255, nothing)

print("Наведите руку в центр экрана и двигайте слайдеры пока рука не будет белой на маске.")
print("Нажмите 'q' для выхода и запомните значения.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Читаем значения слайдеров
    lh = cv2.getTrackbarPos('Lower H', 'HSV Calibration')
    ls = cv2.getTrackbarPos('Lower S', 'HSV Calibration')
    lv = cv2.getTrackbarPos('Lower V', 'HSV Calibration')
    uh = cv2.getTrackbarPos('Upper H', 'HSV Calibration')
    us = cv2.getTrackbarPos('Upper S', 'HSV Calibration')
    uv = cv2.getTrackbarPos('Upper V', 'HSV Calibration')
    
    lower_skin = np.array([lh, ls, lv])
    upper_skin = np.array([uh, us, uv])
    
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    cv2.putText(frame, f"L: {lh},{ls},{lv} U: {uh},{us},{uv}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Показываем исходный кадр и маску рядом
    combined = np.hstack([frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)])
    cv2.imshow('HSV Calibration', combined)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(f"\nИтоговые значения:")
        print(f"lower_skin = np.array([{lh}, {ls}, {lv}])")
        print(f"upper_skin = np.array([{uh}, {us}, {uv}])")
        break

cap.release()
cv2.destroyAllWindows()
