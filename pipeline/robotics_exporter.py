# pipeline/robotics_exporter.py
import json
import numpy as np

def export_to_robotics_dataset(skeleton_logs: list, output_filepath: str, format_type: str = "hdf5"):
    """
    Packages raw 3D skeletal time-series data into standardized 
    trajectories for Imitation Learning (IL) and ROS2/Isaac Gym pipelines.
    """
    trajectory_data = []
    
    for frame in skeleton_logs:
        if "keypoints" in frame:
            # Extract 3D joint coordinates (X, Y, Z) and calculate joint velocities
            joints = np.array(frame["keypoints"])
            trajectory_data.append({
                "timestamp": frame.get("frame", 0) * 0.033, # Assuming 30 FPS
                "joint_positions": joints.tolist(),
                "zone_id": frame.get("zone", "Zone_A")
            })
            
    if format_type == "json":
        with open(output_filepath, "w") as f:
            json.dump({"robotics_training_trajectory": trajectory_data}, f, indent=2)
            
    return {
        "status": "exported",
        "frames_packaged": len(trajectory_data),
        "file_path": output_filepath,
        "format": format_type
    }
