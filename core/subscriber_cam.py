#!/usr/bin/env python3
import os
import cv2                                          # to display the images
import numpy as np
from cv_bridge import CvBridge, CvBridgeError       # to convert ros image messages to OpenCV images
import rospy                                        # ROS Python Interface
from sensor_msgs.msg import CompressedImage         # Image message definition
from tensorflow.keras.models import load_model, model_from_json
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from tensorflow.keras.preprocessing import image

model = model_from_json(open("model.json", "r").read())
model.load_weights('model.h5')

class CamSubscriber(object):

    """
        The following code will display MiRo's camera data
    """
    def __init__(self, normalised = True):
        rospy.init_node("cam_subscriber")
        # OpenCV bridge is used for converting ROS img data to data that can be used by OpenCV
        self.bridge = CvBridge()
        self.cam_data = [None, None]

        topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
        # Create two new subscribers to receive camera images with attached callbacks
        self.sub_caml = rospy.Subscriber(
            topic_base_name + "/sensors/caml/compressed",
            CompressedImage,
            self.callback_caml,
            queue_size=1,
            tcp_nodelay=True,
        )
        self.sub_camr = rospy.Subscriber(
            topic_base_name + "/sensors/camr/compressed",
            CompressedImage,
            self.callback_camr,
            queue_size=1,
            tcp_nodelay=True,
        )

    def callback_caml(self, ros_image):  # Left camera
        self.callback_cam(ros_image, 0)

    def callback_camr(self, ros_image):  # Right camera
        self.callback_cam(ros_image, 1)

    # Unified callback for both functions
    def callback_cam(self, ros_image, index):
        """
        Callback function executed upon image arrival
        """
        try:
            # Convert compressed ROS image to raw CV image
            image = self.bridge.compressed_imgmsg_to_cv2(ros_image, "bgr8")
            # Store image as class attribute for further use
            self.cam_data[index] = image
            face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_haar_cascade.detectMultiScale3(gray_image, 1.05, 3, 0, (20, 20), outputRejectLevels=True)
            for (x,y,w,h) in faces:
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), thickness=2)
        except CvBridgeError as e:
            # Ignore corrupted frames
            pass

if __name__ == '__main__':
    camera = CamSubscriber()
    rospy.sleep(0.5) # short wait to make sure everything is initialised
    while not rospy.is_shutdown():
        # if camera.cam_data[0] is not None:
        #     cv2.imshow("Left cam", camera.cam_data[0])
        if camera.cam_data[0] is not None:
            cv2.imshow("Right cam", camera.cam_data[1])
        cv2.waitKey(1)
