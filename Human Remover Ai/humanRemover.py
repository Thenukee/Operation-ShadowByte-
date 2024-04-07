import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import ctypes

def remove_humans_from_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Path to YOLOv3 configuration and weights files
    config_path = "yolov3.cfg"
    weights_path = "yolov3.weights"

    # Load YOLO
    net = cv2.dnn.readNet(weights_path, config_path)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Resize and convert the image to blob format
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Process the detections
    height, width, channels = image.shape
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # 0 is the class id for person in COCO dataset
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Remove humans from the image
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            # Set the removed pixels to a specific shade (here, green)
            image[y:y + h, x:x + w] = [0, 255, 0]  # BGR color format, [B, G, R]

    # Get the screen size
    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # Resize the image if it exceeds the screen size
    if width > screen_width or height > screen_height:
        image = cv2.resize(image, (screen_width, screen_height))

    # Display the image with humans removed
    cv2.imshow("Image without humans", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def select_image():
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
    if file_path:
        remove_humans_from_image(file_path)

# Create the main window
root = tk.Tk()
root.title("Remove Humans from Image")

# Create a button to select an image
select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(padx=20, pady=20)

# Start the GUI event loop
root.mainloop()
