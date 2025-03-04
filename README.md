This repo provide an S3 proxy in the form of container, providing
- no authentication to upload/download S3 object
- S3 proxy will perform authentication against S3 endpoint

This container may be useful in certain use case like if you want to load document in your private S3 bucket for your RAG system, supporting simple API call without authentication.

Build the container with this command
#docker build -t s3-proxy .
