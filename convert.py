import cv2
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from flask import Flask, request, send_file
import jwt
import os

app = Flask(__name__)

# Define function to resize images with black fill

def resize_with_black_fill(frame, output_width, output_height):
    h, w = frame.shape[:2]
    aspect_ratio = w / h
    
    if aspect_ratio > output_width / output_height:
        new_w = output_width
        new_h = int(new_w / aspect_ratio)
    else:
        new_h = output_height
        new_w = int(new_h * aspect_ratio)
    
    resized_frame = cv2.resize(frame, (new_w, new_h))
    black_filled_frame = np.zeros((output_height, output_width, 3), dtype=np.uint8)
    y_offset = (output_height - new_h) // 2
    x_offset = (output_width - new_w) // 2
    black_filled_frame[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_frame
    
    return black_filled_frame


# Route to handle video creation and delivery

@app.route('/display', methods=['POST'])
def display():
    # Get JWT token from request headers
    # Decode JWT token to extract username and user_id
    # Query user_images table to get image paths for the user
    # Build function to fetch image paths from user_images table and store in user_images list 
    user_images = []


    # Define output video parameters
    output_width = 1920
    output_height = 1080
    fps = 24

    # Create a list to hold video clips
    clips = []

    # Loop through each image path
    for image_path in user_images:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_resized = resize_with_black_fill(img, output_width, output_height)

        clip = ImageClip(img_resized, duration=1/fps)

        clips.append(clip)

    # Concatenate all clips into a single video
    final_clip = concatenate_videoclips(clips)

    # Define temporary directory to store video
    # Define temporary file path for the video
    # Write video to temporary file
    # Send video file to user 

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)