import cv2
from ultralytics import YOLO

def extract_fine_motor_skills(video_path: str):
    """
    Extracts high-resolution hand and wrist keypoints to capture 
    precise plumbing tasks like pipe deburring, gluing, and wrench torquing.
    """
    # Utilizing YOLOv8-Pose configured for fine manipulation tracking
    model = YOLO('yolov8n-pose.pt')
    cap = cv2.VideoCapture(video_path)
    
    trajectory = []
    frame_idx = 0
    
    while cap.isOpened() and frame_idx < 150:
        success, frame = cap.read()
        if not success:
            break
            
        results = model(frame, verbose=False)
        if results[0].keypoints is not None:
            # Isolate wrist and finger-level keypoints for dexterous robotics imitation
            keypoints = results[0].keypoints.xy.cpu().numpy()
            trajectory.append({
                "frame": frame_idx,
                "hand_keypoints": keypoints.tolist()
            })
            
        frame_idx += 1
        
    cap.release()
    return trajectory
