# Hermes Desktop App — Build & Install Reference

## Source Location
- Repo: ~/.hermes/hermes-agent/apps/desktop/
- Package.json name: "hermes", version 0.15.1
- Electron 40.9.3, Node 22+ required

## Build Steps
1. cd ~/.hermes/hermes-agent/apps/desktop
2. npm install --install-workspaces=false --legacy-peer-deps --ignore-scripts
   (Workspace hoisting issue — packages go to root node_modules)
3. npx tsc -b  (TypeScript compile)
4. npx vite build  (Renderer build) — must run with background=true
5. node scripts/assert-dist-built.cjs  (Verify dist/)
6. node scripts/stage-native-deps.cjs  (Stage node-pty native deps)
7. npm run builder -- --dir  (Electron-builder, produces unpacked app)
   - Downloads Electron binary (~115MB) on first run — takes ~4 min
   - Output: release/linux-unpacked/Hermes

## AppImage Build (Distribution Package)
8. npx electron-builder --linux AppImage
   - Produces: release/Hermes-0.15.1-linux-x86_64.AppImage (~141MB)
   - Self-contained, runs on most Linux distros without install
   - Copy to ~/.local/bin/hermes-desktop.appimage && chmod +x

## Install
- Binary: release/linux-unpacked/Hermes (chmod +x)
- AppImage: ~/.local/bin/hermes-desktop.appimage
- Symlink: ln -sf .../Hermes ~/.local/bin/hermes-desktop
- Desktop entry: ~/.local/share/applications/hermes.desktop
- Launch: hermes-desktop or hermes desktop

## Desktop Entry Template
```
[Desktop Entry]
Name=Hermes
Comment=Native desktop shell for Hermes Agent
Exec=/home/bob/.local/bin/hermes-desktop.appimage
Icon=/home/bob/.hermes/hermes-agent/apps/desktop/public/icon.svg
Type=Application
Categories=Development;Utility;
Terminal=false
StartupNotify=true
```

## Launch Flags
- --no-sandbox  (required for root/headless)
- --skip-build  (skip auto-build, use existing)
- --cwd PATH    (initial project directory)

## Notes
- Gateway auto-reloads after git pull + pip install -e .
- Cannot restart gateway from inside gateway process
- Desktop app launches dashboard backend on 127.0.0.1:9120
- AppImage is preferred for distribution; unpacked binary for development
