import json
import functions_framework
from google.cloud import storage

# In production, we use the real Google Cloud Storage library
storage_client = storage.Client()

def orchestrator_logic(bucket_name, file_name):
    """Core stateless routing logic."""
    print(f"Processing file: {file_name} in bucket: {bucket_name}")
    
    # 1. Fetch the blueprint from the bucket
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob("pipelines/audio_intel_v3.json")
    
    try:
        blueprint = json.loads(blob.download_as_text())
        print(f"Loaded active blueprint: {blueprint['pipeline_id']}")
    except Exception as e:
        print(f"Error loading blueprint: {e}")
        return "Blueprint Error"

    # 2. Logic execution (routing, model calls, etc.)
    return "Success"

@functions_framework.cloud_event
def gcs_orchestrator_router(cloud_event):
    """Entry point triggered by GCS bucket uploads."""
    data = cloud_event.data
    bucket = data["bucket"]
    name = data["name"]
    
    # Ignore folder creation events
    if name.endswith("/"):
        return "OK", 200
        
    orchestrator_logic(bucket, name)
    return "OK", 200

@functions_framework.http
def http_orchestrator_gateway(request):
    """HTTPS Entry point for direct API calls."""
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    request_json = request.get_json(silent=True)
    
    if not request_json or 'bucket' not in request_json or 'file_name' not in request_json:
        return {"error": "Missing bucket or file_name in payload"}, 400

    bucket = request_json['bucket']
    file_name = request_json['file_name']
    
    # Run the exact same stateless logic
    result = orchestrator_logic(bucket, file_name)
    
    headers = {'Access-Control-Allow-Origin': '*'}
    return {"status": result, "processed_file": file_name}, 200, headers
