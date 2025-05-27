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

# Step 2: Extract archives
echo "[*] Extracting NeoDeskX.7z..."
7z x NeoDeskX.7z || { echo "[!] Failed to extract NeoDeskX.7z"; exit 1; }

echo "[*] Extracting NeoDeskX.zip..."
unzip -o NeoDeskX.zip || { echo "[!] Failed to extract NeoDeskX.zip"; exit 1; }

# Step 3: Make main script executable
echo "[*] Making main script executable..."
chmod +x setup-termux-NeoDeskX

# Step 4: Run main setup script
echo "[*] Running setup-termux-NeoDeskX..."
./setup-termux-NeoDeskX || { echo "[!] setup-termux-NeoDeskX failed"; exit 1; }

echo ""
echo -e "\033[1;32m[✔] NeoDeskX Installation Completed Successfully!\033[0m"
