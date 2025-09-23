# Installation and Setup Guide

<cite>
**Referenced Files in This Document**
- [README.md](file://README.md)
- [main.py](file://main.py)
- [requirements.txt](file://requirements.txt)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Environment Setup](#environment-setup)
4. [Dependency Installation](#dependency-installation)
5. [GitHub Token Configuration](#github-token-configuration)
6. [Platform-Specific Instructions](#platform-specific-instructions)
7. [Authentication Impact](#authentication-impact)
8. [Running the Application](#running-the-application)
9. [Common Setup Issues](#common-setup-issues)
10. [Troubleshooting](#troubleshooting)

## Introduction

The github_cve_monitor is a Python-based application designed to automatically monitor GitHub repositories for CVE (Common Vulnerabilities and Exposures) information. This guide provides comprehensive instructions for setting up the development environment, configuring authentication, and resolving common setup issues.

The application uses GitHub's API to search for repositories containing CVE identifiers and maintains a local SQLite database to track changes over time. It generates daily reports and maintains historical data for analysis.

## Prerequisites

### Python Environment

Before setting up the github_cve_monitor, ensure you have the following prerequisites installed:

1. **Python 3.6 or higher**: The application requires Python 3.6 or later for proper functionality
2. **pip package manager**: Used for installing Python dependencies
3. **Git**: Recommended for cloning the repository and managing updates

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 512MB RAM (1GB recommended)
- **Storage**: At least 100MB free disk space
- **Network**: Internet connection for GitHub API access

### Verify Python Installation

To check if Python is installed and verify the version:

```bash
python --version
# or
python3 --version
```

Expected output should show Python 3.6 or higher version number.

## Environment Setup

### Creating a Virtual Environment

It's recommended to create a virtual environment to isolate project dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Directory Structure

After setup, your project directory should look like this:

```
github_cve_monitor/
├── venv/                 # Virtual environment (created during setup)
├── db/                   # Database directory (automatically created)
├── docs/                 # Output documentation directory
├── main.py              # Main application script
├── requirements.txt     # Dependencies file
└── README.md           # Project documentation
```

## Dependency Installation

### Installing Required Packages

The application requires two main dependencies as specified in the requirements.txt file:

1. **peewee**: A lightweight ORM for SQLite database operations
2. **requests**: HTTP library for making API requests to GitHub

### Installation Steps

Execute the following command to install all dependencies:

```bash
pip install -r requirements.txt
```

### Package Details

- **peewee==3.18.2**: Provides database abstraction and ORM functionality
- **requests==2.31.0**: Handles HTTP communication with GitHub API

### Verification

After installation, verify that packages are correctly installed:

```bash
pip list | grep -E "(peewee|requests)"
```

Expected output:
```
peewee          3.18.2
requests        2.31.0
```

**Section sources**
- [requirements.txt](file://requirements.txt#L1-L3)
- [main.py](file://main.py#L1-L15)

## GitHub Token Configuration

### Understanding Authentication

The github_cve_monitor supports GitHub Token authentication to increase API rate limits from 60 requests per hour (unauthenticated) to 5000 requests per hour (authenticated).

### Creating a GitHub Personal Access Token

1. **Access GitHub Settings**:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token"

2. **Token Permissions**:
   - Select "repo" scope for repository access
   - Choose appropriate scopes based on your needs
   - Set expiration date or select "No expiration"

3. **Copy Token**:
   - After creation, copy the token value
   - Store securely - you won't be able to see it again

### Setting Environment Variables

#### Local Development

Set the `GITHUB_TOKEN` environment variable:

**Linux/macOS**:
```bash
export GITHUB_TOKEN=your_token_here
echo "export GITHUB_TOKEN=your_token_here" >> ~/.bashrc  # Add to startup
```

**Windows (Command Prompt)**:
```cmd
set GITHUB_TOKEN=your_token_here
```

**Windows (PowerShell)**:
```powershell
$env:GITHUB_TOKEN="your_token_here"
```

#### Persistent Configuration

Add the export statement to your shell profile for persistent configuration:

**Bash/Zsh** (Linux/macOS):
```bash
echo 'export GITHUB_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

**Fish Shell** (Linux/macOS):
```fish
echo 'set -gx GITHUB_TOKEN "your_token_here"' >> ~/.config/fish/config.fish
```

### GitHub Actions Configuration

For automated deployments using GitHub Actions:

1. **Repository Secrets**:
   - Go to your GitHub repository
   - Navigate to Settings → Secrets and variables → Actions
   - Add a new secret named `GH_TOKEN` with your token value

2. **Workflow Integration**:
   - The application automatically detects `GH_TOKEN` in GitHub Actions
   - No additional configuration is required in the workflow files

**Section sources**
- [README.md](file://README.md#L25-L45)
- [main.py](file://main.py#L100-L120)

## Platform-Specific Instructions

### Linux/macOS Setup

#### Step-by-Step Installation

```bash
# Clone the repository
git clone https://github.com/adminlove520/github_cve_monitor.git
cd github_cve_monitor

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GITHUB_TOKEN=your_token_here

# Run the application
python main.py
```

#### Directory Permissions

Ensure proper permissions for the database and output directories:

```bash
chmod 755 .
mkdir -p db docs
chmod 755 db docs
```

### Windows Setup

#### PowerShell Installation

```powershell
# Clone repository
git clone https://github.com/adminlove520/github_cve_monitor.git
cd github_cve_monitor

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable
$env:GITHUB_TOKEN="your_token_here"

# Run the application
python main.py
```

#### Command Prompt Installation

```cmd
REM Clone repository
git clone https://github.com/adminlove520/github_cve_monitor.git
cd github_cve_monitor

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Set environment variable
set GITHUB_TOKEN=your_token_here

REM Run the application
python main.py
```

### Docker Setup (Alternative)

For containerized deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV GITHUB_TOKEN=""
CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t github-cve-monitor .
docker run -e GITHUB_TOKEN=$GITHUB_TOKEN github-cve-monitor
```

## Authentication Impact

### Rate Limit Comparison

Understanding the difference between authenticated and unauthenticated API access:

| Authentication Type | Rate Limit | Requests per Hour | Use Case |
|---------------------|------------|-------------------|----------|
| Unauthenticated | 60 | 60 | Testing, limited usage |
| Authenticated | 5000 | 5000 | Production, regular usage |

### Implementation Details

The application automatically detects and handles authentication:

```python
github_token = os.environ.get('GITHUB_TOKEN')
headers = {}

if github_token:
    headers['Authorization'] = f'token {github_token}'
    print("Using GitHub Token for authentication")
else:
    per_page = 30  # Reduced limit without token
    print("No GitHub Token found, using unauthenticated request")
```

### Rate Limit Monitoring

The application includes built-in rate limit monitoring:

```python
if 'X-RateLimit-Limit' in response.headers:
    print(f"API Rate Limit: {response.headers.get('X-RateLimit-Remaining')}/{response.headers.get('X-RateLimit-Limit')}")
```

This helps developers understand their current rate limit status and adjust their usage accordingly.

**Section sources**
- [main.py](file://main.py#L100-L130)

## Running the Application

### Basic Execution

After successful setup, run the application:

```bash
python main.py
```

### Expected Output

The application will generate several types of reports:

1. **Full Report**: Complete historical data in `docs/README.md`
2. **Daily Reports**: Current day's data in `docs/Data/YYYY-Www-dd/daily_YYYYMMDD.md`
3. **Index Files**: Navigation and metadata in various locations

### Directory Structure After Execution

```
github_cve_monitor/
├── db/
│   └── cve.sqlite      # SQLite database file
├── docs/
│   ├── README.md       # Full report
│   ├── Data/           # Daily reports organized by date
│   │   ├── YYYY-Www-dd/
│   │   │   └── daily_YYYYMMDD.md
│   │   └── index.md    # Daily reports index
│   └── _sidebar.md     # Navigation sidebar
└── main.py
```

### Scheduling Automation

For automated execution, configure cron jobs or scheduled tasks:

**Linux/macOS Cron**:
```bash
# Edit crontab
crontab -e

# Add daily execution at midnight
0 0 * * * cd /path/to/github_cve_monitor && source venv/bin/activate && python main.py >> logs/cron.log 2>&1
```

**Windows Task Scheduler**:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to daily at desired time
4. Action: Start a program
5. Program/script: python.exe
6. Add arguments: main.py
7. Start in: path to project directory

## Common Setup Issues

### Missing Dependencies

**Problem**: ImportError or ModuleNotFoundError
```
ModuleNotFoundError: No module named 'peewee'
```

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip install peewee requests
```

### Incorrect Token Configuration

**Problem**: Rate limiting or authentication errors
```
HTTP 403 Forbidden: Rate limit exceeded
```

**Solution**:
1. Verify token is set correctly:
```bash
echo $GITHUB_TOKEN  # Linux/macOS
echo %GITHUB_TOKEN% # Windows Command Prompt
echo $env:GITHUB_TOKEN # Windows PowerShell
```

2. Check token permissions and expiration

### Permission Errors

**Problem**: Cannot create database or write files
```
PermissionError: [Errno 13] Permission denied
```

**Solution**:
```bash
# Fix directory permissions
chmod 755 .
chmod 755 db
chmod 755 docs

# Or run with elevated privileges (not recommended)
sudo python main.py
```

### Database Connection Issues

**Problem**: SQLite database access errors
```
sqlite3.OperationalError: unable to open database file
```

**Solution**:
1. Ensure database directory exists:
```bash
mkdir -p db
```

2. Check file permissions:
```bash
ls -la db/
```

3. Verify Python has write access to the directory

### Network Connectivity Issues

**Problem**: Unable to connect to GitHub API
```
ConnectionError: HTTPSConnectionPool
```

**Solution**:
1. Check internet connectivity
2. Verify firewall settings
3. Configure proxy if behind corporate firewall

## Troubleshooting

### Debug Mode

Enable debug output for detailed troubleshooting:

```python
# Add to main.py for enhanced logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### API Access Problems

#### Issue: Rate Limit Exceeded

**Symptoms**:
- HTTP 403 responses
- Rate limit headers present but exceeded
- Random delays in execution

**Diagnosis**:
```python
# Check rate limit headers
print(response.headers.get('X-RateLimit-Remaining'))
print(response.headers.get('X-RateLimit-Reset'))
```

**Solutions**:
1. Use GitHub Token authentication
2. Implement exponential backoff
3. Reduce API calls frequency

#### Issue: Token Authentication Failures

**Symptoms**:
- HTTP 401 Unauthorized
- Invalid token errors
- Authentication header issues

**Diagnosis**:
```python
# Test token validity
headers = {'Authorization': f'token {github_token}'}
response = requests.get('https://api.github.com/user', headers=headers)
print(response.status_code)
print(response.json())
```

**Solutions**:
1. Regenerate GitHub token
2. Verify token permissions
3. Check token format and length

#### Issue: SSL Certificate Problems

**Symptoms**:
- SSL certificate verification errors
- HTTPS connection failures
- Certificate authority issues

**Solutions**:
```bash
# Update certificates
pip install --upgrade certifi

# Or disable SSL verification (not recommended for production)
export PYTHONHTTPSVERIFY=0
```

### Performance Issues

#### Slow API Responses

**Causes**:
- Rate limiting
- Network latency
- Large dataset processing

**Optimizations**:
1. Enable token authentication
2. Implement caching mechanisms
3. Optimize database queries
4. Use pagination efficiently

#### Memory Usage

**Monitoring**:
```python
import psutil
process = psutil.Process(os.getpid())
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
```

**Solutions**:
1. Process data in chunks
2. Close database connections properly
3. Clear unused variables

### Log Analysis

Enable comprehensive logging for troubleshooting:

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('application.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks

Implement health checks for automated monitoring:

```python
def health_check():
    """Perform basic health checks"""
    checks = []
    
    # Check Python version
    checks.append(("Python Version", sys.version))
    
    # Check dependencies
    try:
        import peewee
        import requests
        checks.append(("Dependencies", "OK"))
    except ImportError as e:
        checks.append(("Dependencies", f"Missing: {e}"))
    
    # Check database
    try:
        db.connect()
        checks.append(("Database", "OK"))
    except Exception as e:
        checks.append(("Database", f"Error: {e}"))
    
    return checks
```

**Section sources**
- [main.py](file://main.py#L100-L150)
- [main.py](file://main.py#L350-L400)

## Conclusion

The github_cve_monitor setup process involves several key steps: environment preparation, dependency installation, GitHub token configuration, and platform-specific adjustments. By following this comprehensive guide, you should be able to successfully deploy and run the application.

Key takeaways for successful setup:

1. **Always use GitHub tokens** for production environments to avoid rate limiting
2. **Verify environment variables** are correctly set before running the application
3. **Monitor rate limits** to prevent API access issues
4. **Implement proper error handling** for robust operation
5. **Schedule automation** for continuous monitoring

For ongoing maintenance, regularly update dependencies, monitor API changes, and keep your GitHub token secure and up-to-date.