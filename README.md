This repo provide an S3 proxy in the form of container, providing
- no authentication to upload/download S3 object
- S3 proxy will perform authentication against S3 endpoint

This container may be useful in certain use case like if you want to load document in your private S3 bucket for your RAG system, supporting simple API call without authentication.

__Steps:__
1. Build the container with this command <br>
`#docker build -t s3-proxy .`
2. Update values in environment file (.env)
3. Perform API call
Curl example for each function
- List files: <br>
`curl -X GET "http://localhost:5001/list"`
- Upload file: <br>
`curl -X POST http://localhost:5001/upload -F "file=@/location/yourfile.txt"`
- Download file: <br>
`curl -X GET "http://localhost:5001/download?filename=yourfile.txt" -o yourfile_downloaded.txt`
- Delete file: <br>
`curl -X DELETE "http://localhost:5001/delete?filename=yourfile.txt"`
