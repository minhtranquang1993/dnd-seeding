# Improvement Brief: mode `anti` — reply review xấu bằng giọng khách cũ

## Hiện trạng (baseline, đọc từ SKILL.md + qa_seeding.py)

Skill `dnd-seeding` đang có 8 mode: `group` · `story` · `reply-group` · `ads` · `live` ·
`maps` · `maps_foreigner` · `koc`. **Không mode nào xử lý tình huống có review xấu.**

Đo trên code:

| Sự thật | Vị trí |
|---|---|
| `COMMAND_MODES` có 10 entry (kể cả alias `reply_group`/`google_maps`), không có `anti` | `qa_seeding.py:1019` |
| `QUOTA_10_10` có 9 row; mode thiếu row → warn, và nếu draft mang `10/10` → **fail 5A** "no quota row" | `qa_seeding.py:867`, `1515` |
| `check_new_angles` (sàn Kiểu 6+7 chống toàn khen) chỉ chạy khi `mode == "reply-group"` | `qa_seeding.py:1584` |
| `check_topic_fit` (M6, bám service câu hỏi gốc) cũng chỉ chạy khi `mode == "reply-group"` | `qa_seeding.py:1645` |
| Không có regex nào bắt giọng brand/admin ("bệnh viện chúng tôi", "xin lỗi quý khách") | grep toàn file: 0 hit |
| Không có regex nào bắt việc đấu khẩu / quy kết người review ("chắc đối thủ", "dựng chuyện") | grep toàn file: 0 hit |

**Hệ quả nếu chạy tay không có mode:** gõ `/dnd-seeding anti "..."` hôm nay sẽ rơi về
`DEFAULT_MODE = "group"` (`qa_seeding.py:1022`, luật "token đầu không khớp mode nào → chạy
group, không đoán"). Tức là sinh 28 bài đăng group thay vì 20 comment reply — sai hoàn toàn,
và **`--check` vẫn PASS** vì nó đang chấm theo luật `group`.

**Cái đã có và dùng lại được:**

- `parse_items()` + `SECTION_RX` đọc header `### Kiểu N:` — dùng luôn, không sửa.
- `BRAND_RX` (`:951`) và cơ chế `NO_BRAND_SECTIONS` — đã có sẵn để cưỡng chế "Kiểu 7 không nhắc DND".
- `check_bans` §7C (hết đau · superlative VN/EN · so sánh viện · cam kết) — mode mới **không**
  được miễn gì, nên chỉ cần không thêm row vào `EXEMPT` là tự có hiệu lực.
- `check_topic_fit` (M6-B/C/D) — gate bám service, đã test 28 ca `SELFTEST_COMPARE` + 20 ca `SELFTEST_TOPICS`.
- Luật phí §6 / M2 / footer 2 lớp — áp cho mọi mode, không có ngoại lệ, không cần sửa.

## Mục tiêu cải thiện (đo được)

1. `/dnd-seeding anti "<review xấu>"` route đúng sang mode `anti`, không rơi về `group`.
2. Output là ~20 comment **giọng khách hàng đã trải nghiệm tốt tại DND**, không phải giọng
   thương hiệu / admin / CSKH.
3. Comment **không đấu khẩu, không quy kết** người viết review xấu.
4. Ba luật trên **không thể vi phạm im lặng** — `--check` fail, không chỉ là chữ trong SKILL.md.

## Quyết định đã chốt với user (Gate 1)

| Câu | Chốt |
|---|---|
| Giọng reply | **Khách hàng đã trải nghiệm tốt tại DND**, KHÔNG phải giọng brand |
| Nền tảng | **Comment group/fanpage** (không làm Google Maps — Maps không cho khách reply review của người khác) |
| Điểm phàn nàn có thể đúng thật | **Né hẳn** — không nhắc lại điểm đó, chỉ kể trải nghiệm tốt của mình |
| Mật độ nhắc DND | **Như `reply-group`**: tối đa 1 lần/comment, có comment chỉ nói "chỗ Trương Định q3", ≥1 comment không nhắc DND |
| Sàn chống toàn khen | **Giữ Kiểu 7** (hỏi lại người đăng, trung tính, không khen, không nhắc DND) |
| QA gate | **Có** — thêm gate M7 cưỡng chế |

## Hướng đề xuất

### A. SKILL.md — MODE 6 mới: `/dnd-seeding anti "<review xấu>"`

**Cách hoạt động:** đọc review xấu user paste → in marker → sinh ~20 comment.

**Marker bắt buộc in ở đầu output** (script parse — thiếu là fail M7-A):

```
**Mode:** anti
**Review xấu:** <paste nguyên văn review>
**Topic:** <service> / <phase>
```

`Topic` dùng đúng `detect_topic()` hiện có, không thêm bảng mới.

**6 kiểu comment (~20 item):**

| Kiểu | Số | Nội dung |
|---|---|---|
| 1 | 5 | Khách đã mổ kể trải nghiệm của mình — bs nào, phương pháp, thị lực |
| 2 | 3 | Khách đi khám (chưa mổ) kể buổi khám — bs giải thích, quy trình |
| 3 | 3 | Người nhà dẫn ba mẹ / con đi (Phaco, Ortho-K) |
| 4 | 3 | Khách tái khám / khách lâu năm — đi nhiều lần, được theo dõi |
| 5 | 3 | Khách ở tỉnh, hoặc khách đi nhiều viện rồi chọn DND — **không được nói DND vượt trội** (§7C cấm so sánh viện) |
| **7** | **≥2** | **Hỏi lại người đăng — trung tính, KHÔNG khen, KHÔNG nhắc DND** (sàn cứng) |

**Vì sao nhảy từ 5 sang 7, bỏ số 6:** `Kiểu 6` trong `reply-group` nghĩa là "review có điểm
chưa hài lòng thật" — mode `anti` **cấm** đúng thứ đó (chốt "né hẳn"). Để số 6 mang hai nghĩa
trái ngược trong cùng một parser (`SECTION_RX` trả int, dùng chung) là mời người sửa sau nối
sai hằng số. Nên đặt **bất biến toàn skill**: `Kiểu 7` = trung tính/hỏi lại/không nhắc brand ở
mọi mode; `Kiểu 6` = mixed-có-điểm-dở, **chỉ** `reply-group`. Mode `anti` không dùng số 6.

### B. QA script — gate M7 `anti`

| Rule | Gác gì | Ngưỡng | Độ dài áp dụng |
|---|---|---|---|
| **M7-A** | Draft `anti` thiếu dòng `**Review xấu:**` | 0 | **mọi độ dài** |
| **M7-B** | Giọng brand / admin / CSKH | 0 hit | mọi độ dài |
| **M7-C** | Đấu khẩu / quy kết người viết review | 0 hit | mọi độ dài |
| **M7-D** | Sàn Kiểu 7: <2 item, hoặc item Kiểu 7 nhắc brand, hoặc không phải câu hỏi | ≥2 item | full run (≥10 item) |
| **M7-E** | Item **không** thuộc Kiểu 7 mang cụm chưa-hài-lòng (nhượng bộ điểm dở) | 0 item | mọi độ dài |

**M7-B `BRAND_VOICE_RX`** — cụm chỉ người của bệnh viện mới nói:
`bệnh viện chúng tôi` · `chúng tôi xin` · `chúng tôi rất` · `quý khách` · `quý anh/chị` ·
`kính gửi` · `bộ phận cskh` · `chăm sóc khách hàng` · `ban giám đốc` · `phản hồi từ bệnh viện` ·
`rất tiếc về trải nghiệm` · `xin lỗi vì sự bất tiện` · `ghi nhận phản hồi` · `liên hệ tổng đài của chúng tôi`

Cố ý **không** đưa `chúng tôi` trơn vào list: khách thật nói "vợ chồng chúng tôi đi khám" hợp
lệ. Gate hẹp mà đúng đáng tin hơn gate rộng báo nhầm — cùng lý do `KX_CONTEXT` loại
`nhỏ thuốc giãn` (`checks.md` §M6).

**M7-C `ATTACK_REVIEWER_RX`** — quy kết động cơ hoặc phủ nhận người đăng:
`đối thủ` · `nói xấu` · `dựng chuyện` · `bịa` · `vu khống` · `nick ảo` · `seeding` · `được thuê` ·
`chắc (b|bạn|bn) chưa (đi|khám|mổ)` · `đừng tin` · `bốc phốt` · `phá hoại` · `dìm`

Đây là luật quan trọng nhất của mode: quy kết người khiếu nại làm thread nổ to hơn chính review
xấu, và 20 nick cùng quy kết một người là dấu hiệu seeding rõ nhất.

**M7-E `CONCESSION_RX`** — cưỡng chế chốt "né hẳn". Lấy cùng danh sách cụm với
`DISSATISFACTION_RX` nhưng **viết regex riêng, không reuse**:

> `DISSATISFACTION_RX` đang dùng ở hướng **fail-open** (M5 đòi Kiểu 6 *phải* có ≥1 cụm — khớp
> nhầm thì chỉ là cho qua một draft). M7-E dùng nó ở hướng **fail-closed** (có cụm → fail draft).
> Đảo hướng thì false-positive đổi giá: `đông` trơn trong `DISSATISFACTION_RX` sẽ khớp
> `đông đúc`, `mùa đông`, `đông y`, `Hà Đông`. Nên M7-E siết `đông` thành
> `(hơi|khá|rất|quá) đông|đông (người|khách|quá|lắm)`. Reuse nguyên regex là mượn một mức
> chính xác được đo ở hướng khác.

**M7-D `QUESTION_RX`** — item Kiểu 7 phải thực sự là câu hỏi, không phải comment khen dán vào
cho đủ sàn: `?` hoặc `\bv$` · `k ạ` · `chưa ạ` · `nhỉ` · `ntn` · `thế nào` · `bao lâu` · `bn` ·
`hôm nào` · `bs nào` · `ai biết`.

**M6 dùng lại cho `anti`** (không viết bản mới): đổi guard `mode != "reply-group"` thành
`mode not in TOPIC_FIT_MODES = {"reply-group", "anti"}`, và cho M6 đọc marker theo mode —
`**Câu hỏi gốc:**` cho `reply-group`, `**Review xấu:**` cho `anti`. Lý do: review xấu về Phaco
mà 20 comment kể chuyện mổ SMILE là **đúng con bug M6 đã dựng để chặn**, chỉ đổi bối cảnh.
Review xấu chung chung ("bs thái độ kém") → `detect_topic` trả `none` → M6-B/C tự skip, đúng
hành vi hiện có.

M6-A vẫn chỉ đòi `**Câu hỏi gốc:**` cho `reply-group`; marker của `anti` do M7-A gác. Một
marker cho một mode, không đòi cả hai.

**`QUOTA_10_10["anti"]`** = `{"allowed": {1}, "max_ratio": 0.20}` — giống `reply-group`: chỉ
Kiểu 1 (khách đã mổ, kể thị lực) được mang `10/10`, ≤20% item/run. Thiếu row này thì mode rơi
vào nhánh "no quota row" (`:1516`) — warn khi không có `10/10`, fail khi có.

**`EXEMPT`: không thêm row.** `anti` chịu đủ §7C: không claim hết đau, không superlative,
không so sánh viện, không cam kết. Thread phòng thủ đúng là chỗ dễ trượt superlative nhất.
Không thêm row vào `EXEMPT` cũng có nghĩa `--docsync` (bảng 7B) không cần sửa —
`check_exempt_table` chỉ đòi row cho mode **có** trong `EXEMPT` (`:3121`).

### C. Routing

Thêm `anti` vào `COMMAND_MODES` (`:1019`) và list của `detect_mode` (`:1003`). `anti` không
phải prefix/substring của mode nào đang có nên thứ tự longest-first không bị ảnh hưởng.

Fixture routing bắt buộc: `/dnd-seeding reply-group "có ai anti bên đó k"` phải vẫn ra
`reply-group` — chữ `anti` trong ngoặc kép là văn của user, không phải lệnh (luật
`parse_command`, brief §6 cũ).

### D. `qa/checks.md`

Thêm 5 row M7 vào bảng gate, một mục M7 giải thích hai chỗ dễ nới sai (`chúng tôi` trơn,
reuse `DISSATISFACTION_RX`), và block fixture `H`.

## Phạm vi

**Trong:** `SKILL.md` (When to Use · Process Flow Bước 1 · MODE 6 mới · §7A row · Common
Mistakes) · `scripts/qa_seeding.py` (M7 + `QUOTA_10_10` row + routing + fixtures) ·
`qa/checks.md`.

**Ngoài — cố ý không đụng:**

- `fees-promos.md` · `services.md` — không có số mới, không có service mới
- `detect_bucket()` · `free_exam_allowed()` · M2 · footer 2 lớp — dùng lại y nguyên
- `detect_topic()` · `TOPIC_TOK` · `TOPIC_LADDER` · `SERVICE_DRIFT_TARGETS` · `_is_comparison`
  — dùng lại, **không sửa logic**; chỉ mở rộng *mode nào* gọi M6
- `EXEMPT` · `BAN_KEYS` · anti-repeat · bảng 7B
- `check_new_angles` (M5) — vẫn chỉ `reply-group`
- 8 mode cũ · danh sách bác sĩ

## Rủi ro regression

| Rủi ro | Chặn bằng |
|---|---|
| **Mở M6 cho `anti` làm hồi quy `reply-group`** | Guard đổi từ so sánh chuỗi sang set `TOPIC_FIT_MODES`; toàn bộ 24 fixture `SELFTEST_M6*` + `SELFTEST_COMPARE` (28 ca) + `SELFTEST_TOPICS` (20 ca) phải xanh không sửa một dòng nào |
| **M6 đọc marker theo mode → `reply-group` mất marker mà vẫn pass** | M6-A giữ nguyên: `reply-group` thiếu `**Câu hỏi gốc:**` → FAIL ở mọi độ dài. Fixture "reply-group without the marker" phải còn fail đúng M6-A |
| **M7-E false-positive vì reuse `DISSATISFACTION_RX`** | Viết `CONCESSION_RX` riêng, siết `đông`. Fixture: "e ở Hà Đông qua khám" và "khám mùa đông cx đông đúc gì đâu" → PASS |
| **M7-B bắt nhầm khách thật nói `chúng tôi`** | `chúng tôi` trơn KHÔNG vào list. Fixture: "vợ chồng chúng tôi đi khám bên DND" → PASS |
| **M7-C bắt nhầm khi review xấu được quote lại** | M7-C soi **item**, không soi dòng `**Review xấu:**` (dòng marker không khớp `ITEM_RX`/`ITEM_HEADER_RX` nên `parse_items` bỏ qua). Fixture: review xấu chứa chữ "dựng chuyện" ở marker → PASS |
| **`anti` mang `10/10` mà không có quota row → fail 5A khó hiểu** | Thêm row `QUOTA_10_10["anti"]`. Fixture: `10/10` ở Kiểu 1 → PASS, ở Kiểu 7 → FAIL |
| **Sàn Kiểu 7 lách bằng comment khen dán nhãn 7** | M7-D đòi item Kiểu 7 khớp `QUESTION_RX` **và** không nhắc brand. Fixture: "mình mổ bên DND ổn lắm" trong Kiểu 7 → FAIL |
| **Thêm marker `**Review xấu:**` phá `parse_items()`** | Dòng không khớp `ITEM_RX`/`SECTION_RX`/`ITEM_HEADER_RX`; selftest xác nhận số item không đổi |
| **20/20 comment đều tích cực = fingerprint §7 dựng ra để chặn** | **Rủi ro còn lại, user đã chốt "né hẳn".** Giảm nhẹ bằng: sàn Kiểu 7 ≥2 item trung tính · anti-repeat vẫn áp (>15% warn, >30% block) · §7C vẫn cấm superlative + so sánh viện · quota `10/10` ≤20%. Không loại bỏ được hết, và ghi ra đây có chủ đích |
| Sync thiếu runtime (đã xảy ra: 3 runtime 3 version) | Không thêm file mới → mục "Repo & đồng bộ" vẫn 5 path, không sửa |

## Acceptance criteria

- [ ] `--selftest` xanh, **không sửa** bất kỳ fixture cũ nào ngoài việc thêm mới
- [ ] `SELFTEST_BUCKETS` (19 ca) · `SELFTEST_TOPICS` (20 ca) · `SELFTEST_COMPARE` (28 ca) không đổi kết quả
- [ ] `--docsync SKILL.md` PASS (không thêm row `EXEMPT` nên bảng 7B không đổi)
- [ ] `--heldout qa/heldout.tsv` 28/28 như cũ
- [ ] Routing: `/dnd-seeding anti "bs khám ẩu chờ 2 tiếng"` → mode `anti`, payload đúng
- [ ] Routing: `/dnd-seeding reply-group "có ai anti bên đó k"` → mode `reply-group`
- [ ] **M7-A:** draft `anti` thiếu `**Review xấu:**` → FAIL M7-A, kể cả draft 1 item
- [ ] **M7-B:** "bệnh viện chúng tôi rất tiếc về trải nghiệm của quý khách" → FAIL M7-B;
      "vợ chồng chúng tôi đi khám bên DND" → PASS
- [ ] **M7-C:** "chắc đối thủ dựng chuyện thôi, đừng tin" → FAIL M7-C;
      review xấu ở marker có chữ "dựng chuyện" → PASS
- [ ] **M7-D:** full run 20 item không có Kiểu 7 → FAIL M7-D; Kiểu 7 nhắc DND → FAIL M7-D;
      Kiểu 7 là câu khen không phải câu hỏi → FAIL M7-D
- [ ] **M7-E:** "hôm e đi cx chờ hơi lâu mà bs bên DND khám kỹ" → FAIL M7-E;
      "e ở Hà Đông" / "mùa đông" → PASS
- [ ] **M6 dùng lại:** review xấu về Phaco + comment kể mổ SMILE → FAIL M6-B
- [ ] **M6 skip đúng:** review xấu chung chung ("bs thái độ kém") → `detect_topic` = `none`,
      M6-B/C skip, draft hợp lệ PASS
- [ ] **5A:** `10/10` ở Kiểu 1 trong hạn ngạch → PASS; ở Kiểu 7 → FAIL
- [ ] Draft mẫu `anti` 20 item đầy đủ 6 kiểu: `--check` PASS
- [ ] Reviewer APPROVE
