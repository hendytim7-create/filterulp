"""
Platform detection - KEYWORD MODE v2.7
Simple keyword-based detection.
Special case: PrestaShop uses pattern (karena randomized URL).
"""

import re
from urllib.parse import urlparse
from typing import Optional, Dict, List, Tuple

# ===============================
# PLATFORM PATTERNS - KEYWORD ONLY
# ===============================
# HANYA detection keyword + special cases

PLATFORM_PATTERNS: Dict[str, List[Tuple[str, re.Pattern, int]]] = {
    # ========== CMS - KEYWORD ==========
    
    "wordpress.txt": [
        ("any", re.compile(r"\b(wp-login|wp-admin)\b", re.I), 120),
    ],
    
    "joomla.txt": [
        ("any", re.compile(r"\badministrator\b", re.I), 120),
    ],
    
    "drupal.txt": [
        ("any", re.compile(r"\bdrupal\b", re.I), 110),
    ],
    
    # ========== E-LEARNING - KEYWORD ==========
    
    "moodle.txt": [
        ("any", re.compile(r"\bmoodle\b", re.I), 110),
    ],
    
    "ojs_journal.txt": [
        ("any", re.compile(r"\b(ojs|journal|e-journal |jurnal | e-jurnal)\b", re.I), 100),
    ],
    
    # ========== E-COMMERCE - KEYWORD ==========
    
    "prestashop.txt": [
        # SPECIAL: Pattern-based untuk randomized admin URL
        ("path", re.compile(r"/admin[a-z0-9]{6,20}(/|$)", re.I), 150),
        ("any", re.compile(r"\bprestashop\b", re.I), 100),
    ],
    
    "magento.txt": [
        ("any", re.compile(r"\bmagento\b", re.I), 110),
    ],
    
    "opencart.txt": [
        ("any", re.compile(r"\bopencart\b", re.I), 110),
    ],
    
    # ========== DATABASE - KEYWORD ==========
    
    "phpmyadmin.txt": [
        ("any", re.compile(r"\bphpmyadmin\b", re.I), 120),
    ],
    
    # ========== MONITORING - KEYWORD ==========
    
    "grafana.txt": [
        ("any", re.compile(r"\bgrafana\b", re.I), 110),
    ],
    
    "laravel.txt": [
        ("any", re.compile(r"\blaravel\b", re.I), 110),
    ],
    
    # ========== CONTROL PANELS - PORT BASED ==========
    
    "cpanel.txt": [
        ("host", re.compile(r":2083\b", re.I), 160),
    ],
    
    "whm.txt": [
        ("host", re.compile(r":2087\b", re.I), 160),
    ],
    
    "plesk.txt": [
        ("host", re.compile(r":8443\b", re.I), 160),
    ],
    
    # ========== REMOTE ACCESS - SCHEME BASED ==========
    
    "ssh.txt": [
        ("any", re.compile(r"^ssh://", re.I), 160),
    ],
    
    "ftp.txt": [
        ("any", re.compile(r"^ftp://", re.I), 160),
    ],
}


def identify_platform(url_extracted: str) -> Optional[str]:
    """
    Identify platform - KEYWORD MODE (SIMPLE)
    
    Strategy:
    1. Check SPECIAL CASES dulu (PrestaShop pattern, ports, schemes)
    2. Then KEYWORD matching (simple & fast)
    3. Return platform atau None
    """
    if not url_extracted:
        return None
    
    s = url_extracted.strip()
    if not s:
        return None
    
    # Parse URL
    parse_target = s if re.match(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://', s) else ("http://" + s)
    
    try:
        p = urlparse(parse_target)
    except Exception:
        p = None
    
    host = (p.netloc or "").lower() if p else ""
    path = (p.path or "").lower() if p else ""
    whole = s.lower()
    
    best_match = (None, -1)
    
    # ========== SPECIAL CASES (HIGH PRIORITY) ==========
    
    # PrestaShop: KHUSUS pattern /admin{6-20 random}/
    if re.search(r"/admin[a-z0-9]{6,20}(/|$)", path, re.I):
        return "prestashop.txt"
    
    # Control Panels: Port-based (tertinggi priority)
    if ":2083" in host:
        return "cpanel.txt"
    if ":2087" in host:
        return "whm.txt"
    if ":8443" in host:
        return "plesk.txt"
    
    # SSH/FTP: Scheme-based (tertinggi priority)
    if whole.startswith("ssh://"):
        return "ssh.txt"
    if whole.startswith("ftp://"):
        return "ftp.txt"
    
    # ========== KEYWORD MATCHING (SIMPLE) ==========
    
    for filename, patterns in PLATFORM_PATTERNS.items():
        # Skip special cases yang udah di-check
        if filename in ["prestashop.txt", "cpanel.txt", "whm.txt", "plesk.txt", "ssh.txt", "ftp.txt"]:
            continue
        
        for component, regex, score in patterns:
            matched = False
            
            if component == "host" and host:
                if regex.search(host):
                    matched = True
            elif component == "path" and path:
                if regex.search(path):
                    matched = True
            elif component == "any":
                if regex.search(whole):
                    matched = True
            
            if matched and score > best_match[1]:
                best_match = (filename, score)
    
    return best_match[0]


def get_platform_info(platform_file: Optional[str]) -> Dict[str, str]:
    """Get info platform"""
    platform_map = {
        "wordpress.txt": {"name": "WordPress", "type": "CMS", "keyword": "wp-login, wp-admin"},
        "joomla.txt": {"name": "Joomla", "type": "CMS", "keyword": "administrator"},
        "drupal.txt": {"name": "Drupal", "type": "CMS", "keyword": "drupal"},
        "moodle.txt": {"name": "Moodle", "type": "LMS", "keyword": "moodle"},
        "ojs_journal.txt": {"name": "OJS Journal", "type": "Academic", "keyword": "journal, ojs"},
        "prestashop.txt": {"name": "PrestaShop", "type": "E-Commerce", "keyword": "/admin{random}/"},
        "magento.txt": {"name": "Magento", "type": "E-Commerce", "keyword": "magento"},
        "opencart.txt": {"name": "OpenCart", "type": "E-Commerce", "keyword": "opencart"},
        "phpmyadmin.txt": {"name": "phpMyAdmin", "type": "Database", "keyword": "phpmyadmin"},
        "grafana.txt": {"name": "Grafana", "type": "Monitoring", "keyword": "grafana"},
        "laravel.txt": {"name": "Laravel", "type": "Framework", "keyword": "laravel"},
        "cpanel.txt": {"name": "cPanel", "type": "Control Panel", "keyword": ":2083"},
        "whm.txt": {"name": "WHM", "type": "Control Panel", "keyword": ":2087"},
        "plesk.txt": {"name": "Plesk", "type": "Control Panel", "keyword": ":8443"},
        "ssh.txt": {"name": "SSH", "type": "Remote Access", "keyword": "ssh://"},
        "ftp.txt": {"name": "FTP", "type": "File Transfer", "keyword": "ftp://"},
    }
    return platform_map.get(platform_file, {"name": "Unknown", "type": "Unclassified", "keyword": "none"})


def list_all_platforms() -> List[str]:
    """Get list platforms"""
    return sorted(PLATFORM_PATTERNS.keys())


def count_platforms() -> int:
    """Get total platforms"""
    return len(PLATFORM_PATTERNS)
