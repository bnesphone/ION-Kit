# ION Kit - Docker Usage Guide

## Quick Start

### Build the Image
```bash
docker build -t ion-kit .
```

### Run Commands
```bash
# System check
docker run ion-kit check

# Analyze a project
docker run -v $(pwd):/workspace ion-kit analyze /workspace

# Run validation
docker run ion-kit validate

# Remove image backgrounds
docker run -v $(pwd):/workspace ion-kit bg /workspace/input.jpg /workspace/output.png
```

## Using Docker Compose

### Services Available

1. **ion-kit** - Main service for general commands
2. **ion-kit-test** - Run test suite
3. **ion-kit-mock-api** - Mock API server

### Commands
```bash
# Start services
docker-compose up ion-kit
docker-compose up ion-kit-test
docker-compose up ion-kit-mock-api

# Run specific command
docker-compose run ion-kit check
docker-compose run ion-kit analyze /workspace
```

## Development Workflow

### Mount Your Project
```bash
# Analyze your project
docker run -v /path/to/project:/workspace ion-kit analyze /workspace

# Lint your code
docker run -v /path/to/project:/workspace ion-kit lint /workspace

# Run tests
docker run -v /path/to/project:/workspace ion-kit test
```

### Interactive Shell
```bash
docker run -it --entrypoint /bin/bash ion-kit
```

## CI/CD Integration

### GitHub Actions
```yaml
name: ION Kit Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build ION Kit
        run: docker build -t ion-kit .
      - name: Run validation
        run: docker run -v ${{ github.workspace }}:/workspace ion-kit validate
```

### GitLab CI
```yaml
validate:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t ion-kit .
    - docker run -v $(pwd):/workspace ion-kit validate
```

## Volume Mounts

| Mount Point | Purpose |
|-------------|---------|
| `/workspace` | Your project directory |
| `/output` | Generated files |
| `/schemas` | API schemas for mock server |

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `ION_KIT_VERSION` | 6.1.0 | Version identifier |
| `PYTHONUNBUFFERED` | 1 | Real-time output |

## Troubleshooting

### Permission Issues
If you encounter permission errors, run with user mapping:
```bash
docker run --user $(id -u):$(id -g) -v $(pwd):/workspace ion-kit analyze /workspace
```

### Slow First Run
First run downloads models (~150MB for background remover). Subsequent runs are fast.

### Node Modules
Node modules are pre-installed in the image. No need to mount node_modules.

## Production Deployment

### Push to Registry
```bash
# Tag
docker tag ion-kit:latest your-registry.com/ion-kit:6.1.0

# Push
docker push your-registry.com/ion-kit:6.1.0
```

### Run in Production
```bash
docker run -d \
  --name ion-kit-api \
  -v /path/to/schemas:/schemas \
  -p 8000:8000 \
  your-registry.com/ion-kit:6.1.0 \
  mock /schemas/api-schema.json
```

## Size Optimization

Current image size: ~800MB

To reduce:
```dockerfile
# Use alpine base (not recommended, compatibility issues)
FROM python:3.11-alpine

# Or use multi-stage build
FROM python:3.11-slim as builder
# ... build steps ...
FROM python:3.11-slim
COPY --from=builder /app /app
```

## Security Notes

- Image runs as root by default
- Consider using `--user` flag in production
- Limit container resources with `--memory` and `--cpus`
- Use read-only volumes when possible: `-v $(pwd):/workspace:ro`
