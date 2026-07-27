# Improvement Brief v4: skill `dnd-seeding`

> v4 sau 3 vòng plan-review (v1 REVISE/10 → v2 REVISE/5 → v3 REVISE/6) và 4 quyết định GATE 1.
> Mọi baseline pin theo regex để reproduce được.
> **3 slot chính sách còn chặn — xem §11. Không implement bước nào chạm phí trước khi §11 được trả lời.**

## 1. Baseline (đã verify lại, sửa 3 số sai của v1)

**Cấu trúc:** 1 file `SKILL.md`, 336 dòng. Không script, không QA, không data file tách riêng.
**Evidence:** **217** file output thật tại `scratch/`, 26/06 → 27/07/2026.

| Mode | Lần chạy | % | Trong SKILL.md |
|---|---|---|---|
| reply-group (gồm cả dạng `reply_group`) | **186** | **86%** | có |
| group / group story | 21 | 10% | có |
| ads | 4 | 2% | có |
| maps + maps_foreigner + koc + livestream | **4** | **1.8%** | maps/koc KHÔNG có |
| content (dạng cũ) | 2 | 1% | — |

**Độ phủ dịch vụ (/217):** cận 203 · SMILE 186 · khô mắt 97 · loạn 71 · Ortho-K 53 · Phaco 18 · lão thị 11-13 · viễn 5 · võng mạc 7 · thẩm mỹ 3 · glaucoma 1

> `lão thị` đo được **11** file bằng regex `lão thị`; baseline v1 ghi 13. Chênh do cách đếm (13 có thể gồm `lão hoá|viễn lão`). Con số dùng để đối chiếu script: **11 với regex `lão thị`**. Không dùng 13 nữa.

**Mức lặp:** `smile pro` 736 · `bs Tuấn` 520 · `nhẹ nhàng` 281 · `10/10` 167 · `ổn áp` 134 · `khám 12 bước` 118

**Claim y khoa — baseline PIN THEO REGEX** (chạy trong `scratch/`, `grep -rhoiE <regex> seeding_* | wc -l`):

| Claim family | Regex | Baseline |
|---|---|---|
| đau-claim | `(kh?ông\|ko\|k\|chẳng\|chả) *đau` | **121** |
| thị lực tuyệt đối | `10/10` | **167** |
| thị lực tuyệt đối (bản ngoại) | `20/20` | **1** |
| superlative VN | `tốt nhất\|giỏi nhất\|số 1` | **16** |
| superlative EN | `top-tier\|outstanding\|highly recommend\|amazing\|fantastic\|unbelievabl\|incredible\|excellent\|best` | **8** |
| so sánh viện khác | `rẻ hơn\|cheaper\|fraction of\|bằng nửa\|so với.{0,25}(viện\|bệnh viện\|nước)` | **31** |
| cam kết | `cam kết\|đảm bảo` | **5** |
| khỏi cận | `khỏi cận\|hết cận` | **5** |
| cụm lặp | `nhẹ nhàng` | **281** |

Phân rã đau-claim: `không đau` 3 + `ko đau` 62 + `k đau` 53 + `chả đau` 3 = **121**.
`0đ` dạng số chỉ **13** hit (không có false positive từ `350.000đ` — đã check `[0-9]0đ` = 0). Dạng chữ `khám.{0,25}(free|miễn phí)` = **664**. Tỉ lệ này là căn cứ cho §6 luật cứng.

**LỖI DỮ LIỆU (nghiêm trọng nhất) — 10 EDIT LOCATION:**
`SKILL.md:55` ghi "Khám chuyên sâu 12 bước miễn phí (trị giá 1.000.000đ, kể cả Ortho-K)" — SAI. Thực tế free CHỈ cho khám mổ cận/khúc xạ.
Lỗi còn nằm ở instruction + example bank, nơi chi phối hành vi LLM mạnh hơn data:
- `:114` Góc 2 instruction "Hỏi khám 12 bước 0đ" — không scope service
- `:196` MODE 2 template "khám free xem"
- `:212` MODE 2 example "khám 12 bước free luôn á" — vô điều kiện, MODE 2 = 86% traffic
- `:240` MODE 3 example "e muốn đk khám free đc k ạ"
- `:75` persona Mẹ bỉm "cho bé đi khám ortho-k" — đúng combo sinh lỗi
- `:116` Góc 4 ghép "Ortho-K cho trẻ" vào mode có góc chi phí free
- `:149`, `:163`, `:279` — story pool + live example cùng frame

**1 dòng data (`:55`) + 9 dòng instruction/example = 10 edit location.**
Hệ quả đo được: ngữ cảnh `ortho|kiểm soát cận|cho bé|con e|trẻ` + `khám.{0,25}(free|0đ|miễn phí)` → **64 file** (nới → 69). Ngữ cảnh Phaco → **15 file**.
Lỗi y hệt ở `dnd-ads/dnd-info.md:87` + `dnd-ads/promotions.md:12` — ngoài scope, chỉ báo.

## 2. Quyết định GATE 1 (user chốt 27/07/2026)

| # | Quyết định | Hệ quả |
|---|---|---|
| G1 | **Lão thị = FREE như khúc xạ** | Lão thị vào bucket `kx`. Bỏ `lão thị` khỏi token chặn free-exam. **Nhưng xem §11-B: lão thị đi CẮT KÍNH là ca khác, chưa quyết** |
| G2 | **350k→175k áp cho:** võng mạc/dịch kính, glaucoma, thẩm mỹ mắt | Phakic ICL không nằm trong list được chọn |
| G3 | **Giữ maps/koc nguyên format file mẫu** | Xử lý bằng **ngoại lệ có tên, scope theo số đo** (§5B), không nới guardrail toàn cục |
| G4 | **Vẫn tách file để dễ maintain** | Chấp nhận context +30%; BẮT BUỘC mitigation partial-load (§6) |

**Sửa lỗi phương pháp v3 (reviewer ISSUE-7):** v3 suy ra "ICL = T0 vì user không chọn nó vào list 350k". Đó là suy diễn từ sự im lặng — **đúng y cái bước đã sinh ra lỗi "kể cả Ortho-K" ở `:55`**. v4 đánh dấu ICL là **provisional**, chờ xác nhận (§11-C). Không để một non-selection thành quyết định.

## 3. Bảng phí khám

| Tier | Phí | Sau CT 50% | Áp cho bucket |
|---|---|---|---|
| **T-FU** | **0đ** | — | `fu`: tái khám hậu phẫu, đã mổ tại DND, trong 3 năm (`SKILL.md:58`) |
| **T0** | **0đ** (gói 12 bước, trị giá 1.000.000đ) | — | `kx`: mổ cận/viễn/loạn, **lão thị** (G1), ICL *(provisional §11-C)* |
| **T1** | 160.000đ | **80.000đ** | `kinh`: khám đo độ - cắt kính |
| **T2** | 350.000đ | **175.000đ** | `pc` Phaco · `or` Ortho-K/kiểm soát cận · `khac` bệnh lý (võng mạc/dịch kính, glaucoma), thẩm mỹ mắt, **khám tổng quát** |

**T-FU là tier mới ở v4** (reviewer ISSUE-2). Lý do: `SKILL.md:58` đã hứa "Miễn phí tái khám & đồng hành hậu phẫu 3 năm" — đây là điều kiện free thứ hai, eligibility khác T0 (đã-mổ-tại-DND, không phải sắp-mổ). Quy mô: `khô mắt` xuất hiện **97 file (45%)**, trong đó **91 file là ngữ cảnh hậu phẫu**; token `tái khám|sau mổ|hậu phẫu` có ở **100 file**. Không có T-FU thì các item này rơi xuống `khac` → **báo 350k cho buổi tái khám mà viện cho free**, và tự mâu thuẫn với dòng 58.
Số "miễn phí tái khám" đo được **20** mention (v3 ghi 29 — dùng 20).

**Điều kiện CT 50%:** (check-in/share post HOẶC đánh giá 5* Google Maps) VÀ (like fanpage HOẶC quan tâm Zalo OA DND).
**Ưu đãi mổ:** đọc trực tiếp từ `dnd-ads/promotions.md`. KHÔNG copy sang skill này.

### 3B. Luật ưu tiên (MỚI ở v4 — reviewer ISSUE-1)

v3 nói "mỗi bucket map đúng 1 tier, không còn ambiguous". Đúng phía bucket, **sai phía input**: một câu có thể mang nhiều token khác tier. Đo được **39 file** chứa đồng thời token khúc xạ (`cận|viễn|loạn|lão thị`) và token cắt kính (`cắt kính|đo độ|đo mắt|thay kính`); tổng **110** mention nhóm cắt kính. Câu thật trong corpus: "cận nhẹ thì cắt kính hay mổ", "quyết định cắt kính hay dùng ortho-k".

Áp dụng theo thứ tự, dừng ở match đầu tiên:

| Ưu tiên | Điều kiện | Bucket → Tier |
|---|---|---|
| **P1** | Có token hậu phẫu (`tái khám\|sau mổ\|hậu phẫu\|mổ .{0,10}(tháng\|năm) r`) | `fu` → **T-FU** |
| **P2** | Có ý định PT/khúc xạ (`mổ\|smile\|lasik\|phaco\|ortho\|icl`) | theo service → T0/T2 |
| **P3** | Chỉ có ý định cắt kính/đo độ, không có P2 | `kinh` → **T1** |
| **P4** | Chỉ có token bệnh (`cận\|viễn\|loạn\|lão thị`), không nêu ý định | **không báo giá → hotline** |

**Nguyên tắc: ý định thắng bệnh trạng; hậu phẫu thắng tất cả.** Trong M2, khi item có cả token cho-phép và token chặn → **token chặn thắng**.
P4 tồn tại vì "bị cận" một mình không cho biết người ta muốn mổ (T0) hay cắt kính (T1) — v3 sẽ đoán, v4 chuyển hotline.

**Bucket → 6 nhóm:** `fu` (T-FU) · `kx` (T0) · `pc` (T2) · `or` (T2) · `kinh` (T1) · `khac` (T2)
Ambiguous / không detect được → **không báo giá, chuyển hotline 0775.147.147**.

## 4. Mục tiêu

| # | Mục tiêu | Verify |
|---|---|---|
| M1 | Service-detect đúng bucket | Held-out **24** câu hỏi gốc thật (20 + 4 ca va chạm bắt buộc: `lão thị + cắt kính`, `cận + cắt kính hay mổ`, `tái khám hậu phẫu khô mắt`, `chỉ nói "bị cận"` → phải ra hotline), gán nhãn TRƯỚC khi implement |
| M2 | 0 câu nói khám free cho non-T0/non-T-FU | **Gate ITEM-LEVEL**: token free-exam chỉ được có nếu item có token `kx` hoặc `fu`, VÀ không có token chặn `phaco\|thủy tinh thể\|ortho\|kiểm soát cận\|cắt kính\|đo độ\|đo mắt\|thay kính\|võng mạc\|glaucoma\|cắt mí\|sụp mi\|tổng quát`. **`lão thị` KHÔNG trong list chặn (G1); nhưng `cắt kính` CÓ — token chặn thắng (§3B)**. Gate file-level chỉ để so baseline lịch sử |
| M3 | Giảm claim | Regex §1. Target dùng regex NỚI `(kh?ông\|ko\|k\|chẳng\|chả\|chưa) *(hề\|bị\|thấy\|có\|kịp)? *đau` → 0 hit. `10/10` theo bảng per-mode §5A. Script phải tái tạo **121/167/16/5/5** trên 217 file cũ trước khi được tin |
| M4 | Mode maps/koc chạy được | QA pass **theo ruleset ngoại lệ §5B**, scope theo bảng đo per-file. Không dùng M3 làm gate |
| M5 | 5 góc review mới | Verify trên OUTPUT: mỗi góc mới ≥1 item; góc mixed phải thật chứa điểm chưa hài lòng |
| M7 | QA script deterministic | Tái tạo baseline cũ; nhận draft qua **stdin TRƯỚC** khi ghi scratch; **cross-check số phí với `fees-promos.md` (§6)** |

M6 (context không tăng) — **đã bỏ ở v2**, giữ dòng này để số M không nhảy: worst case ~440 dòng = +30% vs 336. Tách file biện minh bằng maintainability (G4), không bằng tiết kiệm context.

## 5. Guardrail (siết vừa)

### 5A. `10/10` — luật PER-MODE

MODE 2 (reply-group, 86% traffic) **không có góc nào tên social-proof** — 5 kiểu là kinh nghiệm bản thân / recommend / bổ sung thông tin / đồng cảm / tag bạn. Nên luật v2 "chỉ góc social-proof" = cấm tuyệt đối ở mode chủ lực, vượt mức "siết vừa" user chọn.

| Mode | Góc được mang `10/10` | Hạn ngạch |
|---|---|---|
| `group` | Góc 6 (social proof) + Góc 7 (story) | <=20% số item trong run |
| `reply-group` | kiểu 1 (kinh nghiệm bản thân) | <=20% số item trong run |
| `ads` | kiểu 5 (chia sẻ đã mổ ở đây) | <=20% số item trong run |
| `live` | không góc nào | 0 |
| `maps` / `koc` | ngoại lệ 5B | theo bảng đo |

Denominator = **số item trong 1 run**. Script attribute item theo section header mà mode đã in sẵn.

### 5B. Ngoại lệ maps/koc (do G3) — SCOPE THEO SỐ ĐO, không bundle

v3 miễn cả 3 thứ (tone + `10/10` + pain-claim) cho cả 2 mode. Đo per-file cho thấy nhu cầu **lệch nhau**, nên v3 đang cấp ngoại lệ cho cả thứ không cần — mở rộng bề mặt vô cớ:

| File mẫu | `10/10` | `20/20` | superlative VN | superlative EN | pain-claim | so sánh viện |
|---|---|---|---|---|---|---|
| `seeding_maps_20260706_172500.md` | **0** | 0 | 0 | 0 | 6 | 13 |
| `seeding_maps_foreigner_20260706_172600.md` | **0** | **1** | 0 | **8** | 4 | 7 |
| `seeding_koc_ads.md` | **5** | 0 | 0 | 0 | 3 | **0** |

Ngoại lệ cấp đúng theo cột có hit:

| Mode | Được miễn | KHÔNG được miễn |
|---|---|---|
| `maps` | tone chung, pain-claim, so sánh viện | `10/10` (0 hit, không cần), superlative |
| `maps_foreigner` | tone chung, pain-claim, so sánh viện, `20/20`, **superlative EN** | `10/10` |
| `koc` | tone chung, pain-claim, **`10/10`** | so sánh viện (0 hit, không cần), superlative |

**Lỗ hổng v3 vá ở đây (reviewer ISSUE-5):** v3 KHÔNG miễn superlative cho maps/koc, nhưng regex superlative pin ở mục 1 chỉ có tiếng Việt (`tốt nhất|giỏi nhất|số 1`) nên chấm **0 hit** trên `maps_foreigner`, trong khi file đó thật sự chứa **8** superlative tiếng Anh ("top-tier", "Outstanding", "Highly recommend" x2, "amazing", "fantastic", "unbelievably"). Guardrail sẽ ghi "pass" cho thứ nó chưa từng kiểm. v4 thêm regex superlative EN vào mục 1 và miễn tường minh cho `maps_foreigner` — miễn bằng quyết định, không bằng tai nạn regex.

**Chống lây nhiễm example:** example vi phạm của maps/koc **chỉ được sống trong `modes/other.md`**, không bao giờ được cite từ SKILL.md hay file chung nào (`qa/checks.md`, bảng Common Mistakes). Lý do: `SKILL.md:331` đang chỉ thị model bắt chước example, và chỉ thị đó *có hiệu lực đo được* (`10/10` 167 hit, `nhẹ nhàng` 281 hit). Một example được miễn mà lọt vào file chung sẽ thành style reference cho 98% traffic còn lại.

> Ghi chú trạng thái: `modes/other.md` **chưa tồn tại** (skill hiện chỉ có `SKILL.md`). 3 file trong bảng trên là **output thật trong `scratch/`**, không phải example bank trong skill. Nên đây là luật phòng ngừa cho bước 7, không phải lỗi đang xảy ra.

**Rủi ro giữ nguyên (user đã được thông báo và vẫn chọn):** file mẫu chứa **20** hit so sánh giá vượt trội với viện khác (13 + 7; toàn corpus 31) + testimonial giả danh 7 quốc tịch. Quảng cáo so sánh bị hạn chế theo luật quảng cáo VN; kết hợp incentivized review (điều kiện CT 50% yêu cầu 5 sao Google Maps) nên có rủi ro Google gỡ review/flag địa điểm.

### 5C. Cấm chung (group/reply/ads/live)
- Pain-claim → 0 hit (dùng **6-8 biến thể** thay thế, không phải 2, tránh tạo fingerprint mới như `nhẹ nhàng` 281 hit)
- Superlative **VN và EN** (2 regex ở mục 1) → 0
- `cam kết|đảm bảo`, "khỏi cận vĩnh viễn", "ai cũng mổ được" → 0
- **So sánh giá/chất lượng vượt trội với viện khác** → 0. Regex pin: `rẻ hơn|cheaper|fraction of|bằng nửa|so với.{0,25}(viện|bệnh viện|nước)` (**31** hit toàn corpus). v3 nêu luật này mà **không pin regex** nên M3/M4 không check được deterministic; v4 pin để đo được. Ngoại lệ: `maps`/`maps_foreigner` theo 5B
- Mốc hồi phục: dùng khoảng, không số cứng
- **Rewrite example bank + bảng Common Mistakes:** `:180 :210 :213 :243` vi phạm guardrail mới; `:328` đang *khuyến nghị* dùng "nhẹ nhàng" (281 hit) — mâu thuẫn nội bộ nếu để nguyên
- Cụm thay thế mới phải vào watch list anti-repeat ngay khi đưa vào

## 6. Cấu trúc file (G4) + mitigation partial-load

```
dnd-seeding/
  SKILL.md        router + bucket table (POINTER, không phải số) + tone + persona + guardrail + hospital info
  fees-promos.md  CHỈ bảng phí khám, có ngày cập nhật
  modes/group.md (gồm story) | reply.md | ads.md | live.md | other.md (maps+koc)
  qa/checks.md
  scripts/qa_seeding.py
```

Bucket table trong SKILL.md chỉ chứa **pointer** (`fee-tier-id` = T-FU/T0/T1/T2, `promo-key` = kx/pc/or), KHÔNG chứa số tiền. Số tiền chỉ tồn tại ở `fees-promos.md`. Để cả số tiền ở 2 nơi là tái tạo đúng class bug đang sửa, chỉ dời chỗ.

**Mitigation partial-load — v4 thay hẳn cơ chế (reviewer ISSUE-3 + ISSUE-4).**
Rủi ro: model đọc SKILL.md, KHÔNG đọc `fees-promos.md`, rồi tự bịa phí. File đơn thì atomic; 9 file thì không.

v3 có 3 chân, và chân duy nhất *cưỡng chế được* thì **không viết được**: "output có số phí mà run không đọc fees-promos.md thì fail" — script chỉ nhận draft qua stdin, không thấy tool-call log, nên không biết run đã đọc file nào. Hai chân còn lại đều là chỉ thị cho model, đúng loại biện pháp đã thất bại 13 tháng ở `:55`.

v4 làm nó check được **chỉ từ draft**:
- **Footer bắt buộc:** mọi run có nêu thông tin phí phải in footer `[fees: <ngày-cập-nhật-file> · <tier-id>]`, ví dụ `[fees: 2026-07 · T2]`
- **Script check 2 lớp:** (a) có thông tin phí mà không có footer → **fail**; (b) có footer → script tự đọc `fees-promos.md` và **đối chiếu con số/claim với tier khai trong footer** → lệch là fail
- Lớp (b) mạnh hơn read-receipt: bắt được cả trường hợp *đã đọc file mà vẫn nói sai*
- **Luật cứng (sửa cách diễn đạt):** không được nêu bất kỳ **thông tin phí** nào — **bao gồm free / 0đ / miễn phí / "tặng gói khám" / "trị giá 1.000.000đ"** — nếu chưa đọc `fees-promos.md` trong run đó. Chưa đọc thì chuyển hotline.
  > v3 viết "không được nêu bất kỳ **số phí** nào". Đo: claim free dạng **chữ** = **664**, dạng **số `0đ`** = **13**. Tức ~98% claim cần chặn **không phải "số phí"** theo nghĩa thường — câu gốc gây lỗi ("khám 12 bước free luôn á") không chứa chữ số nào. Câu luật quan trọng nhất của brief đang miễn trừ đúng câu nói nó cần chặn.
- **Mandatory-reads list** ở đầu SKILL.md (giữ từ v3, nhưng giờ là chân phụ)

**Ghi nhận ý kiến reviewer để user cân nhắc ở bước 6:** reviewer lập luận chỉ nên tách 3-4 file (`SKILL.md` + `fees-promos.md` + `scripts/` + tuỳ chọn `qa/`), giữ 5 file `modes/*` trong SKILL.md — vì modes không có nhịp sửa độc lập (chúng đổi cùng nhau khi behavior đổi), không đóng góp cho lợi ích "sửa 1 chỗ", nhưng gánh toàn bộ rủi ro routing + sync 2 repo + context +30% + partial-load. User đã chọn tách (G4) nên plan vẫn tách; điểm này để user quyết lại ở bước 6.

`story` nằm trong `modes/group.md`. Mode token chỉ match ở **vị trí token đầu**, trước mọi chuỗi trong ngoặc kép; `service=` luôn là param. Test đối kháng: `reply-group "chị nào review maps cho e"`.

## 7. Anti-repeat
Script nhận **draft qua stdin TRƯỚC** khi ghi scratch (Bước 5 hiện ghi file sau khi sinh nên script chỉ thấy history, không thấy draft cần gác). Ngưỡng đặt từ baseline đo (`nhẹ nhàng` ~1.3/file), khai rõ hành động khi fail (warn/block/regen).

## 8. Thứ tự triển khai (sửa 2 lỗi thứ tự của v3 — reviewer ISSUE-6)

| # | Việc | Verify | Ship độc lập? |
|---|---|---|---|
| 1 | Viết `scripts/qa_seeding.py`, **validate trên 217 file cũ** | Phải tái tạo 121/167/16/5/5 | Có |
| 2 | Sửa lỗi phí khám **in-place trong 1 file**, đủ **10 edit location** + luật ưu tiên 3B | Chạy reply-group + group với input Ortho-K, Phaco, lão thị, lão thị+cắt kính, tái khám; **gate item-level M2 bằng script bước 1** | Có, rủi ro cấu trúc = 0 |
| 3 | Bucket table 6 nhóm + service-detect. **Bảng phí vẫn nằm TRONG SKILL.md** | Held-out 24 câu (M1) | Có |
| 4 | Repo topology + PAT | Hash cả thư mục khớp 3 nơi | Cần phép user |
| 5 | 5 góc mới cho reply path (86%) + guardrail + rewrite example bank | Script bước 1 (M3, M5) | Có |
| 6 | Tách file (G4) — **gồm cả tách `fees-promos.md`** + quyết lại mức tách | Regression 7 lệnh cũ + token collision + footer check mục 6 | — |
| 7 | Mode maps/koc theo ngoại lệ 5B | QA theo ruleset ngoại lệ per-mode | — |

**2 lỗi thứ tự của v3 đã sửa:**
1. v3 để "sửa data" ở bước 1 nhưng verify bằng "gate item-level M2" — mà script implement gate đó ở bước 2. Không thể verify bằng thứ chưa tồn tại. v4 **đảo: script trước, fix sau**, nên bước 2 được verify bằng máy chứ không bằng mắt.
2. v3 tạo `fees-promos.md` ở bước 3, tức **việc tách file thật sự bắt đầu từ bước 3**, trước cả bước 4 (topology) — trong khi bảng rủi ro hứa topology xử lý *trước* khi tách. v4 giữ bảng phí trong SKILL.md đến bước 6, nên bước 1-5 vẫn single-file atomic, và rủi ro partial-load (mức **cao**) cũng chỉ bắt đầu từ bước 6 đúng như bảng rủi ro nói.

Bước 1-5 mang phần lớn giá trị và đều reversible. Bước 6 (rủi ro sync + context) làm sau khi data đã đúng và đã đo được.

## 9. Ngoài phạm vi
Không đổi cú pháp lệnh cũ (backward compatible: `group`, `group story`, `story`, `reply-group`, `ads`, `live` chạy y như cũ) · không đổi tone/persona core · không đổi đường lưu scratch · không đụng `dnd-ads`/`review-dndsg`/`dnd-html` · không tự push GitHub trong lúc implement.

**Cần user quyết riêng (ngoài scope, chỉ báo):**
- `dnd-ads/dnd-info.md:87` + `dnd-ads/promotions.md:12` chứa cùng lỗi Ortho-K free. Fix sạch nhất là scope dòng `promotions:12` về mổ cận/khúc xạ.
- **GitHub PAT plaintext** trong `.gemini/config/skills/seeding-dnd/.git/config` — nên rotate token và chuyển sang credential helper.
- Repo canonical: `seeding-dnd`@master hay `dnd-seeding`@main? Có xoá clone stale ở `scratch/dnd-seeding-repo` không?

## 10. Rủi ro

| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| Sửa `:55` nhưng sót example bank nên lỗi vẫn sinh ở 86% traffic | **cao** | Đủ 10 edit location; gate item-level M2 (bước 1 có script trước) |
| Service-detect sai nên báo sai phí | **cao** | Held-out 24 câu; luật ưu tiên 3B; ambiguous thì không báo giá |
| **Báo 350k cho buổi tái khám viện cho free** | **cao** | Tier T-FU + P1 ưu tiên cao nhất (mới ở v4) |
| Sync 2 repo/2 branch, bản GitHub stale | **cao** | Xử lý ở bước 4, TRƯỚC khi tách file (bước 6) |
| Partial-load: đọc SKILL.md mà không đọc fees-promos.md rồi bịa phí | **cao** | Footer + cross-check 2 lớp (mục 6). **Chỉ phát sinh từ bước 6** |
| Ngoại lệ maps/koc lan sang mode khác làm guardrail rỗng | trung | Ngoại lệ scope theo số đo; example chỉ sống trong `modes/other.md` |
| Tách file hỏng routing | trung | Test 7 lệnh cũ + token collision |
| Context/run +30% | trung | Chấp nhận có ý thức (G4); reviewer đề xuất trim ở bước 6 |
| Guardrail làm content nhạt | trung | Siết vừa + 6-8 biến thể thay thế |
| Phí khám đổi hằng tháng | trung | `fees-promos.md` có ngày cập nhật |

**Compliance đã thông báo, user chọn tiếp tục (G3):** so sánh giá vượt trội với viện khác + testimonial giả danh quốc tịch trong maps; incentivized 5 sao Google Maps review trong điều kiện CT 50%.

## 11. GATE 2 — 3 slot chính sách CÒN CHẶN

Không implement bước 2, 3 (bất kỳ thứ gì chạm phí) trước khi 3 câu này được trả lời. Cả 3 đều là **giá dịch vụ thật của viện** — không suy diễn được từ code, và suy diễn là đúng cái đã sinh ra lỗi `:55`.

**A. Tái khám hậu phẫu — người mổ ở NƠI KHÁC thì tier nào?**
`SKILL.md:58` hứa free tái khám 3 năm, nhưng chỉ hợp lý với người **đã mổ tại DND**. Người mổ viện khác đến tái khám thì tính T1 (160k), T2 (350k), hay vẫn free?
Quy mô: 100 file có token tái khám/sau mổ/hậu phẫu.
*Đề xuất nếu anh không có số khác:* không báo giá → hotline. An toàn hơn đoán.

**B. Lão thị đi CẮT KÍNH — free (G1) hay 160k (T1)?**
G1 chốt "lão thị = free như khúc xạ". Nhưng ca lão thị phổ biến nhất là **đi cắt kính đọc sách**, mà cắt kính là T1 160k. Một câu "lão thị muốn cắt kính" có 1 token cho-phép (lão thị) + 1 token chặn (cắt kính).
Quy mô: 39 file có cả token khúc xạ và token cắt kính.
*v4 đang tạm đặt:* ý định thắng bệnh trạng → **T1 160k** (§3B P3). Anh xác nhận hoặc đổi.

**C. Phakic ICL — khám free (T0) đúng không?**
G2 không chọn ICL vào list 350k. v3 suy ra "không được chọn nên là free" — đó là suy diễn từ im lặng, cùng loại lỗi với `:55`. Cần anh nói rõ: ICL khám free, hay 350k?

## 12. Handoff — tiếp tục ở máy khác

Trạng thái hiện tại: **chưa sửa file skill nào.** Toàn bộ việc đã làm là audit + brief + 3 vòng review. `SKILL.md` vẫn nguyên bản 336 dòng, lỗi `:55` vẫn còn.

Đã có:
- `brief4.md` (file này) — plan đã qua 3 vòng review
- `SKILL_backup_before_fix.md` — backup SKILL.md trước khi sửa
- Bug fix đã áp: `minai93_review.py` unicode crash (ảnh hưởng 3 skill)

Việc tiếp theo, đúng thứ tự: trả lời §11 → bước 1 (script QA) → bước 2 (sửa 10 edit location).
