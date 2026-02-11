# Build script for AI Agent Toolkit (Windows)

Write-Host "🔨 Building AI Agent Toolkit..." -ForegroundColor Cyan

# Clean previous builds
Write-Host "🧹 Cleaning previous builds..." -ForegroundColor Yellow
Remove-Item -Recurse -Force build, dist, *.egg-info -ErrorAction SilentlyContinue

# Build the package
Write-Host "📦 Building package..." -ForegroundColor Yellow
python -m build

Write-Host "✅ Build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📦 Distribution files created in dist/" -ForegroundColor Cyan
Write-Host ""
Write-Host "To install locally for testing:" -ForegroundColor Yellow
Write-Host "  pip install dist/ai_agent_toolkit-1.0.0-py3-none-any.whl" -ForegroundColor White
Write-Host ""
Write-Host "To publish to PyPI:" -ForegroundColor Yellow
Write-Host "  twine upload dist/*" -ForegroundColor White
