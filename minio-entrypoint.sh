#!/bin/sh

# Start the initialization script in the background
/init-minio.sh &

# Start MinIO server
exec minio server /data --console-address ":9001" 