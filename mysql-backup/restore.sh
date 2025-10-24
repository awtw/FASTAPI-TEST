#!/bin/bash

# MySQL restore script
# This script restores a MySQL database from a compressed backup file

# Configuration
BACKUP_DIR="/backups"
MYSQL_HOST="${MYSQL_HOST:-mysql}"
MYSQL_PORT="${MYSQL_PORT:-3306}"
MYSQL_USER="${MYSQL_USER:-root}"
MYSQL_PASSWORD="${MYSQL_PASSWORD:-root}"
MYSQL_DATABASE="${MYSQL_DATABASE:-template_db}"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to list available backups
list_backups() {
    log "Available backups:"
    ls -lh "${BACKUP_DIR}"/mysql_backup_*.sql.gz 2>/dev/null | nl -v 0 || {
        log "No backups found in ${BACKUP_DIR}"
        return 1
    }
}

# Function to restore backup
restore_backup() {
    local backup_file="$1"
    
    if [ ! -f "${backup_file}" ]; then
        log "ERROR: Backup file not found: ${backup_file}"
        return 1
    fi
    
    log "Starting restore from: ${backup_file}"
    log "WARNING: This will overwrite the existing database!"
    
    # Perform the restore
    if gunzip -c "${backup_file}" | mysql \
        -h "${MYSQL_HOST}" \
        -P "${MYSQL_PORT}" \
        -u "${MYSQL_USER}" \
        -p"${MYSQL_PASSWORD}"; then
        
        log "Restore completed successfully"
        return 0
    else
        log "ERROR: Restore failed!"
        return 1
    fi
}

# Main execution
main() {
    log "=== MySQL Restore Script Started ==="
    
    # Wait for MySQL to be ready
    until mysqladmin ping -h"${MYSQL_HOST}" -P"${MYSQL_PORT}" -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" --silent; do
        log "Waiting for MySQL to be ready..."
        sleep 5
    done
    
    # Check if backup file was provided as argument
    if [ $# -eq 1 ]; then
        # Restore specific backup file
        restore_backup "$1"
    else
        # Interactive mode - list backups and let user choose
        if list_backups; then
            echo
            read -p "Enter the number of the backup to restore (or full path): " selection
            
            if [[ "$selection" =~ ^[0-9]+$ ]]; then
                # User entered a number, get the corresponding file
                backup_file=$(ls "${BACKUP_DIR}"/mysql_backup_*.sql.gz 2>/dev/null | sed -n "$((selection+1))p")
                if [ -n "$backup_file" ]; then
                    restore_backup "$backup_file"
                else
                    log "ERROR: Invalid selection"
                    exit 1
                fi
            else
                # User entered a path
                restore_backup "$selection"
            fi
        else
            exit 1
        fi
    fi
}

# Run main function
main "$@" 