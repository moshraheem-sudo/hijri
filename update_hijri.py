#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to fetch the official Hijri date from the Office of His Eminence Sayyid Ali al-Sistani (sistani.org)
and update `hijri.json`.
"""

import os
import re
import json
import urllib.request
from datetime import datetime, timezone, timedelta

MONTH_MAP = {
    "محرم": 1,
    "صفر": 2,
    "ربيع الأول": 3,
    "ربيع الاول": 3,
    "ربيع الآخر": 4,
    "ربيع الثاني": 4,
    "ربيع الاخر": 4,
    "ربيع الثانى": 4,
    "جمادى الأولى": 5,
    "جمادى الاولى": 5,
    "جمادى الأول": 5,
    "جمادى الاول": 5,
    "جمادى الآخرة": 6,
    "جمادى الاخرة": 6,
    "جمادى الثانية": 6,
    "جمادى الثانيه": 6,
    "رجب": 7,
    "شعبان": 8,
    "رمضان": 9,
    "شهر رمضان": 9,
    "شوال": 10,
    "ذو القعدة": 11,
    "ذو القعده": 11,
    "ذو الحجة": 12,
    "ذو الحجه": 12,
}

def normalize_digits(text: str) -> str:
    """Converts Eastern Arabic/Persian numerals to standard ASCII digits."""
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    for i, ch in enumerate(arabic_digits):
        text = text.replace(ch, str(i))
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    for i, ch in enumerate(persian_digits):
        text = text.replace(ch, str(i))
    return text

def fetch_sistani_html() -> str:
    """Fetches HTML from sistani.org with retry and proper headers."""
    urls = [
        "https://www.sistani.org/",
        "https://www.sistani.org/arabic/"
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ar,en;q=0.9"
    }

    last_error = None
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                if resp.status == 200:
                    return resp.read().decode("utf-8", errors="ignore")
        except Exception as e:
            last_error = e
            continue

    raise RuntimeError(f"Failed to fetch data from sistani.org: {last_error}")

def parse_sistani_data(html: str) -> dict:
    # 1. Match uts timestamp if present
    uts_match = re.search(r"uts\s*=\s*(\d+)", html)
    uts = int(uts_match.group(1)) if uts_match else None

    # 2. Match #home-date div
    match = re.search(r'<div id=["\']home-date["\']>(.*?)</div>', html, re.DOTALL)
    if not match:
        raise ValueError("Could not find <div id='home-date'> in sistani.org")

    raw_html = match.group(1)
    clean_text = re.sub(r"<[^>]+>", " ", raw_html)
    clean_text = clean_text.replace("&nbsp;", " ")
    parts = [p.strip() for p in clean_text.split("||") if p.strip()]

    if not parts:
        raise ValueError(f"Unable to parse parts from home-date: {raw_html}")

    hijri_raw = parts[0]
    hijri_norm = normalize_digits(hijri_raw)

    # Day of week (e.g. الثلاثاء)
    day_name_match = re.search(r"^(الأحد|الاحد|الإثنين|الاثنين|الثلاثاء|الأربعاء|الاربعاء|الخميس|الجمعة|الجمعه|السبت)", hijri_norm.strip())
    day_name = day_name_match.group(1) if day_name_match else ""

    # Parse Hijri: e.g. "6 - جمادى الآخرة - 1448 هـ"
    m = re.search(r"(\d{1,2})\s*-\s*([^-]+?)\s*-\s*(\d{4})", hijri_norm)
    if not m:
        raise ValueError(f"Could not extract Hijri day/month/year from: '{hijri_norm}'")

    hijri_day = int(m.group(1))
    hijri_month_name = m.group(2).strip()
    hijri_year = int(m.group(3))

    hijri_month = None
    for name, num in MONTH_MAP.items():
        if name in hijri_month_name or hijri_month_name in name:
            hijri_month = num
            break

    if hijri_month is None:
        raise ValueError(f"Unknown Hijri month: '{hijri_month_name}'")

    # Gregorian date
    gregorian_str = None
    for part in parts:
        gm = re.search(r"([A-Za-z]{3},\s*\d{1,2}\s+[A-Za-z]{3}\s+\d{4})", part)
        if gm:
            gregorian_str = gm.group(1)
            break

    if gregorian_str:
        gregorian_dt = datetime.strptime(gregorian_str, "%a, %d %b %Y")
        gregorian_date_str = gregorian_dt.strftime("%Y-%m-%d")
    else:
        if uts:
            gregorian_dt = datetime.fromtimestamp(uts, timezone.utc) + timedelta(hours=3)
            gregorian_date_str = gregorian_dt.strftime("%Y-%m-%d")
        else:
            gregorian_dt = datetime.now()
            gregorian_date_str = gregorian_dt.strftime("%Y-%m-%d")

    # Gregorian anchor date (1st of the Hijri month)
    anchor_dt = gregorian_dt - timedelta(days=(hijri_day - 1))
    gregorian_anchor_str = anchor_dt.strftime("%Y-%m-%d")

    # Najaf local time
    najaf_tz = timezone(timedelta(hours=3))
    if uts:
        najaf_dt = datetime.fromtimestamp(uts, timezone.utc) + timedelta(hours=3)
        time_najaf = najaf_dt.strftime("%H:%M:%S")
    else:
        time_najaf = datetime.now(najaf_tz).strftime("%H:%M:%S")

    now_iso = datetime.now(najaf_tz).strftime("%Y-%m-%dT%H:%M:%S+03:00")

    return {
        "hijri_day": hijri_day,
        "hijri_month": hijri_month,
        "hijri_year": hijri_year,
        "hijri_month_name": hijri_month_name,
        "day_name": day_name,
        "gregorian_date": gregorian_date_str,
        "gregorian_anchor_date": gregorian_anchor_str,
        "time_najaf": time_najaf,
        "status": "verified",
        "source": "https://www.sistani.org/",
        "last_updated": now_iso
    }

def update_file(new_data: dict, file_path: str = "hijri.json") -> bool:
    old_data = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                old_data = json.load(f)
        except Exception as e:
            print(f"Warning reading existing {file_path}: {e}")

    # Check if core fields changed
    core_keys = ["hijri_day", "hijri_month", "hijri_year", "gregorian_anchor_date", "gregorian_date"]
    has_changed = False
    for k in core_keys:
        if old_data.get(k) != new_data.get(k):
            has_changed = True
            break

    if not has_changed and old_data:
        print(f"No changes in core Hijri data. Day: {new_data['hijri_day']}, Month: {new_data['hijri_month']}, Year: {new_data['hijri_year']}")
        return False

    # Structure payload to preserve backward compatibility:
    # Top fields are the exact ones existing apps read, followed by enriched fields.
    payload = {
        "hijri_day": new_data["hijri_day"],
        "hijri_month": new_data["hijri_month"],
        "hijri_year": new_data["hijri_year"],
        "hijri_month_name": new_data["hijri_month_name"],
        "day_name": new_data["day_name"],
        "gregorian_date": new_data["gregorian_date"],
        "gregorian_anchor_date": new_data["gregorian_anchor_date"],
        "time_najaf": new_data["time_najaf"],
        "status": new_data["status"],
        "source": new_data["source"],
        "last_updated": new_data["last_updated"]
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Successfully updated {file_path} with: {payload['hijri_day']}-{payload['hijri_month']}-{payload['hijri_year']} ({payload['hijri_month_name']})")
    return True

if __name__ == "__main__":
    html = fetch_sistani_html()
    data = parse_sistani_data(html)
    changed = update_file(data, "hijri.json")
    if changed:
        print("STATUS=UPDATED")
    else:
        print("STATUS=NO_CHANGE")
