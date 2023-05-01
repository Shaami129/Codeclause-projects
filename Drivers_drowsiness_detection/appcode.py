import cv2
import numpy as np
import playsound

def detect_drowsiness(frame, eye_region):
    canny = cv2.Canny(eye_region, 30, 50)

    ratio = np.sum(canny == 255) / (canny.shape[0] * canny.shape[1])

    if ratio < 0.25:
        return True
    else:
        return False

def play_alarm():
    playsound.playsound('C:\\Users\\shame\\OneDrive\\Desktop\\Codeclause projects\\Drivers_drowsiness_detection\\alarm.mp3')

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    counter = 0
    alarm_playing = False

    while True:
        ret, frame = cap.read()

        height, width = frame.shape[:2]
        eye_region = frame[int(height * 0.2):int(height * 0.5), int(width * 0.25):int(width * 0.75)]

        if detect_drowsiness(frame, eye_region):
            counter += 1

            if counter > 10 and not alarm_playing:
                play_alarm()
                alarm_playing = True
        else:
            counter = 0
            alarm_playing = False

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
