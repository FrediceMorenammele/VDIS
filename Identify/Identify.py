import cv2
import time

def main():
    platecascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

    minArea = 500
    cap = cv2.VideoCapture(0)
    count = 0

    while True:
        success, img = cap.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

        numberplates = platecascade.detectMultiScale(imgGray, 1.1, 4)

        for (x, y, w, h) in numberplates:
            area = w * h
            if area > minArea:
                # Calculate the larger ROI bounds size
                roi_width = w + 400
                roi_height = h + 400

                # Calculate the top-left corner coordinates for the larger ROI
                x_roi = max(0, x - 200)
                y_roi = max(0, y - 200)

                # Create the larger ROI around the number plate
                imgRoi = img[y_roi: y_roi + roi_height, x_roi: x_roi + roi_width]
                cv2.imshow("Car ROI", imgRoi)

                # Automatically capture number plate
                cv2.imwrite("C:/Users/fredi/source/repos/python/Identify/pictures/Plate_" + str(count) + ".jpg", imgRoi)
                cv2.rectangle(img, (0, 200), (640, 300), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, "SCAN SAVED", (15, 265), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 2)
                cv2.imshow("RESULTS", img)
                cv2.waitKey(500)
                count = count + 1

                # Check if two pictures have been taken
                if count == 3:
                    time.sleep(3)  # Pause for 2 seconds
                    break

        cv2.imshow("RESULT", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
