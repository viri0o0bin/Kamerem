import cv2
import time
from picamera2 import Picamera2

picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
picam2.configure(config)
picam2.start()

print("Видеонаблюдение запущено. Нажмите 'q' для выхода.")

frame_count = 0
start_time = time.time()

while True:
    frame = picam2.capture_array()
    frame_count += 1
    fps = frame_count / (time.time() - start_time)

    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Video Surveillance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
