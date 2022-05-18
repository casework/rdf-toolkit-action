#!/usr/bin/env bash

java -jar rdf-toolkit.jar \
  --infer-base-iri \
  --inline-blank-nodes \
  --source "${INPUT_TTL_FILE}" \
  --source-format turtle \
  --target "${OUTPUT_TTL_FILE}" \
  --target-format turtle