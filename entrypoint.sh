#!/usr/bin/env bash

java -jar rdf-toolkit.jar \
  --infer-base-iri \
  --inline-blank-nodes \
  --source "${INPUT_TTL_FILE}" \
  --source-format turtle \
  --target "${INPUT_TTL_FILE}.normalized" \
  --target-format turtle

# Set the output for the job
echo "::set-output name=output-file::${INPUT_TTL_FILE}.normalized"
