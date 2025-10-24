#!/bin/bash

# Entrypoint script for MySQL backup container
# This script sets up cron jobs and keeps the container running

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Set up environment variables for cron
printenv | grep -E '^MYSQL_|^BACKUP_' > /etc/environment

# Create cron job based on BACKUP_SCHEDULE environment variable
BACKUP_SCHEDULE="${BACKUP_SCHEDULE:-0 2 * * *}"  # Default: 2 AM daily

# Create crontab entry
echo "${BACKUP_SCHEDULE} /usr/local/bin/backup.sh >> /var/log/mysql-backup.log 2>&1" > /etc/crontabs/root

# Create log file
touch /var/log/mysql-backup.log

# Start cron daemon in foreground mode
crond -f -l 2 &
CRON_PID=$!

log "=== MySQL Backup Container Started ==="
log "Backup schedule: ${BACKUP_SCHEDULE}"
log "Backup retention: ${BACKUP_RETENTION_DAYS:-7} days"
log "Target database: ${MYSQL_DATABASE:-template_db}"

# Run initial backup if BACKUP_ON_STARTUP is set
if [ "${BACKUP_ON_STARTUP}" = "true" ]; then
    log "Running initial backup..."
    /usr/local/bin/backup.sh
fi

# Keep container running and tail the log
tail -f /var/log/mysql-backup.log &

# Wait for cron daemon
wait $CRON_PID 