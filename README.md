# Computer-Vision-Edge-Detection

## Introduction
In this project, I implemented **edge detection** through OpenCv, with **Canny** edge detection and **Sobel** edge detection: https://opencv.org/. 
Some sample output of process images:
  
  Sobel:
![image](https://user-images.githubusercontent.com/81957118/116080464-74f28980-a6dc-11eb-9fc2-c780883ed4b9.png)

  Canny:
![image](https://user-images.githubusercontent.com/81957118/116080916-f518ef00-a6dc-11eb-90cd-4e9f3d7945d7.png)

## Run on your local machine
### Jupyter Notebook
I have created both a flask based web version of the project and a jupyter notebook version.

To run the jupyter notebook, list of required libraries can be found at:
  
  OpenCv: https://pypi.org/project/opencv-python/
  
  Numpy: https://numpy.org/install/
  
  Matplotlib: https://matplotlib.org/stable/users/installing.html
  
  Imageio: https://imageio.readthedocs.io/en/stable/installation.html
  
The jupyter notebook is located at: **./models/models.ipynb**

### Web
For web implementation I use Flask, to run the web version, go to **./web** in command line and type **flask run**.
### Structure and features
There is real time edge detection by capturing information from camera through: 

**http://127.0.0.1:5000/camera/** for web

**real_time_transform(transform_method, cam = 0)** for jupyter notebook

![image](https://user-images.githubusercontent.com/81957118/116084167-d3216b80-a6e0-11eb-9dea-83d983e8d86f.png)

There is image converter for different edge detection filter

**http://127.0.0.1:5000/upload/** for web

**my_sobel(src, output_to_screen=False, gray_scale = True)
my_canny(src, output_to_screen=False)**
For jupyter notebook, where src means source to target image place, output_to_screen refers to whether print edge detection filtered image to screen.

There is also a video convertor which will convert your video into purly edge detected form: **video_transform(input_path, transform_method, output_path)**
 

https://user-images.githubusercontent.com/81957118/116084892-973ad600-a6e1-11eb-937d-0d79dbc20788.mp4

Feel free to change the filter and play around the code :)


## Future development
There are few thing I wish for future development.
1. Although I have implmented video transformer which will transform the video into edge detected form, I haven't implemented it in the web based version, that could be concidered as next step.
2. Also real time edge detection works well on local machine, it relys on cv2.VideoCapture(0), which needs to access local camera. However, when trying to deploy to web, such camera capture won't work. A more detailed implemetation for live streaming on client side which both concideration on fluency of videos for real time edge detection and performance of edge detection is quite helpful.
3. More filters :)
4. Feel free to contact me with:
    
    Email: WujiZhu1999@outlook.com
