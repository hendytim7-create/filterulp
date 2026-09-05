"""
Configuration management untuk parser application.
Centralized settings untuk mudah di-maintain dan scale.

All application-wide settings are defined here:
- GUI appearance & dimensions
- Processing parameters (concurrency, buffer size)
- Logging configuration
- Custom pattern detection
- Result storage paths
"""

import os
from pathlib import Path

# ===============================
# APPLICATION METADATA
# ===============================
APP_NAME = "FullFilterGUI"
APP_VERSION = "2.6.0"
APP_DESCRIPTION = "High-Performance Credential Parser & Classifier"

# ===============================
# APPLICATION PATHS
# ===============================
# Base directory (same level as v1parser.py)
APP_DIR = Path(__file__).parent.resolve()
RESULT_DIR = APP_DIR / "result"
LOGS_DIR = APP_DIR / "logs"

# Create directories if they don't exist
RESULT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ===============================
# GUI WINDOW CONFIGURATION
# ===============================
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION} - Clean & High Performance Edition"
WINDOW_WIDTH = 950
WINDOW_HEIGHT = 680
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 580

# ===============================
# PARSING CONFIGURATION
# ===============================
# Default parse mode: "line" for single-line or "block" for stealer logs
DEFAULT_PARSE_MODE = "line"

# Enable deduplication by default
DEFAULT_DEDUPLICATE = True

# Concurrency settings
DEFAULT_MAX_CONCURRENCY = 80
MIN_CONCURRENCY = 10
MAX_CONCURRENCY = 500

# ===============================
# FILE WRITER (I/O) CONFIGURATION
# ===============================
# Batch lines before flush (reduce I/O overhead)
BUFFER_SIZE = 100

# Write queue max size (prevent memory bloat)
WRITE_QUEUE_SIZE = 500

# ===============================
# LOGGING CONFIGURATION
# ===============================
LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
LOG_FILE = LOGS_DIR / "parser.log"
LOG_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB per file
LOG_BACKUP_COUNT = 3  # Keep 3 backup log files

# ===============================
# UI UPDATE INTERVALS
# ===============================
# Update progress stats every N seconds (reduce CPU overhead)
STATS_UPDATE_INTERVAL = 0.2

# Console output debounce (reduce UI spam)
CONSOLE_UPDATE_DEBOUNCE = 0.1

# ===============================
# COLOR SCHEME (Dark Mode)
# ===============================
class Colors:
    """Centralized color definitions for consistent UI theming"""
    
    # Backgrounds
    BG_DARK = "#0a0a0a"      # Main background
    BG_PANEL = "#141424"      # Panel background
    BG_INPUT = "#1e1e30"      # Input/text area background
    
    # Accent Colors
    ACCENT_RED = "#ff3333"    # Primary action (START, errors)
    ACCENT_CYAN = "#00d9ff"   # Secondary action, info
    ACCENT_GREEN = "#00ff88"  # Success, ready status
    ACCENT_YELLOW = "#ffaa00" # Warning, processing
    
    # Text Colors
    TEXT_WHITE = "#ffffff"        # Primary text
    TEXT_GRAY = "#cccccc"         # Secondary text
    TEXT_DARK_GRAY = "#888888"    # Tertiary text
    
    # Borders
    BORDER_CYAN = "#00d9ff"

# ===============================
# PLATFORM DETECTION - PATTERN KEYS
# ===============================
# Keys digunakan untuk smart block detection (parse_block_smart mode)
# Digunakan untuk identify URL, username, password dari unstructured data

CORE_URL_KEYS = {
    "url", "host", "site", "link", "domain", "address",
    "uri", "target", "page", "location", "endpoint",
    "server", "website", "portal", "panel"
}

CORE_USER_KEYS = {
    "user", "username", "login", "email", "account",
    "usr", "mail", "identity", "u", "admin",
    "uname", "uid", "userid", "member"
}

CORE_PASS_KEYS = {
    "pass", "password", "pwd", "pasw", "secret", "p",
    "passwd", "pswd", "pw", "credentials",
    "credential", "passphrase", "token"
}

# ===============================
# PARSE MODE DEFAULTS BY INPUT TYPE
# ===============================
# Automatically select parse mode berdasarkan input type
PARSE_MODE_AUTO_SELECT = {
    "single_file": "line",      # Single .txt file -> line mode
    "multiple_files": "line",   # Multiple .txt files -> line mode
    "folder": "block"           # Folder input -> block mode (stealer logs)
}

# ===============================
# OUTPUT CONFIGURATION
# ===============================
# Result files naming scheme
RESULT_FILE_EXTENSION = ".txt"
UNCLASSIFIED_FILENAME = "unclassified.txt"

# Output encoding
OUTPUT_ENCODING = "utf-8"
OUTPUT_NEWLINE = "\n"

# Separator untuk combo output (URL|USER|PASS)
COMBO_SEPARATOR = "|"

# ===============================
# PLATFORM TARGETS
# ===============================
# List dari semua target platforms yang di-support
# Urutan: ini adalah urutan file output akan di-create
SUPPORTED_PLATFORMS = [
    "wordpress.txt",
    "joomla.txt",
    "drupal.txt",
    "prestashop.txt",
    "magento.txt",
    "opencart.txt",
    "shopify.txt",
    "laravel.txt",
    "moodle.txt",
    "ojs_journal.txt",
    "phpmyadmin.txt",
    "grafana.txt",
    "cpanel.txt",
    "whm.txt",
    "plesk.txt",
    "ssh.txt",
    "ftp.txt",
]

# ===============================
# VALIDATION RULES
# ===============================
# Minimum URL length untuk dianggap valid
MIN_URL_LENGTH = 5

# Maximum URL length untuk dianggap valid
MAX_URL_LENGTH = 2048

# Minimum password length
MIN_PASSWORD_LENGTH = 1

# Require email-like username?
REQUIRE_EMAIL_FORMAT = False  # If True, username harus @ format

# ===============================
# PERFORMANCE TUNING
# ===============================
# File size limit untuk load ke memory sekaligus (bytes)
# Files lebih besar akan di-read in chunks
FILE_CHUNK_SIZE = 1024 * 1024  # 1MB chunks

# Max concurrent file operations
MAX_CONCURRENT_FILES = 50

# ===============================
# DEBUG & DEVELOPMENT
# ===============================
# Enable verbose logging & debug output
DEBUG = False

# Log parsed combos ke console (only in DEBUG mode)
DEBUG_LOG_COMBOS = False

# Dry-run mode (process tapi jangan write results)
DRY_RUN = False

# ===============================
# FEATURE FLAGS
# ===============================
# Enable/disable features
FEATURES = {
    "export_json": False,      # Export results to JSON (future)
    "export_csv": False,       # Export results to CSV (future)
    "auto_cleanup": True,      # Auto-cleanup temp files
    "backup_results": False,   # Backup previous results (future)
}

# ===============================
# STATISTICS & MONITORING
# ===============================
# Track processing statistics
ENABLE_STATS = True

# Show detailed platform breakdown in results
SHOW_PLATFORM_STATS = True

# Auto-generate summary report
GENERATE_SUMMARY_REPORT = True

# ===============================
# HELPER FUNCTIONS
# ===============================

def get_result_filepath(platform_filename: str) -> Path:
    """
    Get full path untuk result file dari platform
    
    Args:
        platform_filename: e.g., "wordpress.txt"
    
    Returns:
        Full path: result/wordpress.txt
    """
    return RESULT_DIR / platform_filename


def get_log_filepath() -> Path:
    """Get full path untuk log file"""
    return LOG_FILE


def validate_config() -> bool:
    """
    Validate configuration values
    
    Returns:
        True jika valid, False jika ada yang error
    """
    errors = []
    
    # Check concurrency
    if not (MIN_CONCURRENCY <= DEFAULT_MAX_CONCURRENCY <= MAX_CONCURRENCY):
        errors.append(
            f"DEFAULT_MAX_CONCURRENCY ({DEFAULT_MAX_CONCURRENCY}) "
            f"harus antara {MIN_CONCURRENCY} dan {MAX_CONCURRENCY}"
        )
    
    # Check directories exist
    if not RESULT_DIR.exists():
        errors.append(f"RESULT_DIR tidak bisa di-create: {RESULT_DIR}")
    
    if not LOGS_DIR.exists():
        errors.append(f"LOGS_DIR tidak bisa di-create: {LOGS_DIR}")
    
    # Check color values format
    for attr_name in dir(Colors):
        if not attr_name.startswith("_"):
            color_value = getattr(Colors, attr_name)
            if not isinstance(color_value, str) or not color_value.startswith("#"):
                errors.append(f"Colors.{attr_name} bukan valid hex color")
    
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  ❌ {error}")
        return False
    
    return True


def print_config_summary():
    """Print configuration summary untuk debugging"""
    print(f"""
╔══════════════════════════════════════════════════╗
║        {APP_NAME} v{APP_VERSION} - Configuration
╚══════════════════════════════════════════════════╝

📁 Paths:
  • Result Dir: {RESULT_DIR}
  • Logs Dir: {LOGS_DIR}

⚙️  Parsing:
  • Default Mode: {DEFAULT_PARSE_MODE}
  • Default Concurrency: {DEFAULT_MAX_CONCURRENCY}
  • Deduplication: {DEFAULT_DEDUPLICATE}

💾 I/O:
  • Buffer Size: {BUFFER_SIZE} lines
  • Write Queue Size: {WRITE_QUEUE_SIZE}

📊 Platforms Supported: {len(SUPPORTED_PLATFORMS)}
  {', '.join([p.replace('.txt', '') for p in SUPPORTED_PLATFORMS[:6]])}...

📝 Detection Keys:
  • URL Keys: {len(CORE_URL_KEYS)} patterns
  • User Keys: {len(CORE_USER_KEYS)} patterns
  • Pass Keys: {len(CORE_PASS_KEYS)} patterns
""")


# ===============================
# RUN VALIDATION ON IMPORT
# ===============================
if not validate_config():
    print("\n⚠️  WARNING: Configuration validation failed!")
    print("Some features may not work correctly.\n")
