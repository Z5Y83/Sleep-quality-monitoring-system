
# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import datetime
import time


def display(datums):
    datum = datums[0]
    out=datum.cvOutputData
    # cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", out)
    # cv2.putText(out,data,(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),1,cv2.LINE_AA)
    key = cv2.waitKey(1)
    return (key == 27)
    return out





# 生成唯一的檔名
# timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# filename = f"C:/Users/user/Desktop/data_{timestamp}.txt"





def printKeypoints(datums):
    datum = datums[0]
    # print("Body keypoints: \n" + str(datum.poseKeypoints))
    # print("Face keypoints: \n" + str(datum.faceKeypoints))
    # print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
    # print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))


    #wedo
    import numpy as np

    def calculate_angle(ax,bx,cx,ay,by,cy): #計算身體臥躺角度

        radians = np.arctan2(cy-by, cx-bx) - np.arctan2(ay-by, ax-bx) 

        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
            
        return angle 

    Leye_x = datum.poseKeypoints[0,15,0]
    Leye_y = datum.poseKeypoints[0,15,1]
    Leye_z = datum.poseKeypoints[0,15,2]
    Reye_x = datum.poseKeypoints[0,16,0]
    Reye_y = datum.poseKeypoints[0,16,1]
    Reye_z = datum.poseKeypoints[0,16,2]
    Lear_x = datum.poseKeypoints[0,17,0]
    Lear_y = datum.poseKeypoints[0,17,1]
    Lear_z = datum.poseKeypoints[0,17,2]
    Rear_x = datum.poseKeypoints[0,18,0]
    Rear_y = datum.poseKeypoints[0,18,1]
    Rear_z = datum.poseKeypoints[0,18,2]
    # print(Leye_x,Leye_y,Leye_z)
    # print(Reye_x,Reye_y,Reye_z)
    # print(Lear_x,Lear_y,Lear_z)
    # print(Rear_x,Reye_y,Rear_z)

    global data

    Langle = 0
    Rangle = 0
     #抓取節點判斷睡姿
    if Leye_x != 0 and Reye_x != 0 and Lear_x != 0 and Rear_x != 0: #只要耳朵和眼睛都有抓到就判斷為正躺正臉
        print('正躺正臉')
        data = 'lying with positive face'
        return data
        # cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", out)
        # cv2.putText(out,data,(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),1,cv2.LINE_AA)
    # key = cv2.waitKey(1)        

    
    elif Leye_x != 0 and Reye_x != 0 and (Lear_x == 0 or Rear_x == 0): #若抓不到其中一邊耳朵座標（括號內容）為側躺
        print('正躺側臉')
        data = 'lying with side face'
        return data
        # cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", out)
        # cv2.putText(out,data,(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),1,cv2.LINE_AA)
    # key = cv2.waitKey(1)

    # elif(Leye_x == 0 and Lear_x == 0 and Reye_x == 0 and Rear_x == 0):
    #     print("沒有監測到人")
    #     data = 'There is nobody!'
    #     return data
        

    elif (Leye_x == 0 and Lear_x == 0) or (Reye_x == 0 and Rear_x == 0): #當同一側的耳朵和眼睛沒有辨識到，辨識結果不是側睡就是趴睡
        # print('側睡或趴睡')

        if (Reye_x == 0 and Rear_x == 0) : #當右側的眼睛和耳朵沒有辨識到，透過左側的節點去計算角度
            ax = datum.poseKeypoints[0,17,0]
            ay = datum.poseKeypoints[0,17,1]
            bx = datum.poseKeypoints[0,5,0]
            by = datum.poseKeypoints[0,5,1]
            cx = datum.poseKeypoints[0,2,0]
            cy = datum.poseKeypoints[0,2,1]

            Langle = calculate_angle(ax,bx,cx,ay,by,cy)
            Rangle = 180 - Langle


        if (Leye_x == 0 and Lear_x == 0) : #當左側的眼睛和耳朵沒有辨識到，透過右側的節點去計算角度
            ax = datum.poseKeypoints[0,18,0]
            ay = datum.poseKeypoints[0,18,1]
            bx = datum.poseKeypoints[0,2,0]
            by = datum.poseKeypoints[0,2,1]
            cx = datum.poseKeypoints[0,5,0]
            cy = datum.poseKeypoints[0,5,1]

            Rangle = calculate_angle(ax,bx,cx,ay,by,cy)
            Langle = 180 - Rangle

        angle = abs(Langle - Rangle)   #如果角度在45到135範圍內，定義為趴睡
        if(angle>=45 and angle<=135) :
            print("趴睡")
            data = 'sleep on your stomach'
            return data
            # cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", out)
            # cv2.putText(out,data,(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),1,cv2.LINE_AA)
    # key = cv2.waitKey(1)
        
        else:
            print("側睡")
            data = 'lying on side'
            return data
            # cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", out)
            # cv2.putText(out,data,(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),1,cv2.LINE_AA)
    # key = cv2.waitKey(1)
            #cv2.putText(out,data,(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),1,cv2.LINE_AA)
            
    #return data
    # print(Langle)
    # print(Rangle)


    # 開啟檔案並寫入資料
    # with open(filename, "w") as file:
    #     file.write(data)






try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../python/openpose/Release');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-display", action="store_true", help="Disable display.")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../../models/"
    
    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item


    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython(op.ThreadManagerMode.AsynchronousOut)
    opWrapper.configure(params)
    opWrapper.start()







    # Main loop
    # a = int(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) #設定起始時間
    # filename = f"C:/Users/user/Desktop/data_{a}.txt"
    save_image_time=2
    userWantsToExit = False
    i=0
    last_saved_time = time.time() #記下最後存下的圖的時間
    while not userWantsToExit:
        # Pop frame
        datumProcessed = op.VectorDatum()

        # 設定保存圖片的目錄
        # output_directory = 'output_images'
        # os.makedirs(output_directory, exist_ok=True)

        if opWrapper.waitAndPop(datumProcessed):
            if not args[0].no_display:
                # Display image
                userWantsToExit = display(datumProcessed)

                # 取得檢測結果
                output_image = datumProcessed[0].cvOutputData

                #判斷影像內是否有辨識到人

                if datumProcessed[0].poseKeypoints is not None and len(datumProcessed[0].poseKeypoints) > 0: # 如果檢測到人執行上方的程式
                    printKeypoints(datumProcessed)
                else:
                    print("未監測到人像")
                    continue
                
            current_time = time.time()
            data=printKeypoints(datumProcessed)
            cv2.putText(output_image,data,(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(21,63,178),3,cv2.LINE_AA)
            # cv2.imshow('out',output_image)
            if current_time - last_saved_time >= save_image_time:

                # name = os.path.join(output_directory, f"C:/Users/user/Desktop/data_{a}.jpg")
                # cv2.imwrite(name, output_image)

                # b = int(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) #設定結束時間
                # c = b-a  #計算時間間隔
                # if c == 5: # 每5秒保存一張圖片
                #     filename = f"C:/Users/user/Desktop/data_{b}.txt"
                #     a = b
                    # 以日期和時間來命名圖片
                    # name = os.path.join(output_directory, f"C:/Users/user/Desktop/data_{b}.jpg")
                    # cv2.imwrite(name, output_image)

            
                cv2.imwrite('C:/openpose-master/openpose-master/build/examples/tutorial_api_python/tt/tt2/'+str(i)+'.jpg',output_image)
                i+=1
                last_saved_time = current_time


        else:
            break


    

    # cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
    
    # time.sleep(10000)
    cv2.waitKey(0)

    

except Exception as e:
    print(e)
    sys.exit(-1)

