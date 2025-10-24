#!/bin/bash
set -euo pipefail

# ===== Configuration =====
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"; exit' INT TERM EXIT
LOG_FILE="${TEMP_DIR}/encrypt.log"
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
Encrypt File Tool v${VERSION}
Securely encrypts a file using AES-256 and protects the key with AWS KMS.

Usage: $(basename "$0") [OPTIONS] <input_file> <kms_key_arn>

Options:
  -o, --output PATH     Output directory for encrypted files (default: same as input)
  -a, --algorithm ALG   KMS encryption algorithm (default: RSAES_OAEP_SHA_256)
  -i, --ivec IV         Provide custom initialization vector (hex format)
  -s, --salt SALT       Provide custom salt (hex format)
  -h, --help            Display this help message
  -v, --version         Display version information

Example:
  $(basename "$0") secret.txt arn:aws:kms:region:account:key/key-id
  $(basename "$0") --output /secure/dir secret.txt arn:aws:kms:region:account:alias/my-key

EOF
}

# ===== Main Script =====
# Check dependencies
check_dependencies

# Default values
OUTPUT_DIR=""
KMS_ALGORITHM="RSAES_OAEP_SHA_256"
CUSTOM_IV=""
CUSTOM_SALT=""

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -a|--algorithm)
            KMS_ALGORITHM="$2"
            shift 2
            ;;
        -i|--ivec)
            CUSTOM_IV="$2"
            shift 2
            ;;
        -s|--salt)
            CUSTOM_SALT="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--version)
            echo "Encrypt File Tool v${VERSION}"
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

INPUT_FILE="$1"
KMS_KEY_ARN="$2"

# Validate input file
if [ ! -f "$INPUT_FILE" ]; then
    log "ERROR" "Input file '$INPUT_FILE' not found"
    exit 1
fi

# Set output directory
if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="$(dirname "$INPUT_FILE")"
fi

# Create output directory if it doesn't exist
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR" || { log "ERROR" "Could not create output directory '$OUTPUT_DIR'"; exit 1; }
fi

# Set output filenames
INPUT_FILENAME="$(basename "$INPUT_FILE")"
ENCRYPTED_FILE="${OUTPUT_DIR}/${INPUT_FILENAME}.enc"
KEY_FILE="${OUTPUT_DIR}/${INPUT_FILENAME}.key"
METADATA_FILE="${OUTPUT_DIR}/${INPUT_FILENAME}.meta"

# Generate a random 256-bit (32-byte) AES key
log "INFO" "Generating AES key..."
AES_KEY_FILE="${TEMP_DIR}/aes_key"
openssl rand 32 | base64 > "$AES_KEY_FILE"
AES_KEY=$(<"$AES_KEY_FILE")

# Additional encryption arguments based on custom parameters
OPENSSL_ARGS=()
if [ -n "$CUSTOM_IV" ]; then
    echo -n "$CUSTOM_IV" | xxd -r -p > "${TEMP_DIR}/iv"
    OPENSSL_ARGS+=(-iv "$(xxd -p "${TEMP_DIR}/iv")")
fi

if [ -n "$CUSTOM_SALT" ]; then
    echo -n "$CUSTOM_SALT" | xxd -r -p > "${TEMP_DIR}/salt"
    OPENSSL_ARGS+=(-S "$(xxd -p "${TEMP_DIR}/salt")")
fi

# Encrypt the file with the AES key
log "INFO" "Encrypting file..."
OPENSSL_CMD=(openssl enc -aes-256-cbc)
if [ ${#OPENSSL_ARGS[@]} -eq 0 ]; then
    OPENSSL_CMD+=(-salt)
else
    OPENSSL_CMD+=("${OPENSSL_ARGS[@]}")
fi

"${OPENSSL_CMD[@]}" -in "$INPUT_FILE" -out "$ENCRYPTED_FILE" -base64 -k "$AES_KEY" -pbkdf2 -iter 10000 -md sha256

if [ $? -ne 0 ]; then
    log "ERROR" "File encryption failed"
    secure_delete "$AES_KEY_FILE"
    secure_delete "$ENCRYPTED_FILE"
    exit 1
fi

# Encrypt the AES key with KMS
log "INFO" "Encrypting AES key with KMS using $KMS_ALGORITHM..."
KMS_OUTPUT_FILE="${TEMP_DIR}/kms_output.json"

aws kms encrypt \
    --key-id "$KMS_KEY_ARN" \
    --plaintext "$AES_KEY" \
    --encryption-algorithm "$KMS_ALGORITHM" \
    --output json > "$KMS_OUTPUT_FILE"

if [ $? -ne 0 ]; then
    log "ERROR" "KMS encryption failed"
    secure_delete "$AES_KEY_FILE"
    secure_delete "$ENCRYPTED_FILE"
    secure_delete "$KMS_OUTPUT_FILE"
    exit 1
fi

# Extract encrypted key and key ID
ENCRYPTED_KEY=$(jq -r '.CiphertextBlob' "$KMS_OUTPUT_FILE")
KEY_ID=$(jq -r '.KeyId' "$KMS_OUTPUT_FILE")

# Save the encrypted AES key
echo "$ENCRYPTED_KEY" > "$KEY_FILE"

# Save metadata
cat > "$METADATA_FILE" << EOF
{
  "version": "${VERSION}",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "filename": "${INPUT_FILENAME}",
  "encryption": {
    "file_algorithm": "AES-256-CBC",
    "key_algorithm": "${KMS_ALGORITHM}",
    "pbkdf2_iterations": 10000,
    "hash_algorithm": "sha256"
  },
  "kms": {
    "key_id": "${KEY_ID}"
  }
}
EOF

FILE_SIZE=$(stat -c%s "$INPUT_FILE" 2>/dev/null || stat -f%z "$INPUT_FILE")
ENCRYPTED_SIZE=$(stat -c%s "$ENCRYPTED_FILE" 2>/dev/null || stat -f%z "$ENCRYPTED_FILE")

log "SUCCESS" "Encryption complete!"
log "INFO" "Original file size: $(numfmt --to=iec-i --suffix=B ${FILE_SIZE} 2>/dev/null || echo "${FILE_SIZE} bytes")"
log "INFO" "Encrypted file size: $(numfmt --to=iec-i --suffix=B ${ENCRYPTED_SIZE} 2>/dev/null || echo "${ENCRYPTED_SIZE} bytes")"
log "INFO" "Encrypted file: ${ENCRYPTED_FILE}"
log "INFO" "Encrypted key: ${KEY_FILE}"
log "INFO" "Metadata file: ${METADATA_FILE}"

# Clean up sensitive files
secure_delete "$AES_KEY_FILE"
secure_delete "$KMS_OUTPUT_FILE"

# Clean up variables containing sensitive data
AES_KEY=""