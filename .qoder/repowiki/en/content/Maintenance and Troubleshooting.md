# Maintenance and Troubleshooting Guide

<cite>
**Referenced Files in This Document**
- [README.md](file://README.md)
- [main.py](file://main.py)
- [requirements.txt](file://requirements.txt)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Common Issues and Solutions](#common-issues-and-solutions)
3. [GitHub API Rate Limiting](#github-api-rate-limiting)
4. [Authentication Failures](#authentication-failures)
5. [Empty Report Generation](#empty-report-generation)
6. [Database Connection Errors](#database-connection-errors)
7. [Environment Configuration](#environment-configuration)
8. [Debugging Techniques](#debugging-techniques)
9. [Database Inspection](#database-inspection)
10. [Error Recovery Procedures](#error-recovery-procedures)
11. [Known Limitations](#known-limitations)
12. [Performance Optimization](#performance-optimization)

## Introduction

The github_cve_monitor application is designed to automatically monitor GitHub repositories for CVE (Common Vulnerabilities and Exposures) information and generate comprehensive reports. This guide provides detailed troubleshooting procedures, maintenance strategies, and diagnostic techniques to ensure optimal operation of the monitoring system.

The application uses Python with SQLite database storage and interacts with the GitHub API to collect CVE-related repository data. It generates both full historical reports and daily intelligence briefings, making it essential to maintain proper configuration and handle common operational issues effectively.

## Common Issues and Solutions

### Application Startup Problems

**Issue**: Application fails to start or throws import errors
**Symptoms**: 
- ImportError exceptions during startup
- ModuleNotFoundError for missing packages
- Database connection failures

**Diagnostic Steps**:
1. Verify Python environment requirements
2. Check package installations
3. Validate database file permissions

**Solution**:
```bash
# Install required packages
pip install -r requirements.txt

# Verify package installation
pip show peewee requests

# Check database directory permissions
ls -la db/
```

### Network Connectivity Issues

**Issue**: Unable to connect to GitHub API
**Symptoms**:
- Timeout errors during API calls
- SSL certificate verification failures
- Proxy-related connectivity problems

**Diagnostic Steps**:
1. Test basic internet connectivity
2. Verify proxy settings if applicable
3. Check firewall configurations

**Solution**:
```python
# Add retry mechanism with exponential backoff
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
```

**Section sources**
- [main.py](file://main.py#L1-L50)

## GitHub API Rate Limiting

### Understanding Rate Limits

The GitHub API has strict rate limiting policies that significantly impact application performance:

- **Unauthenticated requests**: 60 requests per hour
- **Authenticated requests with token**: 5,000 requests per hour
- **Search API limits**: 1,000 requests per hour

### Rate Limit Monitoring

The application includes built-in rate limit monitoring:

```python
if 'X-RateLimit-Limit' in response.headers:
    print(f"API Rate Limit: {response.headers.get('X-RateLimit-Remaining')}/{response.headers.get('X-RateLimit-Limit')}")
```

### Rate Limit Solutions

**Without Authentication Token**:
- The application implements random delays between requests
- Delays range from 3 to 15 seconds to avoid hitting rate limits
- Pagination continues until all pages are processed

**With Authentication Token**:
- Significantly increases rate limit to 5,000 requests per hour
- Reduces need for random delays
- Improves overall performance and reliability

**Section sources**
- [main.py](file://main.py#L150-L180)

## Authentication Failures

### Token Configuration Issues

**Problem**: GitHub API returns 401 Unauthorized errors
**Causes**:
- Incorrect or expired GITHUB_TOKEN
- Environment variable not properly set
- Token lacks necessary permissions

### Verification Steps

1. **Check Environment Variable**:
```bash
# Linux/macOS
echo $GITHUB_TOKEN

# Windows
echo %GITHUB_TOKEN%
```

2. **Verify Token Validity**:
```python
import requests
headers = {'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}'}
response = requests.get('https://api.github.com/user', headers=headers)
print(response.status_code)  # Should be 200
```

3. **Test Token Permissions**:
- Ensure token has `repo` scope for private repository access
- Verify token hasn't exceeded monthly quota
- Check if token has been revoked

### Token Setup Instructions

**Local Development**:
```bash
# Linux/macOS
export GITHUB_TOKEN=your_token_here

# Windows
set GITHUB_TOKEN=your_token_here
```

**GitHub Actions**:
1. Go to your repository settings
2. Navigate to "Secrets and variables" → "Actions"
3. Add a new secret named `GH_TOKEN`
4. Paste your GitHub Personal Access Token

**Section sources**
- [README.md](file://README.md#L25-L45)
- [main.py](file://main.py#L150-L170)

## Empty Report Generation

### Causes of Empty Reports

The application handles several scenarios where no new CVE data is available:

1. **No New Data Today**: When no new CVE repositories are created today
2. **API Limitations**: Rate limits preventing data collection
3. **Network Issues**: Failed API requests
4. **Authentication Problems**: Invalid tokens or permissions

### Fallback Mechanism

The application implements intelligent fallback strategies:

```python
# If no today data, use recent records
if len(today_list) == 0:
    print("当日无数据，尝试获取最近7天的数据...")
    # Get recent records from last 7 days
    cur.execute(f"SELECT * FROM CVE_DB WHERE created_at >= '{seven_days_ago}' ORDER BY created_at DESC;")
    recent_records = cur.fetchall()
    
    # If still no data, get latest 10 records
    if len(recent_records) == 0:
        print("最近7天无数据，获取最近10条记录...")
        cur.execute("SELECT * FROM CVE_DB ORDER BY created_at DESC LIMIT 10;")
        recent_records = cur.fetchall()
```

### Diagnostic Commands

To troubleshoot empty report issues:

1. **Check Database Records**:
```sql
SELECT COUNT(*) FROM CVE_DB;
SELECT * FROM CVE_DB ORDER BY created_at DESC LIMIT 10;
```

2. **Verify Recent Activity**:
```python
# Check if there are recent records in database
cur.execute("SELECT created_at FROM CVE_DB ORDER BY created_at DESC LIMIT 1;")
last_record = cur.fetchone()
print(f"Last record date: {last_record[0]}")
```

3. **Monitor API Responses**:
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Section sources**
- [main.py](file://main.py#L350-L390)

## Database Connection Errors

### SQLite Database Issues

The application uses SQLite for local data storage. Common database problems include:

**File Permission Issues**:
- Database file locked by another process
- Insufficient write permissions
- Disk space exhaustion

**Corruption Issues**:
- Database file corruption
- Transaction failures
- Concurrent access conflicts

### Database Maintenance

**Check Database Health**:
```python
# Verify database connection
try:
    db.connect()
    print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")

# Check table structure
cur = db.cursor()
cur.execute("PRAGMA table_info(CVE_DB);")
columns = cur.fetchall()
print(f"Database columns: {[col[1] for col in columns]}")
```

**Repair Corrupted Databases**:
```python
# Backup existing database
import shutil
shutil.copy('db/cve.sqlite', 'db/cve_backup.sqlite')

# Recreate database
db.drop_tables([CVE_DB])
db.create_tables([CVE_DB])
```

### Database Directory Management

Ensure proper directory structure:
```bash
# Create required directories
mkdir -p db docs/docs/Data
chmod 755 db docs/docs/Data
```

**Section sources**
- [main.py](file://main.py#L20-L30)

## Environment Configuration

### Essential Environment Variables

The application relies on specific environment variables for proper operation:

**Required Variables**:
- `GITHUB_TOKEN`: GitHub Personal Access Token for authenticated API requests
- `PYTHONPATH`: Python module search path (if using virtual environments)

**Optional Variables**:
- `LANG`: Locale setting for Chinese character display
- `LC_ALL`: Locale configuration

### Configuration Validation

**Script for Environment Validation**:
```python
import os
import sys

def validate_environment():
    """Validate required environment variables"""
    required_vars = ['GITHUB_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Missing required environment variables: {missing_vars}")
        return False
    
    print("All required environment variables are set")
    return True

if __name__ == "__main__":
    validate_environment()
```

### Virtual Environment Setup

**Recommended Setup**:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

**Section sources**
- [main.py](file://main.py#L150-L170)
- [requirements.txt](file://requirements.txt#L1-L3)

## Debugging Techniques

### Enabling Verbose Output

The application includes built-in debugging capabilities:

```python
# Enable debug printing
def get_info(year):
    # ... existing code ...
    
    if github_token:
        print(f"DEBUG: GITHUB_TOKEN is set. Value: {github_token[:5]}...")  # Print partial token for security
        headers['Authorization'] = f'token {github_token}'
        print(f"Using GitHub Token for authentication (Year: {year})")
    else:
        print("DEBUG: GITHUB_TOKEN is NOT set.")
        per_page = 30  # Unauthenticated requests
        print(f"No GitHub Token found, using unauthenticated request (Year: {year})")
    
    print("DEBUG: os.environ content:")
    for key, value in os.environ.items():
        if "GITHUB" in key.upper():  # Only print relevant environment variables
            print(f"  {key}: {value[:10]}...")
```

### Log Analysis

**Key Log Messages to Monitor**:
1. `DEBUG: GITHUB_TOKEN is set/unset` - Token configuration status
2. `API Rate Limit: X/Y` - Current API usage
3. `Using GitHub Token for authentication` - Authentication success
4. `No GitHub Token found` - Unauthenticated requests
5. `获取到 X 条原始数据` - Data collection progress
6. `更新 Y 条记录` - Database update status

### Manual Testing Commands

**Test GitHub API Access**:
```bash
# Test with curl
curl -H "Authorization: token $GITHUB_TOKEN" \
     "https://api.github.com/search/repositories?q=CVE-2024&sort=updated&page=1&per_page=10"

# Test without token
curl "https://api.github.com/search/repositories?q=CVE-2024&sort=updated&page=1&per_page=10"
```

**Test Database Operations**:
```python
# Interactive database testing
from main import db, CVE_DB

# Test connection
db.connect()

# Test queries
results = CVE_DB.select().limit(5)
for record in results:
    print(f"CVE: {record.cve}, Repo: {record.full_name}")
```

**Section sources**
- [main.py](file://main.py#L150-L180)

## Database Inspection

### Manual Data Verification

**Inspect Database Content**:
```python
# Connect to database
from main import db, CVE_DB

def inspect_database():
    """Manual database inspection"""
    db.connect()
    
    # Count total records
    total_records = CVE_DB.select().count()
    print(f"Total records: {total_records}")
    
    # Check recent records
    recent_records = CVE_DB.select().order_by(CVE_DB.created_at.desc()).limit(10)
    print("\nRecent records:")
    for record in recent_records:
        print(f"  {record.cve} - {record.full_name} ({record.created_at})")
    
    # Check for duplicates
    query = """
    SELECT cve, COUNT(*) as count 
    FROM CVE_DB 
    GROUP BY cve 
    HAVING count > 1
    """
    duplicates = db.execute_sql(query)
    print(f"\nDuplicate CVEs: {duplicates.rowcount}")
    
    # Check for malformed CVEs
    malformeds = CVE_DB.select().where(CVE_DB.cve.contains('_'))
    print(f"Records with underscore CVEs: {malformeds.count()}")

if __name__ == "__main__":
    inspect_database()
```

### Database Schema Validation

**Verify Table Structure**:
```sql
PRAGMA table_info(CVE_DB);
```

**Expected Columns**:
- `id` (INTEGER): Unique identifier
- `full_name` (VARCHAR): Repository full name
- `description` (VARCHAR): Repository description
- `url` (VARCHAR): GitHub URL
- `created_at` (VARCHAR): Creation timestamp
- `cve` (VARCHAR): CVE identifier

### Data Quality Checks

**Automated Data Validation Script**:
```python
def validate_data_quality():
    """Perform data quality checks"""
    db.connect()
    
    # Check for empty descriptions
    empty_desc = CVE_DB.select().where(CVE_DB.description == '')
    print(f"Records with empty descriptions: {empty_desc.count()}")
    
    # Check for malformed URLs
    malformed_urls = CVE_DB.select().where(~CVE_DB.url.startswith('https://github.com/'))
    print(f"Potentially malformed URLs: {malformed_urls.count()}")
    
    # Check for invalid CVE formats
    invalid_cves = CVE_DB.select().where(~CVE_DB.cve.regexp(r'^CVE-\d{4}-\d{4,7}$'))
    print(f"Potentially invalid CVE formats: {invalid_cves.count()}")
```

**Section sources**
- [main.py](file://main.py#L20-L30)
- [main.py](file://main.py#L350-L390)

## Error Recovery Procedures

### Application Restart Strategies

**Graceful Shutdown**:
```python
import signal
import sys

def graceful_shutdown(signum, frame):
    """Handle graceful shutdown"""
    print("Shutting down gracefully...")
    try:
        db.close()
    except:
        pass
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)
```

### Recovery After Failed Runs

**Step-by-Step Recovery Process**:

1. **Check Application Status**:
```bash
# Check if application is running
ps aux | grep python | grep main.py

# Kill hanging processes
pkill -f "python.*main.py"
```

2. **Reset Database State**:
```python
# Reset database for fresh start
from main import db, CVE_DB

def reset_database():
    """Reset database to clean state"""
    try:
        db.drop_tables([CVE_DB])
        db.create_tables([CVE_DB])
        print("Database reset completed")
    except Exception as e:
        print(f"Database reset failed: {e}")
```

3. **Clear Temporary Files**:
```bash
# Remove temporary files
rm -rf docs/Data/* tmp/*

# Clear cache if applicable
find . -name "*.pyc" -delete
```

### Error Handling Implementation

**Enhanced Error Handling**:
```python
import traceback
import logging

def safe_execute(func):
    """Decorator for safe function execution with error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            logging.error(traceback.format_exc())
            return None
    return wrapper

@safe_execute
def get_info_with_retry(year, max_retries=3):
    """Get information with automatic retry"""
    for attempt in range(max_retries):
        try:
            return get_info(year)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            wait_time = 2 ** attempt
            time.sleep(wait_time)
            print(f"Retry {attempt + 1} after {wait_time}s")
    return None
```

**Section sources**
- [main.py](file://main.py#L150-L180)

## Known Limitations

### Timezone Issues

**Current Problem**: UTC-CN timezone discrepancy causing 24-hour delay
**Impact**: Daily reports may show yesterday's data instead of today's
**Status**: Fixed in version 2.1 (as noted in README)

**Verification**:
```python
from datetime import datetime, timezone
import pytz

# Check timezone handling
utc_now = datetime.now(timezone.utc)
local_tz = pytz.timezone('Asia/Shanghai')
local_now = utc_now.astimezone(local_tz)

print(f"UTC time: {utc_now}")
print(f"Local time: {local_now}")
print(f"Difference: {(local_now - utc_now).total_seconds() / 3600} hours")
```

### Pagination Constraints

**Limitation**: GitHub API paginates results at 100 items per page
**Workaround**: The application handles pagination automatically
**Code Reference**:
```python
# Automatic pagination handling
while True:
    api = f"https://api.github.com/search/repositories?q=CVE-{year}&sort=updated&page={page}&per_page={per_page}"
    response = requests.get(api, headers=headers)
    
    if len(items) < per_page:
        break  # Last page reached
    page += 1
```

### Data Extraction Limitations

**CVE Pattern Matching**: Uses regex pattern `[Cc][Vv][Ee][-_]\d{4}[-_]\d{4,7}`
**Potential Issues**:
- May miss CVEs with unusual formatting
- Could incorrectly extract CVE-like strings from descriptions
- Limited to CVE format detection

**Enhancement Suggestions**:
```python
# Enhanced CVE pattern matching
import re

def extract_cve_enhanced(text):
    """Enhanced CVE extraction with multiple patterns"""
    patterns = [
        r'\bCVE[-_]\d{4}[-_]\d{4,7}\b',  # Standard format
        r'\bCVE\s*\d{4}[-_]\d{4,7}\b',  # With space
        r'\bCVE\d{4}[-_]\d{4,7}\b',     # Compact format
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return matches[0].replace('_', '-')
    
    return "CVE Not Found"
```

### Historical Data Retrieval

**Limitations**:
- Historical data retrieval can be slow for older years
- Rate limiting affects historical data collection
- No incremental updates for historical data

**Optimization Strategy**:
```python
# Optimized historical data retrieval
def get_historical_data(start_year=2000, end_year=2024):
    """Retrieve historical data with optimized rate limiting"""
    results = []
    
    for year in range(end_year, start_year - 1, -1):
        try:
            year_data = get_info(year)
            if year_data:
                results.extend(year_data)
                # Add delay between years
                time.sleep(random.uniform(2, 5))
        except Exception as e:
            print(f"Failed to retrieve data for year {year}: {e}")
            continue
    
    return results
```

**Section sources**
- [README.md](file://README.md#L15-L25)
- [main.py](file://main.py#L150-L180)

## Performance Optimization

### Request Optimization

**Rate Limit Management**:
```python
import time
import random

def optimized_api_request(api_url, headers=None, max_retries=3):
    """Optimized API request with intelligent delays"""
    for attempt in range(max_retries):
        response = requests.get(api_url, headers=headers, timeout=30)
        
        # Check rate limit headers
        if 'X-RateLimit-Remaining' in response.headers:
            remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
            if remaining < 10:
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                sleep_time = max(0, reset_time - int(time.time())) + 60
                print(f"Approaching rate limit, sleeping for {sleep_time}s")
                time.sleep(sleep_time)
        
        if response.status_code == 200:
            return response.json()
        
        if attempt == max_retries - 1:
            raise Exception(f"API request failed after {max_retries} attempts")
        
        # Exponential backoff
        wait_time = 2 ** attempt + random.uniform(1, 3)
        time.sleep(wait_time)
    
    return None
```

### Memory Management

**Large Dataset Handling**:
```python
def process_large_dataset(items, batch_size=100):
    """Process large datasets in batches to manage memory"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        yield batch
        
        # Small pause between batches
        time.sleep(0.1)

# Usage
for batch in process_large_dataset(all_items):
    db_match(batch)
```

### Caching Strategy

**Implement Local Caching**:
```python
import hashlib
import json
from pathlib import Path

CACHE_DIR = Path("cache")

def get_cached_response(url, ttl=3600):
    """Get cached response if available and not expired"""
    CACHE_DIR.mkdir(exist_ok=True)
    
    # Create cache key
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_file = CACHE_DIR / f"{cache_key}.json"
    
    if cache_file.exists():
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        # Check if cache is still valid
        if time.time() - data['timestamp'] < ttl:
            return data['data']
    
    return None

def cache_response(url, data):
    """Cache API response"""
    CACHE_DIR.mkdir(exist_ok=True)
    
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_file = CACHE_DIR / f"{cache_key}.json"
    
    with open(cache_file, 'w') as f:
        json.dump({
            'timestamp': time.time(),
            'data': data,
            'url': url
        }, f)
```

### Monitoring and Metrics

**Implementation Metrics Collection**:
```python
import time
from collections import defaultdict

class PerformanceMonitor:
    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_times = {}
    
    def start_timer(self, operation):
        """Start timing an operation"""
        self.start_times[operation] = time.time()
    
    def end_timer(self, operation):
        """End timing and record metrics"""
        if operation in self.start_times:
            duration = time.time() - self.start_times[operation]
            self.metrics[operation].append(duration)
            del self.start_times[operation]
    
    def get_average_duration(self, operation):
        """Get average duration for an operation"""
        durations = self.metrics.get(operation, [])
        return sum(durations) / len(durations) if durations else 0
    
    def log_performance_summary(self):
        """Log performance summary"""
        print("\n=== Performance Summary ===")
        for operation, durations in self.metrics.items():
            avg_duration = sum(durations) / len(durations)
            min_duration = min(durations)
            max_duration = max(durations)
            print(f"{operation}: avg={avg_duration:.2f}s, min={min_duration:.2f}s, max={max_duration:.2f}s")

# Global performance monitor
perf_monitor = PerformanceMonitor()

# Usage in main functions
def get_info(year):
    perf_monitor.start_timer(f"get_info_{year}")
    # ... existing code ...
    perf_monitor.end_timer(f"get_info_{year}")
```

This comprehensive troubleshooting guide provides detailed procedures for maintaining and operating the github_cve_monitor application effectively. Regular monitoring, proper configuration, and adherence to these guidelines will ensure reliable operation and minimize downtime.