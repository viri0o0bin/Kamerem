import cv2
import numpy as np
import pyautogui
import time

pyautogui.FAILSAFE = False

# HSV для ЧЁРНОЙ перчатки
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 50])  # Низкая яркость = чёрный

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

screen_width, screen_height = pyautogui.size()

last_click_time = 0
click_cooldown = 0.3

print("Программа запущена. Используется чёрная перчатка. Нажмите 'q' для выхода.")
print(f"Разрешение экрана: {screen_width}x{screen_height}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Ошибка: не удалось захватить кадр")
        break
    
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Маска для чёрного цвета
    mask = cv2.inRange(hsv, lower_black, upper_black)
    
    # Морфологические операции
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Находим контуры
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Самый большой контур
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        
        if area > 500:
            # Центроид
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Переводим в координаты экрана
                screen_x = int((cx / 640) * screen_width)
                screen_y = int((cy / 480) * screen_height)
                
                # Движение мышки
                pyautogui.moveTo(screen_x, screen_y, duration=0.05)
                
                # Рисуем центроид
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                cv2.drawContours(frame, [largest_contour], 0, (0, 255, 0), 2)
                
                # Поиск пальцев
                hull = cv2.convexHull(largest_contour)
                defects = cv2.convexityDefects(largest_contour, cv2.convexHull(largest_contour, returnPoints=False))
                
                fingers = []
                if defects is not None:
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        far = tuple(largest_contour[f][0])
                        cv2.circle(frame, far, 5, (0, 0, 255), -1)
                        fingers.append(far)
                
                # Клик при близких пальцах
                if len(fingers) >= 2:
                    distances = [(np.sqrt((f[0]-cx)**2 + (f[1]-cy)**2), f) for f in fingers]
                    distances.sort()
                    
                    if len(distances) >= 2:
                        dist = np.sqrt((distances[0][1][0] - distances[1][1][0])**2 + 
                                     (distances[0][1][1] - distances[1][1][1])**2)
                        
                        current_time = time.time()
                        if dist < 30 and (current_time - last_click_time) > click_cooldown:
                            pyautogui.click()
                            last_click_time = current_time
                            print("Клик!")
                        
                        cv2.line(frame, distances[0][1], distances[1][1], (255, 0, 0), 2)
                        cv2.putText(frame, f"Distance: {dist:.0f}", (20, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    # Показываем кадр и маску
    cv2.imshow("Black Glove Hand Tracking", frame)
    cv2.imshow("Mask", mask)
    
    # Выход
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
