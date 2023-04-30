import cv2
import numpy as np
import playsound

def play_alarm():
    # play an alarm sound when the driver is drowsy
    playsound.playsound('alarm.mp3')

def detect_drowsiness(frame, eye_region):
    # apply canny edge detection to the eye region
    canny = cv2.Canny(eye_region, 30, 50)

    # calculate the ratio of white pixels to the total number of pixels
    ratio = np.sum(canny == 255) / (canny.shape[0] * canny.shape[1])

    # if the ratio is less than 0.25, the driver is drowsy
    if ratio < 0.25:
        return True
    else:
        return False

if __name__ == "__main__":
    # initialize video capture object
    cap = cv2.VideoCapture(0)

    # initialize variables
    counter = 0
    alarm_playing = False

    while True:
        # capture frame-by-frame
        ret, frame = cap.read()

        # get the region of interest for the eyes
        height, width = frame.shape[:2]
        eye_region = frame[int(height * 0.2):int(height * 0.5), int(width * 0.25):int(width * 0.75)]

        # detect drowsiness
        if detect_drowsiness(frame, eye_region):
            counter += 1

            # play alarm sound if driver is drowsy for more than 10 consecutive frames
            if counter > 10 and not alarm_playing:
                play_alarm()
                alarm_playing = True
        else:
            counter = 0
            alarm_playing = False

        # display the resulting frame
        cv2.imshow('frame', frame)

        # exit on key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
