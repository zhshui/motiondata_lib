#!/usr/bin/env bash
set -euo pipefail
editor_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export LD_LIBRARY_PATH="$editor_dir/.runtime/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
input_path="${1:-.}"
if [[ -f "$input_path" ]]; then
    motion_file="$(realpath -- "$input_path")"
    dataset_dir="$(mktemp -d /tmp/h1-motion-input.XXXXXX)"
    cleanup() {
        rm -f -- "$dataset_dir/$(basename -- "$motion_file")"
        rmdir -- "$dataset_dir"
    }
    trap cleanup EXIT
    ln -s -- "$motion_file" "$dataset_dir/$(basename -- "$motion_file")"
elif [[ -d "$input_path" ]]; then
    dataset_dir="$input_path"
else
    printf 'Input file or directory does not exist: %s\nUsage: %s [motion.npz or directory]\n' "$input_path" "$0" >&2
    exit 1
fi
"$editor_dir/.venv/bin/python" "$editor_dir/main.py" "$dataset_dir" --robot unitree_h1 --format supermimic
