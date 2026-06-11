#!/bin/bash

DOCKER_USERNAME="inderpreet26"
SOURCE_REPO="${DOCKER_USERNAME}/fitness-tracker-dev"
TARGET_REPO="${DOCKER_USERNAME}/fitness-tracker-prod"
TAG="latest"
LOG_FILE="promotion_$(date +%Y%m%d_%H%M%S).log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

log "=== Image Promotion Started ==="

# Step 1 - Pull from dev
log "Pulling ${SOURCE_REPO}:${TAG}"
docker pull ${SOURCE_REPO}:${TAG} || { log "ERROR: Pull failed"; exit 1; }

# Step 2 - Tag for prod
log "Tagging as ${TARGET_REPO}:${TAG}"
docker tag ${SOURCE_REPO}:${TAG} ${TARGET_REPO}:${TAG} || { log "ERROR: Tag failed"; exit 1; }

# Step 3 - Push to prod
log "Pushing ${TARGET_REPO}:${TAG}"
docker push ${TARGET_REPO}:${TAG} || { log "ERROR: Push failed"; exit 1; }

# Step 4 - Validate
log "Validating pushed image..."
docker pull ${TARGET_REPO}:${TAG} || { log "ERROR: Validation failed"; exit 1; }

log "=== Image Promotion Complete ==="
