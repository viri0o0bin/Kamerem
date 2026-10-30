import cv2
import numpy as np
import pyautogui

# Fail-safe: press Ctrl+Alt+Delete to stop
pyautogui.FAILSAFE = True

# Open video capture from PS2 camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Screen size for mouse mapping
screen_width, screen_height = pyautogui.size()

# Morphological kernel (5x5 ellipse)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# HSV skin color range
lower_skin = np.array([0, 20, 70])
upper_skin = np.array([20, 255, 255])

print("Hand-controlled mouse started. Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to read frame")
        break
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create skin mask
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Morphological operations for noise reduction
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Calculate centroid using moments
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Map camera coordinates to screen coordinates
            screen_x = (cx / 640) * screen_width
            screen_y = (cy / 480) * screen_height
            
            # Move mouse
            pyautogui.moveTo(screen_x, screen_y, duration=0.1)
            
            # Draw circle on frame for debugging
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
    
    # Display the frame with mask overlay
    cv2.imshow("Hand Detection", frame)
    cv2.imshow("Mask", mask)
    
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Mouse control stopped.")
                     
