import cv2
from deepface import DeepFace
import os
import json
import time
import argparse

# Function to extract faces from a video and save coordinates in a JSON file
def extract_faces_from_video(video_path, output_folder, json_path, detector_backend, downsampling_rate=1):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the video
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    face_data = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if (downsampling_rate > 1) and (frame_count % downsampling_rate != 0):
            frame_count += 1
            continue
        # Detect faces in the frame
        try:
            faces = DeepFace.extract_faces(frame, 
                                           detector_backend,
                                           enforce_detection=False,
                                           anti_spoofing=False)
            face_res  = {
                "frame": frame_count,
                "faces": []
            }
            for _, face in enumerate(faces):
                # Save face coordinates
                face_res['faces'].append({
                    'coordinates': face['facial_area'],
                    'confidence': face['confidence']
                })
            face_data.append(face_res)
        except:
            pass

        frame_count += 1

    cap.release()

    # Save face data to JSON file in output folder
    with open(json_path, 'w') as json_file:
        json.dump(face_data, json_file, indent=4)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process video to extract faces.')
    parser.add_argument('--video_path', type=str, default='/app/data/first_10_seconds.mp4', help='Path to the video file in data directory. Use /app/data/<video_filename.mp4> format')
    parser.add_argument('--downsampling_rate', type=int, default=1, help='Downsampling rate for the video frames')

    args = parser.parse_args()

    sample_video_path = args.video_path
    assert os.path.exists(sample_video_path), f'Video file not found at: {sample_video_path}'
    downsampling_rate = args.downsampling_rate
    assert downsampling_rate > 0, 'Downsampling rate should be a positive integer'
    
    video_filename = os.path.basename(sample_video_path).split('.')[0]

    backend = 'retinaface'
    start_time = time.time()  # Start time measurement
    print(f'Processing video with backend: {backend}')
    # add backend name to file paths
    output_folder = f'/app/data/processed_video_{backend}'
    json_path = f'/app/data/processed_video_{backend}/extracted_faces_{video_filename}.json'
    extract_faces_from_video(sample_video_path, output_folder, json_path, detector_backend=backend, downsampling_rate=downsampling_rate)
    end_time = time.time()  # End time measurement
    print(f'Processing video with backend: {backend} took {end_time - start_time} seconds')