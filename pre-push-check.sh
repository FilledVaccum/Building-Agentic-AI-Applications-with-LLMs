#!/bin/bash
# Pre-push security and validation script
# Run this before pushing to GitHub

set -e

echo "🔍 Running pre-push security checks..."
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Function to print colored output
print_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
    ((ERRORS++))
}

print_warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
    ((WARNINGS++))
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# 1. Check for sensitive files
echo "1️⃣  Checking for sensitive files..."
SENSITIVE_PATTERNS=(
    "*.env"
    "*.pem"
    "*.key"
    "*.p12"
    "*.pfx"
    "*_rsa"
    "*_dsa"
    "secrets.json"
    "credentials.json"
    "*.secret"
)

for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if git ls-files | grep -q "$pattern"; then
        print_error "Sensitive file pattern found: $pattern"
    fi
done

if [ $ERRORS -eq 0 ]; then
    print_success "No sensitive file patterns found"
fi
echo ""

# 2. Check for hardcoded credentials in staged files
echo "2️⃣  Scanning for hardcoded credentials..."
CREDENTIAL_PATTERNS=(
    "api[_-]?key\s*=\s*['\"][^'\"]{20,}"
    "password\s*=\s*['\"][^'\"]{8,}"
    "secret\s*=\s*['\"][^'\"]{20,}"
    "token\s*=\s*['\"][^'\"]{20,}"
    "aws[_-]?access[_-]?key"
    "aws[_-]?secret"
    "AKIA[0-9A-Z]{16}"
    "sk-[a-zA-Z0-9]{32,}"
)

for file in $(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|js|ts|json|yaml|yml|sh|env)$'); do
    if [ -f "$file" ]; then
        for pattern in "${CREDENTIAL_PATTERNS[@]}"; do
            if grep -iE "$pattern" "$file" > /dev/null 2>&1; then
                # Exclude test files and examples
                if [[ ! "$file" =~ (test_|_test\.py|\.example|SECURITY\.md|\.env\.example) ]]; then
                    print_error "Potential hardcoded credential in $file"
                fi
            fi
        done
    fi
done

if [ $ERRORS -eq 0 ]; then
    print_success "No hardcoded credentials detected"
fi
echo ""

# 3. Check for large files
echo "3️⃣  Checking for large files (>10MB)..."
LARGE_FILES=$(git ls-files | xargs -I {} du -m {} 2>/dev/null | awk '$1 > 10 {print $2}')
if [ -n "$LARGE_FILES" ]; then
    while IFS= read -r file; do
        print_warning "Large file detected: $file"
    done <<< "$LARGE_FILES"
else
    print_success "No large files detected"
fi
echo ""

# 4. Verify .gitignore exists and is comprehensive
echo "4️⃣  Verifying .gitignore..."
if [ ! -f ".gitignore" ]; then
    print_error ".gitignore file not found"
else
    REQUIRED_PATTERNS=(
        "*.env"
        "__pycache__"
        "*.pyc"
        ".DS_Store"
        "*.key"
        "*.pem"
    )
    
    for pattern in "${REQUIRED_PATTERNS[@]}"; do
        if ! grep -q "$pattern" .gitignore; then
            print_warning ".gitignore missing pattern: $pattern"
        fi
    done
    
    if [ $WARNINGS -eq 0 ]; then
        print_success ".gitignore is comprehensive"
    fi
fi
echo ""

# 5. Check for TODO/FIXME comments in production code
echo "5️⃣  Checking for TODO/FIXME markers..."
TODO_COUNT=$(git grep -i "TODO\|FIXME" -- '*.py' '*.js' '*.ts' | grep -v "test_" | wc -l || true)
if [ "$TODO_COUNT" -gt 0 ]; then
    print_warning "Found $TODO_COUNT TODO/FIXME comments in production code"
else
    print_success "No TODO/FIXME markers in production code"
fi
echo ""

# 6. Run Python tests if available
echo "6️⃣  Running tests..."
if [ -f "requirements.txt" ] && command -v pytest &> /dev/null; then
    if pytest tests/ -q --tb=short 2>&1 | tail -5; then
        print_success "All tests passed"
    else
        print_error "Some tests failed"
    fi
else
    print_warning "pytest not available or requirements.txt not found"
fi
echo ""

# 7. Check Python code quality
echo "7️⃣  Checking Python code quality..."
if command -v flake8 &> /dev/null; then
    if flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics > /dev/null 2>&1; then
        print_success "No critical Python syntax errors"
    else
        print_warning "Python syntax issues detected"
    fi
else
    print_warning "flake8 not installed (optional)"
fi
echo ""

# 8. Verify required files exist
echo "8️⃣  Verifying required files..."
REQUIRED_FILES=(
    "README.md"
    "LICENSE"
    "SECURITY.md"
    ".gitignore"
    "requirements.txt"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Required file missing: $file"
    else
        print_success "Found $file"
    fi
done
echo ""

# 9. Check for .DS_Store and other OS files
echo "9️⃣  Checking for OS-specific files..."
OS_FILES=$(git ls-files | grep -E '(\.DS_Store|Thumbs\.db|desktop\.ini)' || true)
if [ -n "$OS_FILES" ]; then
    print_error "OS-specific files found in git: $OS_FILES"
else
    print_success "No OS-specific files in git"
fi
echo ""

# 10. Verify .kiro configuration
echo "🔟 Checking .kiro configuration..."
if [ -d ".kiro" ]; then
    # Check if sensitive .kiro files are gitignored
    if git check-ignore .kiro/settings/lsp.json > /dev/null 2>&1; then
        print_success ".kiro sensitive files are gitignored"
    else
        print_warning ".kiro/settings/lsp.json should be gitignored"
    fi
    
    # Verify steering and specs are included
    if [ -f ".kiro/steering/ncp-aai-course-development-guide.md" ]; then
        print_success ".kiro steering document found"
    else
        print_warning ".kiro steering document not found"
    fi
else
    print_warning ".kiro directory not found (optional)"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}❌ Found $ERRORS error(s)${NC}"
    echo "Please fix the errors before pushing to GitHub."
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Found $WARNINGS warning(s)${NC}"
    echo ""
    read -p "Continue with push? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Push cancelled."
        exit 1
    fi
else
    echo -e "${GREEN}✅ All checks passed!${NC}"
    echo "Repository is ready for GitHub push."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
