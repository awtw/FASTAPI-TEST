#!/bin/bash
set -euo pipefail

# ===== Configuration =====
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"; exit' INT TERM EXIT
LOG_FILE="${TEMP_DIR}/decrypt.log"
VERSION="1.1.0"

# ===== Functions =====
log() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" | tee -a "$LOG_FILE"
}

secure_delete() {
    local file="$1"
    if [[ -f "$file" ]]; then
        if command -v shred &> /dev/null; then
            shred -uzn 3 "$file" 2>/dev/null || rm -f "$file"
        else
            rm -f "$file"
        fi
    fi
}

check_dependencies() {
    local missing_deps=()

    for cmd in openssl aws base64 jq; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log "ERROR" "Missing required dependencies: ${missing_deps[*]}"
        exit 1
    fi
}

show_help() {
    cat << EOF
Decrypt File Tool v${VERSION}
Decrypts files encrypted with the companion encryption tool.

Usage: $(basename "$0") [OPTIONS] <encrypted_file> <kms_key_arn>

Options:
  -o, --output PATH     Output directory for decrypted files (default: same as input)
  -n, --name STRING     Custom name for the decrypted file (default: original name)
  -k, --key PATH        Custom path to the key file (default: <encrypted_file>.key)
  -a, --algorithm ALG   KMS decryption algorithm (default: determined from metadata)
  -f, --force           Overwrite existing output file
  -v, --verbose         Enable verbose output
  -h, --help            Display this help message

Example:
  $(basename "$0") secret.txt.enc arn:aws:kms:region:account:key/key-id
  $(basename "$0") --output /safe/dir --name original.txt secret.txt.enc arn:aws:kms:region:account:alias/my-key

EOF
}

# ===== Main Script =====
# Check dependencies
check_dependencies

# Default values
OUTPUT_DIR=""
OUTPUT_NAME=""
KEY_FILE=""
KMS_ALGORITHM=""
FORCE=false
VERBOSE=false

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -n|--name)
            OUTPUT_NAME="$2"
            shift 2
            ;;
        -k|--key)
            KEY_FILE="$2"
            shift 2
            ;;
        -a|--algorithm)
            KMS_ALGORITHM="$2"
            shift 2
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*|--*)
            log "ERROR" "Unknown option $1"
            show_help
            exit 1
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

# Restore positional parameters
set -- "${POSITIONAL_ARGS[@]}"

# Check arguments
if [ "$#" -ne 2 ]; then
    log "ERROR" "Missing required arguments"
    show_help
    exit 1
fi

ENCRYPTED_FILE="$1"
KMS_KEY_ARN="$2"

# Validate encrypted file
if [ ! -f "$ENCRYPTED_FILE" ]; then
    log "ERROR" "Encrypted file '$ENCRYPTED_FILE' not found"
    exit 1
fi

# Set paths
BASE_NAME="${ENCRYPTED_FILE%.enc}"
ENCRYPTED_DIR="$(dirname "$ENCRYPTED_FILE")"
METADATA_FILE="${BASE_NAME}.meta"

# Set key file if not specified
if [ -z "$KEY_FILE" ]; then
    KEY_FILE="${BASE_NAME}.key"
fi

# Check if key file exists
if [ ! -f "$KEY_FILE" ]; then
    log "ERROR" "Key file '$KEY_FILE' not found"
    exit 1
fi

# Set output directory
if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="$ENCRYPTED_DIR"
fi

# Create output directory if it doesn't exist
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR" || { log "ERROR" "Could not create output directory '$OUTPUT_DIR'"; exit 1; }
fi

# Set output name and file
if [ -z "$OUTPUT_NAME" ]; then
    OUTPUT_NAME="$(basename "$BASE_NAME").dec"
fi
OUTPUT_FILE="${OUTPUT_DIR}/${OUTPUT_NAME}"

# Check if output file exists and handle force flag
if [[ -f "$OUTPUT_FILE" && "$FORCE" != true ]]; then
    log "ERROR" "Output file '$OUTPUT_FILE' already exists. Use --force to overwrite."
    exit 1
fi

# Check for metadata and extract algorithm if available
if [[ -f "$METADATA_FILE" && -z "$KMS_ALGORITHM" ]]; then
    if command -v jq &> /dev/null; then
        KMS_ALGORITHM=$(jq -r '.encryption.key_algorithm // "RSAES_OAEP_SHA_256"' "$METADATA_FILE")
        if $VERBOSE; then
            log "INFO" "Using algorithm '$KMS_ALGORITHM' from metadata"
        fi
    fi
fi

# If algorithm is still empty, use default
if [ -z "$KMS_ALGORITHM" ]; then
    KMS_ALGORITHM="RSAES_OAEP_SHA_256"
    if $VERBOSE; then
        log "INFO" "Using default algorithm '$KMS_ALGORITHM'"
    fi
fi

# Read the encrypted key
ENCRYPTED_KEY=$(cat "$KEY_FILE")
ENCRYPTED_KEY_FILE="${TEMP_DIR}/encrypted_key"
echo "$ENCRYPTED_KEY" > "$ENCRYPTED_KEY_FILE"

if $VERBOSE; then
    log "DEBUG" "Encrypted key length (base64): $(echo -n "$ENCRYPTED_KEY" | wc -c) bytes"
    log "DEBUG" "Attempting KMS decryption..."
fi

# Decrypt the AES key using KMS
AES_KEY_FILE="${TEMP_DIR}/aes_key"
KMS_ERROR_FILE="${TEMP_DIR}/kms_error.log"

# Ensure the key is properly base64 decoded before passing to KMS
base64 -d "$ENCRYPTED_KEY_FILE" > "${ENCRYPTED_KEY_FILE}.decoded"

if $VERBOSE; then
    log "DEBUG" "Base64 decoded key size: $(stat -c%s "${ENCRYPTED_KEY_FILE}.decoded" 2>/dev/null || stat -f%z "${ENCRYPTED_KEY_FILE}.decoded") bytes"
fi

aws kms decrypt \
    --key-id "$KMS_KEY_ARN" \
    --ciphertext-blob "fileb://${ENCRYPTED_KEY_FILE}.decoded" \
    --encryption-algorithm "$KMS_ALGORITHM" \
    --output json > "${TEMP_DIR}/kms_output.json" 2>"$KMS_ERROR_FILE" || {
        log "ERROR" "KMS decryption failed"
        if $VERBOSE; then
            log "DEBUG" "KMS error message:"
            cat "$KMS_ERROR_FILE"
        fi
        secure_delete "$ENCRYPTED_KEY_FILE"
        secure_delete "${TEMP_DIR}/kms_output.json"
        exit 1
    }

# Extract plaintext key
jq -r '.Plaintext' "${TEMP_DIR}/kms_output.json" > "$AES_KEY_FILE"
AES_KEY=$(<"$AES_KEY_FILE")

# Decrypt the file with the AES key
log "INFO" "Decrypting file..."
openssl enc -d -aes-256-cbc -salt -in "$ENCRYPTED_FILE" \
    -out "$OUTPUT_FILE" -base64 -k "$AES_KEY" -pbkdf2 -iter 10000 -md sha256 || {
        log "ERROR" "File decryption failed"
        secure_delete "$AES_KEY_FILE"
        secure_delete "$ENCRYPTED_KEY_FILE"
        if [[ -f "$OUTPUT_FILE" ]]; then
            secure_delete "$OUTPUT_FILE"
        fi
        exit 1
    }

# Calculate file sizes
ENCRYPTED_SIZE=$(stat -c%s "$ENCRYPTED_FILE" 2>/dev/null || stat -f%z "$ENCRYPTED_FILE")
DECRYPTED_SIZE=$(stat -c%s "$OUTPUT_FILE" 2>/dev/null || stat -f%z "$OUTPUT_FILE")

log "SUCCESS" "Decryption complete!"
log "INFO" "Encrypted file size: $(numfmt --to=iec-i --suffix=B ${ENCRYPTED_SIZE} 2>/dev/null || echo "${ENCRYPTED_SIZE} bytes")"
log "INFO" "Decrypted file size: $(numfmt --to=iec-i --suffix=B ${DECRYPTED_SIZE} 2>/dev/null || echo "${DECRYPTED_SIZE} bytes")"
log "INFO" "Decrypted file: ${OUTPUT_FILE}"

# Copy log file to output directory if verbose
if $VERBOSE; then
    cp "$LOG_FILE" "${OUTPUT_DIR}/decrypt-$(date +%Y%m%d-%H%M%S).log"
    log "INFO" "Log saved to: ${OUTPUT_DIR}/decrypt-$(date +%Y%m%d-%H%M%S).log"
fi

# Clean up sensitive files
secure_delete "$AES_KEY_FILE"
secure_delete "$ENCRYPTED_KEY_FILE"
secure_delete "${TEMP_DIR}/kms_output.json"

# Clean up variables containing sensitive data
AES_KEY=""