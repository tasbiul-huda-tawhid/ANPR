import cv2
import os
import pytesseract
# Path to the Haar cascade file
haar_cascade = r"D:\study\Intern_Mahsa (2024)\ANPR_sys_1.0\model\haarcascade_russian_plate_number.xml"

# Create the plates directory if it does not exist
if not os.path.exists("plate_number"):
    os.makedirs("plate_number")

# Open the webcam
cap = cv2.VideoCapture(0)

# Set the width and height of the capture frame
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Minimum area for plate detection
min_area = 500  # Adjust this value according to your needs

count = 0
plate_cascade = cv2.CascadeClassifier(haar_cascade)

if plate_cascade.empty():
    print("Error loading Haar cascade file. Check the path.")
    exit()

def is_valid_plate(w, h):
    if h == 0:
        return False
    aspect_ratio = w / float(h)
    return 2.0 < aspect_ratio < 6.0  # Typical aspect ratio range for number plates

# Initialize pytesseract
pytesseract.pytesseract.tesseract_cmd = r"D:\tools\Tesseract\tesseract.exe"

while True:
    # Read a frame from the webcam
    success, img = cap.read()
    if not success:
        print("Failed to capture frame.")
        break

    # Convert the frame to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    img_gray = cv2.GaussianBlur(img_gray, (5, 5), 0)

    # Detect plates in the grayscale image
    plates = plate_cascade.detectMultiScale(img_gray, scaleFactor=1.8, minNeighbors=5, minSize=(40, 40))

    # Draw rectangles around detected plates and save the plate images
    for (x, y, w, h) in plates:
        area = w * h
        if area > min_area and is_valid_plate(w, h):
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
            plate_roi = img[y:y + h, x:x + w]
            plate_text = pytesseract.image_to_string(plate_roi, lang='eng', config='--psm 11')
            with open(f"plate_number/scanned_plate_{count}.txt", "w") as f:
                f.write(plate_text.strip())
            count += 1

    # Display the result
    cv2.imshow("Result", img)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()