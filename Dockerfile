FROM openjdk:19-slim-buster

WORKDIR /opt/workdir/

# Ensure the expected environment variables exist
ENV INPUT_TTL_FILE "input.ttl"
ENV OUTPUT_TTL_FILE "normalized.ttl"

# Install wget for downloading the rdf-toolkit.jar
RUN apt-get update \
    && apt-get install wget --no-install-recommends -y \
    && rm -rf /var/lib/apt/lists/*

# Download the rdf-toolkit.jar file for ready packaging
# Try retrieval from Github, then from files.caseontology.org.
RUN	wget \
	  --output-document rdf-toolkit.jar \
	  https://github.com/trypuz/openfibo/blob/1f9ab415e8ebd131eadcc9b0fc46241adeeb0384/etc/serialization/rdf-toolkit.jar?raw=true \
	  || wget \
	    --output-document rdf-toolkit.jar \
	    http://files.caseontology.org/rdf-toolkit.jar

# Copy in the entrypoint file
COPY entrypoint.sh /opt/workspace/entrypoint.sh

# Define the command to normalize the provided TTL file
CMD ["bash", "/opt/workspace/entrypoint.sh"]

