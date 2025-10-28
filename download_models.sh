#!/bin/bash
# Enhanced Google Drive Download Script for CryptoQ Models
# Handles permissions, retries, and skips already-downloaded files

set -e

# Configuration
MODEL_CONFIG="model_config.json"
MAX_RETRIES=3
RETRY_DELAY=5

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if jq is installed
check_dependencies() {
    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed. Installing..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y jq
        elif command -v yum &> /dev/null; then
            sudo yum install -y jq
        elif command -v brew &> /dev/null; then
            brew install jq
        else
            log_error "Please install jq manually: https://stedolan.github.io/jq/"
            exit 1
        fi
    fi
    
    if ! command -v curl &> /dev/null; then
        log_error "curl is required but not installed"
        exit 1
    fi
}

# Create directory structure
create_directories() {
    log_info "Creating directory structure..."
    
    for level in Level1 Level2 Level3; do
        for fold in Fold1 Fold2 Fold3 Fold4 Fold5; do
            mkdir -p "models/$level/$fold"
        done
    done
    
    log_success "Directory structure created successfully!"
}

# Extract file ID from Google Drive URL
extract_file_id() {
    local url="$1"
    if [[ $url == *"id="* ]]; then
        echo "$url" | sed 's/.*id=\([^&]*\).*/\1/'
    elif [[ $url == *"/file/d/"* ]]; then
        echo "$url" | sed 's/.*\/file\/d\/\([^\/]*\).*/\1/'
    else
        echo ""
    fi
}

# Download file with retries
download_file() {
    local file_id="$1"
    local output_path="$2"
    local description="$3"
    local attempt=1
    
    while [ $attempt -le $MAX_RETRIES ]; do
        log_info "Downloading $description (attempt $attempt/$MAX_RETRIES)..."
        
        # Method 1: Direct download
        local download_url="https://drive.google.com/uc?export=download&id=$file_id"
        
        if curl -L -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
                --connect-timeout 30 --max-time 1800 \
                -o "$output_path" "$download_url" 2>/dev/null; then
            
            # Check if file was downloaded and is not empty
            if [ -f "$output_path" ] && [ -s "$output_path" ]; then
                local file_size=$(stat -c%s "$output_path" 2>/dev/null || stat -f%z "$output_path" 2>/dev/null)
                log_success "Downloaded $description ($file_size bytes)"
                return 0
            else
                log_warning "Downloaded file is empty, retrying..."
            fi
        else
            log_warning "Download failed, retrying..."
        fi
        
        # Wait before retry
        if [ $attempt -lt $MAX_RETRIES ]; then
            log_info "Waiting $RETRY_DELAY seconds before retry..."
            sleep $RETRY_DELAY
        fi
        
        ((attempt++))
    done
    
    log_error "Failed to download $description after $MAX_RETRIES attempts"
    return 1
}

# Main download function
download_models() {
    log_info "Starting CryptoQ Model Download Process..."
    echo "============================================================"
    
    # Check if model config exists
    if [ ! -f "$MODEL_CONFIG" ]; then
        log_error "Model configuration file '$MODEL_CONFIG' not found!"
        exit 1
    fi
    
    # Create directories
    create_directories
    echo
    
    # Initialize counters
    local total_downloads=0
    local successful_downloads=0
    local failed_downloads=()
    
    # Count total downloads
    total_downloads=$(jq '.model_urls | length' "$MODEL_CONFIG")
    
    # Download each model
    local current=0
    jq -r '.model_urls | to_entries[] | "\(.key)|\(.value)"' "$MODEL_CONFIG" | while IFS='|' read -r description url; do
        ((current++))
        echo "[$current/$total_downloads] Processing $description..."
        
        # Extract file ID
        local file_id=$(extract_file_id "$url")
        if [ -z "$file_id" ]; then
            log_error "Could not extract file ID from $url"
            failed_downloads+=("$description")
            continue
        fi
        
        # Set output path
        local output_path="models/$description/model.pth"
        
        # Check if file already exists
        if [ -f "$output_path" ] && [ -s "$output_path" ]; then
            local file_size=$(stat -c%s "$output_path" 2>/dev/null || stat -f%z "$output_path" 2>/dev/null)
            log_info "Skipping $description - file already exists ($file_size bytes)"
            ((successful_downloads++))
        else
            # Download the file
            if download_file "$file_id" "$output_path" "$description"; then
                ((successful_downloads++))
            else
                failed_downloads+=("$description")
            fi
        fi
        
        echo "----------------------------------------"
    done
    
    # Summary
    echo
    echo "============================================================"
    echo "DOWNLOAD SUMMARY"
    echo "============================================================"
    echo "Successfully downloaded: $successful_downloads/$total_downloads models"
    
    if [ ${#failed_downloads[@]} -eq 0 ]; then
        log_success "All model files have been downloaded successfully!"
        echo "You can now use them locally without pushing to GitHub."
    else
        log_warning "${#failed_downloads[@]} downloads failed."
        echo "Failed downloads:"
        for failed in "${failed_downloads[@]}"; do
            echo "  - $failed"
        done
        echo
        echo "To fix failed downloads:"
        echo "1. Check Google Drive file permissions (set to 'Anyone with the link')"
        echo "2. Verify file IDs are correct"
        echo "3. Run the script again to retry failed downloads"
    fi
    
    echo
    echo "Model files are stored in:"
    echo "   models/Level1/Fold1-5/"
    echo "   models/Level2/Fold1-5/"
    echo "   models/Level3/Fold1-5/"
}

# Main execution
main() {
    check_dependencies
    download_models
}

# Run main function
main "$@"
