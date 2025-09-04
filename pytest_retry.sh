#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


RETRIES=2
WAIT_BETWEEN=10
BACKUP_DIR=original_test_run

declare -a BACKUP_FROM_FIRST_RUN=()

usage() {
  cat <<EOF
Pytest wrapper that retries failed tests while preserving original test artifacts.

Usage: $0 [options] -- [pytest args...]

Options:
  -r, --retry NUM        Number of retry attempts (default: ${RETRIES}).
                         Retries happen only if the first pytest run exits with code 1 (tests failed).
  -w, --wait SECONDS     Seconds to wait between retries (default: ${WAIT_BETWEEN}).
  -b, --backup PATH      File or directory to back up after the first run *if* we will retry.
                         Can be given multiple times.
  -h, --help             Show this help.

Behavior:
  • After first run:
      - If exit code != 1, the script exits immediately with that code.
      - If exit code = 1, it backs up the listed PATHs, then retries with 'pytest --lf'.
  • On each retry, the full original pytest args are reused with '--lf'.
  • Final exit code is pytest's last exit code.
EOF
}

PARSED=$(getopt -o r:w:hb: -l retry:,wait:,help,backup: -- "$@") || {
  usage
  exit 2
}
eval set -- "$PARSED"

while true; do
  case "$1" in
  -r | --retry)
    RETRIES="$2"
    shift 2
    ;;
  -w | --wait)
    WAIT_BETWEEN="$2"
    shift 2
    ;;
  -h | --help)
    usage
    exit 0
    ;;
  -b | --backup)
    BACKUP_FROM_FIRST_RUN+=("$2")
    shift 2
    ;;
  --)
    shift
    break
    ;;
  *)
    echo "Unknown: $1"
    exit 3
    ;;
  esac
done

command -v pytest >/dev/null 2>&1 || {
  echo "'pytest' not found" >&2
  exit 127
}

pytest "$@"
rc=$?

# Only retry tests if otherwise everything was okay, but some of the tests failed
# https://docs.pytest.org/en/stable/reference/exit-codes.html
if [[ rc -ne 1 ]]; then
  exit $rc
fi

mkdir -p $BACKUP_DIR
# backup original test results
for file in "${BACKUP_FROM_FIRST_RUN[@]}"; do
  [[ -e "$file" ]] && cp -a -- "$file" "$BACKUP_DIR/"
done

for ((i = 1; i <= RETRIES; i++)); do
  printf "\nATTEMPT %d/%d: Sleeping %d seconds before retrying failed tests\n" $i "$RETRIES" "$WAIT_BETWEEN"
  sleep "$WAIT_BETWEEN"
  printf "ATTEMPT %d/%d: Retrying failed tests\n\n" $i "$RETRIES"

  pytest --lf "$@"
  rc=$?

  if [[ rc -ne 1 ]]; then
    break
  fi
done

for file in "${BACKUP_FROM_FIRST_RUN[@]}"; do
  if [[ -e "$BACKUP_DIR/$(basename "$file")" ]]; then
    cp -a -- "$BACKUP_DIR/$(basename "$file")" "$file"
  fi
done

exit $rc
