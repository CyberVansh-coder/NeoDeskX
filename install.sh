#!/data/data/com.termux/files/usr/bin/bash

clear
echo -e "\033[1;36m"
/bin/cat << "EOF"
 /$$   /$$                     /$$$$$$$                      /$$       /$$   /$$       /$$$$$$                       /$$               /$$ /$$                    
| $$$ | $$                    | $$__  $$                    | $$      | $$  / $$      |_  $$_/                      | $$              | $$| $$                    
| $$$$| $$  /$$$$$$   /$$$$$$ | $$  \ $$  /$$$$$$   /$$$$$$$| $$   /$$|  $$/ $$/        | $$   /$$$$$$$   /$$$$$$$ /$$$$$$    /$$$$$$ | $$| $$  /$$$$$$   /$$$$$$ 
| $$ $$ $$ /$$__  $$ /$$__  $$| $$  | $$ /$$__  $$ /$$_____/| $$  /$$/ \  $$$$/         | $$  | $$__  $$ /$$_____/|_  $$_/   |____  $$| $$| $$ /$$__  $$ /$$__  $$
| $$  $$$$| $$$$$$$$| $$  \ $$| $$  | $$| $$$$$$$$|  $$$$$$ | $$$$$$/   >$$  $$         | $$  | $$  \ $$|  $$$$$$   | $$      /$$$$$$$| $$| $$| $$$$$$$$| $$  \__/
| $$\  $$$| $$_____/| $$  | $$| $$  | $$| $$_____/ \____  $$| $$_  $$  /$$/\  $$        | $$  | $$  | $$ \____  $$  | $$ /$$ /$$__  $$| $$| $$| $$_____/| $$      
| $$ \  $$|  $$$$$$$|  $$$$$$/| $$$$$$$/|  $$$$$$$ /$$$$$$$/| $$ \  $$| $$  \ $$       /$$$$$$| $$  | $$ /$$$$$$$/  |  $$$$/|  $$$$$$$| $$| $$|  $$$$$$$| $$      
|__/  \__/ \_______/ \______/ |_______/  \_______/|_______/ |__/  \__/|__/  |__/      |______/|__/  |__/|_______/    \___/   \_______/|__/|__/ \_______/|__/      

EOF
echo -e "\033[0m"
echo ""
echo "╔════════════════════════════════════╗"
echo "║      NeoDeskX Auto Installer      ║"
echo "╚════════════════════════════════════╝"
echo ""

# Kill dpkg lock process if exists
LOCK_PID=$(lsof /data/data/com.termux/files/usr/var/lib/dpkg/lock-frontend 2>/dev/null | awk 'NR>1 {print $2}' | head -n 1)
if [ -n "$LOCK_PID" ]; then
    echo "[*] Killing apt lock process (PID: $LOCK_PID)..."
    kill -9 "$LOCK_PID"
    sleep 1
fi

# Delete existing folder
if [ -d "$HOME/NeoDeskX" ]; then
    echo "[*] Removing old NeoDeskX directory..."
    rm -rf "$HOME/NeoDeskX"
fi

# Clone repo
echo "[+] Cloning NeoDeskX from GitHub..."
git clone https://github.com/CyberVansh-coder/NeoDeskX.git || {
    echo "[-] Git clone failed. Check your connection or repo URL."
    exit 1
}

cd NeoDeskX || {
    echo "[-] Cannot enter NeoDeskX directory!"
    exit 1
}

# Install required packages
echo "[+] Installing packages..."
yes | pkg update && yes | pkg install git unzip p7zip proot-distro || {
    echo "[-] Package install failed!"
    exit 1
}

# Extract archive
echo "[+] Extracting NeoDeskX.7z..."
7z x NeoDeskX.7z -aoa

# Run setup
echo "[+] Starting NeoDeskX Setup..."
bash setup-termux-NeoDeskX

echo "[✓] Installation complete!"