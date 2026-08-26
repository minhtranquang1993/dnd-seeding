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
5. Gate mới **không được chặn oan** review xấu mà user dán vào, cũng không chặn oan câu seeding
   hợp lệ đã có trong corpus — mọi luật đều phải sweep qua 4 file output cũ trước khi chốt.

> Mục 5 thêm vào sau vòng tự-kiểm. Bản đầu của brief này vi phạm nó ở 8 chỗ: review verbatim làm
> draft fail 5 gate, `CONCESSION_RX` bắt oan 4 câu corpus, M7-B bắt oan 2 câu, M7-C bắt oan 3 câu,
> M7-F bắt oan 2 câu. Tất cả chỉ lộ ra khi chạy regex lên data thật, không lộ ra khi đọc brief.

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
**Review xấu:**
> <paste nguyên văn review, mỗi dòng bắt đầu bằng "> ">
> <dòng 2 nếu có>
**Topic:** <service> / <phase>
```

`Topic` dùng đúng `detect_topic()` hiện có, không thêm bảng mới.

**Review xấu phải là BLOCKQUOTE (`>`), không phải văn trần.** Đây là fix cho một bypass đo được
ở vòng tự-kiểm thứ hai:

> Bản trước định nghĩa block là "từ marker tới dòng trống / `**`-marker / `#` header". Probe: dán
> hai comment seeding thật **ngay dưới** dòng marker, không có dòng trống —
> `1. e mổ bên DND xong hết cận luôn, k đau gì, bs giỏi nhất Sài Gòn` và
> `2. bên đó rẻ hơn viện khác nhiều` — cả hai **lọt vào block** rồi bị excise. Kết quả:
> `dau_claim` · `cure_myopia` · `superlative_vn` · `compare_other_hospital` **tất cả về 0**, và 2
> item biến mất khỏi `parse_items`. Tức là chính cái excise dựng ra để chống chặn-oan lại thành
> đường lách ban.

Blockquote bịt được vì ranh giới không còn phụ thuộc dòng trống:

| Ca | Kết quả đo |
|---|---|
| Review 3 dòng `>` hợp lệ | block đủ 4 dòng · `detect_topic` = `phaco` (đúng) · item = 4 (đúng) · `**Topic:**` còn nguyên · 5C = 0 |
| Dán item không có `>` ngay sau quote | block chỉ ăn dòng `>`; 2 item smuggle thành **item thật** → **cả 4 họ 5C bắn** |
| Review có `1.` / `2.` **trong** quote | `ITEM_RX.match("> 1. chờ 2 tiếng")` = `False` → **không sinh item ma, không cần excise** |
| `detect_topic` trên quote có số | vẫn ra `phaco` — bỏ `>` trước khi detect |
| Review viết văn trần (không `>`) | `REVIEW_Q_RX` không khớp → **FAIL M7-A** (sai format), không im lặng bỏ qua |

Rủi ro còn lại: model tự bỏ `>` trước các comment của nó để giấu. Nhưng dòng `>` **không phải
comment copy-paste được** — user copy từ danh sách có số, còn blockquote hiển thị rõ là phần
review. Nên cái giá là model tự ăn mất quota item của mình, không phải lách ban im lặng.

**Cả `**Mode:**` và `**Review xấu:**` đều bắt buộc.** Thiếu dòng Mode thì `detect_mode` trả
`unknown` và **cả họ gate M7 tắt im lặng** (đo được, xem §C).

**6 kiểu comment (~20 item):**

| Kiểu | Số | Nội dung |
|---|---|---|
| 1 | 5 | Khách đã mổ kể trải nghiệm của mình — bs nào, phương pháp, thị lực |
| 2 | 3 | Khách đi khám (chưa mổ) kể buổi khám — bs giải thích, quy trình |
| 3 | 3 | Người nhà dẫn ba mẹ / con đi (Phaco, Ortho-K) |
| 4 | 3 | Khách tái khám / khách lâu năm — đi nhiều lần, được theo dõi |
| 5 | 3 | Khách ở tỉnh, hoặc khách đi nhiều viện rồi chọn DND — **không được nói DND vượt trội** (§7C + M7-F) |
| **7** | **≥2** | **Hỏi lại người đăng — trung tính, KHÔNG khen, KHÔNG nhắc DND, KHÔNG kể trải nghiệm bản thân** (sàn cứng) |

**Kiểu 5 là kiểu rủi ro nhất của mode.** "Khách đã đi nhiều viện rồi chọn DND" mời gọi đúng thứ
§7C cấm — so sánh viện. Đo được trên draft probe: câu "e khám 3 chỗ r mới chốt bên này, tại thấy
bs giải thích **rõ nhất** với e" đi qua mọi gate hiện có. Nên M7-F ra đời, và Kiểu 5 phải viết
theo hình "**đã xem nhiều nơi, chốt chỗ này**" mà **không xếp hạng** — nêu lý do cụ thể ("bs chịu
giải thích", "gần nhà") thay vì so bên nào hơn.

**Vì sao nhảy từ 5 sang 7, bỏ số 6:** `Kiểu 6` trong `reply-group` nghĩa là "review có điểm
chưa hài lòng thật" — mode `anti` **cấm** đúng thứ đó (chốt "né hẳn"). Để số 6 mang hai nghĩa
trái ngược trong cùng một parser (`SECTION_RX` trả int, dùng chung) là mời người sửa sau nối
sai hằng số. Nên đặt **bất biến toàn skill**: `Kiểu 7` = trung tính/hỏi lại/không nhắc brand ở
mọi mode; `Kiểu 6` = mixed-có-điểm-dở, **chỉ** `reply-group`. Mode `anti` không dùng số 6.

**Đã verify bằng code, không suy luận:** `SECTION_RX` (`:973`) khớp cả `Kiểu`/`Góc`/`Nhóm` và
trả **int trần** — `### Kiểu 7:` và `### Góc 7:` cùng ra `section=7`. Ba hằng số keyed theo int
đó: `NO_BRAND_SECTIONS={7}` · `NO_SCORE_SECTIONS={6,7,8,9,10}` · `TOPIC_NEUTRAL_SECTIONS={7}`.
Hệ quả cụ thể cho `anti`:

| Hằng số | Có tự áp cho `anti`? | Vì sao |
|---|---|---|
| `TOPIC_NEUTRAL_SECTIONS={7}` | ✅ **có** | Đọc trong `check_topic_fit` (`:1691`), mà M6 được mở cho `anti` → Kiểu 7 tự động ra khỏi mẫu số M6-C. Đúng ý muốn, không cần code thêm |
| `QUOTA_10_10["anti"]={"allowed":{1}}` | ✅ **có** | `check_quota_10_10` chạy mọi mode → `10/10` ở Kiểu 7 fail 5A |
| `NO_BRAND_SECTIONS` · `NO_SCORE_SECTIONS` | ❌ **KHÔNG** | Chỉ đọc trong `check_new_angles`, mà hàm đó `return` ngay nếu `mode != "reply-group"` (`:1584`) — và M5 **vẫn giữ** guard đó (nằm ngoài phạm vi). Nên **M7-D phải tự kiểm "Kiểu 7 không nhắc brand"**, không thừa hưởng được |

Điểm cuối là cái dễ sai nhất: đọc `NO_BRAND_SECTIONS={7}` rồi tưởng `anti` được bảo vệ miễn phí
là sai — nó nằm sau một guard chỉ mở cho `reply-group`.

### B. QA script — gate M7 `anti`

| Rule | Gác gì | Ngưỡng | Độ dài áp dụng |
|---|---|---|---|
| **M7-A** | Draft `anti` thiếu block `**Review xấu:**` | 0 | **mọi độ dài** |
| **M7-B** | Giọng brand / admin / CSKH | 0 item | mọi độ dài |
| **M7-C** | Quy kết động cơ **hoặc** phủ nhận lời kể của người đăng | 0 item | mọi độ dài |
| **M7-D** | Sàn Kiểu 7: <2 item · Kiểu 7 nhắc brand · không phải câu hỏi · mang trải nghiệm/đánh giá ngôi thứ nhất | ≥2 item ở full run; 3 luật per-item áp mọi độ dài | xem dưới |
| **M7-E** | Item **không** thuộc Kiểu 7 mang khung nhượng bộ | 0 item | mọi độ dài |
| **M7-F** | Xếp hạng chung ("khám kỹ nhất") hoặc so sánh viện phi-giá ("bên này ổn hơn chỗ khác") | 0 item | mọi độ dài |

**M7-A định nghĩa `**Review xấu:**` là một BLOCKQUOTE (`>`)** — chi tiết và bảng đo ở §A. Hai
lý do, cả hai đo được:

> **(1) Bản dùng `ORIGINAL_Q_RX` một dòng làm M6 tắt im lặng và sinh item ma.**
> `ORIGINAL_Q_RX` (`:659`) là `^\*\*Câu hỏi gốc:\*\*\s*(.+)$` — `.` không khớp newline nên chỉ bắt
> **dòng 1**. Câu hỏi gốc là một dòng; **review xấu dán vào thì không**. Đo: review 2 dòng, dòng 2
> có `phaco` → `detect_topic(dòng 1)` = `('pre','none')` → `check_topic_fit` early-return `:1679`
> → **M6-B/C không bao giờ chạy**. Và review dán kèm gạch đầu dòng số khớp `ITEM_RX` (`:975`) →
> `parse_items` sinh item `section=None` (đo: 4 item thay vì 2), tính là substantive trong M6-C
> (`:1691`), làm loãng mẫu số 5A/ANTIREP.
>
> **(2) Block "tới dòng trống" là một đường lách ban.** Đo: dán 2 comment seeding thật ngay dưới
> marker, không dòng trống → cả hai lọt vào block, bị excise, **4 họ 5C về 0**. Blockquote bịt
> được vì ranh giới là ký tự `>`, không phải khoảng trắng.

**Block đó bị EXCISE khỏi (a) body của 5C/M3, (b) `parse_items`.** Không excise thì mọi draft
`anti` fail vì chính cái review nó đang trả lời:

> Probe với review verbatim "**cam kết** mổ xong **hết cận** mà giờ e vẫn cận, chỗ khác **rẻ hơn**
> nhiều, dịch vụ **tệ nhất** Sài Gòn, **k đau** gì mà mắt mờ" → **5 FAIL** (`5C dau_claim` ·
> `5C commitment` · `5C cure_myopia` · `5C compare_other_hospital` · `M3`), **không một cái nào
> đến từ 20 comment.** Sau excise: 0 hit cả 4 họ.

Với blockquote thì `parse_items` **tự** không sinh item ma (`ITEM_RX` không khớp dòng `>`), nên
excise chỉ còn cần cho phần (a) — ít cơ chế hơn, ít chỗ sai hơn.

Cùng nguyên tắc `DENY_FREE_RX`/`REFUTE_RX` đã có (`:709`, `:958`): gate không được phạt draft vì
nó **trích dẫn** thứ nó đang phản hồi. `check_bans` giữ nguyên scan toàn văn cho phần còn lại,
nên vi phạm ở preamble/footer vẫn bị bắt.

**M7-B `BRAND_VOICE_RX`** — phải là **khung tự-xưng-thể-chế**, không phải đại từ:
`bệnh viện chúng tôi` · `chúng tôi (xin|rất|thành thật) (lỗi|tiếc|mong|ghi nhận|cảm ơn|xin lỗi)` ·
`xin lỗi quý` · `quý khách` · `quý anh/chị` · `kính gửi` ·
`bộ phận (cskh|chăm sóc khách hàng)` · `ban giám đốc` · `phản hồi từ (bệnh viện|bv)` ·
`rất tiếc về trải nghiệm` · `xin lỗi vì sự bất tiện` · `ghi nhận phản hồi` ·
`tổng đài của chúng tôi`

> Bản đầu để `chúng tôi rất` và `chăm sóc khách hàng` trơn. Đo được hai câu khách thật bị bắt oan:
> "vợ chồng **chúng tôi rất** yên tâm khi mổ bên đây" và "bên đó **chăm sóc khách hàng** tốt lắm".
> Bỏ `chúng tôi` trơn thôi là chưa đủ — phải neo vào **động từ thể chế**. Đã kiểm 8/8.

**M7-C hai tầng: blacklist động cơ (hẹp) + luật CẤU TRÚC phủ nhận ngôi thứ hai.**

`qa/checks.md:104` và `:344` đã ghi thành doctrine: **blacklist fail open**, và hatch M6 từng
phải viết lại thành allowlist vì đúng lý do đó. Bản đầu của M7-C là blacklist phẳng — mà đây lại
là luật quan trọng nhất của mode. Đo được **6 câu lách** không chứa token nào trong list:
"chắc b hên xui gặp hôm đó thôi" · "1 sao mà kể như thật" · "acc mới tinh nhỉ" · "post này lạ
nha" · "b nói vậy chứ e thấy k đúng" · "chắc b gặp hôm đông thôi".

Nên tách hai tầng:

- **Tầng 1 — quy kết động cơ** (blacklist, nhưng chỉ giữ họ không nhập nhằng): `đối thủ` ·
  `nói xấu <bệnh viện>` · `dựng chuyện` · `bịa (chuyện|đặt|ra)` · `vu khống` · `nick ảo` ·
  `\bseeding\b` · `(được|đc) thuê` · `bốc phốt` · `phá hoại` · `dìm hàng` · `làm màu` · `chơi xấu`
- **Tầng 2 — cấu trúc phủ nhận** (đại từ ngôi 2 + nghi ngờ/phủ định lời kể của họ):
  `chắc <b> ...(hên xui|gặp hôm|k đúng|nói quá|dựng)` · `<b> (nói|kể|viết|post) vậy (chứ|mà|nhưng)` ·
  `(kể|nói) như thật` · `(1|một) sao mà` · `acc (mới|ảo|lạ)` · `(post|bài|cmt) này (lạ|sao|k)` ·
  `(k|không) (tin|đúng|thật) (đâu|nha|á)` · `đừng tin` · `k(hông)? có thật`

Và **bỏ `chắc b chưa (đi|khám|mổ)`** khỏi list: nó bắt oan "chắc b **chưa đi khám** lại đúng k ạ?"
— chính là hình dạng Kiểu 7 mà M7-D **bắt buộc phải có**. Hai gate trong cùng một plan kéo ngược
nhau.

**Cũng bỏ `nhầm|lộn` khỏi tầng 2** — đo được ở vòng tự-kiểm thứ hai: nó bắt oan
"chắc b **nhầm** lịch nghỉ trưa r, bên đó nghỉ 12h-13h" và "chắc b **lộn** chi nhánh r, DND Hà Nội
khác DND SG". Đó là **đính chính dữ kiện**, không phải phủ nhận trải nghiệm — và nó là loại comment
hữu ích nhất trên một thread có review sai thông tin. Phân biệt: `hên xui`/`gặp hôm`/`nói quá` phủ
nhận **lời kể**; `nhầm`/`lộn` sửa **một dữ kiện kiểm được**.

Đã kiểm 17/17: 8 câu quy kết (gồm cả 6 câu lách blacklist) FAIL, 9 câu hợp lệ PASS (gồm 2 câu đính
chính dữ kiện và hình dạng Kiểu 7). Sweep per-item 4 file corpus: 0 hit.

**M7-B/M7-C/M7-E/M7-F soi ITEM, không soi toàn văn** — khác §7C (`check_bans` scan cả draft,
`:1812`). Lý do đo được: `\bseeding\b` xuất hiện ở **dòng tiêu đề file** của cả 3 file scratch cũ
(`# Seeding Reply-Group - ...`). Soi toàn văn thì mọi draft đều fail M7-C vì chính cái tiêu đề
skill tự in ra. Sweep per-item trên 4 file corpus: 0 hit cả 3 họ M7-C.

**M7-E `CONCESSION_RX`** — cưỡng chế chốt "né hẳn". **Không reuse `DISSATISFACTION_RX`, và
không phải bản siết nhẹ của nó** — gác theo **khung nhượng bộ**, không gác theo từ vựng triệu chứng.

> Sweep `DISSATISFACTION_RX` lên corpus thật cho thấy tại sao. Cụm `khô mắt` khớp
> `seeding_reply-group_...:23` ("vết mổ nhỏ nên mau lành vs **đỡ khô mắt** hơn mấy gói khác") và
> `seeding_group_...:28` ("e làm văn phòng **sợ khô mắt** quá"); `đông lắm` khớp
> `seeding_group_...:23` ("cuối tuần có **đông lắm** k ạ"). Cả ba là câu hợp lệ — hai câu đầu
> còn đang **nói tốt** cho DND. `đi xa` khớp "e ở Long An lên nên **đi xa** chút mà vẫn đáng".
>
> Nguyên nhân: `DISSATISFACTION_RX` dùng ở hướng **fail-open** (M5 đòi Kiểu 6 *phải* có ≥1 cụm;
> khớp nhầm chỉ là cho qua một draft). M7-E dùng hướng **fail-closed** — khớp nhầm là chặn draft
> đúng. Đảo hướng thì false-positive đổi giá, nên không mượn lại được độ chính xác đo ở hướng kia.
>
> Thứ user từ chối là **hình "ừ đúng, nhưng…"**, không phải từ `khô mắt`. Nên gác đúng hình đó:

- Dấu thừa nhận: `nói thật` · `thật ra thì` · `thú thật` · `công nhận` · `đúng là` ·
  `phải công nhận` · `điểm trừ` · `(k|không) hài lòng` · `chưa hài lòng` · `có điểm` ·
  `nhược điểm` · `mặt hạn chế`
- Mệnh đề cân bằng: `bù lại` · `nhưng bù` · `còn lại thì` · `được cái`
- Ngôi thứ nhất đồng tình: `(e|em|mình|tui|t|tớ|nhà e|nhà mình) (cũng|cx) (chờ|đợi|bị|thấy|gặp)` ·
  `(cũng|cx) (chờ|đợi) (hơi|khá|rất|quá)? lâu` · `(cũng|cx) (hơi|khá|rất|quá)? (đông|chậm|lộn xộn)` ·
  `(hôm|bữa) (e|em|mình|tui|đó|nọ) .{0,20}(chờ|đợi) (hơi|khá|rất|quá)? lâu`

Đã kiểm: 15 ca (9 phải PASS lấy từ corpus thật + 6 hình nhượng bộ phải FAIL) đúng 15/15, và
sweep 4 file scratch cũ = 0 hit.

**M7-E fail-open có chủ đích — và đây là giới hạn phải nói thẳng.** Probe 4 câu nhượng bộ **không
mang cụm nào** trong list, cả 4 đều lách: "hôm e đi thì phải **ngồi đợi tới trưa**, mà bs khám kỹ" ·
"e đi **3 lần mới xong** hết các bước, nhưng đáng" · "**chỗ đó hơi chật**, bs thì ổn" ·
"e **chờ mất buổi sáng**, bs bên DND khám kỹ".

Không đóng được bằng regex: tập "cách nói một điểm dở" là mở, và siết thêm là quay lại đúng lỗi
`DISSATISFACTION_RX` — bắt oan câu hợp lệ. Nên chấp nhận M7-E ở hướng fail-open, khác hẳn M7-C
(vốn phải fail-closed vì hậu quả nặng hơn). Ghi rõ hai lý do:

1. **Hậu quả bất đối xứng.** M7-C lọt → thread đấu khẩu với người khiếu nại, hỏng thật. M7-E lọt →
   một comment cân bằng lẫn vào 20 comment tích cực, tức là **trông thật hơn**. Vi phạm chốt "né
   hẳn" của user, nhưng không phải thiệt hại.
2. **Luật vẫn có trong SKILL.md.** M7-E bắt các hình phổ biến nhất; phần còn lại là prose. Đây là
   đúng mức mà một gate regex làm được, và nói ra thì tốt hơn để người sau tưởng nó kín.

**M7-D — ba luật per-item + một sàn đếm.** Item Kiểu 7 phải: (a) khớp `QUESTION_RX`, (b) không
nhắc `BRAND_RX`, (c) **không mang trải nghiệm/đánh giá ngôi thứ nhất** (`SELF_EXP_RX`). Ba luật
(a)(b)(c) áp **mọi độ dài**; sàn "≥2 item Kiểu 7" chỉ fail ở **full run (≥10 item)** — theo đúng
cách `check_new_angles` đã tách (`:1593` vs `:1580`). Bản đầu ghi "full run" cho cả rule, tức là
draft `anti` 6 item mang Kiểu 7 khen-có-nhắc-brand sẽ không fail gì.

`QUESTION_RX`: `?` · `\bv$` · `k ạ$` · `chưa ạ$` · `nhỉ` · `ntn` · `thế nào` · `bao lâu` ·
`\bbn\b` · `hôm nào` · `bs nào` · `ai biết` · `(có|đã) .{0,20}chưa` · `sao ạ` · `j ạ` · `gì ạ` ·
`mấy giờ` · `khi nào`. Đã kiểm 10/10.

`SELF_EXP_RX` — điều kiện (c), thêm vì `BRAND_RX` chỉ là `\bDND\b|Trương Định` (`:951`):

> Đo được lỗ: "**bên đó ổn lắm**, b khám lại chưa v?" thoả cả (a) và (b) — nó là khen thương hiệu
> có dán câu hỏi ở đuôi, và `bên đó` chính là cách nói SKILL.md §Tone `:269` **khuyến khích**. Sàn
> chống-toàn-khen là phòng tuyến cấu trúc duy nhất còn lại sau khi chốt "né hẳn" bỏ Kiểu 6; nếu
> nó thoả được bằng khen + câu hỏi thì 20/20 comment vẫn tích cực mà gate báo xanh.

`(e|em|mình|tui|nhà e|mẹ e|ba e|con e) .{0,25}(mổ|khám|tái khám)` ·
`(ổn|tốt|hài lòng|khen|yên tâm|khéo|kỹ|nhiệt tình|xịn|đáng) (lắm|quá|thật|ghê|á|nha|r)` ·
`(rất|khá|siêu) (ổn|tốt|hài lòng|yên tâm|khéo|kỹ|nhiệt tình)`

Đã kiểm 9/9: 3 câu khen-dán-câu-hỏi FAIL, 6 câu hỏi thuần PASS. Sweep Kiểu 7 của corpus: 0 hit.

**M7-G `safety_absolute` — vào `BAN_EXTRA`, không vào M7.** Thread phòng thủ về biến chứng mời
gọi đúng một họ claim mà §7C không phủ, và **không gate nào bắn**: "mổ bên đó **an toàn 100%**" ·
"**chưa nghe ai bị biến chứng** cả" · "**k có ca nào bị sao** hết" · "bs mổ mấy nghìn ca rồi
**chưa lỗi ca nào**". Đây là claim an toàn y khoa tuyệt đối, dưới nick giả, trên thread đã có
người khiếu nại — output rủi ro pháp lý cao nhất skill này sinh ra được.

Đặt vào `BAN_EXTRA` (`:911`) thay vì M7 để nó **mode-agnostic** (mọi mode đều nên bị chặn) và
thừa hưởng `count_unrefuted` sẵn có. Đã kiểm 8/8: 5 claim FAIL, 3 câu hợp lệ PASS ("bs giải
thích rõ rủi ro cho e" · "e chưa nghe bs nói gì thêm" · "bs dặn nếu thấy gì bất thường thì gọi
lại"). Sweep per-item 4 file corpus: 0 hit.

**M7-F `SUPERLATIVE_GEN` + `COMPARE_GEN`** — bịt lỗ đo được ở §7C, phát hiện khi chạy draft
`anti` 20 item thật qua `--check`: **draft PASS nhưng có 3 câu vi phạm tinh thần §7C.**

Nguyên nhân là hai regex hiện có hẹp hơn bảng §7C mô tả:

| Regex hiện có | Thực tế chỉ bắt | Không bắt |
|---|---|---|
| `superlative_vn` (`:CLAIM_REGEX`) | `tốt nhất` · `giỏi nhất` · `số 1` | `khám kỹ nhất` · `rõ nhất` · `uy tín nhất q3` · `hiện đại nhất` · `hơn hẳn` · `vượt trội` |
| `compare_other_hospital` | so sánh **giá**: `rẻ hơn` · `bằng nửa` · `so với...viện` | so sánh **chất lượng**: "bên này ổn hơn chỗ cũ" · "viện khác k bằng bên này" |

`anti` là mode dễ trượt nhất vào đúng khoảng trống đó: Kiểu 5 (khách đã đi nhiều viện) mời gọi
so sánh chất lượng, và một thread phòng thủ thì bản năng là xếp hạng. Draft probe của tôi tự
sinh ra "bs giải thích **rõ nhất** với e" mà không gate nào bắn.

**`ASKING_RX` — hỏi không phải là claim.** Sweep corpus tìm ra 2 câu sẽ bị bắt oan:

- `seeding_ads_...:10` "gói **rẻ nhất** bên mình giờ là bao nhiêu thế ad"
- `seeding_group_...:9` "k biết bên dnd bác sĩ nào **khám kỹ nhất** mng nhỉ"

Cả hai là **câu hỏi**, không phải xếp hạng — và cả hai là comment seeding hợp lệ. Tiền lệ trong
repo này: fixture `B3` đã tách "*nêu* phí" khỏi "*hỏi* phí", chỉ câu nêu mới cần footer. M7-F
theo đúng nguyên tắc đó: item khớp `ASKING_RX` (`?` · `nhỉ` · `k ạ` · `nào...nhất` ·
`là bao nhiêu` · `cho e hỏi` · `ai biết` · `thế ad/mn`) được miễn.

Đã kiểm 19 ca: 10 xếp hạng/so sánh phải FAIL + 9 phải PASS (gồm cả 2 câu corpus thật ở trên và
idiom `nhất là` = "especially"). Đúng 19/19; sweep 4 file corpus per-item = 0 hit.

Cụm `đông nhất` bị **loại khỏi** `SUPERLATIVE_GEN` có chủ đích: "chỗ này đông nhất" không phải
lời khen thương hiệu, và nó chồng lấn `CONCESSION_RX`. Một cụm chỉ thuộc một gate.

**M7-D `QUESTION_RX`** — chi tiết đã ghi ở mục M7-D phía trên.

**M6 dùng lại cho `anti`** (không viết bản mới): đổi guard `mode != "reply-group"` thành
`mode not in TOPIC_FIT_MODES`, và cho M6 đọc marker theo mode — `**Câu hỏi gốc:**` cho
`reply-group`, **block** `**Review xấu:**` cho `anti`. Lý do: review xấu về Phaco mà 20 comment
kể chuyện mổ SMILE là **đúng con bug M6 đã dựng để chặn**, chỉ đổi bối cảnh.

`TOPIC_FIT_MODES = {"reply-group", "reply_group", "anti"}` — **có alias `reply_group`.**

> Đo được lỗ có sẵn: `**Mode:** reply_group` + item lạc đề textbook ("bạn qua DND… mình mổ smile
> pro bên đó thoát kính r") trên câu hỏi Phaco → **PASS, không gate nào bắn**. `QUOTA_10_10` mang
> cả hai cách viết (`:870-871`) và `COMMAND_MODES` nhận `reply_group` (`:1019`), nhưng M5/M6 so
> chuỗi đúng `"reply-group"` nên alias đi vòng qua cả hai. Đây là lỗ **có trước**, nhưng lợi ích
> đã nêu của việc refactor sang set chính là "guard đổi từ so sánh chuỗi sang set" — ship cái set
> mà vẫn để lọt một alias đã biết thì mất đúng thứ mình đang mua, và giá là một chuỗi.

**M6-B/C bị SKIP khi review khớp ≥2 nhãn service.** `TOPIC_LADDER` là first-match, viết cho câu
hỏi **một ý định**; review xấu thì kể tràn nhiều dịch vụ.

> Đo: "đi **đo độ cắt kính** ở đây sai độ, mà tư vấn **mổ cận smile pro** cứ đẩy giá" →
> `('pre','kinh')`. Với `SERVICE_DRIFT_TARGETS["kinh"] = ("kx",)` (`:647`) thì **mọi** comment kể
> chuyện mổ SMILE fail M6-B — mà đó là phần lớn khách DND và là giọng chủ đạo của cả example bank.
> M6-C còn đòi ≥60% item mang token `kinh`.

`qa/checks.md:81` đã ghi: over-fire là hướng tệ hơn vì nó dạy người viết nhồi token. Nên review
khớp ≥2 nhãn → coi như `none` cho M6-B/C, **và `note` phải in ra danh sách nhãn đã khớp**.
Review một service ("mẹ tôi mổ phaco ở đây bị viêm" → `phaco`) vẫn bị gác đầy đủ. Đã đo cả 3 ca.

**In nhãn ra là để chống chính cái skip này bị lợi dụng.** Về lý thuyết model có thể **bịa thêm**
một khiếu nại thứ hai vào block quote để tắt M6 — đo được: `phaco` một mình → M6 active; thêm
", mà đo độ cắt kính cũng sai" → `['phaco','kinh']` → M6 skip. Nhưng:

- Block là **văn của user**, không phải model sinh; SKILL.md yêu cầu dán verbatim.
- Block được in nguyên trong output, user đang giữ bản gốc → bịa thêm là **nhìn thấy được**.
- Với `note` in cả nhãn, chính output của `--check` cũng phơi ra chỗ pad.

Nên xếp low-severity: cần model chủ động bịa, và dấu vết hiện ở hai nơi. Không dựng thêm cơ chế
verify (so block với input gốc) vì input gốc không có trong file để đối chiếu.

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

Thêm `anti` vào `COMMAND_MODES` (`:1019`) và list candidate của `detect_mode` (`:1003`), đặt
**cuối** list và **kèm ranh giới từ** cho riêng nó — `anti` là tiếng mạng phổ biến ("bị anti",
"hội anti", "anti fan") nên có thể xuất hiện trong câu hỏi được quote.

**Marker cũng phải là trigger, không chỉ dòng `**Mode:**`.**

> Đo được: draft `anti` có block `**Review xấu:**` và `**Topic:**` nhưng **thiếu dòng
> `**Mode:**`** → `detect_mode` trả `unknown`. Với `unknown` thì `check_new_angles` và
> `check_topic_fit` return ngay, cả họ M7 không chạy, và `--check` in **PASS**. Toàn bộ họ gate
> mới được kích hoạt bởi một dòng do chính model tự viết — đúng hình dạng ISSUE-5 mà script tự ghi
> ở `:876` và `:1517`.

Nên: có block `**Review xấu:**` mà mode detect ra **không phải** `anti` → **FAIL** (mode/marker
mismatch). Fixture: draft có marker, không có dòng Mode → FAIL, không phải PASS.

Đã verify bằng code:

- **29/29 fixture M6** (`SELFTEST_M6` 21 + `_COVERAGE` 3 + `_SENTENCE` 3 + `_NEIGHBOUR` 2) và cả
  3 draft GOOD đều khai `**Mode:** reply-group` **tường minh**. `MODE_RX` (`:982`) thắng head-scan,
  nên đổi guard `check_topic_fit` sang set membership **không thể** reroute fixture nào — đo, không suy luận.
- Head-scan với `anti` thêm vào cuối: `# Seeding Group - DND` + dòng `**Review xấu:**` vẫn ra
  `group`; `# Seeding Anti - DND` ra `anti`.
- Chuỗi `anti` **không** xuất hiện trong 400 ký tự đầu của cả 4 file scratch cũ → không mode nào
  bị đánh cắp routing.

Fixture routing bắt buộc: `/dnd-seeding reply-group "có ai anti bên đó k"` phải vẫn ra
`reply-group` — chữ `anti` trong ngoặc kép là văn của user, không phải lệnh (luật
`parse_command`). Thêm fixture: draft `reply-group` không có dòng `**Mode:**` mà câu hỏi chứa
"anti" → **không** được route sang `anti`.

### D. `qa/checks.md`

Thêm 7 row M7 (A→G) vào bảng gate, một mục M7 giải thích các chỗ dễ nới sai (khung thể chế vs đại
từ · blacklist 2 tầng · excise block review · CONCESSION theo hình không theo từ vựng · ASKING_RX ·
SELF_EXP_RX), và block fixture `H`.

**Sửa luôn 3 con số đã lệch trong `checks.md`** (đo được, không phải do lần này gây ra):
`SELFTEST_COMPARE` thực tế **69** ca chứ không phải 28 (`checks.md:197`, `:58`);
`SELFTEST_TOPICS` **19** ca chứ không phải 15 (`checks.md:240`). Số sai làm luận điểm hồi quy
"N fixture vẫn xanh" không kiểm được — mất fixture với đếm sai trông giống nhau.

## Phạm vi

**Trong:** `SKILL.md` (When to Use · Process Flow Bước 1 · MODE 6 mới · §7A row · Common
Mistakes) · `scripts/qa_seeding.py` (M7 + `BAN_EXTRA.safety_absolute` + `QUOTA_10_10` row +
`TOPIC_FIT_MODES` + routing + fixtures) · `qa/checks.md` (7 row M7 + sửa 3 số đã lệch).

**Ngoài — cố ý không đụng:**

- `fees-promos.md` · `services.md` — không có số mới, không có service mới
- `detect_bucket()` · `free_exam_allowed()` · M2 · footer 2 lớp — dùng lại y nguyên.
  Đã verify trên draft `anti` thật: không nêu phí → PASS; nêu "khám mổ cận free" mà thiếu footer
  → FAIL `FOOTER-A`. Luật phí tự có hiệu lực cho mode mới, không cần code thêm
- `detect_topic()` · `TOPIC_TOK` · `TOPIC_LADDER` · `SERVICE_DRIFT_TARGETS` · `_is_comparison`
  — dùng lại, **không sửa logic**; chỉ mở rộng *mode nào* gọi M6 và thêm luật skip khi review
  khớp ≥2 nhãn
- `EXEMPT` · `BAN_KEYS` · anti-repeat · bảng 7B
- `check_new_angles` (M5) — **guard vẫn chỉ `reply-group` + alias**; không mở cho `anti`
- 8 mode cũ · danh sách bác sĩ

## Lỗ hổng có sẵn — phát hiện khi sweep, KHÔNG sửa lần này

Hai luật trong SKILL.md **chưa có gate nào cưỡng chế ở bất kỳ mode nào**. Đo được trên 4 file
output cũ:

| Luật trong SKILL.md | Vi phạm đo được | Gate |
|---|---|---|
| "Tên riêng LUÔN viết hoa: **DND**, bs **Tuấn**" (§Tone) | `dnd sg` **15 hit** · `bs tuấn` **5 hit** · `dnd sài gòn` 4 hit | không có |
| "Không nhắc bác sĩ ngoài Tuấn / Linh / Hoàng Lan" (§2) | `seeding_reply-group_...:29` viết "**bs hà** mổ cho" — bác sĩ này đã nghỉ | không có |

Cả hai là **lỗ hổng có trước**, áp cho cả 8 mode, không phải do mode `anti` sinh ra — nên để
ngoài phạm vi lần này theo đúng luật "không cleanup lan man ngoài Gate 2". Nhưng ghi ra vì với
mode `anti` thì rủi ro cao hơn hẳn: một thread phòng thủ nhắc tên bác sĩ đã nghỉ là chính xác
thứ người khiếu nại sẽ chụp lại. **Đề xuất làm ở lần improve sau** (gate M8: casing tên riêng +
allowlist bác sĩ), không gộp vào đây.

## Rủi ro regression

| Rủi ro | Chặn bằng |
|---|---|
| **Review verbatim làm mọi draft `anti` fail 5C/M3** | Excise block `**Review xấu:**` khỏi body của 5C/M3. Đo: review verbatim → 5 FAIL (4 họ 5C + M3), sau excise → 0. Fixture 2 chiều: cụm cấm **trong** quote → PASS; **trong** item → FAIL 5C |
| **Excise thành đường lách ban** | Block phải là **blockquote `>`**, không phải "tới dòng trống". Đo: dán 2 item seeding ngay dưới marker không có dòng trống → cả 4 họ 5C về **0** với luật cũ; với blockquote → 2 item đó thành item thật, **cả 4 họ bắn**. Fixture khoá đúng draft đó |
| **Review nhiều dòng làm M6 tắt im lặng** | Blockquote gom đủ mọi dòng `>`. Đo: review 3 dòng có `phaco` ở dòng 2 → `detect_topic` = `phaco` (với luật 1-dòng: `none` → M6 skip) |
| **Review có gạch đầu dòng số sinh item ma** | `ITEM_RX.match("> 1. chờ 2 tiếng")` = `False` → không sinh item ma, **không cần excise cho `parse_items`**. Đo: 2 item, đúng số |
| **Review viết văn trần, không `>`** | `REVIEW_Q_RX` không khớp → **FAIL M7-A** (sai format). Không im lặng bỏ qua |
| **`**Mode:**` thiếu → cả họ M7 tắt mà báo PASS** | Marker cũng là trigger: có `**Review xấu:**` mà mode ≠ `anti` → FAIL mismatch. Fixture: draft có marker, không có dòng Mode → FAIL |
| **M7-C blacklist fail-open** (doctrine `checks.md:104`) | Hai tầng: blacklist động cơ (hẹp) + luật **cấu trúc** phủ nhận ngôi 2. Đo 6 câu lách không chứa token nào → cả 6 bị tầng 2 bắt. Fixture giữ đúng 6 câu đó để ai nới luật là sập |
| **M7-C bắt oan chính hình dạng Kiểu 7 mà M7-D đòi** | Bỏ `chắc b chưa (đi|khám|mổ)`. Fixture: "chắc b chưa đi khám lại đúng k ạ?" → PASS |
| **M7-C bắt oan comment đính chính dữ kiện** | Bỏ `nhầm\|lộn` khỏi tầng 2. Đo: "chắc b **nhầm** lịch nghỉ trưa r, bên đó nghỉ 12h-13h" · "chắc b **lộn** chi nhánh r" → cả hai PASS. Phân biệt: `hên xui`/`nói quá` phủ nhận **lời kể**; `nhầm`/`lộn` sửa **dữ kiện kiểm được** |
| **M7-E lách được bằng cách nói khác** | **Chấp nhận fail-open, có chủ đích.** Đo 4 câu lách ("ngồi đợi tới trưa", "3 lần mới xong", "chỗ đó hơi chật", "chờ mất buổi sáng"). Siết thêm = quay lại lỗi `DISSATISFACTION_RX`. Hậu quả bất đối xứng: M7-E lọt → thread **trông thật hơn**, không phải thiệt hại; M7-C lọt → đấu khẩu, hỏng thật |
| **Multi-service skip bị lợi dụng để tắt M6** | `note` in ra **danh sách nhãn đã khớp**. Đo: `phaco` → M6 active; pad thêm "đo độ cắt kính cũng sai" → `['phaco','kinh']` → skip. Low-severity: block là văn user, in verbatim, user giữ bản gốc → pad hiện ở 2 nơi |
| **M7-D thoả được bằng khen + câu hỏi đuôi** | Thêm điều kiện (c) `SELF_EXP_RX`. Đo: "bên đó ổn lắm, b khám lại chưa v?" thoả cả (a)(b) — `BRAND_RX` chỉ là `\bDND\b\|Trương Định`, mà `bên đó` là cách nói §Tone `:269` khuyến khích. Fixture khoá câu đó → FAIL |
| **M7-D chỉ áp full run → draft ngắn không bị gác gì** | Tách: (a)(b)(c) per-item mọi độ dài, sàn đếm ≥2 chỉ ở full run — theo đúng `check_new_angles` (`:1593` vs `:1580`) |
| **Claim an toàn tuyệt đối không gate nào bắt** | Thêm họ `safety_absolute` vào `BAN_EXTRA` (mode-agnostic, thừa hưởng `count_unrefuted`). Đo 4 câu → 0 gate bắn; sau khi thêm → 8/8 đúng, sweep corpus 0 hit |
| **M6-B over-fire trên review nhiều dịch vụ** | Review khớp ≥2 nhãn → coi như `none` cho M6-B/C + in `note`. Đo: review đo-độ + mổ-cận → `('pre','kinh')`, `SERVICE_DRIFT_TARGETS['kinh']=('kx',)` → mọi comment kể mổ SMILE fail. `checks.md:81`: over-fire là hướng tệ hơn |
| **Alias `reply_group` bỏ qua M5 + M6** | `TOPIC_FIT_MODES` gồm cả `reply_group`. Đo: `**Mode:** reply_group` + drift textbook trên câu hỏi Phaco → PASS hiện tại. Fixture: cùng draft đó → FAIL M6-B |
| **Số fixture trong `checks.md` đã lệch** | Đo lại: `SELFTEST_COMPARE` = **69** (doc ghi 28), `SELFTEST_TOPICS` = **19** (doc ghi 15), `SELFTEST_M6*` tổng = **29** (21+3+3+2). Sửa trong cùng change; acceptance criteria dùng lệnh + `git diff --stat` thay vì con số chép tay |
| **Mở M6 cho `anti` làm hồi quy `reply-group`** | Guard đổi từ so sánh chuỗi sang set `TOPIC_FIT_MODES`. **Đã đo:** 29/29 fixture M6 + 3 draft GOOD đều khai `**Mode:** reply-group` tường minh, `MODE_RX` thắng head-scan → không fixture nào đổi route |
| **M6 đọc marker theo mode → `reply-group` mất marker mà vẫn pass** | M6-A giữ nguyên: `reply-group` thiếu `**Câu hỏi gốc:**` → FAIL ở mọi độ dài. Fixture "reply-group without the marker" phải còn fail đúng M6-A |
| **M7-E false-positive vì mượn `DISSATISFACTION_RX`** | Viết `CONCESSION_RX` riêng, gác **khung nhượng bộ** thay vì từ vựng triệu chứng. Đã sweep corpus: `khô mắt` khớp 2 câu hợp lệ, `đông lắm` 1, `đi xa` 1 — cả bốn PASS với `CONCESSION_RX`. Fixture khoá 4 câu đó |
| **M7-B/C/E/F bắt nhầm chính tiêu đề file skill in ra** | Soi **item**, không soi toàn văn. `\bseeding\b` có trong dòng `# Seeding Reply-Group - ...` của cả 3 file scratch cũ. Sweep per-item 4 file corpus: 0 hit cả 3 họ M7-C |
| **M7-C bắt nhầm câu vô can** | `nói xấu` phải có tân ngữ bệnh viện · `bịa` phải là `bịa chuyện/đặt/ra` · `dìm` phải là `dìm hàng`. Fixture: "e k biết nói xấu ai", "mắt e bị dìm xuống" → PASS |
| **`anti` mang `10/10` mà không có quota row → fail 5A khó hiểu** | Thêm row `QUOTA_10_10["anti"]`. Fixture: `10/10` ở Kiểu 1 → PASS, ở Kiểu 7 → FAIL |
| **20/20 comment đều tích cực = fingerprint §7 dựng ra để chặn** | **Rủi ro còn lại, user đã chốt "né hẳn".** Giảm nhẹ bằng: sàn Kiểu 7 ≥2 item trung tính **có `SELF_EXP_RX` chặn khen ngụy trang** · anti-repeat vẫn áp (>15% warn, >30% block) · §7C + M7-F cấm superlative & so sánh viện · M7-G cấm claim an toàn tuyệt đối · quota `10/10` ≤20%. Không loại bỏ được hết, và ghi ra đây có chủ đích |
| **M7-F bắt oan câu hỏi có chữ "nhất"** | `ASKING_RX` miễn item là câu hỏi, theo tiền lệ fixture `B3` (nêu phí vs hỏi phí). Fixture khoá 2 câu corpus thật: "gói rẻ nhất... là bao nhiêu thế ad" · "bác sĩ nào khám kỹ nhất mng nhỉ" → PASS |
| **M7-F chồng lấn `CONCESSION_RX` ở cụm `đông nhất`** | Loại `đông` khỏi `SUPERLATIVE_GEN`; một cụm chỉ thuộc một gate |
| Sync thiếu runtime (đã xảy ra: 3 runtime 3 version) | Không thêm file mới → mục "Repo & đồng bộ" vẫn 5 path, không sửa |

## Acceptance criteria

Viết dạng **lệnh chạy được**, không dùng con số chép tay — 3 con số trong `checks.md` đã lệch
đúng vì cách viết đó (xem row cuối bảng trên).

**Hồi quy — không được mất fixture nào:**

- [ ] `python3 scripts/qa_seeding.py --selftest` → exit 0
- [ ] `python3 scripts/qa_seeding.py --docsync SKILL.md` → exit 0
- [ ] `python3 scripts/qa_seeding.py --heldout qa/heldout.tsv` → exit 0, 28/28
- [ ] `git diff --stat scripts/qa_seeding.py` — **0 dòng bị xoá** trong các list
      `SELFTEST_M6*` · `SELFTEST_COMPARE` · `SELFTEST_TOPICS` · `SELFTEST_BUCKETS` ·
      `SELFTEST_M5_BAD` (chỉ được thêm)
- [ ] `SELFTEST_DRAFT_GOOD` / `_M5_GOOD` / `_M5_CONTEXT` vẫn PASS, không sửa nội dung

**Routing:**

- [ ] `parse_command('/dnd-seeding anti "bs khám ẩu chờ 2 tiếng")` → `("anti", …)`, payload đúng
- [ ] `parse_command('/dnd-seeding reply-group "có ai anti bên đó k"')` → `("reply-group", …)`
- [ ] Draft `reply-group` **không có** dòng `**Mode:**` mà câu hỏi chứa "anti" → `detect_mode` ≠ `anti`
- [ ] Draft có block `**Review xấu:**` nhưng **thiếu** dòng `**Mode:**` → **FAIL** mode/marker
      mismatch (hiện tại: `detect_mode` = `unknown` → PASS)

**M7-A + blockquote + excise (ca nặng nhất — 6 tiêu chí):**

- [ ] Draft `anti` thiếu block `**Review xấu:**` → FAIL M7-A, kể cả draft 1 item
- [ ] Review viết **văn trần** (`**Review xấu:** bs khám ẩu`, không có `>`) → FAIL M7-A sai format
- [ ] Review verbatim trong quote chứa `cam kết` + `hết cận` + `rẻ hơn` + `k đau` + `tệ nhất`
      → **PASS** (hiện tại: 5 FAIL — 4 họ 5C + `M3`)
- [ ] Cùng những cụm đó nằm **trong item** → **FAIL 5C** (excise không được nới ban)
- [ ] **Anti-smuggle:** 2 item seeding dán ngay dưới marker **không có** `>` → cả 4 họ 5C bắn
      và số item tính đủ (không bị excise nuốt)
- [ ] Review 3 dòng `>` có `phaco` ở dòng 2 → M6 dùng `service=phaco`, không phải `none`
- [ ] Review chứa `> 1.` / `> 2.` → số item **không đổi** so với cùng draft không có review

**M7-B → M7-G:**

- [ ] **M7-B** FAIL: "bệnh viện chúng tôi rất tiếc về trải nghiệm của quý khách" · "chúng tôi xin
      ghi nhận phản hồi" · "bộ phận cskh sẽ liên hệ lại" · "kính gửi quý anh chị"
- [ ] **M7-B** PASS: "vợ chồng chúng tôi rất yên tâm khi mổ bên đây" · "bên đó chăm sóc khách hàng
      tốt lắm" · "điều dưỡng chăm sóc tận tình lắm"
- [ ] **M7-C** FAIL — tầng 1: "chắc đối thủ dựng chuyện thôi" · "nick ảo bốc phốt á" ·
      "b này chắc được thuê" · "dìm hàng bên đó thôi"
- [ ] **M7-C** FAIL — tầng 2 (6 câu lách, không chứa token tầng 1): "chắc b hên xui gặp hôm đó
      thôi" · "1 sao mà kể như thật" · "acc mới tinh nhỉ" · "post này lạ nha" · "b nói vậy chứ e
      thấy k đúng" · "chắc b gặp hôm đông thôi"
- [ ] **M7-C** PASS: "chắc b chưa đi khám lại đúng k ạ?" (hình dạng Kiểu 7 mà M7-D đòi) ·
      "chắc b nhầm lịch nghỉ trưa r, bên đó nghỉ 12h-13h" · "chắc b lộn chi nhánh r, DND Hà Nội
      khác DND SG" (đính chính dữ kiện) · "e k biết nói xấu ai" · "mắt e bị dìm xuống" ·
      draft có tiêu đề `# Seeding Anti - DND`
- [ ] **M7-D** FAIL: full run 20 item không có Kiểu 7 · Kiểu 7 nhắc DND · Kiểu 7 là câu khen ·
      "bên đó ổn lắm, b khám lại chưa v?" trong Kiểu 7 (`SELF_EXP_RX`)
- [ ] **M7-D** draft 6 item có Kiểu 7 nhắc brand → vẫn FAIL (per-item áp mọi độ dài)
- [ ] **M7-D** PASS: "b đi khám hôm nào v?" · "b mổ chưa hay mới khám thôi nhỉ?" · "b cận bn độ r"
- [ ] **M7-E** FAIL: "nói thật hôm e đi cx chờ hơi lâu mà bs bên DND khám kỹ" · "công nhận bên đó
      hơi đông, nhưng bs Tuấn mổ khéo" · "e cx chờ khá lâu, bù lại mổ nhanh"
- [ ] **M7-E** PASS (4 câu từ corpus thật): "vết mổ nhỏ nên đỡ khô mắt hơn mấy gói khác" ·
      "e làm văn phòng sợ khô mắt quá" · "cuối tuần có đông lắm k ạ" ·
      "e ở Long An lên nên đi xa chút mà vẫn đáng"
- [ ] **M7-F** FAIL: "bs giải thích rõ nhất với e" · "bên này khám kỹ nhất" · "chỗ này uy tín nhất
      q3" · "e thấy bên này hơn hẳn chỗ cũ" · "viện khác k bằng bên này"
- [ ] **M7-F** PASS: "gói rẻ nhất bên mình giờ là bao nhiêu thế ad" · "k biết bên dnd bác sĩ nào
      khám kỹ nhất mng nhỉ" · "nhất là mấy hôm trời nắng mắt e mỏi"
- [ ] **M7-G** FAIL: "mổ bên đó an toàn 100%" · "chưa nghe ai bị biến chứng cả" · "k có ca nào bị
      sao hết" · "bs mổ mấy nghìn ca rồi chưa lỗi ca nào"
- [ ] **M7-G** PASS: "bs giải thích rõ rủi ro cho e" · "e chưa nghe bs nói gì thêm" ·
      "bs dặn nếu thấy gì bất thường thì gọi lại"

**M6 dùng lại + hai lỗ có sẵn:**

- [ ] Review xấu về Phaco + comment kể mổ SMILE → FAIL M6-B
- [ ] Review xấu chung chung ("bs thái độ kém, chờ 2 tiếng") → `service=none`, M6-B/C skip, PASS
- [ ] Review khớp **≥2** nhãn ("đo độ cắt kính sai độ… tư vấn mổ cận smile pro cứ đẩy giá") →
      M6-B/C **skip kèm note in ra danh sách nhãn đã khớp**, không FAIL
- [ ] `**Mode:** reply_group` + drift trên câu hỏi Phaco → **FAIL M6-B** (hiện tại: PASS)

**Giới hạn đã biết — ghi vào report, không phải tiêu chí phải đạt:**

- M7-E fail-open: 4 câu nhượng bộ đo được vẫn lách ("ngồi đợi tới trưa" · "3 lần mới xong" ·
  "chỗ đó hơi chật" · "chờ mất buổi sáng"). Chấp nhận có chủ đích, lý do ở §B M7-E
- Multi-service skip có thể bị pad để tắt M6 — low-severity, dấu vết hiện ở output + bản gốc user giữ
- Casing tên riêng + allowlist bác sĩ: không có gate, hoãn sang M8

**Draft mẫu:**

- [ ] Draft `anti` 20 item, 6 kiểu, ghi tại `qa/sample-anti.md`:
      `cat qa/sample-anti.md | python3 scripts/qa_seeding.py --check` → exit 0
- [ ] Draft probe của Gate 1 (chứa "bs giải thích **rõ nhất** với e") → FAIL M7-F; sửa câu đó → PASS
- [ ] `5A`: `10/10` ở Kiểu 1 trong hạn ngạch → PASS; ở Kiểu 7 → FAIL
- [ ] Reviewer APPROVE hoặc stalemate được báo rõ cho user
