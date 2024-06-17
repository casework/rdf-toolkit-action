# RDF Toolkit Action
<a href="https://www.repostatus.org/#active"><img src="https://www.repostatus.org/badges/latest/active.svg" alt="Project Status: Active – The project has reached a stable, usable state and is being actively developed." /></a>
[![Continuous Integration](https://github.com/casework/rdf-toolkit-action/actions/workflows/ci.yml/badge.svg)](https://github.com/casework/rdf-toolkit-action/actions/workflows/ci.yml)
[![Supply Chain](https://github.com/casework/rdf-toolkit-action/actions/workflows/supply-chain.yml/badge.svg)](https://github.com/casework/rdf-toolkit-action/actions/workflows/supply-chain.yml)
[![Build Docker](https://github.com/casework/rdf-toolkit-action/actions/workflows/build.yml/badge.svg)](https://github.com/casework/rdf-toolkit-action/actions/workflows/build.yml)

## Overview
A GitHub Action, Docker image, and [`pre-commit`](https://pre-commit.com/) hook for normalizing RDF files with `rdf-toolkit.jar`.

## Usage
### GitHub Action
_This capability is expected to be developed in a future release._

### pre-commit Hook
_This documentation assumes you already have `pre-commit` installed in your repository. Installation and basic usage instructions for `pre-commit` are available at [https://pre-commit.com/#install](https://pre-commit.com/#install)_

In your `.pre-commit-config.yaml` file, add the following under the `repos` key:

<!--
NOTE: When editing this YAML snippet, confirm the version lines up with the contents of setup.cfg.
-->
```yaml
repos:
-   repo: https://github.com/casework/rdf-toolkit-action
    rev: 0.3.0
    hooks:
    -   id: rdf-toolkit-normalizer
        args:
            - --autofix
```

### Docker
As part of this repository, a `Dockerfile` and related image are built and maintained in Docker Hub at [https://hub.docker.com/repository/docker/kchason/rdf-toolkit-normalizer](https://hub.docker.com/repository/docker/kchason/rdf-toolkit-normalizer).

This Docker image can be run to normalize a TTL graph with the following command:
```shell
docker run --rm \
    -v /path/to/input.ttl:/opt/workdir/input.ttl \
    -v /path/to/store/output/:/opt/workdir/output/ \
    -e INPUT_TTL_FILE="/opt/workdir/input.ttl" \
    -e OUTPUT_TTL_FILE="/opt/workdir/output/output.ttl" \
    kchason/rdf-toolkit-normalizer:latest
```

## Credits
The `rdf-toolkit.jar` tool is obtained from [https://github.com/edmcouncil/rdf-toolkit/](https://github.com/edmcouncil/rdf-toolkit/).


## Licensing

Portions of this repository contributed by NIST are governed by the [NIST Software Licensing Statement](THIRD_PARTY_LICENSES.md#nist-software-licensing-statement).
