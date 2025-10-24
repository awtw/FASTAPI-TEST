#!/bin/bash

# Help function
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Run Alembic migrations with optional skip flags"
    echo ""
    echo "Options:"
    echo "  -r, --skip-revision    Skip the revision generation step"
    echo "  -u, --skip-upgrade     Skip the upgrade head step"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Run both revision and upgrade"
    echo "  $0 -r                 # Skip revision, only run upgrade"
    echo "  $0 -u                 # Skip upgrade, only run revision"
    echo "  $0 -r -u              # Skip both (no operation)"
}

# Initialize flags
SKIP_REVISION=false
SKIP_UPGRADE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--skip-revision)
            SKIP_REVISION=true
            shift
            ;;
        -u|--skip-upgrade)
            SKIP_UPGRADE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# shellcheck disable=SC2164
cd /run

# Run revision generation if not skipped
if [ "$SKIP_REVISION" = false ]; then
    # shellcheck disable=SC2034
    current_date=$(date +"%Y-%m-%d %H:%M:%S")
    echo "Generating Alembic revision..."
    alembic revision --autogenerate -m "revision generated on ${current_date}"
else
    echo "Skipping revision generation"
fi

# Run upgrade if not skipped
if [ "$SKIP_UPGRADE" = false ]; then
    echo "Upgrading database to head..."
    alembic upgrade head
else
    echo "Skipping database upgrade"
fi