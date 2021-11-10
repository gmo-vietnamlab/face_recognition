import cv2
import os


cap = cv2.VideoCapture(0)
new_employee = input()
folder_path = './data/employee_data/' 
os.makedirs(new_employee)

while True:

    try:
        check, frame = cap.read()
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        for i in range(5):
            if key == ord('s'): 
                cv2.imwrite(filename= str(i) + '.jpg', img=frame)
                print("Image saved!")

            elif key == ord(' '):
                cap.release()
                cv2.destroyAllWindows()
                break
        
    except(KeyboardInterrupt):
        cap.release()
        cv2.destroyAllWindows()
        break