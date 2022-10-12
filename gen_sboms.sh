#!/usr/bin/env bash

set -e

# NOTE: This is going away in favor of dl_docs.py.
# This expects you to have syft installed, gcloud cli installed as well as 
# having logged into gcloud
REGISTRY_URL=${1-"https://gcr.io/v2/google-containers"}
BUCKET_URL=${2-"gs://oopsallsboms"}
SYFT_VERSION=$(syft version -o json | jq -r .version)
TOKEN=$(gcloud auth print-access-token)
GOOGLE_CONTAINERS=$(curl   -H "Authorization: Bearer ${TOKEN}"   "${REGISTRY_URL}/tags/list" | jq -r ".child[]")

for image in ${GOOGLE_CONTAINERS}
do
    TAGS=$(crane ls gcr.io/google-containers/${image})
    for tag in ${TAGS}
    do
        DIGEST=$(crane digest ${REGISTRY_URL}/${image}:${tag} | sed s/\:/-/)
        FILENAME=outputs/${image}-${tag}.${DIGEST}.syft.${SYFT_VERSION}.spdx.json
        echo $FILENAME
        syft ${REGISTRY_URL}/${image}:${tag} -o spdx-json=${FILENAME}
        gcloud alpha storage cp ${FILENAME} ${BUCKET_URL}
        docker image prune -a -f
    done
done
