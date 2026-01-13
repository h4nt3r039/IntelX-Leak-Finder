#!/usr/bin/env python3

import requests
import argparse
import time
import os
import json
import re
from datetime import datetime, timezone

API_URL = "API_URL"
                                  # Intelx>Account>Developer tabinda hem API key hem API URL gorsenecekdir.
API_KEY = "API_KEY"

POLL_INTERVAL = 3
MAX_POLL_TIME = 60

HEADERS = {
    "User-Agent": "Força Barça"
}

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
URL_REGEX = re.compile(r'(https?://[^\s:]+)')

def intelx_request(method, path, api_key, **kwargs):
    headers = HEADERS.copy()
    headers["x-key"] = api_key

    r = requests.request(
        method,
        f"{API_URL}{path}",
        headers=headers,
        timeout=30,
        **kwargs
    )

    r.raise_for_status()
    return r

def wait_for_results(search_id, api_key):
    print("[*] Waiting for IntelX to prepare results...")
    waited = 0

    while waited < MAX_POLL_TIME:
        r = intelx_request(
            "GET",
            "/intelligent/search/result",
            api_key,
            params={"id": search_id, "offset": 0, "limit": 1}
        )

        records = r.json().get("records", [])
        if records:
            print("[+] Results ready!")
            return True

        time.sleep(POLL_INTERVAL)
        waited += POLL_INTERVAL
        print(f"[*] Still processing... {waited}s")

    print("[!] Timeout waiting for IntelX results.")
    return False

def scan_content(content, domain):
    domain = domain.lower()
    return [
        line.strip()
        for line in content.splitlines()
        if domain in line.lower()
    ]

URL_REGEX = re.compile(r'(https?://[^\s|:,]+)')

def parse_leak_line(line):
    original_line = line.strip()

    source_url = ""
    url_match = URL_REGEX.search(original_line)
    if url_match:
        source_url = url_match.group(1)

    # URL | USERNAME | PASSWORD
    # Mes: https://site.com/path|Lionel Messi|GOAT112331!#
    if "|" in original_line:
        parts_pipe = [p.strip() for p in original_line.split("|") if p.strip()]
        if len(parts_pipe) >= 3:
            # Eger birinci hissə URL-dirsə
            if parts_pipe[0].startswith("http"):
                return parts_pipe[0], parts_pipe[-2], parts_pipe[-1]
            else:
                return "", parts_pipe[-2], parts_pipe[-1]

    line = original_line.strip('"').strip("'")

    # URL prefix-nin silinmesi
    if "://" in line:
        line = line.split("://", 1)[1]
        if "/" in line:
            line = line.split("/", 1)[1]

    # Username ve password ayrilmasi (; | , -> :)
    for sep in [";", "|", ","]:
        line = line.replace(sep, ":")

    # Leaklerde url hissesinden sonraki space-in silinmesi
    if " " in line:
        tokens = line.split()
        for t in tokens:
            if ":" in t:
                line = t
                break

    parts = [p.strip() for p in line.split(":") if p.strip()]

    if len(parts) < 2:
        return None

    username = None
    password = None

    # Leak-de hansi hissenin username olmasini bildirir (email prioritet)
    for p in parts:
        if EMAIL_REGEX.fullmatch(p):
            username = p
            break

    # Email yoxdursa, sondan ikinci hissə username kimi goturulur
    if not username:
        username = parts[-2]

    password = parts[-1]

    if not username or not password:
        return None

    return source_url, username, password


def main():
    parser = argparse.ArgumentParser(description="IntelX Leak Finder (JSON output)")
    parser.add_argument("domain")
    parser.add_argument("--from", dest="date_from", required=True)
    parser.add_argument("--to", dest="date_to", required=True)
    args = parser.parse_args()

    api_key = API_KEY

    domain = args.domain.lower()
    date_from = datetime.strptime(args.date_from, "%Y-%m-%d").date()
    date_to   = datetime.strptime(args.date_to, "%Y-%m-%d").date()

    today = datetime.now(timezone.utc).date()
    print(f"[+] Running in UTC mode: {today}")

    payload = {
        "term": domain,
        "buckets": ["leaks.private.general"],
        "lookuplevel": 0,
        "maxresults": 1000,
        "timeout": 0
    }

    r = intelx_request("POST", "/intelligent/search", api_key, json=payload)
    search_id = r.json().get("id")

    if not search_id:
        print("[!] Failed to create search")
        return

    print(f"[+] Search ID: {search_id}")

    if not wait_for_results(search_id, api_key):
        return

    offset = 0
    seen = set()
    results = []

    try:
        while True:
            r = intelx_request(
                "GET",
                "/intelligent/search/result",
                api_key,
                params={"id": search_id, "offset": offset, "limit": 100}
            )

            records = r.json().get("records", [])
            if not records:
                break

            for item in records:
                if not item.get("instore"):
                    continue

                leak_date = datetime.fromisoformat(
                    item["date"].replace("Z", "")
                ).date()

                if not (date_from <= leak_date <= date_to):
                    continue

                r = intelx_request(
                    "GET",
                    "/file/read",
                    api_key,
                    params={
                        "type": 1,
                        "storageid": item["storageid"],
                        "bucket": item["bucket"]
                    }
                )

                for line in scan_content(r.text, domain):
                    parsed = parse_leak_line(line)
                    if not parsed:
                        continue

                    source_url, username, password = parsed

                    dedup_key = (username.lower(), password)
                    if dedup_key in seen:
                        continue
                    seen.add(dedup_key)

                    record = {
                        "domain": domain,
                        "leak_id": item["systemid"],
                        "source": "intelx.io",
                        "leak_file": f"https://intelx.io/?did={item['systemid']}",
                        "source_url": source_url,
                        "leak_date": str(leak_date),
                        "username": username,
                        "password": password
                    }

                    print("[LEAK]", record)
                    results.append(record)

            offset += 100
            time.sleep(0.3)

    except KeyboardInterrupt:
        print("\n[!] Stopped by user (Ctrl+C). Saving partial results...")

    output_file = f"{domain}_{date_from}_{date_to}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n[+] Done")
    print(f"    Total unique credentials: {len(results)}")
    print(f"    Output file: {output_file}")

if __name__ == "__main__":
    main()
