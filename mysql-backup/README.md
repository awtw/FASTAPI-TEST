# MySQL Auto Backup Setup

This directory contains the MySQL automatic backup solution for the FastAPI template project.

## Architecture

This backup solution uses a **lightweight Alpine Linux container** that only includes:
- MySQL client tools (`mysqldump`, `mysql`) for backup/restore operations
- Cron daemon for scheduling
- Bash for scripting

**No MySQL server is included** - the backup container connects to your existing MySQL container over the Docker network. This approach:
- Minimizes resource usage (Alpine image is ~10MB vs MySQL image ~600MB)
- Reduces security surface area
- Follows the single-responsibility principle
- Allows independent scaling and management

## Features

- **Automatic scheduled backups** using cron
- **Compressed backups** (gzip) to save disk space
- **Backup rotation** with configurable retention period
- **Easy restore** functionality
- **Container-based** solution that runs alongside your MySQL container

## Configuration

The backup service can be configured through environment variables in `docker-compose.yaml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `MYSQL_HOST` | mysql | MySQL server hostname |
| `MYSQL_PORT` | 3306 | MySQL server port |
| `MYSQL_USER` | root | MySQL username |
| `MYSQL_PASSWORD` | root | MySQL password |
| `MYSQL_DATABASE` | template_db | Database to backup |
| `BACKUP_SCHEDULE` | 0 2 * * * | Cron schedule (default: 2 AM daily) |
| `BACKUP_RETENTION_DAYS` | 7 | Number of days to keep backups |
| `BACKUP_ON_STARTUP` | true | Create backup when container starts |

### Cron Schedule Format

The `BACKUP_SCHEDULE` uses standard cron format:
```
* * * * *
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, Sunday = 0 or 7)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

Examples:
- `0 2 * * *` - Daily at 2:00 AM
- `0 */6 * * *` - Every 6 hours
- `30 3 * * 0` - Weekly on Sunday at 3:30 AM
- `0 0 1 * *` - Monthly on the 1st at midnight

## Usage

### Starting the Backup Service

The backup service is included in your docker-compose setup:

```bash
# Start all services including backup
docker-compose up -d

# Start only the backup service
docker-compose up -d mysql-backup
```

### Manual Backup

To create a backup manually:

```bash
docker exec template-mysql-backup /usr/local/bin/backup.sh
```

### Viewing Backup Logs

```bash
# View real-time logs
docker logs -f template-mysql-backup

# View last 100 lines
docker logs --tail 100 template-mysql-backup
```

### Listing Backups

```bash
# List all backups
ls -lh ./volume/mysql_backups/

# From within container
docker exec template-mysql-backup ls -lh /backups/
```

### Restoring from Backup

#### Interactive Restore

```bash
# This will list available backups and let you choose
docker exec -it template-mysql-backup /usr/local/bin/restore.sh
```

#### Direct Restore

```bash
# Restore specific backup file
docker exec template-mysql-backup /usr/local/bin/restore.sh /backups/mysql_backup_template_db_20240115_020000.sql.gz
```

### Backup File Location

Backups are stored in: `./volume/mysql_backups/`

Backup files are named: `mysql_backup_<database>_<timestamp>.sql.gz`

## Backup Strategy Best Practices

1. **Test Restores Regularly**: Periodically test your restore process to ensure backups are valid
2. **Monitor Disk Space**: Ensure sufficient disk space for backups
3. **Off-site Backups**: Consider copying backups to external storage or cloud
4. **Adjust Retention**: Balance between storage space and backup history needs

## Troubleshooting

### Backup Fails

Check logs:
```bash
docker logs template-mysql-backup
```

Common issues:
- MySQL credentials incorrect
- MySQL container not ready
- Insufficient disk space
- Permission issues on backup directory

### Container Won't Start

Ensure the mysql-backup directory and scripts exist:
```bash
ls -la mysql-backup/
```

### Restore Fails

- Ensure MySQL is running
- Check credentials
- Verify backup file integrity:
  ```bash
  gunzip -t ./volume/mysql_backups/backup_file.sql.gz
  ```

## Advanced Usage

### Backing Up to S3/MinIO

You can extend the backup script to upload to S3/MinIO after local backup:

```bash
# Add to backup.sh after successful backup
aws s3 cp "${BACKUP_DIR}/${BACKUP_FILENAME}" s3://your-bucket/mysql-backups/ --endpoint-url=http://minio:9000
```

### Multiple Database Backup

Modify the backup script to loop through multiple databases:

```bash
DATABASES="db1 db2 db3"
for db in $DATABASES; do
    mysqldump ... --databases $db | gzip > backup_${db}_${TIMESTAMP}.sql.gz
done
```

### Notification on Backup Failure

Add notification logic to the backup script:

```bash
if ! perform_backup; then
    # Send notification (email, Slack, etc.)
    curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
         -H 'Content-type: application/json' \
         --data '{"text":"MySQL backup failed!"}'
fi
``` 