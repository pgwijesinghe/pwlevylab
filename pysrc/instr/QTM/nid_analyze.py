'''
Analyze NID images taken from Nanosurf EasyScan for the QTM Project
'''
import numpy as np
import matplotlib.pyplot as plt
import nanosurf as nsf

# Loading the .nid image
def load_nid_image(file_path):
    nid_file = nsf.util.nid_reader.NIDFileReader()
    ok = nid_file.read(file_path)
    if ok:
        fwd_segment = nid_file.data.image.forward
    return fwd_segment["Topography"]

# Plane leveling
def plane_level_image(image):
    # Get the shape of the image
    x = np.linspace(0, 1, image.shape[1])
    y = np.linspace(0, 1, image.shape[0])
    X, Y = np.meshgrid(x, y)
    
    # Flatten the data for least squares fitting
    X_flat = X.flatten()
    Y_flat = Y.flatten()
    Z_flat = image.flatten()
    
    # Construct the design matrix
    A = np.c_[X_flat, Y_flat, np.ones(X_flat.shape)]
    
    # Perform least squares fitting to find the plane coefficients
    C, _, _, _ = np.linalg.lstsq(A, Z_flat, rcond=None)
    a, b, c = C
    
    # Calculate the fitted plane
    Z_fit = a * X + b * Y + c
    
    # Subtract the fitted plane from the original image
    Z_corrected = image - Z_fit
    
    return Z_corrected, Z_fit

# Load the ndi image
file_path = "./nid_analyze/data.nid"
image = load_nid_image(file_path)

# Apply the plane leveling function
corrected_image, fitted_plane = plane_level_image(image)

# # Plot the original image
# plt.figure(figsize=(8, 6))
# plt.imshow(image, extent=(0, 1, 0, 1), origin='lower')
# plt.title('Original Image')
# plt.colorbar()
# plt.show()

# # Plot the fitted plane
# plt.figure(figsize=(8, 6))
# plt.imshow(fitted_plane, extent=(0, 1, 0, 1), origin='lower')
# plt.title('Fitted Plane')
# plt.colorbar()
# plt.show()

# Plot the corrected image
plt.figure(figsize=(8, 6))
plt.imshow(corrected_image, extent=(0, 1, 0, 1), origin='lower', cmap='viridis')
plt.title('Corrected Image')
plt.colorbar()
plt.show()
