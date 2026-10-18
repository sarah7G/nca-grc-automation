"""
Shared definitions for the NCA GRC-automation experiment.
Every table in the thesis (Chapters 3 and 5) is produced from these functions by run_experiment.py.
All data are SYNTHETIC / SIMULATED (see README).  RNG call order is identical to the original
run_experiment.py, so seed 42 reproduces the original generator exactly.
"""
import platform
import numpy as np, pandas as pd

# ---------------------------------------------------------------- 12 simulated domains -> ECC-1:2018
# (english name, arabic name, ECC-1:2018 sub-domain codes that the domain stands for)
DOMAINS = [("governance", "الحوكمة", ["1-1", "1-2", "1-3", "1-4"]),
           ("risk management", "إدارة المخاطر", ["1-5"]),
           ("asset management", "إدارة الأصول", ["2-1"]),
           ("access control", "التحكم بالوصول", ["2-2"]),
           ("cryptography", "التشفير", ["2-8"]),
           ("network security", "أمن الشبكات", ["2-5"]),
           ("vulnerability management", "إدارة الثغرات", ["2-10"]),
           ("logging and monitoring", "المراقبة والسجلات", ["2-12"]),
           ("incident response", "الاستجابة للحوادث", ["2-13"]),
           ("business continuity", "استمرارية الأعمال", ["3-1"]),
           ("third-party security", "أمن الأطراف الثالثة", ["4-1"]),
           ("security awareness", "التوعية الأمنية", ["1-10"])]
CLASSES = ["compliant", "non_compliant", "neutral"]

# ECC-1:2018 official structure (5 main domains, 29 sub-domains). Used to derive domain/sub-domain
# from the control_id instead of from PDF page headers (which polluted the 'domain' column).
ECC_MAIN = {"1": "Cybersecurity Governance", "2": "Cybersecurity Defense", "3": "Cybersecurity Resilience",
            "4": "Third-Party and Cloud Computing Cybersecurity", "5": "Industrial Control Systems Cybersecurity"}
ECC_SUB = {"1-1": "Cybersecurity Strategy", "1-2": "Cybersecurity Management", "1-3": "Cybersecurity Policies and Procedures",
           "1-4": "Cybersecurity Roles and Responsibilities", "1-5": "Cybersecurity Risk Management",
           "1-6": "Cybersecurity in Information Technology Projects", "1-7": "Compliance with Cybersecurity Standards, Laws and Regulations",
           "1-8": "Periodical Cybersecurity Review and Audit", "1-9": "Cybersecurity in Human Resources",
           "1-10": "Cybersecurity Awareness and Training Program",
           "2-1": "Asset Management", "2-2": "Identity and Access Management",
           "2-3": "Information System and Information Processing Facilities Protection", "2-4": "Email Protection",
           "2-5": "Networks Security Management", "2-6": "Mobile Devices Security", "2-7": "Data and Information Protection",
           "2-8": "Cryptography", "2-9": "Backup and Recovery Management", "2-10": "Vulnerabilities Management",
           "2-11": "Penetration Testing", "2-12": "Cybersecurity Event Logs and Monitoring Management",
           "2-13": "Cybersecurity Incident and Threats Management", "2-14": "Physical Security", "2-15": "Web Application Security",
           "3-1": "Cybersecurity Resilience Aspects of Business Continuity Management",
           "4-1": "Third-Party Cybersecurity", "4-2": "Cloud Computing and Hosting Cybersecurity",
           "5-1": "Industrial Control Systems Protection"}
SUB_TO_DOMAIN = {s: i for i, (_, _, subs) in enumerate(DOMAINS) for s in subs}

# ---------------------------------------------------------------- templates
EN = {0: ["Our {d} controls passed the latest NCA ECC audit, fully compliant.",
          "Good news: the {d} program is aligned with NCA requirements and verified.",
          "We closed all findings on {d}; compliance with ECC confirmed.",
          "{d} policy implemented and evidence reviewed, meets the NCA baseline."],
      1: ["Audit found major gaps in {d}, controls missing and NCA requirements not met.",
          "Our {d} process is non-compliant with ECC, findings still open.",
          "Failed the NCA assessment on {d}: policy not enforced.",
          "No evidence of {d} controls, serious compliance violation."],
      2: ["New phishing campaign targeting banks reported today.",
          "Webinar next week about {d} trends in cybersecurity.",
          "Cyber awareness month starts, join the conference.",
          "Researchers publish a report on ransomware and {d}."]}
AR = {0: ["اجتازت ضوابط {d} لدينا آخر تدقيق للهيئة الوطنية للأمن السيبراني وهي متوافقة بالكامل.",
          "خبر جيد: برنامج {d} متوافق مع متطلبات الهيئة وتم التحقق منه.",
          "أغلقنا جميع الملاحظات في {d} وتم تأكيد الامتثال للضوابط الأساسية.",
          "تم تطبيق سياسة {d} ومراجعة الأدلة وهي تحقق الحد الأدنى للهيئة."],
      1: ["كشف التدقيق فجوات كبيرة في {d} وضوابط مفقودة ومتطلبات الهيئة غير مستوفاة.",
          "عملية {d} لدينا غير متوافقة مع الضوابط الأساسية والملاحظات ما زالت مفتوحة.",
          "رسبنا في تقييم الهيئة بخصوص {d}: السياسة غير مطبقة.",
          "لا يوجد دليل على ضوابط {d} وهناك مخالفة امتثال خطيرة."],
      2: ["حملة تصيد جديدة تستهدف البنوك تم الإبلاغ عنها اليوم.",
          "ندوة الأسبوع القادم عن اتجاهات {d} في الأمن السيبراني.",
          "بدأ شهر التوعية السيبرانية وندعوكم لحضور المؤتمر.",
          "باحثون ينشرون تقريرا عن برامج الفدية و{d}."]}
HASH = ["#NCA", "#cybersecurity", "#ECC", "#infosec", "#الأمن_السيبراني", "#الامتثال", ""]
RULE_POS = ["compliant", "passed", "aligned", "verified", "confirmed", "meets", "متوافق", "اجتاز", "تحقق", "تأكيد"]
RULE_NEG = ["non-compliant", "gaps", "missing", "not met", "failed", "violation", "not enforced", "no evidence",
            "غير متوافق", "فجوات", "مفقودة", "غير مستوفاة", "رسبنا", "مخالفة", "غير مطبقة", "لا يوجد دليل"]


def env_info():
    import sklearn, xgboost
    return {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__, "xgboost": xgboost.__version__}


# ---------------------------------------------------------------- 1. posts
def make_tweets(n, rng, p_confuser=0.35, p_dropout=0.15):
    """Synthetic posts. Label = class of the main template. With prob p_confuser a fragment of a
    DIFFERENT class is appended; tokens are randomly dropped (same RNG order as the original script)."""
    rows = []
    for _ in range(n):
        y = int(rng.choice(3, p=[0.35, 0.35, 0.30]))
        lang = "ar" if rng.random() < 0.5 else "en"
        T = AR if lang == "ar" else EN
        di = int(rng.integers(12)); d = DOMAINS[di]
        dom = d[1] if lang == "ar" else d[0]
        text = T[y][rng.integers(4)].format(d=dom)
        if rng.random() < p_confuser:
            y2 = int(rng.choice([c for c in range(3) if c != y]))
            text += " " + T[y2][rng.integers(4)].format(d=dom)
        toks = [t for t in text.split() if rng.random() > p_dropout]
        text = " ".join(toks) + " " + HASH[rng.integers(len(HASH))]
        rows.append((text.strip(), y, lang, dom, di))
    return pd.DataFrame(rows, columns=["text", "label", "lang", "domain", "domain_id"])


def rule_baseline(texts):
    out = []
    for t in texts:
        tl = t.lower()
        neg = sum(tl.count(k) for k in RULE_NEG)
        pos = sum(tl.count(k) for k in RULE_POS) - sum(tl.count("non-compliant") for _ in [0])
        out.append(1 if neg > max(pos, 0) else (0 if pos > 0 else 2))
    return np.array(out)


# ---------------------------------------------------------------- 3. audit simulator
def simulate_audits(n_orgs, rng, T=365, D=12, sigma_obs=0.02, mag=None):
    """mag=None: gap magnitude ~ U(0.15, 0.40) (main experiment). mag=x: fixed magnitude x (sensitivity grid).
    The magnitude draw is always consumed so the RNG stream is identical to the original when mag is None."""
    base = rng.beta(2, 12, (n_orgs, D)) * 0.6 + 0.05
    x = np.empty((n_orgs, D, T)); x[:, :, 0] = base
    for t in range(1, T):
        x[:, :, t] = x[:, :, t - 1] + 0.1 * (base - x[:, :, t - 1]) + rng.normal(0, 0.01, (n_orgs, D))
    g = np.zeros_like(x); ev = []; tt = np.arange(T)
    for o in range(n_orgs):
        for d in range(D):
            last_end = 40
            for _ in range(rng.poisson(1.2)):
                s = int(rng.integers(max(40, last_end), T - 30)) if last_end < T - 31 else None
                if s is None: break
                k = int(rng.integers(5, 21)); m = float(rng.uniform(0.15, 0.40)); dur = int(rng.integers(20, 121))
                if mag is not None: m = float(mag)
                e = min(s + dur, T - 1)
                prof = np.where(tt < s, 0.0, np.where(tt <= e, m * np.minimum(1, (tt - s) / k), m * np.exp(-(tt - e) / 7.0)))
                g[o, d] += prof
                ev.append((o, d, s, e, k, m)); last_end = e + 30
    true = np.clip(x + g, 0, 1)
    obs = true + rng.normal(0, sigma_obs, true.shape)
    events = pd.DataFrame(ev, columns=["org", "dom", "onset", "end", "ramp", "mag"])
    events["window_end"] = np.minimum(events.end + 21, T - 1)
    return true, obs, events


# ---------------------------------------------------------------- 4. detectors (all use the first 30 days as reference)
def _ref(obs, warm):
    return obs[:, :, :warm].mean(2), obs[:, :, :warm].std(2) + 1e-6


def cusum_alarms(obs, h, k=0.5, warm=30):
    n, D, T = obs.shape
    mu, sd = _ref(obs, warm)
    S = np.zeros((n, D)); alarm = np.zeros((n, D, T), bool)
    for t in range(warm, T):
        S = np.maximum(0, S + (obs[:, :, t] - mu) / sd - k)
        a = S > h; alarm[:, :, t] = a; S[a] = 0
    return alarm


def fixed_alarms(obs, delta, warm=30):
    """Fixed-threshold alert: observed risk exceeds the 30-day reference mean by more than `delta` (raw risk units).
    Consecutive exceedances count as ONE alarm (rising edge), so false alarms are comparable to CUSUM/EWMA."""
    mu, _ = _ref(obs, warm)
    ex = np.zeros(obs.shape, bool); ex[:, :, warm:] = (obs[:, :, warm:] - mu[:, :, None]) > delta
    alarm = ex.copy(); alarm[:, :, 1:] &= ~ex[:, :, :-1]
    return alarm


def ewma_alarms(obs, lam, L, warm=30):
    """One-sided EWMA control chart on the standardised deviation; limit = L * sqrt(lam / (2 - lam)); reset after alarm."""
    n, D, T = obs.shape
    mu, sd = _ref(obs, warm)
    z = np.zeros((n, D)); alarm = np.zeros((n, D, T), bool); lim = L * np.sqrt(lam / (2 - lam))
    for t in range(warm, T):
        z = lam * (obs[:, :, t] - mu) / sd + (1 - lam) * z
        a = z > lim; alarm[:, :, t] = a; z[a] = 0
    return alarm


def eval_alarms(alarm, events, orgs):
    n, D, T = alarm.shape
    ev = events[events.org.isin(orgs)]
    inwin = np.zeros(alarm.shape, bool)
    for r in ev.itertuples(): inwin[r.org, r.dom, r.onset:r.window_end + 1] = True
    sub = alarm[orgs]; iw = inwin[orgs]
    false_alarms = (sub & ~iw).sum()
    series_has_ev = np.zeros((len(orgs), D), bool); idx = {o: i for i, o in enumerate(orgs)}
    for r in ev.itertuples(): series_has_ev[idx[r.org], r.dom] = True
    clean = ~series_has_ev
    fpr_series = float((sub[clean] & ~iw[clean]).any(1).mean()) if clean.any() else np.nan
    det = []
    for r in ev.itertuples():
        w = np.where(alarm[r.org, r.dom, r.onset:r.window_end + 1])[0]
        det.append(w[0] if len(w) else np.nan)
    ev = ev.assign(d_pipe=det)
    return {"recall": float(np.mean(~np.isnan(det))), "false_alarms_per_series_year": float(false_alarms / (len(orgs) * D)),
            "fpr_series_level": fpr_series}, ev


def audit_delays(obs, events, orgs, cycle, rng, tau=0.10, warm=30):
    base30 = obs[:, :, :warm].mean(2); phase = rng.uniform(0, cycle, obs.shape[0]); T = obs.shape[2]
    out = []
    for r in events[events.org.isin(orgs)].itertuples():
        days = np.arange(phase[r.org], T, cycle).astype(int)
        days = days[(days >= r.onset) & (days <= r.end)]
        hit = [a for a in days if obs[r.org, r.dom, a] - base30[r.org, r.dom] > tau]
        out.append(hit[0] - r.onset if hit else np.nan)
    return np.array(out)


def boot_reduction(dp, da, orgs_e, seed, B=1000):
    """95% percentile bootstrap over organisations of 100*(1 - mean(dp)/mean(da))."""
    u = np.unique(orgs_e); S = {o: (dp[orgs_e == o].sum(), da[orgs_e == o].sum()) for o in u}
    br = np.random.default_rng(seed); r_ = []
    for _ in range(B):
        pick = br.choice(u, len(u)); r_.append(100 * (1 - sum(S[o][0] for o in pick) / sum(S[o][1] for o in pick)))
    return [float(np.percentile(r_, 2.5)), float(np.percentile(r_, 97.5))]


def split_orgs(n_orgs, seed):
    """Validation / test organisations used for every drift-detector experiment (30 / 30 when n_orgs = 200)."""
    rng = np.random.default_rng(seed + 11)
    perm = rng.permutation(n_orgs); nt = int(0.15 * n_orgs)
    return perm[:nt], perm[nt:2 * nt]
