import cv2  #imported for opencv
import argparse #any argument passed during runtime
import orien_lines # custom import from orien_lines.py which is used to create orientation lines 
import datetime
from imutils.video import VideoStream # used for videostreaminng. Not used in crrent POC project
from utils import detector_utils as detector_utils # for tensor flow session and loading the model
import pandas as pd
from datetime import date
import xlrd # used to read data and format information from excel sheet
from xlwt import Workbook # used for creating workbook in excel file
from xlutils.copy import copy # used for copying cell contents from one cell to other
import numpy as np
from vidgear.gears import CamGear # used for webcam

lst1 = []
lst2 = []
ap = argparse.ArgumentParser()
ap.add_argument('-d', '--display', dest='display', type=int,default=1, help='Display the detected images using OpenCV. This reduces FPS')
args = vars(ap.parse_args())

# here model will be loaded
detection_graph, sess = detector_utils.load_inference_graph()

# Function to store data of number of time it was able to detect the hand and number of times hand crossed the warning line
# Count will be saved in result.xls file
# this help to keep trakc of how many times employee was using the shredder machine
def save_data(no_of_time_hand_detected, no_of_time_hand_crossed):
    try:
        today = date.today()
        today = str(today)
        rb = xlrd.open_workbook('result.xls')
        sheet = rb.sheet_by_index(0)
        sheet.cell_value(0, 0)

        # print(sheet.nrows)
        q = sheet.cell_value(sheet.nrows - 1, 1)

        rb = xlrd.open_workbook('result.xls')
        # rb = xlrd.open_workbook(loc)
        wb = copy(rb)
        w_sheet = wb.get_sheet(0)
        
        # if we have entry of todays date in the sheet then we will keep on adding the count(hand detected and hand crossed) and update the values
        if q == today:
            w = sheet.cell_value(sheet.nrows - 1, 2)
            e = sheet.cell_value(sheet.nrows - 1, 3)
            w_sheet.write(sheet.nrows - 1, 2, w + no_of_time_hand_detected)
            w_sheet.write(sheet.nrows - 1, 3, e + no_of_time_hand_crossed)
            # save the counts in result.xls
            wb.save('result.xls')

        # if there is no entry of current date in the sheet then we will write the count(hand detected and hand crossed).
        else:
            w_sheet.write(sheet.nrows, 0, sheet.nrows)
            w_sheet.write(sheet.nrows, 1, today)
            w_sheet.write(sheet.nrows, 2, no_of_time_hand_detected)
            w_sheet.write(sheet.nrows, 3, no_of_time_hand_crossed)
            # save the counts in result.xls
            wb.save('result.xls')
   # if sheet was missing in the excel sheet then new sheet will be created and counts will be written
    except FileNotFoundError:
        today = date.today()
        today = str(today)
        # Workbook is created 
        wb = Workbook()
        # add_sheet is used to create sheet. 
        sheet = wb.add_sheet('Sheet 1')
        sheet.write(0, 0, 'Sl.No')
        sheet.write(0, 1, 'Date')
        sheet.write(0, 2, 'Number of times hand detected')
        sheet.write(0, 3, 'Number of times hand crossed')
        m = 1
        sheet.write(1, 0, m)
        sheet.write(1, 1, today)
        sheet.write(1, 2, no_of_time_hand_detected)
        sheet.write(1, 3, no_of_time_hand_crossed)
        # save the counts in result.xls
        wb.save('result.xls')


# Main function
if __name__ == '__main__':
    
    # Detection confidence threshold to draw bounding box
    score_thresh = 0.80
    
    # Below code is for machine camera feed. But since we are using webcam hence we have commented the code. RTSP is real time streaming protocol.
    #rtsp_url = "rtsp://admin:ravi@123@192.168.0.2/H264?ch=1&subtype=0" # 
    #vs = VideoStream(rtsp_url).start()
    #vs = cv2.VideoCapture('rtsp://admin:ravi@123@192.168.0.2/H264?ch=1&subtype=0')
    #vs = VideoStream(0).start()
    
    # we are starting the webcam and taking their live feed for processing.
    options = {'THREADED_QUEUE_MODE': True}
    vs = CamGear(source=0,**options).start()
    #vs = cv2.VideoCapture(0)

    # Orientation of camera
    Orientation = 'bt'
    # input("Enter the orientation of hand progression ~ lr,rl,bt,tb :")

    # line % set for the Machine. We are setting at 30% from the orientation. 
    # Line_Perc1=float(input("Enter the percent of screen the line of machine :"))
    Line_Perc1 = float(15)

    # Line For Safety. We are setting at 30% from the orientation. 
    # Line_Perc2=float(input("Enter the percent of screen for the line of safety :"))
    Line_Perc2 = float(30)

    # max number of hands we want to detect/track. Set to 2
    num_hands_detect = 2

    # Used to calculate frame per second
    start_time = datetime.datetime.now()
    # starting with 0 frames
    num_frames = 0

    # setting up image height and width initally to zero as we are not sure what will camera feed input size would be
    im_height, im_width = (None, None)
    # it pops the webcam feed window with the safety and margin lines
    cv2.namedWindow('Detection', cv2.WINDOW_NORMAL)
    
    # it count the number of objects comes in the frame
    def count_no_of_times(lst):
        x = y = cnt = 0
        for i in lst:
            x = y
            y = i
            if x == 0 and y == 1:
                cnt = cnt + 1
        return cnt

    # in case camera is not working we use try 
    try:
        while True:
            # used for reading the camera feed and converting image to matrix
            frame = vs.read() 
            frame = np.array(frame)
            
            # getting image height and width from the camera frame
            if im_height == None:
                im_height, im_width = frame.shape[:2]

            # Convert image to rgb since opencv loads images in bgr, if not accuracy will decrease
            try:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except:
                print("Error converting to RGB")

            # Run image through tensorflow graph to store model output. once session of Tensorflow is initialized, inside the session model will be loaded
            boxes, scores, classes = detector_utils.detect_objects(frame, detection_graph, sess)
            
            # initialization of orientation lines are done and lines are drawn
            Line_Position2 = orien_lines.drawsafelines(frame, Orientation, Line_Perc1, Line_Perc2)
            
            # Draw bounding boxeses and text
            a, b = detector_utils.draw_box_on_image(num_hands_detect, score_thresh, scores, boxes, classes, im_width, im_height, frame, Line_Position2,Orientation)
            lst1.append(a)
            lst2.append(b)
            no_of_time_hand_detected = no_of_time_hand_crossed = 0
           
           # Calculate Frames per second (FPS)
            num_frames += 1
            elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
            fps = num_frames / elapsed_time
          
          # It writes and Display FPS text on top left of the video and what is the fps value
            if args['display']:           
                detector_utils.draw_text_on_image("FPS : " + str("{0:.2f}".format(fps)), frame)
                cv2.imshow('Detection', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                # we can close the window by pressing function key or writing q and stopping the streaming mechanism
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    vs.stop()
                    break

        no_of_time_hand_detected = count_no_of_times(lst2)
        no_of_time_hand_crossed = count_no_of_times(lst1)   
        # calling save_data function to store the count in excel    
        save_data(no_of_time_hand_detected, no_of_time_hand_crossed)
        print("Average FPS: ", str("{0:.2f}".format(fps)))

    except KeyboardInterrupt:
        no_of_time_hand_detected = count_no_of_times(lst2)
        no_of_time_hand_crossed = count_no_of_times(lst1)
        today = date.today()
        save_data(no_of_time_hand_detected, no_of_time_hand_crossed)
        print("Average FPS: ", str("{0:.2f}".format(fps)))
