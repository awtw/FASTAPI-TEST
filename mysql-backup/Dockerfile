FROM alpine:3.19

# Install MySQL client, bash, and cron
RUN apk add --no-cache \
    mysql-client \
    bash \
    dcron \
    tzdata

# Copy backup scripts
COPY backup.sh /usr/local/bin/backup.sh
COPY restore.sh /usr/local/bin/restore.sh
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Make scripts executable
RUN chmod +x /usr/local/bin/backup.sh \
    && chmod +x /usr/local/bin/restore.sh \
    && chmod +x /usr/local/bin/entrypoint.sh

# Create backup directory
RUN mkdir -p /backups

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"] 