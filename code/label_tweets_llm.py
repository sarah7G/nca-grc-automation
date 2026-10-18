#!/usr/bin/env python3
"""
Label REAL posts with a language model and prepare a human-review sample.

Why: the thesis must say who produced the labels. With this script the honest description is:
"labels were produced by <model> with a fixed prompt; N posts (random sample) were then labelled
independently by a human reviewer and agreement was measured (Cohen's kappa)". These are NOT expert annotations.

Input : CSV with a column `text` (posts you collected yourself, within the platform's terms; remove usernames/links first).
Output: <out>.csv          text,label,label_name,confidence,labeler   (label: 0 compliant, 1 non_compliant, 2 neutral)
        <out>_review.csv   random sample WITHOUT the model label, with an empty `human_label` column to fill (0/1/2)
Then:   python agreement.py --labeled <out>.csv --review <out>_review.csv   (kappa, accuracy, confusion)
        python run_experiment.py --tweets_csv <out>.csv                      (re-run the classifier on the real posts)

Usage:  export ANTHROPIC_API_KEY=...   (never hard-code it)
        python label_tweets_llm.py --input tweets.csv --out labeled --model claude-sonnet-5-5 --review_n 300
        python label_tweets_llm.py --input tweets.csv --out labeled --mock      # dry run, no API, to test the pipeline
NOTE: the API path was written without access to a key and has not been run by the author of this file; test it on 20 posts first.
"""
import argparse, csv, json, os, random, re, sys, time, urllib.request, urllib.error

NAMES = ["compliant", "non_compliant", "neutral"]
PROMPT = """You label social-media posts (Arabic or English) about cybersecurity for a study on NCA (Saudi National Cybersecurity Authority) compliance.
Classes:
- compliant: the post states or clearly implies that an organisation meets / has implemented / passed a cybersecurity control or NCA requirement.
- non_compliant: the post states or clearly implies a gap, failure, violation, missing control or unmet requirement.
- neutral: anything else (news, events, general discussion, marketing, no compliance status).
If a post contains both, choose the class of its main claim. Answer with JSON only: {"label": "compliant|non_compliant|neutral", "confidence": 0.0-1.0}.
Post: """

def call_api(text, model, key, retries=5):
    body = json.dumps({"model": model, "max_tokens": 60, "temperature": 0,
                       "messages": [{"role": "user", "content": PROMPT + text}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, method="POST",
                                 headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    for k in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out = json.load(r)["content"][0]["text"]
            m = re.search(r"\{.*\}", out, re.S); j = json.loads(m.group(0))
            return NAMES.index(j["label"]), float(j.get("confidence", 0))
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError, json.JSONDecodeError) as e:
            time.sleep(2 ** k)
    return None, None

POS = ["compliant", "passed", "aligned", "verified", "متوافق", "اجتاز"]; NEG = ["non-compliant", "gap", "missing", "failed", "violation", "غير متوافق", "فجوات", "رسبنا", "مخالفة"]
def mock(text):
    t = text.lower(); n = sum(k in t for k in NEG); p = sum(k in t for k in POS)
    return (1 if n > p else 0 if p > 0 else 2), 0.5

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--input", required=True); ap.add_argument("--out", default="labeled")
    ap.add_argument("--model", default="claude-sonnet-5-5"); ap.add_argument("--review_n", type=int, default=300)
    ap.add_argument("--seed", type=int, default=42); ap.add_argument("--mock", action="store_true"); ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args(); key = os.environ.get("ANTHROPIC_API_KEY")
    if not a.mock and not key: sys.exit("Set ANTHROPIC_API_KEY (or use --mock for a dry run).")
    rows = [r for r in csv.DictReader(open(a.input, encoding="utf8")) if (r.get("text") or "").strip()]
    if a.limit: rows = rows[:a.limit]
    out = []
    for i, r in enumerate(rows):
        lab, conf = mock(r["text"]) if a.mock else call_api(r["text"], a.model, key)
        if lab is None: print("failed:", i); continue
        out.append({"text": r["text"], "label": lab, "label_name": NAMES[lab], "confidence": conf, "labeler": "mock-keywords" if a.mock else a.model})
        if i % 100 == 0: print(i, "/", len(rows), flush=True)
    with open(a.out + ".csv", "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    random.Random(a.seed).shuffle(idx := list(range(len(out))))
    with open(a.out + "_review.csv", "w", newline="", encoding="utf8") as f:
        w = csv.writer(f); w.writerow(["row_id", "text", "human_label"])
        for i in idx[:a.review_n]: w.writerow([i, out[i]["text"], ""])
    print(f"wrote {a.out}.csv ({len(out)} posts) and {a.out}_review.csv ({min(a.review_n, len(out))} posts to label by hand: 0 compliant, 1 non_compliant, 2 neutral)")
