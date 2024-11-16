import cv2
import numpy as np
import matplotlib.pyplot as plt

def find_rotation_center(image1_path, image2_path):
    # Load the images
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
    
    # Detect ORB keypoints and descriptors
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    
    # Match descriptors using BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    
    # Sort matches by distance
    matches = sorted(matches, key=lambda x: x.distance)
    
    # Extract matched keypoints
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])
    
    # Estimate affine transform
    M, mask = cv2.estimateAffinePartial2D(pts1, pts2)
    
    # Extract rotation and translation
    R = M[:, :2]
    t = M[:, 2]
    
    # Calculate rotation angle
    angle = np.degrees(np.arctan2(R[1, 0], R[0, 0]))
    
    # Calculate center of rotation
    # Calculate the center of the image
    center = np.array([img1.shape[1] / 2, img1.shape[0] / 2])
    
    # Calculate the translation vector for the center of the image
    translation_center = center + t
    
    # Calculate the center of rotation using the inverse rotation matrix
    center_of_rotation = np.linalg.inv(R).dot(translation_center - center) + center
    
    # Convert coordinates to integer for visualization
    center_of_rotation = tuple(map(int, center_of_rotation))
    
    # Mark center of rotation on the images
    img1_color = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    img2_color = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    
    cv2.circle(img1_color, center_of_rotation, 5, (0, 0, 255), -1)
    cv2.circle(img2_color, center_of_rotation, 5, (0, 0, 255), -1)
    
    # Plot the results
    plt.figure(figsize=(10, 5))
    plt.subplot(121), plt.imshow(img1_color), plt.title('Original Image')
    plt.subplot(122), plt.imshow(img2_color), plt.title('Rotated Image')
    plt.show()
    
    # Output the transformation details
    return {
        'rotation_matrix': R,
        'translation_vector': t,
        'rotation_angle': angle,
        'center_of_rotation': center_of_rotation
    }

# Example usage
image1_path = r"C:\Users\pubuduw\Desktop\11.png"
image2_path = r"C:\Users\pubuduw\Desktop\66.png"
result = find_rotation_center(image1_path, image2_path)

print("Rotation Matrix:\n", result['rotation_matrix'])
print("Translation Vector:\n", result['translation_vector'])
print("Rotation Angle (degrees):\n", result['rotation_angle'])
print("Center of Rotation (pixels):\n", result['center_of_rotation'])
