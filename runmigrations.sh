#!/bin/bash

# Django Multi-Environment Migration Script
# This script runs makemigrations and migrate across all environments

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Environment settings modules
# ENVIRONMENTS=("dev" "staging" "prod")
ENVIRONMENTS=("dev" "prod")
SETTINGS_PREFIX="core.settings"

echo "================================================"
echo "Django Multi-Environment Migration Script"
echo "================================================"
echo ""

# Function to run command for a specific environment
run_migration() {
    local env=$1
    local settings_module="${SETTINGS_PREFIX}.${env}"
    
    echo -e "${YELLOW}Processing ${env} environment...${NC}"
    echo "Settings: ${settings_module}"
    echo ""
    
    # Run makemigrations
    echo "Running makemigrations for ${env}..."
    python manage.py makemigrations --settings="${settings_module}"
    
    echo ""
    
    # Run migrate
    echo "Running migrate for ${env}..."
    python manage.py migrate --settings="${settings_module}"
    
    echo -e "${GREEN}✓ Completed ${env} environment${NC}"
    echo "------------------------------------------------"
    echo ""
}

# Main execution
echo "This will run makemigrations and migrate for all environments:"
for env in "${ENVIRONMENTS[@]}"; do
    echo "  - ${env}"
done
echo ""

# read -p "Do you want to continue? (y/n) " -n 1 -r
# echo ""

# if [[ ! $REPLY =~ ^[Yy]$ ]]; then
#     echo "Migration cancelled."
#     exit 0
# fi

python manage.py makemigrations accounts
python manage.py makemigrations photos
python manage.py makemigrations util

# echo ""

# Process each environment
for env in "${ENVIRONMENTS[@]}"; do
    run_migration "$env"
done

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}All environments processed successfully!${NC}"
echo -e "${GREEN}================================================${NC}"
