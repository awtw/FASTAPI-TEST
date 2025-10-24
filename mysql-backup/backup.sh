#!/bin/bash

# MySQL backup script with rotation
# This script creates compressed backups and maintains a specified number of backups

# Configuration
BACKUP_DIR="/backups"
MYSQL_HOST="${MYSQL_HOST:-mysql}"
MYSQL_PORT="${MYSQL_PORT:-3306}"
MYSQL_USER="${MYSQL_USER:-root}"
MYSQL_PASSWORD="${MYSQL_PASSWORD:-root}"
MYSQL_DATABASE="${MYSQL_DATABASE:-template_db}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILENAME="mysql_backup_${MYSQL_DATABASE}_${TIMESTAMP}.sql.gz"

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to perform backup
perform_backup() {
    log "Starting backup of database: ${MYSQL_DATABASE}"
    
    # Perform the backup
    if mysqldump \
        -h "${MYSQL_HOST}" \
        -P "${MYSQL_PORT}" \
        -u "${MYSQL_USER}" \
        -p"${MYSQL_PASSWORD}" \
        --single-transaction \
        --routines \
        --triggers \
        --add-drop-database \
        --databases "${MYSQL_DATABASE}" | gzip > "${BACKUP_DIR}/${BACKUP_FILENAME}"; then
        
        log "Backup completed successfully: ${BACKUP_FILENAME}"
        
        # Get backup size
        BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILENAME}" | cut -f1)
        log "Backup size: ${BACKUP_SIZE}"
        
        return 0
    else
        log "ERROR: Backup failed!"
        return 1
    fi
}

# Function to clean old backups
cleanup_old_backups() {
    log "Cleaning up backups older than ${BACKUP_RETENTION_DAYS} days"
    
    # Find and delete old backups
    find "${BACKUP_DIR}" -name "mysql_backup_${MYSQL_DATABASE}_*.sql.gz" -type f -mtime +${BACKUP_RETENTION_DAYS} -exec rm {} \; -exec echo "Deleted: {}" \;
    
    # List remaining backups
    log "Current backups:"
    ls -lh "${BACKUP_DIR}"/mysql_backup_${MYSQL_DATABASE}_*.sql.gz 2>/dev/null || log "No backups found"
}

# Main execution
main() {
    log "=== MySQL Backup Script Started ==="
    
    # Wait for MySQL to be ready (useful on container startup)
    until mysqladmin ping -h"${MYSQL_HOST}" -P"${MYSQL_PORT}" -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" --silent; do
        log "Waiting for MySQL to be ready..."
        sleep 5
    done
    
    # Perform backup
    if perform_backup; then
        # Clean up old backups only if current backup succeeded
        cleanup_old_backups
        log "=== Backup process completed successfully ==="
        exit 0
    else
        log "=== Backup process failed ==="
        exit 1
    fi
}

# Run main function
main 