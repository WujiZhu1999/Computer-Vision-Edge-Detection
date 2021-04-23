import cv2
import numpy as np
import matplotlib.pyplot as plt
import imageio

#src is cv2 image generated from cv2.imread
#src is supposed to be a BGR image
#grayscale indicate whether image edges should be presented in black white or rgb 
def my_sobel(src, output_to_screen=False, gray_scale = True):
    img = src.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if gray_scale:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
    #x, y gradient by unit16
    x = cv2.Sobel(img,cv2.CV_16S,1,0)
    y = cv2.Sobel(img,cv2.CV_16S,0,1)

    #convert back to unit 8
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)

    #combine
    dst = cv2.addWeighted(absX,0.5,absY,0.5,0)
    if output_to_screen:
        plt.imshow(dst)
    return dst
def my_canny(src, output_to_screen=False):
    img = src.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    med_val = np.median(img) 
    lower = int(max(0 ,0.6*med_val))
    upper = int(min(255,1.4*med_val))
    edges = cv2.Canny(image=img, threshold1=lower,threshold2=upper)
    if output_to_screen:
        plt.imshow(edges)
    return edges
# input: relative file path
# input: transfor methods
# input: output path
def video_transform(input_path, transform_method, output_path):
    assert (input_path != output_path)
    reader = imageio.get_reader(input_path)
    fps = reader.get_meta_data()['fps']
    writer = imageio.get_writer(output_path, fps = fps)
    for i, frame in enumerate(reader):
        frame = transform_method(frame)
        writer.append_data(frame)
        #print(i)
    writer.close()
    #print("Final Frame: ", frame)
    #print("FPS: ", fps)
    print("File: ",output_path," done.")
    return True
def real_time_transform(transform_method, cam = 0):
    cap = cv2.VideoCapture(cam)
    while(True):
        ret, frame = cap.read()
        edges = transform_method(frame)
        cv2.imshow('frame',edges)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return True
