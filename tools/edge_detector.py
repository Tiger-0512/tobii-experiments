import argparse
import cv2

parser = argparse.ArgumentParser(description="Detect the edge of the image and saze it")
parser.add_argument("target_path", help="Target file path")
parser.add_argument("destination_path", help="Destination file path to saze")

args = parser.parse_args()

org_img = cv2.imread(args.target_path)
gray_img = cv2.imread(args.target_path, cv2.IMREAD_GRAYSCALE)
canny_img = cv2.Canny(gray_img, 240, 255)
# sobel_img = cv2.Sobel(gray_img, cv2.CV_32F, 0, 1, ksize=3)

cv2.imshow("canny_img", canny_img)
# cv2.imshow("sobel_img", sobel_img)

cv2.imwrite(args.destination_path, canny_img)

cv2.waitKey(0)

# test image: ..\imagenet_tree_renew\640_640\feline_resized\resized_n02124075_58.JPEG
