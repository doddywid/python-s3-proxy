from flask import Flask, request, send_file
import boto3
import os

app = Flask(__name__)

S3_CLIENT = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
    region_name=os.getenv("S3_REGION_NAME")
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

@app.route("/get-document", methods=["GET"])
def get_document():
    filename = request.args.get("filename")
    if not filename:
        return {"error": "Filename is required"}, 400
    
    local_path = f"/tmp/{filename}"
    
    # Download file from S3 to a temporary location
    S3_CLIENT.download_file(BUCKET_NAME, filename, local_path)

    # Serve file as an attachment
    return send_file(local_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
