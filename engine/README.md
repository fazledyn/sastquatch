## Build
```bash
docker build -f Dockerfile -t sastquatch:latest .
```

## Usage
To run the Docker image, you must mention two parameters: `language` and `queries`
```bash
docker run --rm -v /path/to/source:/workspace/source -v /path/to/result:/workspace/result -t codeql-container:dev --language LANGUAGE --queries QUERIES
```
`LANGUAGE` can be any of the below:
- `python`
- `javascript`

`QUERIES` can be any of the below:
- `code-scanning`
- `security-extended`
- `security-and-quality`

