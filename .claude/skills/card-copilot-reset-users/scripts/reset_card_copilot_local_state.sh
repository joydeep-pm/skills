#!/usr/bin/env bash
set -euo pipefail

PACKAGE="com.cardcopilot.app"
APK_PATH="android/app/build/outputs/apk/release/app-release.apk"

usage() {
  cat <<USAGE
Usage: $0 [--package <android.package>] [--apk <path/to/apk>]

Defaults:
  --package com.cardcopilot.app
  --apk android/app/build/outputs/apk/release/app-release.apk
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --package)
      PACKAGE="${2:-}"
      shift 2
      ;;
    --apk)
      APK_PATH="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

resolve_adb() {
  if command -v adb >/dev/null 2>&1; then
    command -v adb
    return 0
  fi

  local fallback="$HOME/Library/Android/sdk/platform-tools/adb"
  if [[ -x "$fallback" ]]; then
    echo "$fallback"
    return 0
  fi

  echo "ERROR: adb not found in PATH and fallback path is missing" >&2
  return 1
}

ADB_BIN="$(resolve_adb)"

"$ADB_BIN" start-server >/dev/null

if ! "$ADB_BIN" get-state >/dev/null 2>&1; then
  echo "ERROR: no connected Android device detected." >&2
  "$ADB_BIN" devices -l >&2 || true
  exit 1
fi

echo "[reset] Attempting pm clear for $PACKAGE ..."
if "$ADB_BIN" shell pm clear "$PACKAGE" >/tmp/cardcopilot_pm_clear.log 2>&1; then
  echo "[reset] pm clear succeeded."
else
  echo "[reset] pm clear blocked. Falling back to uninstall/reinstall."
  cat /tmp/cardcopilot_pm_clear.log || true

  "$ADB_BIN" uninstall "$PACKAGE" >/dev/null 2>&1 || true

  if [[ -f "$APK_PATH" ]]; then
    echo "[reset] Installing APK: $APK_PATH"
    "$ADB_BIN" install -r "$APK_PATH"
  else
    echo "ERROR: APK not found at '$APK_PATH'. Build it first, then rerun." >&2
    exit 1
  fi
fi

echo "[reset] Launching app..."
"$ADB_BIN" shell monkey -p "$PACKAGE" -c android.intent.category.LAUNCHER 1 >/dev/null

echo "[reset] Done. App state reset complete."
