# -*- coding: utf-8 -*-
"""将中文分析字段合并进 papers.csv（原子替换写入）"""
import csv, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from analysis_part1 import P1
from analysis_part2 import P2
from analysis_part3 import P3

DATA = {}
for d in (P1, P2, P3):
    DATA.update(d)

FIELDS = ["标题翻译", "摘要翻译", "问题挑战", "核心方法", "主要效果", "一句话总结", "关键词", "作者团队简介"]
src = os.path.join(BASE, "papers.csv")

with open(src, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.reader(f))

header = rows[0]
idx = {name: header.index(name) for name in ["编号", "标题", "作者列表", "单位", "摘要", "原文PDF"]}

new_header = ["编号", "标题", "标题翻译", "作者列表", "单位", "摘要", "摘要翻译",
              "问题挑战", "核心方法", "主要效果", "一句话总结", "关键词", "作者团队简介", "原文PDF"]

out_rows, missing, incomplete = [new_header], [], []
for r in rows[1:]:
    if not r or not r[idx["编号"]].strip():
        continue
    n = int(r[idx["编号"]].strip())
    a = DATA.get(n)
    if a is None:
        missing.append(n)
        a = {k: "" for k in FIELDS}
    for k in FIELDS:
        if not a.get(k, "").strip():
            incomplete.append((n, k))
    out_rows.append([
        r[idx["编号"]], r[idx["标题"]], a["标题翻译"], r[idx["作者列表"]], r[idx["单位"]],
        r[idx["摘要"]], a["摘要翻译"], a["问题挑战"], a["核心方法"], a["主要效果"],
        a["一句话总结"], a["关键词"], a["作者团队简介"], r[idx["原文PDF"]],
    ])

tmp = src + ".tmp"
with open(tmp, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerows(out_rows)
os.replace(tmp, src)

print("papers written:", len(out_rows) - 1)
print("missing analysis:", missing or "none")
print("incomplete fields:", incomplete or "none")
print("analysis entries in DATA:", len(DATA))
