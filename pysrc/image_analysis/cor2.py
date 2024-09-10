import cv2
import numpy as np

# Define the file paths to the images
image1_path = r"C:\Users\pubuduw\Desktop\11.png"  # Update with your actual file path
image2_path = r"C:\Users\pubuduw\Desktop\22.png" # Update with your actual file path

# Load the images
image1 = cv2.imread(image1_path)
image2 = cv2.imread(image2_path)

# Check if images are loaded properly
if image1 is None:
    raise ValueError(f"Image at path {image1_path} could not be loaded.")
if image2 is None:
    raise ValueError(f"Image at path {image2_path} could not be loaded.")

# Convert to grayscale
gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Detect keypoints and descriptors using SIFT
sift = cv2.SIFT_create()
keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

# Match descriptors using FLANN matcher
index_params = dict(algorithm=1, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(descriptors1, descriptors2, k=2)

# Filter good matches
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

# Ensure we have enough good matches
if len(good_matches) < 4:
    raise ValueError("Not enough good matches found to compute the transformation.")

# Extract location of good matches
points1 = np.zeros((len(good_matches), 2), dtype=np.float32)
points2 = np.zeros((len(good_matches), 2), dtype=np.float32)

for i, match in enumerate(good_matches):
    points1[i, :] = keypoints1[match.queryIdx].pt
    points2[i, :] = keypoints2[match.trainIdx].pt

# Calculate rotation matrix and translation vector using RANSAC
h, mask = cv2.estimateAffinePartial2D(points1, points2, method=cv2.RANSAC)

# Check if a valid transformation matrix was found
if h is None:
    raise ValueError("Failed to find a valid transformation matrix. Try adjusting parameters or using more features.")
print(points1)
# The center of rotation is the translation vector
center_of_rotation = (int(h[0, 2]), int(h[1, 2]))

# Mark the center of rotation on the images
marked_image1 = image1.copy()
marked_image2 = image2.copy()

cv2.circle(marked_image1, center_of_rotation, 200, (0, 0, 255), -1)  # Red dot
cv2.circle(marked_image2, center_of_rotation, 200, (0, 0, 255), -1)  # Red dot

# Show the images
cv2.imshow('Image 1 with Center of Rotation', marked_image1)
cv2.imshow('Image 2 with Center of Rotation', marked_image2)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Center of rotation:", center_of_rotation)
