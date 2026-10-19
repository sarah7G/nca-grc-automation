#!/usr/bin/env python3
"""
Layer 1 knowledge base + linking of posts to ECC controls (thesis Sections 3.3.1.1, 3.4.2.3, 5.x "Layer 1").

controls.csv is the OUTPUT of layer1_extract.py on ECC-1:2018 (148 records: 52 controls + 96 sub-controls).
Here it is used as the compliance knowledge base:
  1. normalise: derive ECC main domain / sub-domain from the control_id (the PDF-header 'domain' column is unreliable);
  2. extraction report: counts vs the official numbers (114 controls, 105 sub-controls), coverage of the 29 sub-domains,
     defects found (controls merged into one record, inline ids);
  3. domain table: the 12 simulated domains -> ECC-1:2018 sub-domains -> number of controls in the knowledge base;
  4. linking: each ENGLISH post is matched to the control whose text has the highest TF-IDF cosine similarity;
     the ECC domain of that control is compared with the domain the post was generated from (known by construction).
Arabic posts are NOT evaluated: the knowledge base is the English ECC text only (Arabic ECC = future work).
"""
import re
import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from common import DOMAINS, ECC_MAIN, ECC_SUB, SUB_TO_DOMAIN

OFFICIAL = {"controls": 114, "subcontrols": 105}      # official totals of ECC-1:2018
INLINE_ID = re.compile(r"\b\d-\d{1,2}-\d{1,2}(?:-\d)?\b")


def load_controls(path="controls.csv"):
    c = pd.read_csv(path, encoding="utf8").fillna("")
    c["ecc_sub"] = c.control_id.str.extract(r"^(\d+-\d+)")[0]
    c["ecc_main"] = c.control_id.str.extract(r"^(\d+)-")[0].map(ECC_MAIN)
    c["ecc_sub_name"] = c.ecc_sub.map(ECC_SUB)
    c["sim_domain_id"] = c.ecc_sub.map(SUB_TO_DOMAIN)          # NaN when the sub-domain is not one of the 12 simulated domains
    return c


def extraction_report(c):
    n3, n4 = int((c.level == 3).sum()), int((c.level == 4).sum())
    inline = c.text.apply(lambda t: len(INLINE_ID.findall(t)) > 0)
    return {"n_records": int(len(c)), "n_controls_level3": n3, "n_subcontrols_level4": n4,
            "official_controls": OFFICIAL["controls"], "official_subcontrols": OFFICIAL["subcontrols"],
            "control_recall_pct": 100 * n3 / OFFICIAL["controls"], "subcontrol_recall_pct": 100 * n4 / OFFICIAL["subcontrols"],
            "subdomains_covered": int(c.ecc_sub.nunique()), "subdomains_official": len(ECC_SUB),
            "records_with_inline_ids_(merged_controls)": int(inline.sum()),
            "records_whose_pdf_domain_is_page_header": int(c.domain.str.contains("Document Classification").sum()),
            "median_text_chars": float(c.text.str.len().median()), "max_text_chars": int(c.text.str.len().max()),
            "note": "Identifier precision/recall and text fidelity against the reference set built from the ECC-1:2018 PDF "
                    "are computed by layer1_evaluate.py (layer1_ecc/layer1_text_eval.json)."}


def domain_table(c):
    rows = []
    for i, (en, ar, subs) in enumerate(DOMAINS):
        m = c[c.ecc_sub.isin(subs)]
        rows.append({"simulated_domain": en, "arabic": ar, "ecc_subdomain_codes": ", ".join(subs),
                     "ecc_subdomain_names": "; ".join(ECC_SUB[s] for s in subs), "n_controls_in_kb": int(len(m))})
    return rows


def _vectorizer(kind):
    if kind == "word": return TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    return TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True)


def link_posts(posts, c, kind="word"):
    """posts: DataFrame with text, domain (english name), domain_id (English posts only).  Returns accuracy dict."""
    vec = _vectorizer(kind); K = vec.fit_transform(c.text); P = vec.transform(posts.text)
    S = (P @ K.T).toarray()
    top = S.argmax(1); pred_ctrl = c.control_id.values[top]
    pred_dom = c.sim_domain_id.values[top]                                   # NaN -> controls outside the 12 domains
    true = posts.domain_id.values
    ok = np.array([(not np.isnan(p)) and int(p) == t for p, t in zip(pred_dom, true)])
    top3 = np.argsort(-S, 1)[:, :3]
    ok3 = np.array([any((not np.isnan(c.sim_domain_id.values[j])) and int(c.sim_domain_id.values[j]) == t for j in row) for row, t in zip(top3, true)])
    has_name = np.array([d in t.lower() for d, t in zip(posts.domain, posts.text)])      # domain name still readable after token dropout
    zero = S.max(1) == 0
    return {"vectorizer": kind, "n_posts": int(len(posts)), "accuracy_top1_all": float(ok.mean()), "accuracy_top3_all": float(ok3.mean()),
            "n_posts_with_domain_name": int(has_name.sum()), "accuracy_top1_posts_with_domain_name": float(ok[has_name].mean()) if has_name.any() else None,
            "accuracy_top1_posts_without_domain_name": float(ok[~has_name].mean()) if (~has_name).any() else None,
            "share_posts_with_zero_similarity": float(zero.mean()), "chance_level": 1 / 12}


def link_report(df_test_en, c):
    """Primary = word TF-IDF (as specified); the char n-gram variant is reported next to it, not selected on the test set."""
    out = {"n_kb_records": int(len(c)), "word_tfidf": link_posts(df_test_en, c, "word"), "char_tfidf": link_posts(df_test_en, c, "char")}
    kb12 = c[c.sim_domain_id.notna()].reset_index(drop=True)
    out["kb_restricted_to_12_domains"] = {"n_kb_records": int(len(kb12)), "word_tfidf": link_posts(df_test_en, kb12, "word")}
    return out


if __name__ == "__main__":
    import json, sys
    c = load_controls(sys.argv[1] if len(sys.argv) > 1 else "controls.csv")
    print(json.dumps(extraction_report(c), indent=2)); print(pd.DataFrame(domain_table(c)).to_string(index=False))
