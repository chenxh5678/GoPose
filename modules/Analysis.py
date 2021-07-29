import sys,pickle
import cv2
import os

def analysis(video,cut1,cut2,zone = 0):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(dir_path + '\\../resource')
    os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '\\../resource;' +  dir_path + '\\../resource/bin;'
    import pyopenpose as op

    # 载入模型文件
    params = dict()
    params["model_folder"] = "resource/models/"
    # 启动OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    video_name = video.split('/')[-1]
    name = video_name.split('.')[0]
    datum = op.Datum()
    cap = cv2.VideoCapture(video)  # 视频解析
    data_list = []
    while cap.isOpened():
        ret,fram = cap.read()
        if ret == True:
            now = cap.get(1)
            if cut1 != None and cut2 and zone:
                if cut1 <= now <= cut2:
                    datum.cvInputData = fram
                    opWrapper.emplaceAndPop(op.VectorDatum([datum]))
                    data = datum.poseKeypoints
                    data_list.append(data)
                    cv2.imshow('Automatic Recognition of Key Points(Press ESC to exit)',datum.cvOutputData)
                    if cv2.waitKey(20) == 27:
                        break
                else:
                    data_list.append(None)
                    cv2.imshow('Automatic Recognition of Key Points(Press ESC to exit)',fram)
                    if cv2.waitKey(20) == 27:
                        break
            else:
                datum.cvInputData = fram
                opWrapper.emplaceAndPop(op.VectorDatum([datum]))
                data = datum.poseKeypoints
                data_list.append(data)
                cv2.imshow('Automatic Recognition of Key Points(Press ESC to exit)',datum.cvOutputData)
                if cv2.waitKey(20) == 27:
                    break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    with open('data/{}.pkl'.format(name), 'wb') as file0:
        pickle.dump(data_list,file0)
