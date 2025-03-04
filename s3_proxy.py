from flask import Flask, request, send_file, jsonify
import boto3
import os
import requests
from requests_aws4auth import AWS4Auth

app = Flask(__name__)

# Load environment variables
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION_NAME = os.getenv("S3_REGION_NAME")

# AWS Authentication for requests.put()
auth = AWS4Auth(S3_ACCESS_KEY, S3_SECRET_KEY, S3_REGION_NAME, "s3")

# Boto3 S3 Client
S3_CLIENT = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION_NAME
)

@app.route("/list", methods=["GET"])
def list_objects():
    """List objects in the S3 bucket."""
    try:
        response = S3_CLIENT.list_objects_v2(Bucket=S3_BUCKET_NAME)
        objects = [obj["Key"] for obj in response.get("Contents", [])]
        return jsonify(objects)
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/download", methods=["GET"])
def download_file():
    """Download a file from S3."""
    filename = request.args.get("filename")
    if not filename:
        return {"error": "Filename is required"}, 400

    local_path = f"/tmp/{filename}"
    s3_url = f"{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}/{filename}"

    response = requests.get(s3_url, auth=auth)
    if response.status_code == 200:
        with open(local_path, "wb") as file:
            file.write(response.content)
        return send_file(local_path, as_attachment=True)
    else:
        return {"error": f"Download failed: {response.text}"}, response.status_code

@app.route("/delete", methods=["DELETE"])
def delete_file():
    """Delete a file from S3."""
    filename = request.args.get("filename")
    if not filename:
        return {"error": "Filename is required"}, 400

    try:
        S3_CLIENT.delete_object(Bucket=S3_BUCKET_NAME, Key=filename)
        return {"message": f"'{filename}' deleted successfully"}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/upload", methods=["POST"])
def upload_file():
    """Upload a file to S3 using requests.put()."""
    if "file" not in request.files:
        return {"error": "No file part in the request"}, 400

    file = request.files["file"]
    if file.filename == "":
        return {"error": "No selected file"}, 400

    s3_url = f"{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}/{file.filename}"

    headers = {
        "x-amz-content-sha256": "UNSIGNED-PAYLOAD",
        "Content-Type": "application/octet-stream",
    }

    response = requests.put(s3_url, data=file.read(), headers=headers, auth=auth)

    if response.status_code in [200, 201]:
        return {"message": f"'{file.filename}' uploaded successfully"}
    else:
        return {"error": f"Upload failed: {response.text}"}, response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
