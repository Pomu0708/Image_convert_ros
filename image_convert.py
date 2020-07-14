from __future__ import print_function

import roslib
import rospy
#roslib.load_manifest('my_package')
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2


class image_converter:

    def __init__(self):
        self.image_pub = rospy.Publisher("image_topic_2",Image,queue_size=10)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/tello/image_raw",Image,self.callback)

    def callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        
        cropping = cv_image[120:240, 0:320] #input any function
        #cv2.imshow("cropping", cropping)

        #cv2.imshow("Image window", cv_image)
        cv2.waitKey(1)

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cropping, "bgr8"))
        except CvBridgeError as e:
            print(e)

def main(args):
    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)