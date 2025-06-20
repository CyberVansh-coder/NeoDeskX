#!/data/data/com.termux/files/usr/bin/bash

clear
echo -e "\033[1;36m"
/bin/cat << "EOF"
███▄    █ ▓█████  ▒█████  ▓█████▄ ▓█████   ██████  ██ ▄█▀▒██   ██▒
██ ▀█   █ ▓█   ▀ ▒██▒  ██▒▒██▀ ██▌▓█   ▀ ▒██    ▒  ██▄█▒ ▒▒ █ █ ▒░
▓██  ▀█ ██▒▒███   ▒██░  ██▒░██   █▌▒███   ░ ▓██▄   ▓███▄░ ░░  █   ░
▓██▒  ▐▌██▒▒▓█  ▄ ▒██   ██░░▓█▄   ▌▒▓█  ▄   ▒   ██▒▓██ █▄  ░ █ █ ▒
▒██░   ▓██░░▒████▒░ ████▓▒░░▒████▓ ░▒████▒▒██████▒▒▒██▒ █▄▒██▒ ▒██▒
░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒░▒░▒░  ▒▒▓  ▒ ░░ ▒░ ░▒ ▒▓▒ ▒ ░▒ ▒▒ ▓▒▒▒ ░ ░▓ ░
░ ░░   ░ ▒░ ░ ░  ░  ░ ▒ ▒░  ░ ▒  ▒  ░ ░  ░░ ░▒  ░ ░░ ░▒ ▒░░░   ░▒ ░
   ░   ░ ░    ░   ░ ░ ░ ▒   ░ ░  ░    ░   ░  ░  ░  ░ ░░ ░  ░    ░
         ░    ░  ░    ░ ░     ░       ░  ░      ░  ░  ░    ░    ░
                            ░
EOF
echo -e "\033[0m"
echo ""
echo "╔════════════════════════════════════╗"
echo "║      NeoDeskX Auto Installer      ║"
echo "╚════════════════════════════════════╝"
echo ""

# Step 1: Install required packages
echo "[*] Installing required packages..."
pkg install -y p7zip unzip || {
  echo "[!] Failed to install required packages"
  exit 1
}

# Step 2: Ask user for edition
echo ""
echo "Which edition do you want to install?"
echo "1) Basic"
echo "2) Pro"
read -p "Enter choice [1-2]: " choice

case $choice in
  1)
    FILE="NeoDeskX_Basic.7z"
    ;;
  2)
    FILE="NeoDeskX_Pro.7z"
    ;;
  *)
    echo "[!] Invalid choice. Exiting..."
    exit 1
    ;;
esac

# Step 3: Extract selected archive
if [ -f "$FILE" ]; then
  echo "[*] Extracting $FILE..."
  7z x "$FILE" -oNeoDeskX || { echo "[!] Extraction failed"; exit 1; }
else
  echo "[!] $FILE not found in current directory!"
  exit 1
fi

# Step 4: Process based on edition
cd NeoDeskX || { echo "[!] NeoDeskX folder missing"; exit 1; }

if [ "$choice" = "2" ]; then
  ZIP_FILE="NeoDeskX_Pro.zip"
  if [ -f "$ZIP_FILE" ]; then
    echo "[*] Extracting $ZIP_FILE..."
    unzip -o "$ZIP_FILE" || { echo "[!] Failed to extract $ZIP_FILE"; exit 1; }
  else
    echo "[!] $ZIP_FILE not found!"
    exit 1
  fi
  chmod +x setup-termux-NeoDeskX-pro
  ./setup-termux-NeoDeskX-pro || { echo "[!] Pro setup failed"; exit 1; }

else
  chmod +x setup-termux-NeoDeskX
  ./setup-termux-NeoDeskX || { echo "[!] Basic setup failed"; exit 1; }
fi

echo ""
echo -e "\033[1;32m[✔] NeoDeskX Installed Successfully!\033[0m"
