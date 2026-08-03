from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline.component_detector import detect_plumbing_parts
from pipeline.plumbing_validator import verify_plumbing_assembly

app = FastAPI(title="Plumbing Surveillance & Part Extraction Engine", version="1.0")

class FeedRequest(BaseModel):
    video_path: str
    zone_id: str

class ValidationRequest(BaseModel):
    fitting_id: str
    action_log: list

@app.post("/api/v1/track-plumbing")
def track_plumbing(request: FeedRequest):
    try:
        # Detects plumbing parts and hand manipulation actions in video streams
        results = detect_plumbing_parts(request.video_path, request.zone_id)
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/verify-spec")
def verify_spec(request: ValidationRequest):
    # Verifies if the installation sequence meets plumbing and code requirements
    validation = verify_plumbing_assembly(request.fitting_id, request.action_log)
    return {"status": "success", "validation": validation}
  
