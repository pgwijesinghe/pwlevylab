import cv2
import numpy as np

def create_test_images():
    # Create a black square image
    img1 = np.zeros((500, 500, 3), dtype=np.uint8)
    # Draw a white rectangle
    cv2.rectangle(img1, (150, 150), (350, 350), (255, 255, 255), -1)

    # Rotate the image by 45 degrees
    center = (250, 250)
    angle = 45
    scale = 1.0
    M = cv2.getRotationMatrix2D(center, angle, scale)
    img2 = cv2.warpAffine(img1, M, (500, 500))

    # Save the images
    cv2.imwrite('test_image1.jpg', img1)
    cv2.imwrite('test_image2.jpg', img2)

    return 'test_image1.jpg', 'test_image2.jpg'

image1_path, image2_path = create_test_images()
print(f"Created images: {image1_path}, {image2_path}")
