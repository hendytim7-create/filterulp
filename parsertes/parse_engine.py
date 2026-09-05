"""
Parsing engine untuk parsertes package - OPTIMIZED v2.7
- Ultra fast parsing (1-2 pass strategy)
- Comprehensive platform-specific login paths
- Clean & efficient credential extraction
"""

import re
import asyncio
from typing import Optional, Set, Dict, List, Tuple
from urllib.parse import urlparse

from parsertes.platform_detect import identify_platform


# ===============================
# REGEX PATTERNS
# ===============================
URL_REGEX_PATTERN = re.compile(
    r'^(https?://|[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}(?::\d+)?)',
    re.IGNORECASE
)


# ===============================
# BLOCK PARSING - FAST
# ===============================

def split_blocks(text: str) -> List[str]:
    """Split text into blocks - simple & fast"""
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    return blocks if blocks else [text.strip()]


def normalize_url(url: str) -> str:
    """Normalize URL - ultra fast"""
    if not url:
        return ""
    
    s = url.strip()
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://', s):
        s = "http://" + s
    
    try:
        p = urlparse(s)
        host = (p.netloc or "").lower()
        path = (p.path or "").rstrip('/').lower()
        return f"{host}{path}" if path else host
    except Exception:
        return s.lower().rstrip('/')


def validate_credentials(url: str, user: str, pwd: str) -> bool:
    """Quick validation"""
    return bool(
        url and user and pwd and
        len(url) > 5 and len(user) > 0 and len(pwd) > 0 and
        (re.search(r'\.', url) or re.search(r':', url))
    )


def enhance_url_with_login_path(base_url: str, platform: str) -> str:
    """
    Enhance URL dengan platform-specific login path - COMPREHENSIVE
    
    Contoh:
    - WordPress: example.com -> example.com/wp-login.php
    - Joomla: example.com -> example.com/administrator
    - cPanel: example.com -> example.com:2083
    """
    if not base_url or not platform:
        return base_url
    
    platform_name = platform.replace(".txt", "").lower()
    
    # ========== COMPREHENSIVE PATH MAP ==========
    path_map = {
        # ========== CMS ==========
        "wordpress": "/wp-login.php",
        "joomla": "/administrator",
        "joomla_administrator": "/administrator",
        "drupal": "/user/login",
        "drupal_user": "/user/login",
        
        # ========== E-LEARNING & ACADEMIC ==========
        "moodle": "/login/index.php",
        "moodle_login": "/login/index.php",
        "ojs_journal": "/index.php/login",
        "ojs": "/index.php/login",
        
        # ========== E-COMMERCE ==========
        "prestashop": "/admin",
        "prestashop_admin": "/admin",
        "magento": "/admin",
        "magento_admin": "/admin",
        "opencart": "/admin",
        "opencart_admin": "/admin",
        "shopify": "/admin",
        
        # ========== DATABASE MANAGEMENT ==========
        "phpmyadmin": "/phpmyadmin",
        "phpmyadmin_admin": "/phpmyadmin",
        "adminer": "/adminer.php",
        
        # ========== MONITORING & ANALYTICS ==========
        "grafana": "/grafana",
        "grafana_admin": "/grafana",
        
        # ========== FRAMEWORK & CUSTOM ==========
        "laravel": "/admin",
        "laravel_admin": "/admin",
        
        # ========== CONTROL PANELS (PORT-BASED) ==========
        "cpanel": ":2083",
        "cpanel_port": ":2083",
        "whm": ":2087",
        "whm_port": ":2087",
        "plesk": ":8443",
        "plesk_port": ":8443",
        
        # ========== DEFAULT FALLBACK ==========
        "admin": "/admin",
        "login": "/login",
    }
    
    # Try exact match first
    login_path = path_map.get(platform_name, "")
    
    # Try partial match jika tidak ada exact match
    if not login_path:
        for key, path in path_map.items():
            if key in platform_name or platform_name in key:
                login_path = path
                break
    
    # Default fallback
    if not login_path:
        return base_url
    
    try:
        # Parse base URL
        parsed = urlparse(base_url if base_url.startswith("http") else f"http://{base_url}")
        scheme = parsed.scheme or "http"
        host = parsed.netloc
        path = parsed.path.rstrip('/') or ""
        
        # Handle port-based login (cPanel, WHM, Plesk)
        if login_path.startswith(":"):
            # Extract host without existing port
            host_only = host.split(":")[0]
            return f"{scheme}://{host_only}{login_path}"
        
        # Handle path-based login (normal case)
        return f"{scheme}://{host}{path}{login_path}"
    
    except Exception:
        return base_url


def parse_block_smart_fast(block: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    ULTRA FAST: Minimal parsing - extract URL:USER:PASS in 1-2 pass
    
    Strategy:
    1. Cari URL (first line yang match pattern)
    2. Cari USER & PASS (line berikutnya dengan colon)
    3. Done!
    """
    lines = block.split('\n')
    url = user = pwd = None
    
    # Pass 1: Cari URL (dari line pertama yang cocok)
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        
        # Check if line looks like URL
        if re.match(URL_REGEX_PATTERN, line_clean):
            url = line_clean
            break
    
    if not url:
        return None, None, None
    
    # Pass 2: Cari USER & PASS (line berikutnya)
    for line in lines:
        line_clean = line.strip()
        if not line_clean or line_clean == url:
            continue
        
        # Cari colon untuk user:pass
        if ':' in line_clean:
            parts = line_clean.split(':', 1)
            
            if not user:
                user = parts[0].strip()
            elif not pwd:
                pwd = parts[1].strip()
                break
    
    # Validate & return
    if validate_credentials(url, user, pwd):
        return url, user, pwd
    
    return None, None, None


# ===============================
# ASYNC PROCESSORS - FAST
# ===============================

async def process_file_block_mode(
    path: str, global_set: Set[str],
    stats: Dict, sem: asyncio.Semaphore, write_queue: asyncio.Queue,
    callback=None, dedup_enabled=True
) -> None:
    """Process file dalam BLOCK mode - OPTIMIZED"""
    async with sem:
        try:
            import aiofiles
            async with aiofiles.open(path, "r", encoding="utf-8", errors="replace") as f:
                content = await f.read()
            
            blocks = split_blocks(content)
            total_blocks = len(blocks)
            
            if callback:
                await callback("log", f"⏳ Block Mode: {path} ({total_blocks:,} blocks)...")
            
            BATCH_SIZE = 5000  # Increase batch size
            local_matches = []
            
            for i, block in enumerate(blocks, 1):
                stats["blocks"] += 1
                
                # FAST PARSE
                url, user, pwd = parse_block_smart_fast(block)
                if not (url and user and pwd):
                    continue
                
                # Normalize URL
                norm_url = normalize_url(url)
                
                # Classify platform
                platform_file = identify_platform(url)
                
                # Enhance URL dengan login path
                if platform_file:
                    enhanced_url = enhance_url_with_login_path(norm_url, platform_file)
                else:
                    enhanced_url = norm_url
                
                # Create combo
                combo_line = f"{enhanced_url}|{user}|{pwd}"
                
                # Dedup
                if dedup_enabled:
                    if combo_line in global_set:
                        continue
                    global_set.add(combo_line)
                    stats["unique"] += 1
                else:
                    stats["unique"] += 1
                
                # Add to matches
                if platform_file:
                    stats["matches"] += 1
                    local_matches.append((platform_file, combo_line))
                else:
                    local_matches.append(("unclassified.txt", combo_line))
                
                # Batch flush
                if i % BATCH_SIZE == 0:
                    for item in local_matches:
                        await write_queue.put(item)
                    local_matches.clear()
                    await asyncio.sleep(0.0001)
            
            # Final flush
            for item in local_matches:
                await write_queue.put(item)
            
            stats["files"] += 1
            if callback:
                await callback("log", f"✓ Block Mode: {path} DONE")
        
        except Exception as e:
            if callback:
                await callback("log", f"✗ Error: {str(e)}")


async def process_file_line_mode(
    path: str, global_set: Set[str],
    stats: Dict, sem: asyncio.Semaphore, write_queue: asyncio.Queue,
    callback=None, dedup_enabled=True
) -> None:
    """Process file dalam LINE mode - OPTIMIZED"""
    async with sem:
        try:
            import aiofiles
            if callback:
                await callback("log", f"⏳ Line Mode: {path}...")
            
            BATCH_SIZE = 50000  # Increase batch size
            local_matches = []
            
            async with aiofiles.open(path, "r", encoding="utf-8", errors="replace") as f:
                async for line_str in f:
                    line_clean = line_str.strip()
                    if not line_clean:
                        continue
                    
                    stats["lines"] += 1
                    
                    # FAST PARSE: split on colon
                    parts = line_clean.split(":")
                    if len(parts) < 3:
                        continue
                    
                    url = parts[0].strip()
                    user = parts[1].strip()
                    pwd = ':'.join(parts[2:]).strip()
                    
                    # Validate
                    if not validate_credentials(url, user, pwd):
                        continue
                    
                    # Normalize
                    norm_url = normalize_url(url)
                    
                    # Classify
                    platform_file = identify_platform(url)
                    
                    # Enhance
                    if platform_file:
                        enhanced_url = enhance_url_with_login_path(norm_url, platform_file)
                    else:
                        enhanced_url = norm_url
                    
                    # Create combo
                    combo_line = f"{enhanced_url}|{user}|{pwd}"
                    
                    # Dedup
                    if dedup_enabled:
                        if combo_line in global_set:
                            continue
                        global_set.add(combo_line)
                        stats["unique"] += 1
                    else:
                        stats["unique"] += 1
                    
                    # Add matches
                    if platform_file:
                        stats["matches"] += 1
                        local_matches.append((platform_file, combo_line))
                    else:
                        local_matches.append(("unclassified.txt", combo_line))
                    
                    # Batch flush
                    if len(local_matches) >= BATCH_SIZE:
                        for item in local_matches:
                            await write_queue.put(item)
                        local_matches.clear()
                        await asyncio.sleep(0.0001)
            
            # Final flush
            for item in local_matches:
                await write_queue.put(item)
            
            stats["files"] += 1
            if callback:
                await callback("log", f"✓ Line Mode: {path} DONE")
        
        except Exception as e:
            if callback:
                await callback("log", f"✗ Error: {str(e)}")
