#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QA gate for the dnd-seeding skill.

Three modes:
  --baseline DIR   recompute the 9 pinned claim-family counts over a corpus and
                   compare against brief v4 section 1. Gate = the 5 numbers
                   121/167/16/5/5 must reproduce exactly.
  --check FILE     validate a draft (or read from stdin with no FILE). Runs the
                   item-level M2 fee gate, per-mode 10/10 quota (5A), the maps/koc
                   exceptions (5B), the shared bans (5C) and anti-repeat (7).
  --selftest       run built-in fixtures. Needs no corpus.

Deterministic: no network, no randomness, no clock in any comparison.
Exit 0 = pass, 1 = fail, 2 = usage/config error.
"""
import argparse
import os
import re
import sys
import unicodedata

# stdin/stdout as UTF-8 regardless of platform codepage (Windows cp1252 crashes otherwise)
for _s in ("stdin", "stdout", "stderr"):
    _f = getattr(sys, _s, None)
    if _f is not None and hasattr(_f, "reconfigure"):
        try:
            _f.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

# ---------------------------------------------------------------------------
# POLICY CONFIG - the only place real hospital fee policy lives in this script.
# Every value here is a business fact, not an inference. Slots marked OPEN make
# the script refuse to run the fee gate, by design: guessing them is exactly the
# failure mode that produced the SKILL.md:55 bug.
# ---------------------------------------------------------------------------
POLICY_VERSION = "2026-07-27"

# GATE 2 answers from the user, 2026-07-27:
#  A. Follow-up after surgery done at ANOTHER hospital -> charge, NOT free.
#     Free follow-up applies only to patients operated at DND. Tier number OPEN.
#  B. Presbyopia (lao thi) -> free. User rejected the premise of routing lao thi
#     to the glasses-cutting tier ("lao thi dau co can mang kinh nua"), so
#     `lao thi` outranks the `cat kinh` blocker instead of losing to it.
#  C. Phakic ICL -> free exam, because it is refractive surgery. No longer
#     provisional.
POLICY = {
    # bucket -> fee tier id
    "buckets": {
        "fu_dnd": "T-FU",   # operated at DND, within 3 years
        "kx": "T0",         # myopia/hyperopia/astigmatism, presbyopia (G1), phakic ICL (GATE 2-C)
        "kinh": "T1",       # refraction measurement + glasses only
        "pc": "T2",         # phaco
        "or": "T2",         # ortho-k / myopia control
        "khac": "T2",       # retina/vitreous, glaucoma, oculoplastics, general check-up
    },
    # tiers allowed to mention a free exam at all
    "free_exam_tiers": ("T-FU", "T0"),
    # GATE 2-A: follow-up for surgery done elsewhere is charged, and the skill must
    # NOT quote a number for it - hotline instead.
    "fu_other_hospital_is_free": False,
    "fu_other_hospital_tier": "HOTLINE",
    # GATE 2-B: `lao thi` beats the `cat kinh` blocker. Scope is exactly that one
    # blocker - the user confirmed presbyopia patients are not routed to glasses,
    # not that presbyopia overrides every other service.
    "lao_thi_beats_cat_kinh": True,
    # GATE 2-B follow-on, NOT answered: presbyopia is treated via Presbyond (laser,
    # clearly T0) OR Phaco + multifocal IOL. Phaco is a T2 blocker. Whether a
    # presbyopia patient on the phaco path gets the free exam is a fee question
    # nobody has answered, so it routes to hotline rather than being inferred.
    "lao_thi_phaco_path_tier": None,     # OPEN -> "T0" | "T2" | "HOTLINE"
    # GATE 2-C: phakic ICL exam is free (T0), confirmed.
    "icl_tier": "T0",
}
OPEN_SLOTS = [k for k in ("lao_thi_phaco_path_tier",) if POLICY.get(k) is None]

# ---------------------------------------------------------------------------
# Claim-family regexes - PINNED to brief v4 section 1. Do not "improve" these:
# their whole job is to reproduce a historical measurement. Anything stricter or
# looser belongs in a new row, not in an edit to an existing one.
# ---------------------------------------------------------------------------
CLAIM_REGEX = {
    "dau_claim":        r"(kh?ông|ko|k|chẳng|chả) *đau",
    "vision_absolute":  r"10/10",
    "vision_absolute_en": r"20/20",
    "superlative_vn":   r"tốt nhất|giỏi nhất|số 1",
    "superlative_en":   r"top-tier|outstanding|highly recommend|amazing|fantastic|unbelievabl|incredible|excellent|best",
    "compare_other_hospital": r"rẻ hơn|cheaper|fraction of|bằng nửa|so với.{0,25}(viện|bệnh viện|nước)",
    "commitment":       r"cam kết|đảm bảo",
    "cure_myopia":      r"khỏi cận|hết cận",
    "repeat_phrase":    r"nhẹ nhàng",
}

# brief v4 section 1 expected values over the 217-file corpus
BASELINE_EXPECTED = {
    "dau_claim": 121,
    "vision_absolute": 167,
    "vision_absolute_en": 1,
    "superlative_vn": 16,
    "superlative_en": 8,
    "compare_other_hospital": 31,
    "commitment": 5,
    "cure_myopia": 5,
    "repeat_phrase": 281,
}
# M3 says the script is only trusted once these 5 reproduce exactly.
BASELINE_GATE_KEYS = ("dau_claim", "vision_absolute", "superlative_vn",
                      "commitment", "cure_myopia")

# secondary measurements from section 1 / section 3B, reported not gated
AUX_REGEX = {
    "dau_khong":        r"không *đau",
    "dau_ko":           r"ko *đau",
    "dau_k":            r"\bk *đau",
    "dau_cha":          r"chả *đau",
    "fee_zero_digit":   r"0đ",
    "fee_zero_digit_preceded": r"[0-9]0đ",
    "free_exam_words":  r"khám.{0,25}(free|miễn phí)",
    "free_followup":    r"miễn phí tái khám",
    "lao_thi":          r"lão thị",
    "cat_kinh_group":   r"cắt kính|đo độ|đo mắt|thay kính",
    "smile_pro":        r"smile pro",
    "bs_tuan":          r"bs *tuấn",
}

# M3 target regex - widened; must reach 0 hits after step 5
DAU_CLAIM_WIDE = (r"(kh?ông|ko|k|chẳng|chả|chưa) *"
                  r"(hề|bị|thấy|có|kịp)? *đau")


def rx(pattern):
    return re.compile(pattern, re.IGNORECASE)


def count_hits(pattern, text):
    """grep -o semantics: number of non-overlapping matches."""
    return len(rx(pattern).findall(text))


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def norm(s):
    """Fold to NFC and lowercase. Vietnamese arrives in both NFC and NFD."""
    return unicodedata.normalize("NFC", s).lower()

# ---------------------------------------------------------------------------
# Service tokens for the item-level M2 gate (brief section 3B + section 4 M2)
# ---------------------------------------------------------------------------
# A free-exam mention is legal on an item only if the item carries a kx or fu
# token AND carries no blocking token. `lao thi` is deliberately NOT a blocker
# (G1); `cat kinh` IS one, but loses to `lao thi` per GATE 2-B.
TOK = {
    # P1 - post-op, highest priority
    "fu": r"tái khám|sau mổ|hậu phẫu|mổ .{0,10}(tháng|năm) r|mới mổ|vừa mổ|đã mổ",
    # marker that the surgery happened somewhere else -> not T-FU (GATE 2-A)
    # `mo` and the place can be separated by the service ("mo can o vien khac"), so
    # a gap is allowed - but it is TEMPERED against `dnd` and kept comma-free. Both
    # guards are load-bearing: "mo ben DND roi qua vien khac kham lai" says the
    # surgery WAS at DND, and an untempered gap reads it as elsewhere, wrongly
    # denying a free follow-up. Competitor names take an optional facility prefix
    # because "o bv mat sai gon" otherwise slips past and returns fu_dnd -> free,
    # promising a free exam to someone operated on elsewhere (GATE 2-A).
    "fu_elsewhere": (r"mổ(?:(?!dnd)[^,.\n]){0,20}?((ở|bên|tại) )?(viện|bv|bệnh viện|chỗ|nơi) khác"
                     r"|mổ(?:(?!dnd)[^,.\n]){0,20}?(ở|bên|tại) ((bv|bệnh viện|viện|phòng khám|pk) )?"
                     r"(mắt sài gòn|mắt sg|mắt tphcm|việt nhật)"
                     r"|(viện|bv|bệnh viện|chỗ|nơi) khác mổ"
                     r"|mổ(?:(?!dnd)[^,.\n]){0,20}?(ở|bên|tại) đâu khác"),
    # P2 - surgical / refractive intent
    "kx": (r"mổ cận|mổ khúc xạ|smile|lasik|smartsight|smartsurface|"
           r"clear|femto|icl|phakic|khúc xạ|mổ viễn|mổ loạn|lão thị"),
    # generic surgical intent. Brief 3B pins P2 as bare `mổ|smile|lasik|phaco|
    # ortho|icl` then routes "theo service". So bare `mổ` may only fall through to
    # kx AFTER pc/or/khac have been tried - otherwise "mổ phaco" lands in T0-free,
    # which is the SKILL.md:55 bug rebuilt.
    "surgery_generic": r"\bmổ\b|phẫu thuật|bắn laser|đi mổ|mổ mắt",
    "pc": r"phaco|thủy tinh thể|đục thủy tinh",
    "or": r"ortho|orthok|ortho-k|kiểm soát cận|kính đêm|đeo đêm",
    # P3 - glasses only
    "kinh": r"cắt kính|đo độ|đo mắt|thay kính|mua kính|kính mới",
    # other pathology / cosmetic / general
    "khac": (r"võng mạc|dịch kính|glaucoma|tăng nhãn áp|cắt mí|sụp mi|bọng mắt|"
             r"thẩm mỹ mắt|tổng quát"),
    # P4 - condition stated with no intent
    "condition_only": r"cận|viễn|loạn|lão thị",
}

# M2 blockers: tokens that forbid a free-exam claim on the same item
BLOCK_TOKENS = ("pc", "or", "kinh", "khac")

# free-exam mention, both word and digit forms. Section 6 measured 664 word-form
# vs 13 digit-form hits, so the word forms carry the rule.
FREE_EXAM_RX = (r"khám.{0,30}(free|miễn phí|0 *đ|0đ|miễn phi)"
                r"|(free|miễn phí|0đ).{0,30}khám"
                r"|khám 12 bước (free|miễn phí)"
                r"|tặng gói khám"
                r"|gói khám.{0,20}(free|miễn phí|0đ)"
                r"|trị giá 1\.?000\.?000"
                # third way to say free, with no free/0d token at all. The corpus
                # uses it and the earlier alternatives all miss it.
                r"|khám[^.\n]{0,30}(kh?ông|ko|k|chẳng) *(mất|tốn|đóng|thu) *(phí|tiền|đồng|xu)"
                r"|(kh?ông|ko|k|chẳng) *(mất|tốn|đóng|thu) *(phí|tiền|đồng)[^.\n]{0,20}khám")

# Markers that a nearby free-exam mention is being DENIED or scoped away, not
# claimed. "khám phaco co phi, k thuoc goi kham free cua mo can" is the corrected
# messaging - the gate must not punish a disclaimer for naming what it disclaims.
DENY_FREE_RX = (r"(kh?ông|ko|k|chẳng) *(thuộc|áp dụng|bao gồm|nằm trong)"
                r"|khác gói|gói riêng|riêng nha"
                r"|có phí|có tính phí|mất phí|tính phí|đóng phí|phải trả|thu phí")
# ... except these, which are free claims that happen to contain a cost word
POS_FREE_RX = r"(kh?ông|ko|k|chẳng) *(mất|tốn|đóng) *(phí|tiền|đồng)"
DENY_WINDOW = 110  # chars either side of the free mention

# A free mention can also be legal because it is SCOPED to the eligible group
# ("goi tai kham free 3 nam la cho nguoi mo tai DND thoi"). Explaining a boundary
# means naming both sides, so such an item trips fu_elsewhere and would be failed
# by bucket logic alone. Both halves are required: a bare "chi"/"thoi" is far too
# common to treat as scoping on its own.
SCOPE_FREE_RX = r"chỉ|thôi|dành cho|là cho|áp dụng|riêng cho"
ELIGIBILITY_RX = (r"(mổ|khám|phẫu thuật) *(tại|ở|bên) *dnd|tại dnd|bên dnd"
                  r"|mổ cận|khúc xạ|hậu phẫu|trong 3 năm")

# A fee ASSERTION states hospital fee information and so requires the footer.
# Asking a price, or saying "there is a fee, call the hotline", asserts nothing -
# those are mentions. Conflating the two makes the footer fire on almost every ads
# run, and a check that cries wolf gets turned off.
FEE_NUMBER_RX = (r"trị giá 1\.?000\.?000"
                 + r"|160\.?000|350\.?000|80\.?000|175\.?000"
                 + r"|(giá|phí|chi phí|hết|trọn gói|chỉ từ|còn|giảm)"
                 r"[^.\n]{0,25}[0-9][0-9\.,]* *(đ|k|tr|triệu|nghìn|ngàn)\b"
                 + r"|[0-9][0-9\.,]* *(đ|k|tr|triệu|nghìn|ngàn)"
                 r"[^.\n]{0,15}(1 *mắt|2 *mắt|/mắt|trọn gói|1 bên)"
                 + r"|giảm *(đến|tới)? *[0-9]+ *%|hỗ trợ *(đến|tới)? *[0-9]+ *%"
                 + r"|[0-9]+ *% *(chi phí|ưu đãi)")
# kept for reporting only - the broad "any fee word" surface, used to tell
# "mentioned fees but asserted nothing" apart from "said nothing about fees"
FEE_INFO_RX = (FEE_NUMBER_RX + "|" + FREE_EXAM_RX
               + r"|phí khám|giá khám|chi phí khám|bao nhiêu tiền|hết bao nhiêu")

FOOTER_RX = r"\[fees:\s*([0-9]{4}-[0-9]{2}(?:-[0-9]{2})?)\s*·\s*(T-FU|T0|T1|T2)\s*\]"

# ---------------------------------------------------------------------------
# 5A - per-mode 10/10 quota. Section headers the modes actually print are
# "### Goc N: ..." (group) and "### Kieu N: ..." (reply-group / ads / live).
# ---------------------------------------------------------------------------
QUOTA_10_10 = {
    "group":       {"allowed": {6, 7}, "max_ratio": 0.20},
    "story":       {"allowed": {6, 7}, "max_ratio": 0.20},
    "reply-group": {"allowed": {1},    "max_ratio": 0.20},
    "reply_group": {"allowed": {1},    "max_ratio": 0.20},
    "ads":         {"allowed": {5},    "max_ratio": 0.20},
    "live":        {"allowed": set(),  "max_ratio": 0.0},
}

# ---------------------------------------------------------------------------
# 5B - maps/koc exceptions, scoped per measured column. Anything not listed here
# is NOT exempt. Granting by column is the point: v3 bundled all three and so
# exempted things the sample files never needed.
# ---------------------------------------------------------------------------
EXEMPT = {
    "maps":            {"dau_claim", "compare_other_hospital"},
    "maps_foreigner":  {"dau_claim", "compare_other_hospital",
                        "vision_absolute_en", "superlative_en"},
    "koc":             {"dau_claim", "vision_absolute"},
}
# modes that are not maps/koc get no exemptions at all
EXEMPT_DEFAULT = frozenset()

# 5C - shared bans, zero tolerance unless exempted by 5B
BAN_KEYS = ("dau_claim", "superlative_vn", "superlative_en", "commitment",
            "cure_myopia", "compare_other_hospital")
BAN_EXTRA = {
    "cure_forever": r"khỏi cận vĩnh viễn|hết cận vĩnh viễn",
    "everyone_eligible": r"ai (cũng|cx) mổ đượ?c|ai (cũng|cx) mổ đc",
}

# 7 - anti-repeat. Baseline: `nhe nhang` ~1.3 hits/file (281 over 217).
ANTIREPEAT_WATCH = ("nhẹ nhàng", "ổn áp", "10/10", "nhanh gọn", "máy xịn",
                    "êm ru", "nhẹ tênh", "ngọt xớt")
ANTIREPEAT_WARN_PER_ITEM = 0.15   # warn above this share of items
ANTIREPEAT_BLOCK_PER_ITEM = 0.30  # block above this share

SECTION_RX = re.compile(r"^#{2,4}\s*(?:Góc|Kiểu|Nhóm|Group|Type)\s*([0-9]+|[A-Z])\s*[:.—-]",
                        re.IGNORECASE | re.MULTILINE)
ITEM_RX = re.compile(r"^\s*([0-9]{1,3})[\.\)]\s+(.*)$")
# maps/koc output shape: "#### 3. UK Expat (English Teacher)" then body on the
# following lines. Without this the parser reports zero items on those files and
# every item-level check silently degrades to a whole-text check.
ITEM_HEADER_RX = re.compile(r"^#{2,6}\s*([0-9]{1,3})[\.\)]\s*(.*)$")
# story mode prints "Nhóm A/B/C/D"; every story item inherits Góc 7.
STORY_SECTION_FALLBACK = 7
MODE_RX = re.compile(r"^\*\*Mode:\*\*\s*([A-Za-z_\-]+)", re.IGNORECASE | re.MULTILINE)


class Item(object):
    def __init__(self, number, section, text, line):
        self.number = number
        self.section = section   # int section number, or None
        self.text = text
        self.line = line

    def __repr__(self):
        return "Item(%r, sec=%r, line=%r)" % (self.number, self.section, self.line)


def detect_mode(text, explicit=None):
    if explicit:
        return explicit.strip().lower()
    m = MODE_RX.search(text)
    if m:
        return m.group(1).strip().lower()
    head = text[:400].lower()
    for cand in ("maps_foreigner", "reply-group", "reply_group", "google_maps",
                 "maps", "koc", "story", "group", "ads", "live"):
        if cand in head:
            return "maps" if cand == "google_maps" else cand
    return "unknown"


def parse_items(text):
    """Split a draft into numbered items, attributed to the section above them.

    Continuation lines (a wrapped story paragraph) attach to the current item so
    a claim on line 2 of an item is still that item's claim.
    """
    items = []
    section = None
    current = None
    for lineno, raw in enumerate(text.splitlines(), start=1):
        sm = SECTION_RX.match(raw)
        if sm:
            tag = sm.group(1)
            # letter sections come from story mode; all story items are Goc 7
            section = int(tag) if tag.isdigit() else STORY_SECTION_FALLBACK
            current = None
            continue
        ihm = ITEM_HEADER_RX.match(raw)
        if ihm:
            current = Item(int(ihm.group(1)), section, ihm.group(2), lineno)
            items.append(current)
            continue
        if raw.startswith("#"):
            # a non-numbered header ends the current section attribution
            current = None
            continue
        im = ITEM_RX.match(raw)
        if im:
            current = Item(int(im.group(1)), section, im.group(2), lineno)
            items.append(current)
            continue
        if current is not None and raw.strip():
            current.text += "\n" + raw.strip()
    return items

# ---------------------------------------------------------------------------
# Bucket detection - brief section 3B priority ladder, first match wins.
# ---------------------------------------------------------------------------
def detect_bucket(text):
    """Return (bucket, tier, reason). bucket 'ambiguous' -> hotline, no price."""
    t = norm(text)
    has = lambda key: bool(rx(TOK[key]).search(t))

    # P1: post-op beats everything
    if has("fu"):
        if has("fu_elsewhere"):
            # GATE 2-A: operated elsewhere -> not free. Tier itself is an open slot.
            tier = POLICY["fu_other_hospital_tier"]
            if tier is None or tier == "HOTLINE":
                return ("fu_other", None, "P1 post-op elsewhere -> tier unset, hotline")
            return ("fu_other", tier, "P1 post-op elsewhere -> charged")
        return ("fu_dnd", POLICY["buckets"]["fu_dnd"], "P1 post-op at DND")

    # P2: surgical / refractive intent. Presbyopia lives here (G1 + GATE 2-B).
    if has("kx"):
        return ("kx", POLICY["buckets"]["kx"], "P2 refractive/surgical intent")
    if has("pc"):
        return ("pc", POLICY["buckets"]["pc"], "P2 phaco")
    if has("or"):
        return ("or", POLICY["buckets"]["or"], "P2 ortho-k / myopia control")
    if has("khac"):
        return ("khac", POLICY["buckets"]["khac"], "P2 pathology/cosmetic/general")
    # generic `mổ` with no named service, and no pc/or/khac above -> refractive
    if has("surgery_generic"):
        return ("kx", POLICY["buckets"]["kx"], "P2 generic surgical intent")

    # P3: glasses only, no P2 intent
    if has("kinh"):
        return ("kinh", POLICY["buckets"]["kinh"], "P3 glasses only")

    # P4: condition stated, no intent -> no price
    if has("condition_only"):
        return ("ambiguous", None, "P4 condition without intent -> hotline")

    return ("none", None, "no service token")


def free_exam_allowed(text):
    """Item-level M2 gate. Returns (allowed, reason)."""
    t = norm(text)
    bucket, tier, reason = detect_bucket(t)

    blockers = [k for k in BLOCK_TOKENS if rx(TOK[k]).search(t)]
    has_lao_thi = bool(rx(AUX_REGEX["lao_thi"]).search(t))

    # GATE 2-B: presbyopia outranks the glasses blocker, and only that one.
    if POLICY["lao_thi_beats_cat_kinh"] and has_lao_thi and "kinh" in blockers:
        blockers = [b for b in blockers if b != "kinh"]

    # GATE 2-B follow-on: presbyopia named together with the phaco path. Free-exam
    # eligibility here is an unanswered fee question, so it stays blocked. Without
    # this branch, "lao thi beats cat kinh" would generalise into "lao thi beats
    # phaco too" - the same over-generalisation that produced :55.
    if has_lao_thi and "pc" in blockers and POLICY["lao_thi_phaco_path_tier"] is None:
        return (False, "presbyopia via phaco path: fee unanswered (open slot) -> hotline")

    if blockers:
        return (False, "blocked by token(s): %s" % ",".join(blockers))
    if tier in POLICY["free_exam_tiers"]:
        return (True, "%s -> %s" % (bucket, tier))
    if bucket == "fu_other":
        return (False, "post-op elsewhere is not free (GATE 2-A)")
    if bucket in ("ambiguous", "none"):
        return (False, "no eligible service token (%s)" % reason)
    return (False, "%s -> %s not in free tiers" % (bucket, tier))


# ---------------------------------------------------------------------------
# baseline mode
# ---------------------------------------------------------------------------
def collect_corpus(root):
    paths = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in sorted(filenames):
            if fn.startswith("seeding_") and fn.endswith(".md"):
                paths.append(os.path.join(dirpath, fn))
    return sorted(paths)


def run_baseline(root, strict=True):
    paths = collect_corpus(root)
    if not paths:
        print("FAIL: no seeding_*.md files under %s" % root)
        return 2

    blob_parts, per_file = [], []
    for p in paths:
        txt = norm(read_text(p))
        blob_parts.append(txt)
        per_file.append((p, txt))
    blob = "\n".join(blob_parts)

    print("corpus: %d files under %s" % (len(paths), root))
    print("")
    print("%-26s %8s %8s %6s" % ("claim family", "counted", "expected", "gate"))
    print("-" * 52)

    failures = []
    for key in ("dau_claim", "vision_absolute", "vision_absolute_en",
                "superlative_vn", "superlative_en", "compare_other_hospital",
                "commitment", "cure_myopia", "repeat_phrase"):
        got = count_hits(CLAIM_REGEX[key], blob)
        exp = BASELINE_EXPECTED[key]
        gated = key in BASELINE_GATE_KEYS
        ok = (got == exp)
        mark = "OK" if ok else "DIFF"
        print("%-26s %8d %8d %6s %s" % (key, got, exp, "GATE" if gated else "-",
                                        "" if ok else "<- " + mark))
        if gated and not ok:
            failures.append((key, got, exp))

    print("")
    print("decomposition + secondary measures (reported, not gated)")
    print("-" * 52)
    for key in ("dau_khong", "dau_ko", "dau_k", "dau_cha", "fee_zero_digit",
                "fee_zero_digit_preceded", "free_exam_words", "free_followup",
                "lao_thi", "cat_kinh_group", "smile_pro", "bs_tuan"):
        print("%-26s %8d" % (key, count_hits(AUX_REGEX[key], blob)))
    print("%-26s %8d" % ("dau_claim_WIDE (M3 target)", count_hits(DAU_CLAIM_WIDE, blob)))

    # file-level co-occurrence: the measured consequence of the :55 bug
    ortho_ctx = rx(r"ortho|kiểm soát cận|cho bé|con e|trẻ")
    free_ctx = rx(r"khám.{0,25}(free|0đ|miễn phí)")
    phaco_ctx = rx(TOK["pc"])
    n_ortho_free = sum(1 for _p, t in per_file if ortho_ctx.search(t) and free_ctx.search(t))
    n_phaco_free = sum(1 for _p, t in per_file if phaco_ctx.search(t) and free_ctx.search(t))
    n_lao_thi = sum(1 for _p, t in per_file if rx(AUX_REGEX["lao_thi"]).search(t))
    n_both = sum(1 for _p, t in per_file
                 if rx(r"cận|viễn|loạn|lão thị").search(t)
                 and rx(AUX_REGEX["cat_kinh_group"]).search(t))
    n_fu = sum(1 for _p, t in per_file if rx(r"tái khám|sau mổ|hậu phẫu").search(t))
    print("")
    print("file-level co-occurrence (files, not hits)")
    print("-" * 52)
    for label, got, exp in (("ortho_ctx + free_exam", n_ortho_free, 64),
                            ("phaco_ctx + free_exam", n_phaco_free, 15),
                            ("lao thi (regex)", n_lao_thi, 11),
                            ("refractive + glasses tokens", n_both, 39),
                            ("post-op tokens", n_fu, 100)):
        print("%-26s %8d %8d %s" % (label, got, exp, "" if got == exp else "<- DIFF"))

    print("")
    if failures:
        print("BASELINE GATE: FAIL")
        for key, got, exp in failures:
            print("  %s: counted %d, expected %d" % (key, got, exp))
        print("The script is not trusted until these 5 reproduce (M3/M7).")
        return 1
    print("BASELINE GATE: PASS - 121/167/16/5/5 reproduced")
    return 0

# ---------------------------------------------------------------------------
# check mode
# ---------------------------------------------------------------------------
class Report(object):
    def __init__(self):
        self.fails = []
        self.warns = []
        self.notes = []

    def fail(self, code, msg):
        self.fails.append((code, msg))

    def warn(self, code, msg):
        self.warns.append((code, msg))

    def note(self, msg):
        self.notes.append(msg)

    def emit(self):
        for m in self.notes:
            print("  . %s" % m)
        for code, msg in self.warns:
            print("  WARN [%s] %s" % (code, msg))
        for code, msg in self.fails:
            print("  FAIL [%s] %s" % (code, msg))
        return 1 if self.fails else 0


def claims_free_exam(text):
    """True only if the text ASSERTS a free exam.

    A mention wrapped in a denial ("khong thuoc goi kham free", "co phi") is the
    corrected messaging, not a violation. Without this the gate would push writers
    back toward saying nothing about fees, which is how :55 survived 13 months.
    """
    t = norm(text)
    deny_rx, pos_rx = rx(DENY_FREE_RX), rx(POS_FREE_RX)
    scope_rx, elig_rx = rx(SCOPE_FREE_RX), rx(ELIGIBILITY_RX)
    for m in rx(FREE_EXAM_RX).finditer(t):
        lo = max(0, m.start() - DENY_WINDOW)
        window = t[lo:m.end() + DENY_WINDOW]
        # a "khong mat phi" style phrase is itself a free claim, not a denial
        if pos_rx.search(window):
            return True
        if deny_rx.search(window):
            continue
        # scoped to the eligible group -> a statement of the rule, not a claim
        if scope_rx.search(window) and elig_rx.search(window):
            continue
        return True
    return False


def asserts_fee(text):
    """True if the text asserts hospital fee information, so needs the footer.

    Deny-aware for the same reason claims_free_exam is: a disclaimer that names a
    free package in order to exclude it is not an assertion of that package.
    """
    if claims_free_exam(text):
        return True
    return bool(rx(FEE_NUMBER_RX).search(norm(text)))


def check_m2(items, rep):
    """Item-level fee gate. The core of the :55 fix."""
    n_checked = 0
    for it in items:
        if not claims_free_exam(it.text):
            continue
        n_checked += 1
        allowed, reason = free_exam_allowed(it.text)
        if not allowed:
            rep.fail("M2", "item %s (line %d): free-exam claim not allowed - %s\n      %s"
                     % (it.number, it.line, reason, it.text[:120]))
    rep.note("M2: %d item(s) mention a free exam" % n_checked)


def check_footer(text, items, rep, fees_path=None):
    """Section 6 two-layer footer check, runs whenever fee info is present."""
    info_rx = rx(FEE_INFO_RX)
    fee_items = [it for it in items if asserts_fee(it.text)]
    mention_only = [it for it in items
                    if info_rx.search(norm(it.text)) and it not in fee_items]
    m = re.search(FOOTER_RX, text)
    if not fee_items:
        if mention_only:
            rep.note("footer: %d item(s) mention fees without asserting a number "
                     "(question / hotline deflection), footer not required"
                     % len(mention_only))
        else:
            rep.note("footer: no fee information in draft, footer not required")
        return
    if not m:
        rep.fail("FOOTER-A", "draft asserts fee information (%d item(s)) but has no "
                             "[fees: <date> · <tier>] footer:\n      %s"
                 % (len(fee_items), fee_items[0].text[:100]))
        return
    fdate, ftier = m.group(1), m.group(2)
    rep.note("footer: [fees: %s · %s] over %d fee item(s)" % (fdate, ftier, len(fee_items)))
    if fees_path and os.path.exists(fees_path):
        ftxt = read_text(fees_path)
        dm = re.search(r"(?:cập nhật|updated)\D{0,12}([0-9]{4}-[0-9]{2}(?:-[0-9]{2})?)",
                       ftxt, re.IGNORECASE)
        if dm and not fdate.startswith(dm.group(1)[:7]):
            rep.fail("FOOTER-B", "footer date %s does not match %s (%s)"
                     % (fdate, dm.group(1), os.path.basename(fees_path)))
        if ftier not in ftxt:
            rep.fail("FOOTER-B", "tier %s not found in %s" % (ftier, os.path.basename(fees_path)))
    elif fees_path:
        rep.warn("FOOTER-B", "fees file not found at %s, layer (b) skipped" % fees_path)
    else:
        rep.note("footer: layer (b) skipped (no --fees given; fees table still in SKILL.md "
                 "until step 6)")


def check_quota_10_10(mode, items, rep):
    cfg = QUOTA_10_10.get(mode)
    if cfg is None:
        rep.note("5A: mode %r has no quota row (maps/koc handled by 5B)" % mode)
        return
    hits = [it for it in items if "10/10" in it.text]
    if not hits:
        rep.note("5A: no 10/10 in draft")
        return
    n_items = max(len(items), 1)
    for it in hits:
        if it.section is None:
            rep.warn("5A", "item %s (line %d) has 10/10 but no section header to "
                           "attribute it to" % (it.number, it.line))
        elif it.section not in cfg["allowed"]:
            rep.fail("5A", "item %s (line %d): 10/10 in section %d, allowed sections "
                           "for mode %s = %s"
                     % (it.number, it.line, it.section, mode,
                        sorted(cfg["allowed"]) or "none"))
    ratio = len(hits) / float(n_items)
    if cfg["max_ratio"] == 0.0:
        if hits:
            rep.fail("5A", "mode %s allows no 10/10, found %d" % (mode, len(hits)))
        return
    # Floor of 1: a bare ratio bans the FIRST instance in any run under 1/ratio
    # items (1/4 = 25% > 20%), which is an artifact of run length, not a style
    # violation. The 20% ceiling still binds on full-length runs.
    allowed = max(1, int(n_items * cfg["max_ratio"]))
    if len(hits) > allowed:
        rep.fail("5A", "10/10 in %d/%d items (%.0f%%), quota %.0f%% -> max %d"
                 % (len(hits), n_items, ratio * 100, cfg["max_ratio"] * 100, allowed))
    else:
        rep.note("5A: 10/10 in %d/%d items (%.0f%%), quota %.0f%% -> max %d"
                 % (len(hits), n_items, ratio * 100, cfg["max_ratio"] * 100, allowed))


def check_bans(mode, text, items, rep):
    exempt = EXEMPT.get(mode, EXEMPT_DEFAULT)
    if exempt:
        rep.note("5B: mode %r exempt from %s" % (mode, ", ".join(sorted(exempt))))
    body = norm("\n".join(it.text for it in items) if items else text)
    for key in BAN_KEYS:
        if key in exempt:
            continue
        n = count_hits(CLAIM_REGEX[key], body)
        if n:
            sample = rx(CLAIM_REGEX[key]).search(body)
            rep.fail("5C", "%s: %d hit(s), must be 0 (e.g. %r)"
                     % (key, n, sample.group(0) if sample else ""))
    # widened pain-claim regex is the real M3 target
    if "dau_claim" not in exempt:
        n_wide = count_hits(DAU_CLAIM_WIDE, body)
        if n_wide:
            rep.fail("M3", "widened pain-claim regex: %d hit(s), target 0" % n_wide)
    for key, pat in BAN_EXTRA.items():
        n = count_hits(pat, body)
        if n:
            rep.fail("5C", "%s: %d hit(s), must be 0" % (key, n))


def check_antirepeat(items, rep):
    if not items:
        return
    n = float(len(items))
    for phrase in ANTIREPEAT_WATCH:
        c = sum(1 for it in items if phrase in norm(it.text))
        if not c:
            continue
        share = c / n
        if share > ANTIREPEAT_BLOCK_PER_ITEM:
            rep.fail("ANTIREP", "%r in %d/%d items (%.0f%%), block above %.0f%%"
                     % (phrase, c, len(items), share * 100,
                        ANTIREPEAT_BLOCK_PER_ITEM * 100))
        elif share > ANTIREPEAT_WARN_PER_ITEM:
            rep.warn("ANTIREP", "%r in %d/%d items (%.0f%%), warn above %.0f%%"
                     % (phrase, c, len(items), share * 100,
                        ANTIREPEAT_WARN_PER_ITEM * 100))


def run_check(text, mode=None, fees_path=None, label="<stdin>", require_policy=True):
    rep = Report()
    mode = detect_mode(text, mode)
    items = parse_items(text)
    print("check: %s" % label)
    print("  mode=%s items=%d policy=%s" % (mode, len(items), POLICY_VERSION))
    if not items:
        rep.warn("PARSE", "no numbered items found; falling back to whole-text checks")

    if require_policy and OPEN_SLOTS:
        rep.warn("POLICY", "open policy slot(s): %s. Fee-tier reporting for those "
                           "paths falls back to hotline." % ", ".join(OPEN_SLOTS))

    check_m2(items or [Item(0, None, text, 1)], rep)
    check_footer(text, items or [Item(0, None, text, 1)], rep, fees_path)
    check_quota_10_10(mode, items, rep)
    check_bans(mode, text, items, rep)
    check_antirepeat(items, rep)

    rc = rep.emit()
    print("  => %s" % ("FAIL" if rc else "PASS"))
    return rc

# ---------------------------------------------------------------------------
# selftest - fixtures, no corpus needed. These encode the brief's own examples
# plus the 4 mandatory collision cases from M1.
# ---------------------------------------------------------------------------
SELFTEST_BUCKETS = [
    # (text, expected bucket, expected free-exam allowed)
    ("cho bé đi khám ortho-k bên DND có free k ạ", "or", False),
    ("mẹ e bị đục thủy tinh thể, khám phaco bên DND free k", "pc", False),
    ("e cận 5 độ loạn 2 muốn mổ smile pro, khám 12 bước free k ạ", "kx", True),
    ("e bị lão thị, khám bên DND có mất phí k", "kx", True),
    # M1 collision case 1: lao thi + cat kinh -> GATE 2-B, lao thi wins
    ("e lão thị muốn cắt kính đọc sách, khám free k ạ", "kx", True),
    # M1 collision case 2: myopia + glasses-or-surgery question. Bucket is kx via
    # P2 generic intent, but the `cat kinh` blocker still forbids a free-exam claim
    # (brief section 97: in M2 the blocking token wins). The writer has to pick a
    # lane before quoting anything.
    ("cận nhẹ thì cắt kính hay mổ ạ, khám bên DND free k", "kx", False),
    # pure glasses, no surgical intent -> T1, no free exam
    ("e muốn đo độ cắt kính mới, khám free k ạ", "kinh", False),
    # M1 collision case 3: post-op dry eye at DND -> T-FU, free
    ("e mổ smile pro bên DND 2 tháng r, giờ khô mắt đi tái khám free k", "fu_dnd", True),
    # GATE 2-A: post-op elsewhere -> charged, and no number may be quoted
    ("e mổ ở viện khác giờ muốn qua DND tái khám, khám free k ạ", "fu_other", False),
    # fu_elsewhere gap, both directions. Service word between `mo` and the place:
    ("e mổ cận ở viện khác 2 năm trước, giờ qua DND tái khám có free k", "fu_other", False),
    # Facility prefix before a competitor name - was returning fu_dnd -> free:
    ("e mổ loạn ở bv mắt sài gòn giờ qua DND tái khám có free k", "fu_other", False),
    # ...and the tempering that keeps a DND mention inside the gap from reading as
    # elsewhere. Surgery WAS at DND, so the follow-up stays free:
    ("e mổ bên DND rồi qua viện khác khám lại, giờ về DND tái khám", "fu_dnd", True),
    # GATE 2-B follow-on: presbyopia named with the phaco path -> open slot, hotline
    ("mẹ e lão thị, bs nói mổ phaco đặt IOL đa tiêu, khám free k ạ", "kx", False),
    # presbyopia via the laser path is unambiguous T0
    ("e lão thị 50 tuổi, mổ presbyond đc k, khám 12 bước free k", "kx", True),
    # M1 collision case 4: bare condition -> hotline
    ("e bị cận, khám bên DND free k ạ", "ambiguous", False),
    ("khám võng mạc bên DND free k ạ", "khac", False),
    ("e muốn khám tổng quát mắt, có free k", "khac", False),
    ("cận nặng 18 độ giác mạc mỏng, đặt phakic ICL, khám free k ạ", "kx", True),
    ("cắt mí bên DND khám free k ạ", "khac", False),
]

# (text, claims_free_exam expected) - the disclaimer/denial boundary
SELFTEST_DENY = [
    # denials: correct messaging, must NOT count as a free claim
    ("khám phaco là gói có phí bạn nha, k thuộc gói khám free của mổ cận", False),
    ("khám Ortho-K là gói riêng có phí, khác gói khám free khúc xạ", False),
    ("gói tái khám free 3 năm là cho người mổ tại DND thôi, mổ chỗ khác thì có phí", False),
    # real claims: must still be caught
    ("bên DND khám free nha bạn", True),
    ("qua DND khám 12 bước free luôn á", True),
    # double negative: "khong mat phi" IS a free claim
    ("mình mổ bên DND nên tái khám k mất phí", True),
    # scoped to the eligible group: a statement of the rule, not a claim
    ("gói tái khám free 3 năm là cho người mổ tại DND thôi bạn nha, "
     "mổ chỗ khác thì buổi khám có phí", False),
    ("gói khám 12 bước free chỉ áp dụng cho khám mổ cận nha bạn", False),
    # a bare "chi" with no eligibility phrase must NOT count as scoping
    ("qua DND khám 12 bước free luôn á, mình chỉ đi 1 lần là chốt", True),
]

# (text, requires footer)
SELFTEST_FOOTER = [
    ("phí khám Ortho-K thì bạn gọi 0775.147.147 hỏi nha", False),
    ("phí khám cho bé tầm nhiêu ạ", False),
    ("mổ smile pro trọn gói hết bao nhiêu ạ", False),
    ("tc tầm 25tr thì mổ đc gói nào ạ", False),
    ("khám đo độ cắt kính 160.000đ nha bạn", True),
    ("SmileDays hỗ trợ đến 50% chi phí mổ cận", True),
    ("gói mổ chỉ từ 13tr/2 mắt á", True),
    ("bên DND khám mổ cận free nha", True),
]

SELFTEST_DRAFT_BAD = """# Seeding Reply-Group - DND
**Mode:** reply-group

### Kiểu 1: Trả lời từ kinh nghiệm bản thân (2 bình luận)
1. bạn qua DND Trương Định q3 khám 12 bước free luôn á, bs sẽ tư vấn cho bé Ortho-K
2. mình mổ smile pro bên DND SG, giờ 10/10 r, ko đau tí nào nha

### Kiểu 2: Gợi ý/Recommend tự nhiên (2 bình luận)
3. bên DND SG khám free nha bạn, mẹ bạn mổ phaco cũng khám free luôn
4. bên đó rẻ hơn mấy viện khác nhiều, bs giỏi nhất Sài Gòn lun
"""

SELFTEST_DRAFT_GOOD = """# Seeding Reply-Group - DND
**Mode:** reply-group

### Kiểu 1: Trả lời từ kinh nghiệm bản thân (2 bình luận)
1. case mình cx tương tự nè, cận 4.5 loạn 1.75, mổ smile pro bên DND SG, thị lực giờ ổn lắm
2. e mổ smile pro bên DND SG hồi tháng 3, khám 12 bước trước mổ free, bs tư vấn kỹ

### Kiểu 2: Gợi ý/Recommend tự nhiên (2 bình luận)
3. bạn thử qua DND Trương Định q3 khám thử xem, bs Linh khám trẻ em kỹ lắm
4. cho bé đeo Ortho-K thì bạn gọi hotline 0775.147.147 hỏi phí khám nha, mình k rõ giá

[fees: 2026-07 · T0]
"""


def run_selftest():
    print("selftest: policy=%s" % POLICY_VERSION)
    if OPEN_SLOTS:
        print("  open policy slot(s): %s" % ", ".join(OPEN_SLOTS))
    print("")
    print("A. bucket detection + item-level M2 gate")
    print("-" * 68)
    nfail = 0
    for text, exp_bucket, exp_free in SELFTEST_BUCKETS:
        bucket, tier, _reason = detect_bucket(text)
        allowed, reason = free_exam_allowed(text)
        ok = (bucket == exp_bucket and allowed == exp_free)
        if not ok:
            nfail += 1
        print("  %-4s bucket=%-9s tier=%-5s free=%-5s | %s"
              % ("ok" if ok else "FAIL", bucket, tier, allowed, text[:52]))
        if not ok:
            print("       expected bucket=%s free=%s (%s)" % (exp_bucket, exp_free, reason))

    print("")
    print("B. regex sanity - each claim family must fire on its own probe")
    print("-" * 68)
    probes = {
        "dau_claim": "mổ xong ko đau gì hết",
        "vision_absolute": "giờ 10/10 r nha",
        "vision_absolute_en": "vision is 20/20 now",
        "superlative_vn": "bs giỏi nhất Sài Gòn",
        "superlative_en": "the service was outstanding",
        "compare_other_hospital": "bên đó rẻ hơn nhiều",
        "commitment": "bv cam kết kết quả",
        "cure_myopia": "mổ là khỏi cận luôn",
        "repeat_phrase": "mổ nhẹ nhàng lắm",
    }
    for key, probe in probes.items():
        n = count_hits(CLAIM_REGEX[key], norm(probe))
        ok = n >= 1
        if not ok:
            nfail += 1
        print("  %-4s %-24s %d hit(s)  %r" % ("ok" if ok else "FAIL", key, n, probe))

    # the dau_claim decomposition from section 1 must add up
    parts = sum(count_hits(AUX_REGEX[k], norm("không đau ko đau k đau chả đau"))
                for k in ("dau_khong", "dau_ko", "dau_cha"))
    print("  %-4s %-24s decomposition probe = %d" % ("ok" if parts >= 3 else "FAIL",
                                                     "dau_claim parts", parts))

    print("")
    print("B2. disclaimer vs claim - a denial is not a violation")
    print("-" * 68)
    for text, exp in SELFTEST_DENY:
        got = claims_free_exam(text)
        ok = (got == exp)
        if not ok:
            nfail += 1
        print("  %-4s claims_free=%-5s exp=%-5s | %s"
              % ("ok" if ok else "FAIL", got, exp, text[:56]))

    print("")
    print("B3. fee assertion vs fee mention - footer required only for assertions")
    print("-" * 68)
    for text, exp in SELFTEST_FOOTER:
        got = asserts_fee(text)
        ok = (got == exp)
        if not ok:
            nfail += 1
        print("  %-4s asserts=%-5s exp=%-5s | %s"
              % ("ok" if ok else "FAIL", got, exp, text[:56]))

    print("")
    print("B4. 10/10 quota floor - first instance legal in a short run")
    print("-" * 68)
    for n_items, n_hits, exp_fail in ((4, 1, False), (20, 4, False), (20, 5, True),
                                      (6, 2, True)):
        r2 = Report()
        fake = [Item(i + 1, 1, "10/10" if i < n_hits else "x", i + 1)
                for i in range(n_items)]
        check_quota_10_10("reply-group", fake, r2)
        got_fail = bool(r2.fails)
        ok = (got_fail == exp_fail)
        if not ok:
            nfail += 1
        print("  %-4s %2d hits / %2d items -> fail=%-5s exp=%s"
              % ("ok" if ok else "FAIL", n_hits, n_items, got_fail, exp_fail))

    print("")
    print("C. draft check - known-bad draft must FAIL")
    print("-" * 68)
    rc_bad = run_check(SELFTEST_DRAFT_BAD, label="<selftest bad>", require_policy=False)
    if rc_bad == 0:
        nfail += 1
        print("  FAIL: bad draft passed the gate")

    print("")
    print("D. draft check - clean draft must PASS")
    print("-" * 68)
    rc_good = run_check(SELFTEST_DRAFT_GOOD, label="<selftest good>", require_policy=False)
    if rc_good != 0:
        nfail += 1
        print("  FAIL: clean draft was rejected")

    print("")
    if nfail:
        print("SELFTEST: FAIL (%d)" % nfail)
        return 1
    print("SELFTEST: PASS")
    return 0


DOC_BUCKET_ROW_RX = re.compile(
    r"^\|\s*`(fu_dnd|fu_other|kx|kinh|pc|or|khac|ambiguous|none)`\s*\|"
    r"[^|]*\|\s*\*{0,2}([^|*]+?)\*{0,2}\s*\|\s*([^|]*?)\s*\|\s*$")

# What the doc's "free?" column is allowed to say, mapped to a bool.
_DOC_FREE = {"✅": True, "❌": False}


def run_docsync(skill_path):
    """Parse the section-6 bucket table out of SKILL.md and diff it against POLICY.

    The table is a human-readable copy of TOK/POLICY, and copies drift. This makes
    drift a test failure instead of a wrong fee quote six weeks from now.
    """
    rows = {}
    for line in read_text(skill_path).splitlines():
        m = DOC_BUCKET_ROW_RX.match(line.strip())
        if m:
            bucket, tier, free = m.group(1), m.group(2).strip(), m.group(3).strip()
            rows[bucket] = (tier, free)
    if not rows:
        print("FAIL: no bucket table found in %s" % skill_path)
        print("      (expected rows like: | `kx` | ...tokens... | **T0** | ✅ |)")
        return 2

    expected = dict(POLICY["buckets"])
    expected["fu_other"] = POLICY["fu_other_hospital_tier"]
    for k in ("ambiguous", "none"):
        expected[k] = "HOTLINE"

    problems = []
    print("doc-sync: %d bucket row(s) in %s" % (len(rows), os.path.basename(skill_path)))
    for bucket in sorted(expected):
        if bucket not in rows:
            problems.append("%s: missing from doc table" % bucket)
            continue
        doc_tier, doc_free = rows[bucket]
        want_tier = expected[bucket]
        # doc writes hotline as the word; POLICY writes it as HOTLINE
        norm = doc_tier.lower().replace("*", "").strip()
        tier_ok = (norm == "hotline") if want_tier == "HOTLINE" else (doc_tier == want_tier)

        want_free = want_tier in POLICY["free_exam_tiers"]
        got_free = None
        for glyph, val in _DOC_FREE.items():
            if glyph in doc_free:
                got_free = val
                break
        free_ok = (got_free == want_free)

        if not tier_ok:
            problems.append("%s: doc tier %r, POLICY %r" % (bucket, doc_tier, want_tier))
        if not free_ok:
            problems.append("%s: doc free %r, POLICY says %s"
                            % (bucket, doc_free or "(blank)", want_free))
        print("  %-4s %-10s tier %-8s free %s"
              % ("ok" if (tier_ok and free_ok) else "FAIL", bucket, doc_tier, doc_free or "-"))

    extra = sorted(set(rows) - set(expected))
    for bucket in extra:
        problems.append("%s: in doc table but not in POLICY" % bucket)

    print("")
    if problems:
        for p in problems:
            print("  drift: %s" % p)
        print("")
        print("DOCSYNC: FAIL")
        return 1
    print("DOCSYNC: PASS - doc table matches POLICY on all %d buckets" % len(expected))
    return 0


def run_heldout(path):
    """M1: score bucket detection against the held-out labelled set."""
    rows = []
    for raw in read_text(path).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) < 4:
            print("FAIL: malformed row (needs 4 tab-separated fields): %r" % raw[:60])
            return 2
        text, bucket, free, source = (p.strip() for p in parts[:4])
        rows.append((text, bucket, free.lower() == "true", source))
    if not rows:
        print("FAIL: no cases in %s" % path)
        return 2

    print("held-out set: %d case(s) from %s" % (len(rows), os.path.basename(path)))
    by_source = {}
    for _t, _b, _f, s in rows:
        by_source[s] = by_source.get(s, 0) + 1
    print("  sources: %s" % ", ".join("%s=%d" % kv for kv in sorted(by_source.items())))
    print("")

    n_bucket_ok = n_free_ok = 0
    wrong = []
    for text, exp_bucket, exp_free, source in rows:
        got_bucket, tier, _reason = detect_bucket(text)
        got_free, why = free_exam_allowed(text)
        b_ok, f_ok = (got_bucket == exp_bucket), (got_free == exp_free)
        n_bucket_ok += int(b_ok)
        n_free_ok += int(f_ok)
        if not (b_ok and f_ok):
            wrong.append((text, exp_bucket, got_bucket, exp_free, got_free, why, source))
        print("  %-4s %-9s %-9s free %-5s %-5s %-9s %s"
              % ("ok" if (b_ok and f_ok) else "FAIL",
                 exp_bucket, got_bucket, exp_free, got_free, source, text[:44]))

    n = len(rows)
    print("")
    print("bucket accuracy    %d/%d" % (n_bucket_ok, n))
    print("free-gate accuracy %d/%d" % (n_free_ok, n))
    if wrong:
        print("")
        print("misses:")
        for text, eb, gb, ef, gf, why, source in wrong:
            print("  [%s] %s" % (source, text))
            print("      bucket expected %s got %s | free expected %s got %s (%s)"
                  % (eb, gb, ef, gf, why))
        print("")
        print("M1: FAIL")
        return 1
    print("")
    print("M1: PASS - all %d cases correct on both bucket and free-gate" % n)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="qa_seeding.py",
        description="QA gate for the dnd-seeding skill (brief v4).")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--baseline", metavar="DIR",
                   help="recompute pinned claim counts over a corpus of seeding_*.md")
    g.add_argument("--check", metavar="FILE", nargs="?", const="-",
                   help="check a draft; omit FILE or pass - to read stdin")
    g.add_argument("--selftest", action="store_true", help="run built-in fixtures")
    g.add_argument("--heldout", metavar="FILE",
                   help="score bucket detection against a labelled held-out set (M1)")
    g.add_argument("--docsync", metavar="SKILL_MD", nargs="?", const="SKILL.md",
                   help="check the section-6 bucket table in SKILL.md against POLICY")
    ap.add_argument("--mode", help="force mode instead of detecting it")
    ap.add_argument("--fees", help="path to fees-promos.md for footer layer (b)")
    args = ap.parse_args(argv)

    if args.selftest:
        return run_selftest()
    if args.heldout:
        if not os.path.exists(args.heldout):
            print("FAIL: no such file %s" % args.heldout)
            return 2
        return run_heldout(args.heldout)
    if args.docsync:
        if not os.path.exists(args.docsync):
            print("FAIL: no such file %s" % args.docsync)
            return 2
        return run_docsync(args.docsync)
    if args.baseline:
        return run_baseline(args.baseline)
    src = args.check
    if src in (None, "-"):
        return run_check(sys.stdin.read(), args.mode, args.fees, "<stdin>")
    if not os.path.exists(src):
        print("FAIL: no such file %s" % src)
        return 2
    return run_check(read_text(src), args.mode, args.fees, src)


if __name__ == "__main__":
    sys.exit(main())




