#!/data/data/com.termux/files/usr/bin/bash

APP_DIR="/data/data/com.termux/files/usr/opt/appstore"
APP_SCRIPT="$APP_DIR/gtk_app_store.py"
REQUIREMENTS_FILE="$APP_DIR/requirements.txt"

# Function to display notifications
show_notification() {
    if command -v notify-send &>/dev/null; then
        notify-send "Termux App Store" "$1" --urgency=critical
    fi
    echo "$1"
}

check_and_create_directory() {
    if [[ -n "$1" && ! -d "$1" ]]; then
        mkdir -p "$1"
    fi
}

check_and_delete() {
    for item in "$@"; do
        if [[ -e "$item" ]]; then
            rm -rf "$item"
        fi
    done
}

download_file() {
    local dest url max_retries=5 attempt=1

    if [[ -z "$2" ]]; then
        url="$1"
        dest="$(basename "$url")"
    else
        dest="$1"
        url="$2"
    fi

    while ((attempt <= max_retries)); do
        echo "Downloading $dest (Attempt $attempt)..."
        [ ! -s "$dest" ] && rm -f "$dest"

        if command -v wget &>/dev/null; then
            wget --tries=5 --timeout=15 --retry-connrefused -O "$dest" "$url"
        else
            curl -L "$url" -o "$dest"
        fi

        [[ -f "$dest" && -s "$dest" ]] && {
            echo "Download successful."
            return 0
        }
        echo "Download failed. Retrying..."
        ((attempt++))
    done

    echo "Failed to download the file after $max_retries attempts."
    return 1
}

function confirmation_y_or_n() {
    while true; do
        # prompt
        read -r -p "$1 (y/n) " response
        # apply default
        response="${response:-y}"
        # lowercase
        response="${response,,}"

        # reject spaces or slashes
        if [[ "$response" =~ [[:space:]/] ]]; then
            echo
            echo "Invalid input: no spaces or slashes allowed. Enter only 'y' or 'n'."
            echo
            continue
        fi

        # normalize full words to single letters
        if [[ "$response" =~ ^(yes|y)$ ]]; then
            response="y"
        elif [[ "$response" =~ ^(no|n)$ ]]; then
            response="n"
        else
            echo
            echo "Invalid input. Please enter 'y', 'yes', 'n', or 'no'."
            echo
            continue
        fi

        # store in the caller’s variable
        eval "$2='$response'"

        # handle it
        case $response in
        y)
            echo
            echo "Continuing with answer: $response"
            echo
            sleep 0.2
            break
            ;;
        n)
            echo
            echo "Skipping this step"
            echo
            sleep 0.2
            break
            ;;
        esac
    done
}

package_install_and_check() {
    source "/data/data/com.termux/files/usr/bin/termux-setup-package-manager"
    if [[ "$TERMUX_APP_PACKAGE_MANAGER" == "pacman" ]]; then
        PACKAGE_MANAGER="pacman"
    else
        PACKAGE_MANAGER="apt"
    fi

    echo "Starting package installation for: $*"
    for pkg in "$@"; do
        echo "Processing package: $pkg"
        if [[ "$PACKAGE_MANAGER" == "pacman" ]]; then
            pacman -Qi "$pkg" &>/dev/null || pacman -Sy --noconfirm --overwrite '*' "$pkg"
        else
            dpkg --configure -a
            dpkg -s "$pkg" &>/dev/null && apt reinstall "$pkg" -y ||
                apt install "$pkg" -y
        fi
    done
    echo "Package installation completed."
}

install_appstore() {
    package_install_and_check aria2 python python3 pygobject python-pillow
    check_and_delete "$APP_DIR"
    check_and_create_directory "$APP_DIR"

    download_file "$APP_DIR/gtk_app_store.py" "https://raw.githubusercontent.com/sabamdarif/Termux-AppStore/refs/heads/src/gtk_app_store.py"
    download_file "$APP_DIR/terminal_emulator.py" "https://raw.githubusercontent.com/sabamdarif/Termux-AppStore/refs/heads/src/terminal_emulator.py"
    download_file "$APP_DIR/requirements.txt" "https://raw.githubusercontent.com/sabamdarif/Termux-AppStore/refs/heads/src/requirements.txt"

    check_and_create_directory "$APP_DIR/inbuild_functions"
    download_file "$APP_DIR/inbuild_functions/inbuild_functions" "https://raw.githubusercontent.com/sabamdarif/Termux-AppStore/refs/heads/src/inbuild_functions/inbuild_functions"
    chmod +x "$APP_DIR/inbuild_functions/inbuild_functions"

    check_and_create_directory "$APP_DIR/style"
    download_file "$APP_DIR/style/style.css" "https://raw.githubusercontent.com/sabamdarif/Termux-AppStore/refs/heads/src/style/style.css"
    download_file "$APP_DIR/style/terminal_style.css" "https://raw.githubusercontent.com/sabamdarif/Termux-AppStore/refs/heads/src/style/terminal_style.css"

    download_file "$PREFIX/share/applications/org.sabamdarif.termux.appstore.desktop" "https://raw.githubusercontent.com/sabamdarif/Termux-AppStore/refs/heads/src/org.sabamdarif.termux.appstore.desktop"
    if [[ ! -f "$PREFIX/bin/appstore" ]]; then
        download_file "$PREFIX/bin/appstore" "https://raw.githubusercontent.com/sabamdarif/Termux-AppStore/refs/heads/src/appstore"
        chmod +x "$PREFIX/bin/appstore"
    fi
    cd "$APP_DIR" || exit 1
    pip install -r requirements.txt
    cd "$HOME" || exit 1
    echo "Termux App Store has been installed."
    exit 0
}

update_appstore() {
    if [[ ! -d "$APP_DIR" ]]; then
        echo "Install the app store first. Run appstore --install"
        exit 1
    fi

    # Map of local paths to GitHub file paths
    declare -A file_map=(
        ["$APP_DIR/gtk_app_store.py"]="gtk_app_store.py"
        ["$APP_DIR/terminal_emulator.py"]="terminal_emulator.py"
        ["$APP_DIR/inbuild_functions/inbuild_functions"]="inbuild_functions/inbuild_functions"
        ["$APP_DIR/requirements.txt"]="requirements.txt"
        ["$APP_DIR/style/style.css"]="style/style.css"
        ["$APP_DIR/style/terminal_style.css"]="style/terminal_style.css"
        ["$PREFIX/bin/appstore"]="appstore"
        ["$PREFIX/share/applications/org.sabamdarif.termux.appstore.desktop"]="org.sabamdarif.termux.appstore.desktop"
    )

    local update_needed=false
    local failed_hash_checks=()

    for local_path in "${!file_map[@]}"; do
        file="${file_map[$local_path]}"

        # Get GitHub file hash
        github_hash=$(curl -sL "https://raw.githubusercontent.com/sabamdarif/Termux-AppStore/refs/heads/src/${file}" | sha256sum | cut -d ' ' -f 1)

        # Get local file hash
        if [[ -f "$local_path" ]]; then
            local_hash=$(sha256sum "$local_path" | cut -d ' ' -f 1)
        else
            failed_hash_checks+=("$file")
            update_needed=true
            continue
        fi

        # Compare hashes
        if [[ "$local_hash" != "$github_hash" ]]; then
            update_needed=true
            failed_hash_checks+=("$file")
        fi
    done

    if [[ "$update_needed" == true ]]; then
        echo "[-] Updates found for the following files:"
        printf '%s\n' "${failed_hash_checks[@]}"
        echo

        confirmation_y_or_n "Would you like to update the appstore to the latest version" confirm_update

        if [[ "$confirm_update" == "y" ]]; then
            echo "Updating appstore..."
            install_appstore
            echo "Appstore updated successfully"
        else
            echo "Skipping appstore update"
        fi
    else
        echo "You are using the latest version"
    fi
    exit 0
}

remove_appstore() {
    echo "Removing Termux App Store..."
    check_and_delete "$APP_DIR" "$PREFIX/share/applications/org.sabamdarif.termux.appstore.desktop"
    echo "Termux App Store has been removed."
    exit 0
}

# --- handle CLI args ---
while [[ $# -gt 0 ]]; do
    case $1 in
    -i | --install) install_appstore ;;
    -u | --update) update_appstore ;;
    -r | --remove) remove_appstore ;;
    *)
        echo "Unknown option: $1"
        exit 1
        ;;
    esac
    shift
done

# --- pre-launch checks ---
# 1) python3
if ! command -v python3 &>/dev/null; then
    show_notification "Error: Python 3 is not installed. Please install with 'pkg install python'."
    exit 1
fi

# 2) pip
if ! command -v pip &>/dev/null; then
    show_notification "Error: pip is not installed. Please install with 'pkg install python-pip'."
    exit 1
fi

# 3) file-existence check (all downloaded assets)
required_files=(
    "$APP_DIR/gtk_app_store.py"
    "$APP_DIR/terminal_emulator.py"
    "$REQUIREMENTS_FILE"
    "$APP_DIR/inbuild_functions/inbuild_functions"
    "$APP_DIR/style/style.css"
    "$APP_DIR/style/terminal_style.css"
    "$PREFIX/share/applications/org.sabamdarif.termux.appstore.desktop"
)

missing_files=()
for f in "${required_files[@]}"; do
    [[ -e "$f" ]] || missing_files+=("$f")
done

if ((${#missing_files[@]})); then
    missing_list=$(printf "  • %s\n" "${missing_files[@]}")
    show_notification "Error: Missing files:
$missing_list
Please reinstall: appstore --install"
    exit 1
fi

# 4) Python-package dependencies
declare -A PACKAGE_IMPORTS=(
    [Pillow]=PIL [PyYAML]=yaml [requests]=requests
    [urllib3]=urllib3 [fuzzywuzzy]=fuzzywuzzy [thefuzz]=thefuzz
)

echo "Checking Python dependencies..."
MISSING_DEPS=""
while IFS= read -r line || [[ -n $line ]]; do
    [[ $line =~ ^# ]] && continue
    pkg=$(echo "$line" | sed -E 's/^([A-Za-z0-9_-]+).*/\1/')
    imp=${PACKAGE_IMPORTS[$pkg]:-$pkg}
    python3 -c "import $imp" &>/dev/null || MISSING_DEPS+="${MISSING_DEPS:+, }$pkg"
done <"$REQUIREMENTS_FILE"

python3 - <<'EOF' &>/dev/null
import gi
EOF
if [[ $? -ne 0 ]]; then
    MISSING_DEPS+="${MISSING_DEPS:+, }PyGObject"
fi

if [[ -n "$MISSING_DEPS" ]]; then
    show_notification "Error: Missing Python deps: $MISSING_DEPS. Install with 'pip install -r $REQUIREMENTS_FILE'"
    echo "For PyGObject, use: pkg install python-gobject"
    exit 1
fi

# All clear, launch
echo "All checks passed, launching App Store..."
python3 "$APP_SCRIPT"
exit $?