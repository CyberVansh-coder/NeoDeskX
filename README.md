## NeoDeskX – Turn Your Android into a Full Linux Desktop with Wine, Game Streaming, and More

NeoDeskX is a powerful all-in-one Termux-based Linux desktop setup for Android devices. It transforms any Android phone (Android 8–13+) into a fully-functional XFCE desktop environment with support for Wine applications, game streaming (Moonlight), and remote input control — optimized for performance, gaming, and multitasking.

Whether you're a developer, gamer, or tech enthusiast, NeoDeskX delivers a portable and flexible desktop experience directly on your Android device without root access.

## ✨ Features:

---

⚡ Quick & Easy Installation

Seamless, beginner-friendly setup process using a single command.


🖥️ Desktop Environments

Supports XFCE, LXQt, MATE, Openbox, i3WM, and more — all with modern, responsive themes.


🍷 Windows App Support

Run Windows apps via Wine (32-bit and 64-bit) on ARM64 — supports games like GTA Vice City, CS 1.6, Notepad++, and more.


⚙️ Optimized Performance

Hardware acceleration enabled for supported GPUs and devices for smoother experience.


🖱️ GUI Access Options

Supports both Termux:X11 and VNC Viewer for graphical desktop environments.


🛍️ Built-in App Store

One-click install apps from curated lists compatible with Termux and Proot-distro environments.



---

🎮 Gaming & Multimedia

🎨 Pre-Configured XFCE Desktop

Lightweight, mobile-optimized desktop with a polished look and feel.


🎮 Pre-installed Classic Games

Includes open-source games like SuperTux, SuperTuxKart, Pingus, LBreakout2, and more for offline fun.


🌐 Game Streaming with Moonlight

Stream high-end PC games like GTA V, Cyberpunk 2077, etc. via NVIDIA GameStream.


🎮 External Gamepad Support

Connect Bluetooth or USB gamepads and joysticks for an enhanced gaming experience.



---

🛠️ Input & Control Features

🔌 USB & WiFi Input Bridge

Use your Android as a mouse & keyboard — ideal for remote desktops.


🧩 One-Click App Support

Simplified launcher for launching Wine apps, games, or tools instantly.



---

📦 Additional Enhancements

📊 Hardware Compatibility Checker

Automatically checks for Android version, CPU architecture, storage, and GPU support.


🖼️ Offline Assets Bundle

.7z archive includes wallpapers, config files, custom scripts, and essential binaries.


🎯 No Root Required

100% Termux-based — works on any Android 8+ device without root access.


🖼️ Custom Installer UI

Stylish terminal UI with ASCII banners and step-by-step prompts for better clarity.

--- 

To install either the **NeoDeskX** or **NeoDeskX Emulator**, please install the following applications :

- **Termux** : A terminal emulator for Android that allows you to run Linux commands on your device.  
  [![Download Termux](https://img.shields.io/badge/Download-Termux-brightgreen?style=for-the-badge&logo=android)](https://github.com/termux/termux-app/releases/download/v0.118.2/termux-app_v0.118.2+github-debug_arm64-v8a.apk) - click to download

- **Termux-X11 (Xserver)** : Required for running graphical applications within Termux, providing a graphical user interface.
- [![Download Termux-X11](https://img.shields.io/badge/Download-Termux--X11-blue?style=for-the-badge&logo=linux)](https://github.com/termux/termux-x11/releases/download/nightly/app-arm64-v8a-debug.apk) - click to download
  

- **Input Bridge v0.1.9.9 (Overlay HUD/Controller)** : This application allows you to create a touch screen overlay or heads-up display (HUD) that can function as a customizable controller.  
  [![Download Input Bridge](https://img.shields.io/badge/Download-Input%20Bridge-ff69b4?style=for-the-badge&logo=controller)](https://github.com/ahmad1abbadi/extra/releases/download/apps/InputBridge_v0.1.9.9.apk) - click to download
  
## installation 
```
pkg update -y && pkg install -y git && git clone https://github.com/CyberVansh-coder/NeoDeskX.git && cd NeoDeskX && bash install.sh
```
