#!/usr/bin/env bash
set -euo pipefail

SECRETS_DIR=".secrets"
KEY_FILE="$SECRETS_DIR/mock-kms.key"
USAGE="Usage: $0 <init|encrypt|decrypt> [file]

Commands:
  init               Create local mock KMS key material.
  encrypt <file>     Encrypt file -> file.enc using OpenSSL AES-256-GCM.
  decrypt <file>     Decrypt file.enc -> file.dec.
"

cmd=${1:-}
case "$cmd" in
  init)
    mkdir -p "$SECRETS_DIR"
    if [[ -f "$KEY_FILE" ]]; then
      echo "Mock KMS key already exists at $KEY_FILE"
      exit 0
    fi
    head -c 32 /dev/urandom > "$KEY_FILE"
    chmod 600 "$KEY_FILE"
    echo "Generated mock KMS key at $KEY_FILE"
    ;;
  encrypt)
    [[ $# -ge 2 ]] || { echo "$USAGE"; exit 1; }
    [[ -f "$KEY_FILE" ]] || { echo "Run $0 init first"; exit 1; }
    infile=$2
    openssl enc -aes-256-gcm -salt -pbkdf2 -in "$infile" -out "$infile.enc" -pass file:"$KEY_FILE"
    ;;
  decrypt)
    [[ $# -ge 2 ]] || { echo "$USAGE"; exit 1; }
    [[ -f "$KEY_FILE" ]] || { echo "Run $0 init first"; exit 1; }
    infile=$2
    openssl enc -d -aes-256-gcm -salt -pbkdf2 -in "$infile" -out "${infile%.enc}.dec" -pass file:"$KEY_FILE"
    ;;
  *)
    echo "$USAGE"
    exit 1
    ;;
 esac
