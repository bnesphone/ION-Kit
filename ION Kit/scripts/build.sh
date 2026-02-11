#!/bin/bash
# Build script for AI Agent Toolkit

echo "🔨 Building AI Agent Toolkit..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info

# Build the package
echo "📦 Building package..."
python -m build

echo "✅ Build complete!"
echo ""
echo "📦 Distribution files created in dist/"
echo ""
echo "To install locally for testing:"
echo "  pip install dist/ai_agent_toolkit-1.0.0-py3-none-any.whl"
echo ""
echo "To publish to PyPI:"
echo "  twine upload dist/*"
