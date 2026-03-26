#!/usr/bin/env python3
"""
network_scan 本機後端伺服器
用法：
  1. pip install scapy flask flask-cors
  2. 以系統管理員身分執行：python scan_server.py
  3. 用瀏覽器開啟 network_scan.html
"""

import ipaddress
import json
import re
import socket
import sys

from flask import Flask, Response, request, stream_with_context
from flask_cors import CORS

try:
    from scapy.all import ARP, Ether, srp
except ImportError:
    sys.exit("❌ 請先安裝 scapy：pip install scapy flask flask-cors")

app = Flask(__name__)
CORS(app)

# ──────────────────────────────────────────
#  IP 範圍解析
# ──────────────────────────────────────────
def parse_range(raw: str) -> list:
    ips = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        # CIDR 格式 192.168.1.0/24
        if "/" in part:
            try:
                net = ipaddress.IPv4Network(part, strict=False)
                ips.extend(str(h) for h in net.hosts())
                continue
            except ValueError:
                pass
        # 範圍格式 192.168.1.1-254
        m = re.match(r"^(\d+\.\d+\.\d+\.)(\d+)-(\d+)$", part)
        if m:
            prefix = m.group(1)
            for i in range(int(m.group(2)), int(m.group(3)) + 1):
                ips.append(prefix + str(i))
            continue
        # 單一 IP
        if re.match(r"^\d+\.\d+\.\d+\.\d+$", part):
            ips.append(part)
    return ips


# ──────────────────────────────────────────
#  反向 DNS 查詢主機名稱
#  查不到就回傳空字串（前端會顯示 IP 代替）
# ──────────────────────────────────────────
def resolve_hostname(ip: str) -> str:
    try:
        # gethostbyaddr 回傳 (hostname, aliaslist, ipaddrlist)
        hostname = socket.gethostbyaddr(ip)[0]
        # 如果查回來的就是 IP 本身，視為查無名稱
        if hostname == ip:
            return ""
        return hostname
    except Exception:
        return ""


# ──────────────────────────────────────────
#  ARP 掃描主流程（SSE 串流）
# ──────────────────────────────────────────
BATCH   = 50   # 每批 IP 數量
TIMEOUT = 2    # ARP 等待秒數

def arp_scan_stream(ip_list: list):
    total = len(ip_list)
    found = 0

    for i in range(0, total, BATCH):
        batch = ip_list[i : i + BATCH]

        # 組合 ARP 廣播幀
        frame = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=batch)
        answered, _ = srp(frame, timeout=TIMEOUT, verbose=False)

        for sent, received in answered:
            found += 1
            ip  = received.psrc   # 來源 IP
            mac = received.hwsrc  # 來源 MAC

            # 反向 DNS → 取得裝置名稱
            hostname = resolve_hostname(ip)

            record = {
                "ip":       ip,
                "mac":      mac,
                "hostname": hostname,   # 可能為空字串
                "vendor":   "",         # 可接 MAC 廠商 API 補充
            }
            yield "data: " + json.dumps(record) + "\n\n"

        # 進度事件
        yield "data: " + json.dumps({
            "progress": True,
            "done":     min(i + BATCH, total),
            "total":    total,
            "found":    found,
        }) + "\n\n"

    # 完成事件
    yield "data: " + json.dumps({
        "done":  True,
        "total": total,
        "found": found,
    }) + "\n\n"


@app.route("/scan")
def scan():
    raw = request.args.get("range", "").strip()
    if not raw:
        return Response(json.dumps({"error": "缺少 range 參數"}),
                        status=400, mimetype="application/json")
    ip_list = parse_range(raw)
    if not ip_list:
        return Response(json.dumps({"error": "IP 範圍格式錯誤"}),
                        status=400, mimetype="application/json")
    if len(ip_list) > 1024:
        return Response(json.dumps({"error": "IP 範圍超過 1024 個"}),
                        status=400, mimetype="application/json")

    return Response(
        stream_with_context(arp_scan_stream(ip_list)),
        mimetype="text/event-stream",
        headers={
            "Cache-Control":             "no-cache",
            "X-Accel-Buffering":         "no",
            "Access-Control-Allow-Origin": "*",
        },
    )


@app.route("/")
def index():
    return "<h3>network_scan 伺服器運作中</h3><p>請開啟 network_scan.html</p>"


if __name__ == "__main__":
    print("=" * 50)
    print("  network_scan 後端啟動")
    print("  請確認已安裝：pip install scapy flask flask-cors")
    print("  注意：需要系統管理員權限")
    print("  http://127.0.0.1:5050")
    print("=" * 50)
    app.run(host="127.0.0.1", port=5050, threaded=False, debug=False)
