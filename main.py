import cv2
from PIL import Image
import numpy as np
import os

def main():
    """Main function to create a combined video from individual videos of images."""
    try:
        folder_path = get_folder_path()
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

        if not image_files:
            raise ValueError("No image files found in the specified folder.")
        
        image_paths = [os.path.join(folder_path, img) for img in image_files]
        print(f"Images to be processed: {image_files}")

        video_folder = os.path.join(folder_path, 'videos')
        os.makedirs(video_folder, exist_ok=True)
        
        # Create individual 1-second videos for each image
        video_paths = []
        for idx, image_path in enumerate(image_paths):
            video_path = os.path.join(video_folder, f'image_video_{idx}.mp4')
            create_individual_video(image_path, video_path, fps=1)  # Create 1-second video for each image
            video_paths.append(video_path)

        # Combine all individual videos into one final video
        output_video = os.path.join(folder_path, 'combined_video.mp4')
        combine_videos(video_paths, output_video)
    
    except Exception as e:
        print(f"Error: {e}")

def get_folder_path():
    """Ask the user to input the path of a folder and validate it."""
    path_input = input('Enter the path of the folder containing images: ')
    
    if not os.path.exists(path_input):
        raise FileNotFoundError("The entered path is incorrect.")
    
    return path_input

def create_individual_video(image_path, output_video_path, fps):
    """Creates a 1-second video from an image."""
    img = Image.open(image_path).convert('RGB')
    width, height = img.size

    # Initialize video writer with appropriate codec, FPS, and frame size
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Convert image to OpenCV format (BGR)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Write the same image multiple times to create a 1-second video at the specified FPS
    for _ in range(fps):  # 1 frame per second for 1 second
        video_writer.write(img_cv)

    # Release the video writer
    video_writer.release()
    print(f"1-second video saved as {output_video_path}")

def combine_videos(video_paths, output_video_path):
    """Combines a list of videos into one video."""
    # Get the first video to retrieve properties (size, fps, etc.)
    first_video = cv2.VideoCapture(video_paths[0])
    width = int(first_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(first_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(first_video.get(cv2.CAP_PROP_FPS))
    first_video.release()

    # Initialize the final video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Loop through all video files and write them into the final video
    for video_path in video_paths:
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            video_writer.write(frame)
        cap.release()

    # Release the final video writer
    video_writer.release()
    print(f"Final combined video saved as {output_video_path}")

if __name__ == "__main__":
    main()
