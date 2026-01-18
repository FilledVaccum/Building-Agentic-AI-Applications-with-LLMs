#!/bin/bash
# Quick setup script for development environment

echo "🚀 Setting up NCP-AAI Course Development Environment..."
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -q jsonschema hypothesis pytest

# Create .env from template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your NVIDIA API keys"
else
    echo "✅ .env file already exists"
fi

# Make pre-push script executable
chmod +x pre-push-check.sh
echo "✅ Pre-push script is executable"

# Run tests to verify setup
echo ""
echo "🧪 Running tests to verify setup..."
if pytest tests/ -q; then
    echo ""
    echo "✅ All tests passed!"
else
    echo ""
    echo "⚠️  Some tests failed - check dependencies"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your NVIDIA API keys"
echo "2. Run: ./pre-push-check.sh"
echo "3. Start developing!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
