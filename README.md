# RDF Toolkit Action
## Overview
A GitHub Action, Docker image, and [`pre-commit`](https://pre-commit.com/) hook for normalizing RDF files with `rdf-toolkit.jar`.

## Usage
### GitHub Action
TODO

### pre-commit Hook
_This documentation assumes you already have `pre-commit` installed in your repository. Installation and basic usage instructions for `pre-commit` are available at [https://pre-commit.com/#install](https://pre-commit.com/#install)_

In your `.pre-commit-config.yaml` file, add the following under the `repos` key:

```yaml
repos:
-   repo: https://github.com/kchason/rdf-toolkit-action
    rev: v0.1.0
    hooks:
    -   id: rdf-toolkit-normalizer
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
The `rdf-toolkit.jar` tool is obtained from [https://github.com/trypuz/openfibo](https://github.com/trypuz/openfibo).


