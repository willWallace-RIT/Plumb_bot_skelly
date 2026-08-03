import cv2
from ultralytics import YOLO

def process_video_stream(video_path: str, site_zone: str):
    # Load YOLOv8 Pose model (downloads automatically on first run)
    model = YOLO('yolov8n-pose.pt')
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    extracted_skeletons = []

    while cap.isOpened() and frame_count < 300: # Limit frames for MVP processing
        success, frame = cap.read()
        if not success:
            break
            
        # Run inference for keypoints
        results = model(frame, verbose=False)
        if results[0].keypoints is not None:
            keypoints_data = results[0].keypoints.xy.cpu().numpy()
            extracted_skeletons.append({
                "frame": frame_count,
                "zone": site_zone,
                "skeletons_detected": len(keypoints_data),
                "keypoints": keypoints_data.tolist()
            })
            
        frame_count += 1

    cap.release()
    return {
        "processed_frames": frame_count,
        "skeleton_time_series": extracted_skeletons
    }
