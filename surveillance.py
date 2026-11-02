import cv2
import time

cap = cv2.VideoCapture(10)

if not cap.isOpened():
    print("Ошибка: не удалось открыть камеру")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

print("Видеонаблюдение запущено. Нажмите 'q' для выхода.")

frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Ошибка при захвате кадра")
        break
    
    frame_count += 1
    
    # Вычисляем FPS
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time if elapsed_time > 0 else 0
    
    # Показываем FPS на экране
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "Surveillance", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("Video Surveillance", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(f"Выход. Среднее FPS: {fps:.1f}")
        break

cap.release()
cv2.destroyAllWindows()
