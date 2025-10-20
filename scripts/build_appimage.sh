#!/usr/bin/env bash
set -euo pipefail

APP_NAME="kazmiskender"
DIST_DIR="dist/appimage"
BUILD_DIR="build/appimage"

rm -rf "$DIST_DIR" "$BUILD_DIR"
mkdir -p "$DIST_DIR" "$BUILD_DIR"

pyinstaller pyinstaller.spec --distpath "$BUILD_DIR" --workpath "$BUILD_DIR/work"

if ! command -v linuxdeploy >/dev/null 2>&1; then
  echo "linuxdeploy not found. Install from https://github.com/linuxdeploy/linuxdeploy/releases"
  exit 1
fi

linuxdeploy --appdir "$BUILD_DIR/$APP_NAME" --executable "$BUILD_DIR/$APP_NAME/$APP_NAME" --desktop-file app.desktop --output appimage --plugin qt

mv ./*.AppImage "$DIST_DIR/"
echo "AppImage created under $DIST_DIR"
