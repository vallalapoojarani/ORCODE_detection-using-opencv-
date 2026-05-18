import cv2
import webbrowser

# Initialize Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280) ## width
cap.set(4, 720)  ## height 

# Built-in OpenCV QR Detector
detector = cv2.QRCodeDetector()

print("QR Scanner is running... Press 'q' to quit.")

last_data = None

while True:
    success, img = cap.read()
    if not success:
        break

    # Detect and Decode
    data, bbox, _ = detector.detectAndDecode(img)

    # If a QR code is found
    if bbox is not None:
        # FIXED: Reshaping the bbox to a simple 4x2 array
        bbox = bbox.reshape(-1, 2)
        
        for i in range(len(bbox)):
            # Draw green bounding box using integer coordinates
            pt1 = tuple(bbox[i].astype(int))
            pt2 = tuple(bbox[(i+1) % len(bbox)].astype(int))
            cv2.line(img, pt1, pt2, (0, 255, 0), 3)

        if data:
            # Place text near the top corner of the box
            cv2.putText(img, "QR Detected!", (int(bbox[0][0]), int(bbox[0][1]) - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            if data != last_data:
                print(f"Decoded Data: {data}")
                if data.startswith("http"):
                    webbrowser.open(data)
                last_data = data

    cv2.imshow("OpenCV QR Scanner", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()