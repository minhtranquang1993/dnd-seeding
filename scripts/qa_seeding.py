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
    # GATE 3, ANSWERED 2026-07-27: presbyopia is treated via Presbyond (laser,
    # clearly T0) OR Phaco + multifocal IOL. Phaco is a T2 blocker. The user chose
    # to keep this path on the hotline rather than assign it a tier - there is no
    # priced policy for it, and inventing one is what :55 did.
    # This is now a DECISION, not an open slot: the behaviour is identical but the
    # POLICY warning is gone, so a future reader does not treat a settled routing
    # rule as an unfinished one.
    "lao_thi_phaco_path_tier": "HOTLINE",   # was None (open) until GATE 3
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


# The hospital's own phone numbers share the digit-group shape of a price
# (0775.147.147 vs 1.000.000) and sit next to fee words in exactly the drafts
# that correctly refuse to quote a price ("phí khám thì bạn gọi 0775.147.147").
# Blanking them before any money matching keeps a correct deflection from
# reading as a fee assertion.
PHONE_RX = re.compile(r"\b0775[.\s-]?147[.\s-]?147\b"
                      r"|\b1900[.\s-]?8195\b"
                      r"|\b0[0-9]{2,3}[.\s-]?[0-9]{3}[.\s-]?[0-9]{3,4}\b")


def strip_phones(s):
    return PHONE_RX.sub(" <phone> ", s)


def norm_money(s):
    """norm() with phone numbers blanked, for money/fee matching only."""
    return strip_phones(norm(s))

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
# ZERO_D: "0đ" must not be allowed to match the tail of a real price.
# "160.000đ" ends in "0đ", so a bare `0đ` alternative made claims_free_exam()
# true for a CORRECT T1/T2 price quote, and M2 then failed the draft with
# "free-exam claim not allowed". That is the exact false positive the docstring
# on claims_free_exam warns about - a gate that punishes correct fee reporting
# teaches writers to say nothing about fees, which is how :55 lasted 13 months.
ZERO_D = r"(?<![0-9.,])0 *đ"
FREE_EXAM_RX = (r"khám.{0,30}(free|miễn phí|" + ZERO_D + r"|miễn phi)"
                r"|(free|miễn phí|" + ZERO_D + r").{0,30}khám"
                r"|khám 12 bước (free|miễn phí)"
                r"|tặng gói khám"
                r"|gói khám.{0,20}(free|miễn phí|" + ZERO_D + r")"
                # the free 12-step package is the only thing this skill quotes a
                # "trị giá" for; kept generic so a price change cannot silently
                # disable the detector, and scoped to khám so surgery-package
                # values do not read as a free-exam claim
                r"|(gói khám|khám)[^.\n]{0,25}trị giá[^.\n]{0,12}[0-9]"
                r"|trị giá[^.\n]{0,12}[0-9][^.\n]{0,25}(gói khám|khám)"
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
# NOTE: no literal tier amount belongs in this file. An earlier revision listed
# 160.000|350.000|80.000|175.000 here, which made the script a THIRD copy of the
# fee table (SKILL.md + fees-promos.md + here) - the same duplication bug step 6
# exists to remove. The pattern below matches the SHAPE of a Vietnamese money
# token; which amounts are legitimate is decided by FeesTable, parsed from
# fees-promos.md at runtime.
FEE_NUMBER_RX = (r"trị giá[^.\n]{0,12}[0-9][0-9\.,]*"
                 # bare digit groups must carry a currency mark. Without the
                 # mark this alternative also matched the hotline number
                 # (0775.147.147 has the same digit-group shape), so a draft
                 # that correctly deflected to the hotline read as asserting a
                 # fee and demanded a footer.
                 + r"|\b[0-9]{1,3}(?:\.[0-9]{3})+ *(?:đ|đồng)\b"
                 # ... and a bare group is still a price when a fee word is
                 # adjacent, which is how the table amounts appear in prose
                 + r"|(giá|phí|chi phí|hết|trọn gói|chỉ từ|còn|giảm|khám)"
                 r"[^.\n]{0,20}[0-9]{1,3}(?:\.[0-9]{3})+"
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

# Footer accepts one or more tier ids: [fees: 2026-07 · T0] or [... · T0, T2].
# PROMO covers a run that quotes only surgery-promo numbers (fees-promos.md S3)
# and no exam tier. hotline is accepted so a deflection run can still stamp.
FOOTER_TIER_IDS = ("T-FU", "T0", "T1", "T2", "PROMO", "hotline")
FOOTER_RX = (r"\[fees:\s*([0-9]{4}-[0-9]{2}(?:-[0-9]{2})?)\s*·\s*"
             r"((?:T-FU|T0|T1|T2|PROMO|hotline)"
             r"(?:\s*,\s*(?:T-FU|T0|T1|T2|PROMO|hotline))*)\s*\]")

# Any money-shaped token, used to pull the legitimate amounts out of
# fees-promos.md and to pull the claimed amounts out of a draft. Digit groups
# ("350.000", "1.000.000") and short forms ("13tr", "3tr", "50%").
MONEY_TOKEN_RX = re.compile(
    r"[0-9]{1,3}(?:\.[0-9]{3})+"          # 350.000 / 1.000.000
    r"|[0-9]+ *(?:tr|triệu|k|nghìn|ngàn)\b"  # 13tr / 3 triệu
    r"|[0-9]+ *%",                          # 50%
    re.IGNORECASE)


def _money_key(tok):
    """Normalise a money token so draft and table forms compare equal.

    '3.000.000' and '3tr' are the same amount written two ways; a check that
    only did string equality would pass '3tr' against a table holding
    '3.000.000' by accident of absence, not by agreement.
    """
    t = norm(tok).replace(" ", "")
    m = re.match(r"^([0-9]+)(tr|triệu)$", t)
    if m:
        return str(int(m.group(1)) * 1000000)
    m = re.match(r"^([0-9]+)(k|nghìn|ngàn)$", t)
    if m:
        return str(int(m.group(1)) * 1000)
    if re.match(r"^[0-9]+%$", t):
        return t
    return t.replace(".", "").rstrip("đ")


class FeesTable(object):
    """The fee numbers, parsed from fees-promos.md at runtime.

    This class is why layer (b) can catch 'read the file and still said it
    wrong'. It holds no amount of its own - delete fees-promos.md and every
    cross-check below degrades to a warning rather than silently passing.
    """

    def __init__(self, path):
        self.path = path
        self.text = read_text(path)
        self.updated = self._parse_updated()
        self.tier_amounts = {}   # tier id -> set of normalised amount keys
        self.tier_free = {}      # tier id -> bool, may this tier say "free"
        self.promo_amounts = set()
        self._parse_tiers()
        self._parse_promos()

    def _parse_updated(self):
        m = re.search(r"^updated:\s*([0-9]{4}-[0-9]{2}(?:-[0-9]{2})?)",
                      self.text, re.MULTILINE)
        if m:
            return m.group(1)
        m = re.search(r"(?:cập nhật|updated)\D{0,12}([0-9]{4}-[0-9]{2}(?:-[0-9]{2})?)",
                      self.text, re.IGNORECASE)
        return m.group(1) if m else None

    def _rows(self):
        for line in self.text.splitlines():
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and not set(cells[0]) <= set("-: *"):
                yield cells

    def _parse_tiers(self):
        for cells in self._rows():
            tid = cells[0].strip("* `")
            if tid not in FOOTER_TIER_IDS:
                continue
            row = " ".join(cells[1:])
            amounts = set(_money_key(t) for t in MONEY_TOKEN_RX.findall(row))
            self.tier_amounts.setdefault(tid, set()).update(amounts)
            if "✅" in row:
                self.tier_free[tid] = True
            elif "❌" in row and tid not in self.tier_free:
                self.tier_free[tid] = False

    def _parse_promos(self):
        """Amounts from the surgery-promo section (S3), keyed under PROMO."""
        m = re.search(r"^##\s*3\..*?$(.*?)(?=^##\s|\Z)", self.text,
                      re.MULTILINE | re.DOTALL)
        body = m.group(1) if m else ""
        self.promo_amounts = set(_money_key(t) for t in MONEY_TOKEN_RX.findall(body))
        self.tier_amounts.setdefault("PROMO", set()).update(self.promo_amounts)

    def allowed_amounts(self, tiers):
        out = set()
        for t in tiers:
            out |= self.tier_amounts.get(t, set())
        return out

    def any_free_tier(self, tiers):
        return any(self.tier_free.get(t, False) for t in tiers)

    def known_tiers(self):
        return sorted(k for k in self.tier_amounts if k in FOOTER_TIER_IDS)

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
    # 5B is a PER-COLUMN exemption, not a blanket one. maps/maps_foreigner are
    # NOT exempt from 10/10 (brief 5B measured 0 hits in both - the need is
    # absent, so the exemption was never earned). Without these rows the mode
    # fell through to "no quota row" and a full-length maps run carrying 10/10
    # printed PASS - ISSUE-5's exact shape: a guardrail reporting pass for
    # something it never inspected.
    "maps":            {"allowed": set(), "max_ratio": 0.0},
    "maps_foreigner":  {"allowed": set(), "max_ratio": 0.0},
    # koc IS exempt from 10/10 (5 measured hits, exemption earned). Stated as an
    # explicit decision rather than left as a missing key, so the next reader can
    # tell "exempt on purpose" from "forgot to add".
    "koc":             {"exempt": True},
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
# vision_absolute_en ("20/20") belongs here, not in the quota path: brief 5B
# exempts it for maps_foreigner ONLY (1 measured hit there), so everywhere else
# it is a flat ban. It was in neither BAN_KEYS nor BAN_EXTRA, which left "vision
# is 20/20 now" passing in every mode - including the four it is banned in.
# vision_absolute ("10/10") stays OUT of this tuple on purpose: it is
# quota-limited per mode by check_quota_10_10, not banned outright.
BAN_KEYS = ("dau_claim", "superlative_vn", "superlative_en", "commitment",
            "cure_myopia", "compare_other_hospital", "vision_absolute_en")
BAN_EXTRA = {
    "cure_forever": r"khỏi cận vĩnh viễn|hết cận vĩnh viễn",
    "everyone_eligible": r"ai (cũng|cx) mổ đượ?c|ai (cũng|cx) mổ đc",
}

# 7 - anti-repeat. Baseline: `nhe nhang` ~1.3 hits/file (281 over 217).
# The 8 replacement phrases are watched too: swapping one fingerprint for another
# solves nothing, so they enter the list the moment they enter the skill (5C).
ANTIREPEAT_WATCH = ("nhẹ nhàng", "ổn áp", "10/10", "nhanh gọn", "máy xịn",
                    "êm ru", "nhẹ tênh", "ngọt xớt",
                    "dễ chịu hơn", "đỡ hơn", "k căng như", "nhanh hơn",
                    "lúc nào k hay", "bớt áp lực", "thoải mái hơn",
                    "đơn giản hơn")
ANTIREPEAT_WARN_PER_ITEM = 0.15   # warn above this share of items
ANTIREPEAT_BLOCK_PER_ITEM = 0.30  # block above this share

# M5 - the 5 new reply-group angles. Verify on OUTPUT: each new angle needs >=1
# item, and the mixed angle must really carry a dissatisfaction point rather than
# praise in disguise.
NEW_REPLY_SECTIONS = {6: "mixed review", 7: "hỏi lại, không nhắc DND",
                      8: "đính chính", 9: "quy trình/hậu cần",
                      10: "đang cân nhắc"}
MIXED_SECTION = 6
# a mixed item must hit one of these to count as carrying a real downside
DISSATISFACTION_RX = (r"chờ (hơi )?lâu|đông|khô mắt|hơi phiền|bất tiện|đi xa|"
                      r"xa quá|cao hơn (dự tính|mình nghĩ|e nghĩ)|đắt hơn|"
                      r"quên hỏi|phải gọi lại|mất (khá nhiều|nhiều) t(g|hời gian)|"
                      r"nhiều bước|hơi rắc rối|k thích|chưa hài lòng|điểm trừ")
# angles that must not name the brand (7 exists to make the thread look real)
NO_BRAND_SECTIONS = {7}
BRAND_RX = r"\bDND\b|Trương Định"
# angles barred from carrying 10/10 regardless of the mode quota
NO_SCORE_SECTIONS = {6, 7, 8, 9, 10}
# reply-group ships ~20 items; below this a draft is a fragment, so missing
# angles are reported as a note instead of a failure.
M5_FULL_RUN_MIN_ITEMS = 10

# Kiểu 8 exists to correct a false belief, and correcting one means naming it
# ("mổ khúc xạ chỉnh độ hiện tại thôi chứ k phải khỏi cận mãi mãi"). Same
# principle as DENY_FREE_RX for M2: the gate must not punish a refutation for
# quoting what it refutes.
#
# Deliberately narrow:
#   - only the "cure" families. dau_claim is itself phrased as a negation, so a
#     refutation marker there would just be a double negative, and the
#     superlative/compare families have no legitimate refuting form in seeding.
#   - the marker must sit IMMEDIATELY before the token (<=12 chars), not merely
#     nearby. A wide window would let "k phải lo j" 80 chars away excuse a real
#     claim further down the same item.
REFUTABLE_BANS = ("cure_myopia", "cure_forever")
REFUTE_RX = r"(kh?ông|ko|k|chẳng|chưa) *phải[^.\n]{0,12}$|chứ +(kh?ông|ko|k)[^.\n]{0,12}$"

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


# ---------------------------------------------------------------------------
# Command routing (brief section 6). detect_mode() above reads the mode off a
# finished DRAFT; this reads it off the COMMAND LINE, which is a different job
# with a different failure mode: a mode name that happens to appear inside the
# user's quoted question must not steal the routing.
# ---------------------------------------------------------------------------
COMMAND_PREFIX_RX = re.compile(r"^\s*/?(?:dnd-seeding|seeding-dnd)\b", re.IGNORECASE)

# Longest-first so `reply-group` wins over `group`, `maps_foreigner` over `maps`.
COMMAND_MODES = ("maps_foreigner", "reply-group", "reply_group", "google_maps",
                 "maps", "koc", "group", "story", "ads", "live")

DEFAULT_MODE = "group"

# A quoted question or a parenthesised live payload ends the mode-token region.
PAYLOAD_START_RX = re.compile(r"[\"“”'(]")
PARAM_RX = re.compile(r"^([a-z_]+)=(.*)$", re.IGNORECASE)


def parse_command(raw):
    """Route a command line to (mode, params, payload).

    Rules from brief section 6:
      - a mode token is recognised ONLY at the first token position, and only
        before any quoted string. `reply-group "chi nao review maps cho e"` is
        reply-group; the word `maps` inside the quotes is the user's text.
      - `service=` (and any k=v) is always a param, never a mode.
      - `group story` collapses to the story sub-mode.
      - no mode token at all -> DEFAULT_MODE.
    """
    s = COMMAND_PREFIX_RX.sub("", raw or "", count=1)

    cut = PAYLOAD_START_RX.search(s)
    head = s[:cut.start()] if cut else s
    payload = s[cut.start():].strip() if cut else ""

    params, tokens = {}, []
    for tok in head.split():
        pm = PARAM_RX.match(tok)
        if pm:
            params[pm.group(1).lower()] = pm.group(2)
        else:
            tokens.append(tok.lower().strip(",;"))

    mode = DEFAULT_MODE
    if tokens:
        first = tokens[0]
        matched = None
        for cand in COMMAND_MODES:
            if first == cand:
                matched = cand
                break
        if matched == "google_maps":
            matched = "maps"
        if matched:
            mode = matched
            # `group story` -> story. Only in this order and only adjacent.
            if matched == "group" and len(tokens) > 1 and tokens[1] == "story":
                mode = "story"
        # an unrecognised first token is NOT a mode; it stays part of the request
        # and routing falls back to the default rather than guessing.

    if payload:
        payload = payload.strip("\"“”'()").strip()
    return (mode, params, payload)


def parse_items(text):
    """Split a draft into numbered items, attributed to the section above them.

    Continuation lines (a wrapped story paragraph) attach to the current item so
    a claim on line 2 of an item is still that item's claim. A blank line ends
    the item, so trailing prose is not attributed to it.
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
        if not raw.strip():
            # A blank line closes the item. Without this, trailing prose (footer,
            # notes) is appended to the LAST item and would be judged by the
            # item-level M2 gate as if the item itself had said it.
            current = None
            continue
        if current is not None:
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

    # GATE 3: presbyopia named together with the phaco path has no priced policy,
    # so it gets its own bucket that routes to the hotline instead of inheriting
    # T0 from `kx`. Checked BEFORE the kx branch because `lão thị` is itself a kx
    # token - the ordering is the whole mechanism. Previously this case was only
    # handled in free_exam_allowed(), which left detect_bucket() reporting kx/T0
    # for it and hid the row from --docsync.
    if rx(AUX_REGEX["lao_thi"]).search(t) and has("pc"):
        lt_tier = POLICY["lao_thi_phaco_path_tier"]
        if lt_tier in (None, "HOTLINE"):
            return ("lt_phaco", None, "GATE 3 presbyopia via phaco path -> hotline")
        return ("lt_phaco", lt_tier, "GATE 3 presbyopia via phaco path")

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
    if (has_lao_thi and "pc" in blockers
            and POLICY["lao_thi_phaco_path_tier"] in (None, "HOTLINE")):
        return (False, "presbyopia via phaco path: no priced policy (GATE 3) -> hotline")

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
    return bool(rx(FEE_NUMBER_RX).search(norm_money(text)))


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


FEES_FILENAME = "fees-promos.md"


def default_fees_path():
    """Locate fees-promos.md without being told where it is.

    Layer (b) only runs when it has the file. Requiring an explicit --fees means
    the common invocation silently degrades to layer (a) - which is the
    partial-load hole this whole mechanism exists to close. So: look next to the
    script, then one level up (scripts/ -> skill root), then cwd.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(here, FEES_FILENAME),
                 os.path.join(os.path.dirname(here), FEES_FILENAME),
                 os.path.join(os.getcwd(), FEES_FILENAME)):
        if os.path.exists(cand):
            return cand
    return None


def draft_amounts(items):
    """Money tokens from items that ASSERT fees, with the item they came from.

    Scoped to asserting items on purpose. A persona line like "tc tầm 25tr" is a
    budget, not a hospital price, and cross-checking it against the tier table
    would fail an innocent draft - a check that cries wolf gets turned off.
    """
    out = []
    num_rx = rx(FEE_NUMBER_RX)
    for it in items:
        if not asserts_fee(it.text):
            continue
        t = norm_money(it.text)
        for m in num_rx.finditer(t):
            for tok in MONEY_TOKEN_RX.findall(m.group(0)):
                out.append((_money_key(tok), tok, it))
    return out


def check_footer(text, items, rep, fees_path=None):
    """Section 6 two-layer footer check, runs whenever fee info is present.

    (a) fee info present but no footer -> fail.
    (b) footer present -> read fees-promos.md and reconcile the draft's amounts
        and free-claims against the tier the footer declares. Layer (b) is the
        one that catches a run which DID open the file and still said it wrong;
        a read-receipt alone cannot.
    """
    info_rx = rx(FEE_INFO_RX)
    fee_items = [it for it in items if asserts_fee(it.text)]
    mention_only = [it for it in items
                    if info_rx.search(norm_money(it.text)) and it not in fee_items]
    m = re.search(FOOTER_RX, text)
    if not fee_items:
        if mention_only:
            rep.note("footer: %d item(s) mention fees without asserting a number "
                     "(question / hotline deflection), footer not required"
                     % len(mention_only))
        else:
            rep.note("footer: no fee information in draft, footer not required")
        if m:
            rep.warn("FOOTER-A", "footer present but no item asserts fee information")
        return
    if not m:
        rep.fail("FOOTER-A", "draft asserts fee information (%d item(s)) but has no "
                             "[fees: <date> · <tier>] footer:\n      %s"
                 % (len(fee_items), fee_items[0].text[:100]))
        return
    fdate = m.group(1)
    tiers = [t.strip() for t in m.group(2).split(",")]
    rep.note("footer: [fees: %s · %s] over %d fee item(s)"
             % (fdate, ", ".join(tiers), len(fee_items)))

    if not fees_path:
        rep.warn("FOOTER-B", "no --fees given, layer (b) skipped - footer date and "
                             "amounts unverified")
        return
    if not os.path.exists(fees_path):
        rep.warn("FOOTER-B", "fees file not found at %s, layer (b) skipped" % fees_path)
        return

    try:
        ft = FeesTable(fees_path)
    except (IOError, OSError) as exc:
        rep.warn("FOOTER-B", "cannot read %s (%s), layer (b) skipped" % (fees_path, exc))
        return

    base = os.path.basename(fees_path)
    if ft.updated and not fdate.startswith(ft.updated[:7]):
        rep.fail("FOOTER-B", "footer date %s does not match %s (%s)"
                 % (fdate, ft.updated, base))
    elif not ft.updated:
        rep.warn("FOOTER-B", "no updated: date found in %s, date check skipped" % base)

    unknown = [t for t in tiers if t not in ft.known_tiers()]
    if unknown:
        rep.fail("FOOTER-B", "tier(s) %s not found in %s (known: %s)"
                 % (", ".join(unknown), base, ", ".join(ft.known_tiers())))
        return

    # free-claim vs declared tier
    free_items = [it for it in fee_items if claims_free_exam(it.text)]
    if free_items and not ft.any_free_tier(tiers):
        rep.fail("FOOTER-B", "draft claims a free exam but declared tier(s) %s are "
                             "not free-eligible per %s:\n      %s"
                 % (", ".join(tiers), base, free_items[0].text[:110]))

    # amounts vs declared tier
    allowed = ft.allowed_amounts(tiers)
    if allowed:
        seen = set()
        for key, tok, it in draft_amounts(items):
            if key in allowed or key in seen:
                continue
            seen.add(key)
            rep.fail("FOOTER-B", "amount %r (line %d) is not listed under tier(s) %s "
                                 "in %s:\n      %s"
                     % (tok, it.line, ", ".join(tiers), base, it.text[:110]))
    else:
        rep.note("footer: tier(s) %s carry no amount in %s (deflection tier), "
                 "amount cross-check not applicable" % (", ".join(tiers), base))


def check_quota_10_10(mode, items, rep):
    cfg = QUOTA_10_10.get(mode)
    if cfg is None:
        # An unknown mode used to get a NOTE, which reads as "checked, fine" in a
        # PASS report. It is not checked at all, so it is a WARN.
        rep.warn("5A", "mode %r has no quota row - 10/10 was NOT checked for this "
                       "mode. Add a row to QUOTA_10_10 (or mark it exempt)." % mode)
        return
    if cfg.get("exempt"):
        n_hits = sum(1 for it in items if "10/10" in it.text)
        rep.note("5A: mode %s is exempt from the 10/10 quota per 5B (%d hit(s), "
                 "not gated)" % (mode, n_hits))
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


def check_new_angles(mode, items, rep):
    """M5 - the 5 new reply-group angles, verified on OUTPUT.

    Coverage (every new angle >=1 item) only *fails* on a full-length run. A
    short draft or fixture legitimately carries a couple of angles, and failing
    those would make the gate untrustworthy for the case it was built for.
    Per-item rules below apply whenever the angle is present, at any run length.
    """
    if mode != "reply-group":
        return
    by_section = {}
    for it in items:
        by_section.setdefault(it.section, []).append(it)

    present = sorted(s for s in NEW_REPLY_SECTIONS if by_section.get(s))
    missing = [s for s in NEW_REPLY_SECTIONS if not by_section.get(s)]
    full_run = len(items) >= M5_FULL_RUN_MIN_ITEMS
    if missing:
        msg = ("new angles missing: %s (present: %s)"
               % (", ".join("Kiểu %d (%s)" % (s, NEW_REPLY_SECTIONS[s]) for s in missing),
                  ", ".join("Kiểu %d" % s for s in present) or "none"))
        if full_run:
            rep.fail("M5", msg)
        else:
            rep.note("M5: %s -- not failed, draft has %d item(s) (< %d, not a full run)"
                     % (msg, len(items), M5_FULL_RUN_MIN_ITEMS))
    else:
        rep.note("M5: all 5 new angles present (Kiểu %s)"
                 % ", ".join(str(s) for s in present))

    # the mixed angle must carry a real downside, not praise in disguise
    for it in by_section.get(MIXED_SECTION, []):
        if not rx(DISSATISFACTION_RX).search(norm(it.text)):
            rep.fail("M5", "item %s (line %d) is in Kiểu %d (mixed) but carries no "
                           "dissatisfaction point" % (it.number, it.line, MIXED_SECTION))

    for sec in sorted(NO_BRAND_SECTIONS):
        for it in by_section.get(sec, []):
            m = rx(BRAND_RX).search(it.text)
            if m:
                rep.fail("M5", "item %s (line %d) is in Kiểu %d, which must not name the "
                               "brand (found %r)" % (it.number, it.line, sec, m.group(0)))

    for sec in sorted(NO_SCORE_SECTIONS):
        for it in by_section.get(sec, []):
            if "10/10" in it.text:
                rep.fail("M5", "item %s (line %d): 10/10 in Kiểu %d, reserved for Kiểu 1"
                         % (it.number, it.line, sec))


def count_unrefuted(key, pattern, text):
    """Count ban hits, skipping ones a refutation marker directly precedes.

    Returns (count, first_sample). Only REFUTABLE_BANS get the exemption; every
    other family counts every hit.
    """
    hits = list(rx(pattern).finditer(text))
    if key not in REFUTABLE_BANS:
        return len(hits), (hits[0].group(0) if hits else None)
    kept = [m for m in hits if not rx(REFUTE_RX).search(text[:m.start()])]
    return len(kept), (kept[0].group(0) if kept else None)


def check_bans(mode, text, items, rep):
    exempt = EXEMPT.get(mode, EXEMPT_DEFAULT)
    if exempt:
        rep.note("5B: mode %r exempt from %s" % (mode, ", ".join(sorted(exempt))))
    # 5C is a FILE-level ban ("Cấm chung -> 0 hit"), so it scans the whole draft
    # rather than only parsed items. Scanning items only would let a banned
    # phrase sitting in a preamble/footer pass unchecked - a false negative,
    # which is the failure mode brief 5B calls out (a guardrail reporting
    # "pass" for something it never inspected).
    body = norm(text)
    for key in BAN_KEYS:
        if key in exempt:
            continue
        n, sample = count_unrefuted(key, CLAIM_REGEX[key], body)
        if n:
            rep.fail("5C", "%s: %d hit(s), must be 0 (e.g. %r)" % (key, n, sample or ""))
    # widened pain-claim regex is the real M3 target
    if "dau_claim" not in exempt:
        n_wide = count_hits(DAU_CLAIM_WIDE, body)
        if n_wide:
            rep.fail("M3", "widened pain-claim regex: %d hit(s), target 0" % n_wide)
    for key, pat in BAN_EXTRA.items():
        n, _ = count_unrefuted(key, pat, body)
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


def run_check(text, mode=None, fees_path=None, label="<stdin>", require_policy=True,
              rep_out=None):
    """Check one draft. rep_out, if a list, receives the Report so a caller can
    assert on WHICH gate fired - 'it failed' is not evidence the intended gate
    works."""
    rep = Report()
    if rep_out is not None:
        rep_out.append(rep)
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
    check_new_angles(mode, items, rep)
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
    # GATE 3: own bucket, not kx. Before GATE 3 was answered this asserted "kx"
    # with free=False, which passed while detect_bucket reported a tier (T0) that
    # the free gate then refused - two answers to one question.
    ("mẹ e lão thị, bs nói mổ phaco đặt IOL đa tiêu, khám free k ạ", "lt_phaco", False),
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

# Layer (b) fixtures. These are DRAFT-level: layer (b) reconciles the footer's
# declared tier against what the draft actually says, so a one-line fixture
# cannot exercise it. Each entry is (label, draft, expected FAIL code or None).
# The point of these: a run that DID open fees-promos.md and still misquoted it
# must fail. A read-receipt cannot catch that; this can.
# The 7 documented legacy commands, plus the adversarial cases from brief
# section 6. Splitting SKILL.md is only safe if every command that worked before
# still routes to the same mode after - these are that regression.
# (command, expected mode, expected payload substring or None)
SELFTEST_COMMANDS = [
    # --- the 7 legacy commands from "When to Use" ---
    ("/dnd-seeding group", "group", None),
    ("/dnd-seeding group story", "story", None),
    ("/dnd-seeding story", "story", None),
    ('/dnd-seeding reply-group "e cận 5 độ mổ smile đc k"', "reply-group",
     "e cận 5 độ mổ smile đc k"),
    ("/dnd-seeding ads", "ads", None),
    ("/dnd-seeding live (workshop bs Tuấn nói về smile pro)", "live",
     "workshop bs Tuấn nói về smile pro"),
    ("/dnd-seeding", "group", None),          # no param -> default group
    # --- adversarial: mode word inside the user's quoted question ---
    ('/dnd-seeding reply-group "chị nào review maps cho e"', "reply-group",
     "chị nào review maps cho e"),
    ('/dnd-seeding reply-group "ai đi koc bên đó chưa"', "reply-group",
     "ai đi koc bên đó chưa"),
    ('/dnd-seeding reply-group "bên đó có ads gì k"', "reply-group",
     "bên đó có ads gì k"),
    ('/dnd-seeding reply-group "live stream hôm qua ai coi"', "reply-group",
     "live stream hôm qua ai coi"),
    # --- adversarial: service= is a param, never a mode ---
    ("/dnd-seeding ads service=phaco", "ads", None),
    ("/dnd-seeding service=maps group", "group", None),
    # --- adversarial: story only collapses when adjacent and in order ---
    ("/dnd-seeding story group", "story", None),
    # --- prefix variants and bare invocation ---
    ("dnd-seeding ads", "ads", None),
    ("seeding-dnd koc", "koc", None),
    ("/dnd-seeding maps_foreigner", "maps_foreigner", None),
    ("/dnd-seeding maps", "maps", None),
    # --- unrecognised first token must not be guessed into a mode ---
    ("/dnd-seeding bịa-mode-không-tồn-tại", "group", None),
]

# Per-mode exemption fixtures (brief 5B). Each asserts WHICH gate fires, because
# "it failed" is not evidence the intended column was checked - the bug these
# replace was a maps run passing because no gate looked at 10/10 at all.
# (label, mode, item text, expected fail code or None)
SELFTEST_MODE_EXEMPT = [
    ("maps: 10/10 not exempt", "maps", "bs Tuấn khám kỹ, mắt e giờ 10/10 nha", "5A"),
    ("maps: 20/20 not exempt", "maps", "my vision is 20/20 now", "5C"),
    ("maps: superlative EN not exempt", "maps", "the service was outstanding", "5C"),
    ("maps: pain-claim exempt", "maps", "mổ xong e ko thấy đau gì", None),
    ("maps: compare exempt", "maps", "bên đây rẻ hơn viện e đi trước", None),
    ("maps_fr: 20/20 exempt", "maps_foreigner", "my vision is 20/20 now", None),
    ("maps_fr: superlative EN exempt", "maps_foreigner",
     "the service was outstanding, highly recommend", None),
    ("maps_fr: 10/10 not exempt", "maps_foreigner", "now 10/10 after surgery", "5A"),
    ("koc: 10/10 exempt", "koc", "mắt e giờ 10/10 lun nha", None),
    ("koc: pain-claim exempt", "koc", "mổ xong e chẳng thấy đau", None),
    ("koc: compare NOT exempt", "koc", "bên đây rẻ hơn viện kia nhiều", "5C"),
    ("koc: superlative VN NOT exempt", "koc", "bs giỏi nhất Sài Gòn luôn á", "5C"),
    ("group: pain-claim NOT exempt", "group", "mổ xong ko đau gì hết", "5C"),
    ("group: 20/20 NOT exempt", "group", "vision is 20/20 now", "5C"),
]

_FB_HEAD = "# Seeding Reply-Group - DND\n**Mode:** reply-group\n\n"

SELFTEST_FOOTER_B = [
    ("tier T1 + its own amount -> pass",
     _FB_HEAD + "1. khám đo độ cắt kính bên DND 160.000đ nha b\n\n"
     "[fees: 2026-07 · T1]\n", None),
    ("tier T1 declared but T2 amount quoted -> FOOTER-B",
     _FB_HEAD + "1. khám đo độ cắt kính bên DND 350.000đ nha b\n\n"
     "[fees: 2026-07 · T1]\n", "FOOTER-B"),
    ("tier T2 declared but draft claims free -> FOOTER-B",
     _FB_HEAD + "1. mẹ e khám phaco bên DND free lun á\n\n"
     "[fees: 2026-07 · T2]\n", "FOOTER-B"),
    ("tier T0 + free claim in scope -> pass",
     _FB_HEAD + "1. e mổ cận smile pro, khám 12 bước bên DND free nha\n\n"
     "[fees: 2026-07 · T0]\n", None),
    ("stale footer date -> FOOTER-B",
     _FB_HEAD + "1. khám đo độ cắt kính bên DND 160.000đ nha b\n\n"
     "[fees: 2019-01 · T1]\n", "FOOTER-B"),
    ("unknown tier id -> FOOTER-B",
     _FB_HEAD + "1. khám đo độ cắt kính bên DND 160.000đ nha b\n\n"
     "[fees: 2026-07 · T9]\n", "FOOTER-A"),
    ("fee asserted, no footer at all -> FOOTER-A",
     _FB_HEAD + "1. khám đo độ cắt kính bên DND 160.000đ nha b\n", "FOOTER-A"),
    ("promo amount under PROMO tier -> pass",
     _FB_HEAD + "1. bên DND đang hỗ trợ đến 50% chi phí mổ cận á\n\n"
     "[fees: 2026-07 · PROMO]\n", None),
    ("promo amount not in file under PROMO -> FOOTER-B",
     _FB_HEAD + "1. bên DND đang hỗ trợ đến 90% chi phí mổ cận á\n\n"
     "[fees: 2026-07 · PROMO]\n", "FOOTER-B"),
    ("persona budget is not a hospital price -> pass",
     _FB_HEAD + "1. tc e tầm 25tr, khám đo độ cắt kính 160.000đ đúng k b\n\n"
     "[fees: 2026-07 · T1]\n", None),
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

# M5 - a full-length run carrying all 10 angles. 10 items is the smallest draft
# the coverage gate treats as full, so this doubles as the boundary case.
SELFTEST_DRAFT_M5_GOOD = """# Seeding Reply-Group - DND
**Mode:** reply-group

### Kiểu 1: Trả lời từ kinh nghiệm bản thân (1 bình luận)
1. case mình cx tương tự nè, cận 4.5 loạn 1.75, mổ smile pro bên DND SG, giờ 10/10 r nha

### Kiểu 2: Gợi ý/Recommend tự nhiên (1 bình luận)
2. bạn thử qua DND Trương Định q3 khám thử xem, bs Linh khám kỹ lắm

### Kiểu 3: Bổ sung thông tin hữu ích (1 bình luận)
3. theo mình biết bên DND SG đang có smiledays giảm 50% nè bạn

### Kiểu 4: Đồng cảm + dẫn dắt (1 bình luận)
4. e cx sợ vậy nè, hôm mổ thấy dễ chịu hơn e tưởng, bs Tuấn bên DND SG khéo tay

### Kiểu 5: Tag bạn / Rủ đi cùng (1 bình luận)
5. cái này giống case đứa bạn mình mổ bên DND SG nè, để mình hỏi rồi rep lại

### Kiểu 6: Review có điểm chưa hài lòng (1 bình luận)
6. mình mổ bên DND SG, nói thật hôm khám đông nên chờ hơi lâu, về khô mắt mấy tuần
   đầu phải nhỏ thuốc liên tục hơi phiền. còn lại thì mình k tiếc

### Kiểu 7: Hỏi lại người đăng (1 bình luận)
7. bạn khám chuyên sâu chưa v, giác mạc bạn dày bn r? cùng độ mà bs tư vấn khác nhau đó

### Kiểu 8: Đính chính nhầm lẫn kỹ thuật (1 bình luận)
8. cho mình góp ý nhẹ, mổ khúc xạ là chỉnh độ hiện tại thôi chứ k phải khỏi cận mãi mãi nha, sau vẫn cần khám định kỳ

### Kiểu 9: Chi tiết quy trình/hậu cần (1 bình luận)
9. buổi khám mất gần cả buổi sáng vì nhỏ thuốc xong đợi đo lại, nên nhờ ai chở về nha

### Kiểu 10: Người đang cân nhắc, chưa mổ (1 bình luận)
10. e cx đang tìm hiểu giống bạn, tính khám thêm DND Trương Định q3 cho có cái so, chưa mổ nên chưa dám nói j

[fees: 2026-07 · T0]
"""

# Refutation boundary: a Kiểu 8 correction may name the false belief it corrects,
# but the exemption must not become a loophole. (text, should_fail_5C).
SELFTEST_REFUTE = [
    ("mổ khúc xạ chỉnh độ hiện tại thôi chứ k phải khỏi cận mãi mãi", False),
    ("cái này là chỉnh độ hiện tại nha, không phải khỏi cận vĩnh viễn đâu", False),
    ("mổ xong là khỏi cận luôn nha bạn", True),
    ("mổ smile pro xong hết cận vĩnh viễn, k cần đeo kính nữa", True),
    # marker present but attached to something else, claim stands further on
    ("k phải lo j đâu bạn, chỗ này mổ xong là khỏi cận luôn, yên tâm đi nha", True),
]

# M5 negatives - each must fail for exactly one reason.
SELFTEST_M5_BAD = [
    ("mixed angle with no downside", "M5", """**Mode:** reply-group

### Kiểu 6: Review có điểm chưa hài lòng (1 bình luận)
1. mình mổ bên DND SG, bs Tuấn mổ khéo, mọi thứ đều ổn hết, quá hài lòng lun
"""),
    ("Kiểu 7 names the brand", "M5", """**Mode:** reply-group

### Kiểu 7: Hỏi lại người đăng (1 bình luận)
1. bạn khám chưa v, giác mạc dày bn? qua DND Trương Định q3 khám thử đi
"""),
    ("10/10 in a new angle", "M5", """**Mode:** reply-group

### Kiểu 9: Chi tiết quy trình/hậu cần (1 bình luận)
1. buổi khám mất cả buổi sáng, nhờ ai chở về nha, mình mổ xong giờ 10/10 r
"""),
    ("full run missing new angles", "M5", """**Mode:** reply-group

### Kiểu 1: Trả lời từ kinh nghiệm bản thân (10 bình luận)
1. case mình cx tương tự nè, mổ smile pro bên DND SG, thị lực giờ ổn
2. e mổ hồi tháng 3, bs tư vấn kỹ lắm
3. mình mổ bên DND Trương Định, hài lòng
4. cận 5 loạn 2 mình mổ smile pro đc nha
5. e mổ xong đi làm lại sau mấy ngày
6. mình khám ở đây bs Linh tư vấn kỹ
7. e mổ smile pro thấy đỡ hơn e nghĩ
8. mình mổ tháng trước, sinh hoạt bình thường
9. e cx cận nặng mà mổ đc nha bạn
10. mình mổ bên DND SG, bs Tuấn mổ chính
"""),
]


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
    print("B3d. per-mode exemptions (5B) - scoped per column, not bundled")
    print("-" * 68)
    for label, mode, itext, exp_code in SELFTEST_MODE_EXEMPT:
        # 20 filler items so the run is full length; a short run would let
        # ANTIREP fire on the probe and mask which gate actually caught it.
        lines = ["# probe", "**Mode:** %s" % mode, "", "### Nhóm 1: review",
                 "1. %s" % itext]
        lines += ["%d. bv sạch sẽ, nhân viên hướng dẫn rõ ràng" % i
                  for i in range(2, 21)]
        draft = "\n".join(lines) + "\n"
        r4 = Report()
        items4 = parse_items(draft)
        check_quota_10_10(mode, items4, r4)
        check_bans(mode, draft, items4, r4)
        codes = sorted(set(c for c, _ in r4.fails))
        got = codes[0] if codes else None
        ok = (got == exp_code) if exp_code else (not codes)
        if not ok:
            nfail += 1
        print("  %-4s fail=%-5s exp=%-5s | %s"
              % ("ok" if ok else "FAIL", got, exp_code, label))

    print("")
    print("B3c. command routing - 7 legacy commands + adversarial cases")
    print("-" * 68)
    for cmd, exp_mode, exp_payload in SELFTEST_COMMANDS:
        got_mode, got_params, got_payload = parse_command(cmd)
        ok = (got_mode == exp_mode)
        if exp_payload is not None:
            ok = ok and (exp_payload in got_payload)
        if not ok:
            nfail += 1
        print("  %-4s mode=%-15s exp=%-15s | %s"
              % ("ok" if ok else "FAIL", got_mode, exp_mode, cmd[:44]))

    print("")
    print("B3b. footer layer (b) - draft reconciled against fees-promos.md")
    print("-" * 68)
    fees_p = default_fees_path()
    if not fees_p:
        print("  SKIP no fees-promos.md found; layer (b) fixtures cannot run")
        nfail += 1
    else:
        ft_probe = FeesTable(fees_p)
        print("  . using %s (updated=%s, tiers=%s)"
              % (os.path.basename(fees_p), ft_probe.updated,
                 ",".join(ft_probe.known_tiers())))
        for label, draft, exp_code in SELFTEST_FOOTER_B:
            r3 = Report()
            check_footer(draft, parse_items(draft), r3, fees_p)
            codes = [c for c, _ in r3.fails]
            got = codes[0] if codes else None
            ok = (got == exp_code)
            if not ok:
                nfail += 1
            print("  %-4s fail=%-9s exp=%-9s | %s"
                  % ("ok" if ok else "FAIL", got, exp_code, label))

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
    print("B5. refutation boundary - Kiểu 8 may name the belief it corrects")
    print("-" * 68)
    for text, exp_fail in SELFTEST_REFUTE:
        r3 = Report()
        check_bans("reply-group", text, [], r3)
        got_fail = any(c == "5C" for c, _ in r3.fails)
        ok = (got_fail == exp_fail)
        if not ok:
            nfail += 1
        print("  %-4s 5C fail=%-5s exp=%-5s %s"
              % ("ok" if ok else "FAIL", got_fail, exp_fail, text[:52]))

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
    print("E. M5 - full 10-angle run must PASS")
    print("-" * 68)
    rc_m5 = run_check(SELFTEST_DRAFT_M5_GOOD, label="<selftest m5 good>",
                      require_policy=False)
    if rc_m5 != 0:
        nfail += 1
        print("  FAIL: full 10-angle run was rejected")

    print("")
    print("F. M5 negatives - each must fail ON THE M5 GATE, not incidentally")
    print("-" * 68)
    for label, want_code, body in SELFTEST_M5_BAD:
        box = []
        rc = run_check(body, label="<m5: %s>" % label, require_policy=False, rep_out=box)
        codes = set(c for c, _ in box[0].fails) if box else set()
        ok = rc != 0 and want_code in codes
        if not ok:
            nfail += 1
        print("  %-4s %-32s rc=%d codes=%s (want %s)"
              % ("ok" if ok else "FAIL", label, rc,
                 ",".join(sorted(codes)) or "none", want_code))

    print("")
    if nfail:
        print("SELFTEST: FAIL (%d)" % nfail)
        return 1
    print("SELFTEST: PASS")
    return 0


# Any `backticked_key` row, NOT a fixed list of the nine buckets. With a
# hardcoded alternation, adding a tenth row to the doc table (lt_phaco) meant the
# row silently failed to parse and never reached the "in doc but not in POLICY"
# check - docsync printed PASS over a table it had only half read.
DOC_BUCKET_ROW_RX = re.compile(
    r"^\|\s*`([a-z_]+)`\s*\|"
    r"[^|]*\|\s*\*{0,2}([^|*]+?)\*{0,2}\s*\|\s*([^|]*?)\s*\|\s*$")

# The bucket table is identified by its header, so rows of other 4-column tables
# in SKILL.md cannot be mistaken for bucket rows.
DOC_BUCKET_HEADER_RX = re.compile(r"^\|\s*(promo-key|Nhóm)\s*\|.*fee-tier-id|^\|\s*promo-key\s*\|",
                                  re.IGNORECASE)

# What the doc's "free?" column is allowed to say, mapped to a bool.
_DOC_FREE = {"✅": True, "❌": False}


# --- 7B exemption table sync -------------------------------------------------
# The 7B table in SKILL.md is a hand-written copy of EXEMPT + QUOTA_10_10, and
# ISSUE-5 in the brief WAS a drift of exactly this kind: the doc said maps/koc
# were not exempt from superlatives while the pinned regex only covered
# Vietnamese, so maps_foreigner scored 0 hits over 8 real English superlatives.
# A copy nobody diffs is how that happens twice.
DOC_EXEMPT_LABELS = {
    "pain-claim": ("dau_claim",),
    "so sánh viện": ("compare_other_hospital",),
    "10/10": ("vision_absolute",),
    "20/20": ("vision_absolute_en",),
    "superlative en": ("superlative_en",),
    "superlative vn": ("superlative_vn",),
    "superlative": ("superlative_vn", "superlative_en"),
}
# Not claim families - a prose pointer at the Tone section, nothing to diff.
DOC_EXEMPT_IGNORE = ("tone chung",)

DOC_EXEMPT_ROW_RX = re.compile(
    r"^\|\s*`(maps|maps_foreigner|koc)`\s*\|([^|]*)\|([^|]*)\|\s*$")

# 7A (the 10/10 quota table) and 7B (the exemption table) both have three columns
# and both now have maps/maps_foreigner/koc rows, so the row regex alone matches
# the wrong table. Anchor on 7B's own header.
DOC_EXEMPT_HEADER_RX = re.compile(r"^\|\s*Mode\s*\|\s*Được miễn\s*\|", re.IGNORECASE)


def _doc_exempt_keys(cell):
    """Map one doc cell ('tone chung, pain-claim, so sánh viện') to script keys."""
    keys, unknown = set(), []
    for part in re.split(r"[,·]", cell):
        p = part.strip().strip("*`").lower()
        if not p or p in DOC_EXEMPT_IGNORE:
            continue
        p = re.sub(r"\s*\(.*?\)\s*", "", p).strip()
        if not p or p in DOC_EXEMPT_IGNORE:
            continue
        if p in DOC_EXEMPT_LABELS:
            keys.update(DOC_EXEMPT_LABELS[p])
        else:
            unknown.append(p)
    return keys, unknown


def effective_exempt(mode):
    """What the SCRIPT actually exempts for a mode, across both mechanisms.

    vision_absolute lives in QUOTA_10_10 for most modes and in EXEMPT for koc,
    so neither table alone is the answer.
    """
    keys = set(EXEMPT.get(mode, EXEMPT_DEFAULT))
    cfg = QUOTA_10_10.get(mode)
    if cfg is not None and cfg.get("exempt"):
        keys.add("vision_absolute")
    return keys


def check_exempt_table(skill_path, verbose=True):
    """Diff the 7B table in SKILL.md against EXEMPT + QUOTA_10_10."""
    problems, seen, in_table = [], set(), False
    for line in read_text(skill_path).splitlines():
        s = line.strip()
        if DOC_EXEMPT_HEADER_RX.match(s):
            in_table = True
            continue
        if in_table and not s.startswith("|"):
            in_table = False
            continue
        if not in_table:
            continue
        m = DOC_EXEMPT_ROW_RX.match(s)
        if not m:
            continue
        mode, yes_cell, no_cell = m.group(1), m.group(2), m.group(3)
        seen.add(mode)
        doc_yes, unk_yes = _doc_exempt_keys(yes_cell)
        doc_no, unk_no = _doc_exempt_keys(no_cell)
        for u in unk_yes + unk_no:
            problems.append("%s: doc names %r, which maps to no claim family" % (mode, u))
        script_yes = effective_exempt(mode)

        missing = sorted(doc_yes - script_yes)
        extra = sorted(script_yes - doc_yes)
        overlap = sorted(doc_yes & doc_no)
        contradict = sorted(doc_no & script_yes)

        for k in missing:
            problems.append("%s: doc says exempt from %s, script does NOT exempt it"
                            % (mode, k))
        for k in extra:
            problems.append("%s: script exempts %s, doc does not list it" % (mode, k))
        for k in overlap:
            problems.append("%s: doc lists %s in BOTH exempt and not-exempt" % (mode, k))
        for k in contradict:
            problems.append("%s: doc says NOT exempt from %s, script exempts it"
                            % (mode, k))
        if verbose:
            ok = not (missing or extra or overlap or contradict or unk_yes or unk_no)
            print("  %-4s %-16s exempt=%s"
                  % ("ok" if ok else "FAIL", mode, ",".join(sorted(script_yes)) or "-"))

    for mode in sorted(set(EXEMPT) - seen):
        problems.append("%s: exempt in script but has no row in the 7B table" % mode)
    return problems


def run_docsync(skill_path):
    """Parse the section-6 bucket table out of SKILL.md and diff it against POLICY.

    The table is a human-readable copy of TOK/POLICY, and copies drift. This makes
    drift a test failure instead of a wrong fee quote six weeks from now.
    """
    rows, in_table = {}, False
    for line in read_text(skill_path).splitlines():
        s = line.strip()
        if DOC_BUCKET_HEADER_RX.match(s):
            in_table = True
            continue
        if in_table and not s.startswith("|"):
            in_table = False
            continue
        if not in_table:
            continue
        m = DOC_BUCKET_ROW_RX.match(s)
        if m:
            bucket, tier, free = m.group(1), m.group(2).strip(), m.group(3).strip()
            rows[bucket] = (tier, free)
    if not rows:
        print("FAIL: no bucket table found in %s" % skill_path)
        print("      (expected a header row starting | promo-key | ... | fee-tier-id |")
        print("       followed by rows like: | `kx` | ...tokens... | **T0** | ✅ |)")
        return 2

    expected = dict(POLICY["buckets"])
    expected["fu_other"] = POLICY["fu_other_hospital_tier"]
    for k in ("ambiguous", "none"):
        expected[k] = "HOTLINE"
    lt = POLICY["lao_thi_phaco_path_tier"]
    expected["lt_phaco"] = "HOTLINE" if lt in (None, "HOTLINE") else lt

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
    print("doc-sync: 7B exemption table vs EXEMPT + QUOTA_10_10")
    problems += check_exempt_table(skill_path)

    print("")
    if problems:
        for p in problems:
            print("  drift: %s" % p)
        print("")
        print("DOCSYNC: FAIL")
        return 1
    print("DOCSYNC: PASS - %d bucket row(s) match POLICY, 7B table matches EXEMPT"
          % len(expected))
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
    ap.add_argument("--fees", help="path to fees-promos.md for footer layer (b); "
                                   "auto-located next to the skill if omitted")
    ap.add_argument("--no-auto-fees", action="store_true",
                    help="do not auto-locate fees-promos.md (layer (b) then only "
                         "runs if --fees is given)")
    args = ap.parse_args(argv)

    if not args.fees and not args.no_auto_fees:
        args.fees = default_fees_path()

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




