#!/bin/sh

# Wait for MinIO to be ready
echo "Waiting for MinIO to start..."
until curl -f http://localhost:9000/minio/health/live; do
    echo "MinIO is not ready yet..."
    sleep 2
done

echo "MinIO is ready. Setting up bucket..."

# Configure mc (MinIO Client)
mc alias set myminio http://localhost:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}

# Create the bucket
mc mb myminio/template-bucket --ignore-existing

# Create bucket policy for public access
cat > /tmp/bucket-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::template-bucket",
                "arn:aws:s3:::template-bucket/*"
            ]
        }
    ]
}
EOF

# Apply the public policy
mc anonymous set-json /tmp/bucket-policy.json myminio/template-bucket

# Clean up
rm -f /tmp/bucket-policy.json

echo "Bucket 'template-bucket' is now public!"
echo "Access files at: http://localhost:9000/template-bucket/"