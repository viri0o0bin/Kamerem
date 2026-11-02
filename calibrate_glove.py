import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cv2.namedWindow('Glove Calibration')

cv2.createTrackbar('Lower H', 'Glove Calibration', 0, 180, nothing)
cv2.createTrackbar('Lower S', 'Glove Calibration', 0, 255, nothing)
cv2.createTrackbar('Lower V', 'Glove Calibration', 0, 255, nothing)
cv2.createTrackbar('Upper H', 'Glove Calibration', 180, 180, nothing)
cv2.createTrackbar('Upper S', 'Glove Calibration', 255, 255, nothing)
cv2.createTrackbar('Upper V', 'Glove Calibration', 100, 255, nothing)

print("Наведите перчатку в центр экрана и двигайте слайдеры.")
print("Перчатка должна быть БЕЛОЙ на маске справа. Нажмите 'q' для выхода.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lh = cv2.getTrackbarPos('Lower H', 'Glove Calibration')
    ls = cv2.getTrackbarPos('Lower S', 'Glove Calibration')
    lv = cv2.getTrackbarPos('Lower V', 'Glove Calibration')
    uh = cv2.getTrackbarPos('Upper H', 'Glove Calibration')
    us = cv2.getTrackbarPos('Upper S', 'Glove Calibration')
    uv = cv2.getTrackbarPos('Upper V', 'Glove Calibration')
    
    lower = np.array([lh, ls, lv])
    upper = np.array([uh, us, uv])
    
    mask = cv2.inRange(hsv, lower, upper)
    
    cv2.putText(frame, f"L: {lh},{ls},{lv} U: {uh},{us},{uv}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    combined = np.hstack([frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)])
    cv2.imshow('Glove Calibration', combined)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(f"\nИтоговые значения:")
        print(f"lower_glove = np.array([{lh}, {ls}, {lv}])")
        print(f"upper_glove = np.array([{uh}, {us}, {uv}])")
        break

cap.release()
cv2.destroyAllWindows()
