---
name: seeding-dnd
description: >
  Tạo danh sách ~20 content seeding ngắn dạng câu hỏi cho Bệnh viện Mắt Quốc tế DND Sài Gòn.
  Trigger khi user gõ "/dnd-seeding", "dnd-seeding", "seeding-dnd", "content seeding dnd", hoặc yêu cầu
  tạo ý tưởng/câu hỏi đi seeding cho DND.
---

# Seeding DND Skill 👁️

Tạo content seeding tự nhiên cho Bệnh viện Mắt Quốc tế DND Sài Gòn (147 Trương Định, Quận 3, TP.HCM) với 4 chế độ khác nhau tùy mục đích sử dụng.

## Mandatory reads

Trước khi sinh nội dung, đọc theo nhu cầu:

| Khi nào | Bắt buộc đọc |
|---|---|
| **Mọi run có thể nêu thông tin phí hoặc số ưu đãi** (kể cả chữ "free", "miễn phí", "tặng gói khám") | **`fees-promos.md`** — chưa đọc thì không được nêu, phải chuyển hotline |
| Trước khi ghi file scratch | chạy `scripts/qa_seeding.py --check` (pipe draft qua stdin) |
| Muốn biết script gác gì / ngưỡng bao nhiêu | `qa/checks.md` |

`fees-promos.md` là **file duy nhất có số tiền**. SKILL.md chỉ có `fee-tier-id` / `promo-key`.

## Repo & đồng bộ

Repo GitHub: https://github.com/minhtranquang1993/dnd-seeding (nhánh `main`).

Layout 4 file: `SKILL.md` · `fees-promos.md` · `qa/` · `scripts/`.

- **Push:** copy cả 4 path vào clone local, commit, push.
- **Pull về máy:** ghi đè cả 4 path vào **cả 3 runtime** (đường dẫn macOS):
  - `~/.claude/skills/dnd-seeding/`
  - `~/.commandcode/skills/dnd-seeding/`
  - `~/.gemini/config/skills/seeding-dnd/`
- Sync thiếu 1 runtime là sinh version skew — đã xảy ra: 3 runtime từng chạy 3 version khác nhau (492 / 392 / 336 dòng).

## When to Use

- `/dnd-seeding group` — Tạo ~28 bài đăng seeding trên group mổ cận
- `/dnd-seeding group story` (hoặc `/dnd-seeding story`) — Nhánh con: chỉ sinh ~15 bài **story kể chuyện**, bỏ 7 góc còn lại
- `/dnd-seeding reply-group "câu hỏi gốc"` — Tạo ~20 comment reply vào bài người khác trên group
- `/dnd-seeding ads` — Tạo ~20 comment seeding dưới bài quảng cáo của mình
- `/dnd-seeding live (nội dung content live)` — Tạo ~20 comment seeding dùng nick ảo để bình luận trên livestream (workshop/hội thảo)
- `/dnd-seeding maps` — Tạo ~20 review Google Maps tiếng Việt (xem MODE 5A)
- `/dnd-seeding maps_foreigner` — Tạo ~20 review Google Maps tiếng Anh, persona người nước ngoài (MODE 5B)
- `/dnd-seeding koc` — Tạo ~20 item giọng KOC/vlogger (MODE 5C)
- `/dnd-seeding` (không tham số) — Mặc định chạy mode `group`

**Luật nhận lệnh:** mode token chỉ được nhận ở **vị trí token đầu tiên**, và chỉ **trước** mọi chuỗi trong ngoặc kép. `k=v` (ví dụ `service=phaco`) luôn là param, không bao giờ là mode. Token đầu không khớp mode nào → chạy `group`, không đoán.
> Vì vậy `reply-group "chị nào review maps cho e"` là mode **reply-group** — chữ `maps` nằm trong câu hỏi của user, không phải lệnh.

---

## Context & Reference Data

### 1. Thông tin Bệnh viện & Địa chỉ
- **Tên:** Bệnh viện Mắt Quốc tế DND Sài Gòn (viết tắt: DND Sài Gòn, DND SG, DND Trương Định).
- **Địa chỉ:** 147 - 147B - 147Bis Trương Định, Võ Thị Sáu, Quận 3, TP.HCM.
- **Hotline:** 0775.147.147 / 1900 8195.
- **Giờ làm việc:** Thứ 2–7: 08h00–17h00, Chủ nhật: 08h00–12h00.

### 2. Đội ngũ Bác sĩ
- **BSNT Bùi Quang Tuấn (Giám đốc):** 13 năm kinh nghiệm, BS Nội trú ĐH Y Dược Huế, 10 năm Trưởng khoa DND Hà Nội trước khi vào làm GĐ DND Sài Gòn. Chuyên Phaco, khúc xạ, dịch kính - võng mạc. Nổi tiếng khéo tay, tận tâm, hàng chục nghìn ca thành công. **Phụ trách mổ chính** (có khám luôn).
- **ThS.BS Hoàng Mai Linh:** >7 năm nhãn khoa. Khám khúc xạ và khám trẻ em. **Không mổ.**
- **PGS.TS.BS Võ Thị Hoàng Lan:** Chuyên gia khúc xạ. Khám phaco. **Không mổ.**

> **Quy tắc dùng tên bác sĩ trong content:** Nội dung nói về **mổ** → chỉ nhắc BS Tuấn. Nội dung nói về **khám** → có thể dùng BS Tuấn, BS Linh, hoặc BS Hoàng Lan. Không nhắc BS.CKII Nguyễn Đăng Dũng (Chủ tịch hệ thống, vẫn mổ nhưng ít có mặt tại DND Sài Gòn — không truyền thông tên bác trong content seeding).

### 3. Công nghệ Phẫu thuật
- **SMILE Pro (VISUMAX 800, Carl Zeiss - Đức):** 8-10 giây/mắt, vết mổ 2mm, định tâm tự động, phục hồi 24h, ít khô mắt.
- **SmartSight (SCHWIND ATOS):** Không tạo vạt, rạch 2mm, bảo tồn giác mạc.
- **SmartSurfACE (SCHWIND AMARIS 750S):** Laser không chạm, không vạt, không hút chân không, phù hợp giác mạc mỏng/sợ dao kéo.
- **Femto-LASIK / Femto-Pro (FEMTO LDV Z8):** Laser tạo vạt chính xác.
- **Phakic ICL:** Đặt thấu kính nội nhãn cho cận nặng (18-20 diop) hoặc giác mạc quá mỏng.
- **CLEAR:** Phương pháp kết hợp riêng DND.
- **Crosslinking:** Làm bền vững giác mạc, kết hợp thêm.

### 4. Ưu đãi SmileDays 2026

> ⛔ Số của mọi ưu đãi dưới đây nằm ở **`fees-promos.md` §3**. Mục này chỉ liệt kê **có ưu đãi gì**, không có số.
> Muốn nêu số → đọc `fees-promos.md` trước, rồi in footer. Chưa đọc → nói "đang có ưu đãi" + chuyển hotline.

- **Khám chuyên sâu 12 bước miễn phí — CHỈ áp dụng cho khám mổ cận / khúc xạ** (gồm lão thị đường laser, Phakic ICL). **KHÔNG áp dụng cho Ortho-K, Phaco, cắt kính, khám bệnh lý, khám tổng quát** — xem §6. (số: `fees-promos.md` §1, tier T0)
- Hỗ trợ chi phí mổ cận + giá trọn gói 2 mắt. (số: `fees-promos.md` §3)
- Cashback khi share hành trình. Thẻ Family. (số: `fees-promos.md` §3)
- **Miễn phí tái khám & đồng hành hậu phẫu — CHỈ cho người đã mổ tại DND.** Người mổ ở viện khác đến tái khám: **có tính phí, không báo số → chuyển hotline.** (tier T-FU · thời hạn ở `fees-promos.md` §3)
- Check-in nhận quà mùa hè. (không có số)

### 5. Dịch vụ khác
- **Ortho-K:** Kính đeo đêm kiểm soát cận thị trẻ em. **Khám Ortho-K CÓ PHÍ** (T2).
- **Phaco:** Mổ đục thủy tinh thể, 3-5 phút/mắt, 500.000+ ca. **Khám Phaco CÓ PHÍ** (T2).
- **Thẩm mỹ mắt:** Cắt mí, lấy mỡ bọng, chỉnh sụp mi. **Khám CÓ PHÍ** (T2).
- **Lão thị:** điều trị được — Presbyond (laser) hoặc Phaco + IOL đa tiêu. Người lão thị **không phải chỉ có đường đi cắt kính**. Khám lão thị theo đường khúc xạ/laser = **T0 free**; nếu ca đó đi đường **Phaco + IOL đa tiêu** thì **không báo phí khám → hotline** (chưa có chính sách).

---

## 6. Phí khám & luật báo phí

> ⛔ **SỐ TIỀN KHÔNG NẰM Ở FILE NÀY.** Mọi con số phí + ưu đãi sống ở **`fees-promos.md`**.
> File này chỉ giữ **pointer**: `fee-tier-id` (T-FU/T0/T1/T2/hotline) và `promo-key` (fu_dnd/fu_other/kx/kinh/pc/or/khac/lt_phaco/ambiguous/none).
>
> **Chưa đọc `fees-promos.md` trong run này → không được nêu bất kỳ thông tin phí nào → chuyển hotline 0775.147.147.**
> Nếu bạn định nói free/0đ/miễn phí/tặng gói khám/trị giá mà chưa mở file đó, bạn đang sắp tái tạo đúng con bug skill này vừa sửa.

| fee-tier-id | Áp cho | Được nói free? |
|---|---|---|
| **T-FU** | Tái khám hậu phẫu, **đã mổ tại DND**, trong 3 năm | ✅ |
| **T0** | Khám mổ cận/viễn/loạn, **lão thị** (đường khúc xạ/laser), **Phakic ICL** | ✅ |
| **T1** | Khám đo độ - cắt kính | ❌ |
| **T2** | Phaco · Ortho-K/kiểm soát cận · võng mạc-dịch kính, glaucoma · thẩm mỹ mắt · khám tổng quát | ❌ |
| **hotline** | Mổ viện khác tái khám · lão thị đường Phaco+IOL · ambiguous · không detect được | ❌ |

Điều kiện CT 50% và số tiền từng tier: **`fees-promos.md` §1**.

### Luật ưu tiên — áp theo thứ tự, dừng ở match đầu tiên

| Ưu tiên | Điều kiện | Kết quả |
|---|---|---|
| **P1** | Có token hậu phẫu (`tái khám`, `sau mổ`, `hậu phẫu`, `mổ ... tháng/năm r`) | Mổ tại DND → **T-FU free**. Mổ viện khác → **có phí, không báo số, hotline** |
| **P2** | Có ý định mổ/khúc xạ (`mổ`, `smile`, `lasik`, `phaco`, `ortho`, `icl`) | Theo service → T0 hoặc T2 |
| **P3** | Chỉ có ý định cắt kính/đo độ | **T1** |
| **P4** | Chỉ nói bệnh trạng (`cận`, `viễn`, `loạn`) mà không nêu ý định | **không báo giá → hotline** |

**Nguyên tắc:** ý định thắng bệnh trạng; hậu phẫu thắng tất cả.

### Bảng nhóm dịch vụ — dùng để phân loại 1 câu hỏi

> Token lấy từ `TOK` trong `scripts/qa_seeding.py`. **File script là nguồn đúng**; bảng này là bản đọc cho người. Sửa token thì sửa script trước, rồi cập nhật bảng.

| promo-key | Token nhận diện | fee-tier-id | Được nói free? |
|---|---|---|---|
| `fu_dnd` | `tái khám`, `sau mổ`, `hậu phẫu`, `mới/vừa/đã mổ`, `mổ ... tháng/năm r` — **và không** có dấu hiệu mổ viện khác | **T-FU** | ✅ |
| `fu_other` | như trên **+** `mổ ... (ở/bên/tại) viện khác`, `mổ ... ở BV Mắt Sài Gòn / Việt Nhật`, `viện khác mổ` | **hotline** | ❌ không báo số |
| `kx` | `mổ cận`, `mổ viễn`, `mổ loạn`, `khúc xạ`, `smile`, `lasik`, `smartsight`, `smartsurface`, `clear`, `femto`, `icl`, `phakic`, `lão thị` | **T0** | ✅ |
| `kinh` | `cắt kính`, `đo độ`, `đo mắt`, `thay kính`, `mua kính`, `kính mới` | **T1** | ❌ |
| `pc` | `phaco`, `thủy tinh thể`, `đục thủy tinh` | **T2** | ❌ |
| `or` | `ortho`, `ortho-k`, `kiểm soát cận`, `kính đêm`, `đeo đêm` | **T2** | ❌ |
| `khac` | `võng mạc`, `dịch kính`, `glaucoma`, `tăng nhãn áp`, `cắt mí`, `sụp mi`, `bọng mắt`, `thẩm mỹ mắt`, `tổng quát` | **T2** | ❌ |
| `lt_phaco` | `lão thị` **+** `phaco`/`thủy tinh thể`/`IOL đa tiêu` | **hotline** | ❌ chưa có chính sách |
| `ambiguous` | chỉ có `cận`/`viễn`/`loạn`/`lão thị`, không nêu ý định (P4) | **hotline** | ❌ |
| `none` | không có token dịch vụ nào | **hotline** | ❌ |

**Ba cái bẫy hay sai:**

1. **`mổ` trơn không tự động là T0.** Phải thử `pc`/`or`/`khac` trước rồi mới cho `mổ` rơi về `kx`. Nếu không thì `mổ phaco` lọt vào T0-free — đúng con lỗi cũ ở `:55`.
2. **`cận` trơn → hotline, nhưng `lão thị` trơn → free.** Nhìn lệch nhưng đúng: lão thị đi đường nào cũng free (cắt kính theo G2-B, laser theo T0), chỉ còn đường phaco là chưa chốt và đã bị chặn riêng. Còn `cận` thì cắt kính **T1 160k** mà mổ lại **T0 free** — hai giá khác nhau nên buộc phải hỏi.
3. **Nói được nhiều nhóm trong 1 câu thì nhóm chặn thắng.** `lão thị` + `phaco` → hotline, không phải free.

### Luật cứng về thông tin phí

- **Luật 0 — chưa đọc `fees-promos.md` trong run này thì không được nêu bất kỳ thông tin phí nào.** Bao gồm cả dạng chữ: `free`, `miễn phí`, `0đ`, `tặng gói khám`, `trị giá ...`. Chưa đọc → chuyển hotline 0775.147.147.
  > Câu luật này cố ý viết "**thông tin phí**", không phải "số phí". Đo trên corpus cũ: claim free dạng **chữ** = **664**, dạng **số `0đ`** = **13**. Tức ~98% claim cần chặn không phải "số phí" theo nghĩa thường — câu gốc gây lỗi ("khám 12 bước free luôn á") không chứa chữ số nào. Viết thành "số phí" là miễn trừ đúng câu cần chặn.
- **Mỗi câu nói khám free phải tự mang ngữ cảnh service** thuộc T0 hoặc T-FU. Không được nói free chung chung.
- Câu có token chặn (`phaco`, `thủy tinh thể`, `ortho`, `kiểm soát cận`, `cắt kính`, `đo độ`, `đo mắt`, `thay kính`, `võng mạc`, `glaucoma`, `cắt mí`, `sụp mi`, `tổng quát`) → **không được nói free**, dù câu đó có nhắc cận/khúc xạ.
- **Ngoại lệ duy nhất:** `lão thị` + `cắt kính` → vẫn free (người lão thị không bị đẩy sang cắt kính). `lão thị` + `phaco` thì **không** — chuyển hotline.
- "Free / 0đ / miễn phí / tặng gói khám / trị giá <số>" đều là **thông tin phí**, chịu luật này y như con số.
- Không detect được service → **không báo giá, chuyển hotline 0775.147.147**.

### Footer khi có nêu phí

Run nào có nêu **thông tin phí** thì in ở cuối file:

```
[fees: <updated-của-fees-promos.md> · <fee-tier-id>]
```

`<updated>` lấy từ frontmatter `updated:` của `fees-promos.md` — **không hardcode ngày ở đây**. Tier lấy từ bucket table.
Ví dụ, nếu file đó đang `updated: 2026-07` và câu nói về Phaco: `[fees: 2026-07 · T2]`.

Nhiều tier trong 1 run → liệt kê cách nhau dấu phẩy: `[fees: 2026-07 · T0, T2]`.

### Tự kiểm trước khi xuất

Chạy: `python scripts/qa_seeding.py --check draft.md` (hoặc pipe draft qua stdin). Script gác item-level: câu nào nói free mà không đủ điều kiện sẽ fail kèm số dòng.

---

## 7. Guardrail nội dung

Mọi số hit dưới đây đo trên 217 file output cũ. Script `--check` gác tự động; số dòng vi phạm in kèm.

### 7A. `10/10` — hạn ngạch THEO MODE

`10/10` không bị cấm tuyệt đối, nhưng 167 hit trên corpus cũ là quá dày. Luật: chỉ góc kể trải nghiệm cá nhân được mang, tối đa **20% số item trong 1 run**.

| Mode | Góc/Kiểu được mang `10/10` | Hạn ngạch |
|---|---|---|
| `group` | Góc 6 (social proof) + Góc 7 (story) | ≤20% item/run |
| `reply-group` | Kiểu 1 (kinh nghiệm bản thân) | ≤20% item/run |
| `ads` | kiểu 5 (chia sẻ đã mổ ở đây) | ≤20% item/run |
| `live` | không góc nào | 0 |
| `maps` | không góc nào | **0** — đo 0 hit, không được miễn |
| `maps_foreigner` | không góc nào | **0** — đo 0 hit, không được miễn |
| `koc` | mọi item | **miễn hạn ngạch** — đo 5 hit, ngoại lệ có chủ đích |

Mẫu số = số item trong run đó, không phải cả file lịch sử.

### 7B. Ngoại lệ `maps` / `koc`

2 mode này viết giọng review Google Maps / KOC nên nhu cầu khác hẳn. Ngoại lệ cấp **theo từng cột đã đo**, không miễn cả gói:

| Mode | Được miễn | KHÔNG được miễn |
|---|---|---|
| `maps` | tone chung, pain-claim, so sánh viện | `10/10`, superlative |
| `maps_foreigner` | tone chung, pain-claim, so sánh viện, `20/20`, superlative EN | `10/10` |
| `koc` | tone chung, pain-claim, `10/10` | so sánh viện, superlative |

**Không viết Example Bank cho `maps`/`maps_foreigner`/`koc` ở bất kỳ đâu trong skill.** Lý do: skill đang chỉ thị model bắt chước example, và chỉ thị đó có hiệu lực đo được (`10/10` 167 hit, `nhẹ nhàng` 281 hit). Một example chứa vi phạm-được-miễn sẽ thành style reference cho **98% traffic** của 4 mode không được miễn gì.

Layout 4-file không có file mode riêng để cách ly example, nên việc chặn lây nhiễm do **script** cưỡng chế thay vì do vị trí file: `--check` áp `EXEMPT` theo mode, nên cùng câu "mổ xong ko đau gì" **pass** ở `maps` và **fail 5C** ở `group`. Fixture `B3d` khoá hành vi đó cho cả 3 mode.

### 7C. Cấm chung — `group` / `reply-group` / `ads` / `live`

| Cấm | Đo được trên corpus cũ | Thay bằng |
|---|---|---|
| Claim hết đau (`k/ko/không/chẳng/chưa đau`) | **121** hit | Cảm nhận dễ chịu/đỡ hơn dự tính — 6-8 biến thể ở mục Tone |
| Superlative VN (`tốt nhất`, `giỏi nhất`, `số 1`) | 16 | Nói cụ thể việc bs làm, không xếp hạng |
| Superlative EN (`top-tier`, `amazing`, `highly recommend`…) | 5 | như trên (chỉ `maps_foreigner` được miễn) |
| `cam kết` / `đảm bảo` kết quả, "khỏi cận vĩnh viễn", "ai cũng mổ được" | — | "bs bảo mắt e đủ điều kiện", "tuỳ tình trạng mắt" |
| So sánh giá/chất lượng vượt trội với viện khác (`rẻ hơn`, `bằng nửa`, `so với viện X`) | **31** hit | Nêu DND như 1 lựa chọn đang xem xét (Góc 8) |
| Mốc hồi phục bằng số cứng | — | Nói theo khoảng: "tầm 2-3 ngày", "mấy tuần đầu" |

### 7D. Anti-repeat

Cụm trong watch list: `nhẹ nhàng` · `ổn áp` · `10/10` · `nhanh gọn` · `máy xịn` · `êm ru` · `nhẹ tênh` · `ngọt xớt` + 8 biến thể mới ở mục Tone.

- Trên **15%** số item trong run dùng cùng 1 cụm → **warn**
- Trên **30%** → **block**, phải sinh lại

Draft phải đưa qua script **trước khi ghi vào scratch** — ghi trước rồi mới check thì script chỉ thấy lịch sử, không gác được cái đang xuất.

---

## Persona Pool

Xáo trộn persona mỗi lần chạy. Không dùng quá 3 câu cùng 1 persona.

| Persona | Cách nói đặc trưng |
|---------|---------------------|
| **Sinh viên** | "e là sv", "ba mẹ cho tiền mổ", "tc eo hẹp" |
| **Dân văn phòng** | "e làm văn phòng", "ngồi máy tính cả ngày", "sợ khô mắt" |
| **Mẹ bỉm** | "con e cận tăng nhanh", "cho bé đi khám ortho-k", "con mới lớp 5" — **khám Ortho-K có phí (T2), persona này KHÔNG được nói khám free** |
| **Người tỉnh lên SG** | "e ở biên hòa/bình dương/long an", "lên sg mổ về luôn trong ngày" |
| **Tiktoker / KOC** | "e muốn quay review", "share hành trình đc cashback k", "làm content" |
| **Người cận nặng** | "e cận 12 độ", "giác mạc mỏng", "bs bảo k bắn laser đc" |
| **Người đã mổ xong** | "mình mới mổ tuần trước", "tái khám đạt 1.5/1.5", "thoát kính r" |
| **Người tìm hiểu nhiều viện** | "e đi khám 2-3 chỗ r", "đang cân nhắc mổ ở đâu", "so sánh giá/công nghệ mấy viện" |

---

## Tone & Writing Style (Áp dụng cho TẤT CẢ modes)

- **Viết tắt tự nhiên (xen kẽ, không dùng hết):**
  `e` (em), `mn`/`mng` (mọi người), `bs` (bác sĩ), `bv` (bệnh viện), `đc` (được), `k`/`ko` (không), `q3` (quận 3), `j` (gì), `r` (rồi), `vs` (với), `cx` (cũng), `tc` (tài chính), `ntn` (như thế nào), `đt` (điện thoại)
  - **Cách gọi bệnh viện phải đa dạng:** xen kẽ "bv mắt" và "bệnh viện mắt" (lúc viết tắt, lúc viết đầy đủ), thỉnh thoảng chỉ nói "bên viện" / "chỗ này" — đừng câu nào cũng "bv".
- **Tên riêng LUÔN viết hoa (dù cả câu viết thường):**
  - Tên bác sĩ: bs **Tuấn**, bs **Linh**, bs Hoàng **Lan** (chỉ viết hoa TÊN, chữ "bs" vẫn để thường). KHÔNG viết "bs tuấn".
  - Thương hiệu: **DND**, **DND SG**, **DND Sài Gòn**, **DND Trương Định** — KHÔNG viết "dnd", "dnd sg".
  - Địa danh/đường: **Trương Định**, **Sài Gòn**, **Hà Nội**.
- **Phong cách:**
  - Chữ thường (lowercase) là chính — trừ tên riêng ở trên
  - Ngắn gọn, 1-2 ý/câu
  - Biểu cảm: `hihi`, `huhu`, `hic`, `ạ`, `mn ơi`, `nha`, `nè`, `hen`, `á`, `lun`
  - **CẤM** từ marketing: "đẳng cấp quốc tế", "đồng bộ hiện đại", "tiên phong", "trải nghiệm đỉnh cao"
  - Thay bằng: "máy xịn", "khang trang", "nhiệt tình", "nhanh gọn", "ổn áp"
- **Không tạo fingerprint mới:** cụm `nhẹ nhàng` đã bị dùng **281 lần** trên 217 file cũ — dùng lại là tự ký tên. Cần 6-8 biến thể xoay vòng, **mỗi cụm ≤15% số item/run**:
  `dễ chịu hơn e tưởng` · `đỡ hơn e nghĩ nhiều` · `k căng như e lo` · `nhanh hơn e tưởng` · `xong lúc nào k hay` · `bớt áp lực hơn hẳn` · `thoải mái hơn e hình dung` · `đơn giản hơn e tưởng`
  - Biến thể mới cũng vào watch list anti-repeat — thay fingerprint cũ bằng fingerprint mới thì không giải quyết được gì
  - Tuyệt đối không viết thành claim hết đau ("k đau", "ko hề đau"): đó là 121 hit đang phải xoá, xem §7
  - Thỉnh thoảng thiếu dấu chấm cuối câu hoặc lỗi chính tả nhẹ
- **Đa dạng cấu trúc:**
  - Đổi chủ ngữ: e, mình, tui, đứa bạn e, bạn e, con e
  - Đổi cách kết: nhỉ, k ạ, thế nào, ai chưa, cho e hỏi, ai biết k
  - Không 2 câu liên tiếp bắt đầu cùng 1 từ

---

# MODE 1: `/dnd-seeding group`

**Mục đích:** Tạo ~28 bài đăng mới trên các group review mổ cận (Hội mổ cận, Hội review SMILE Pro...). Đóng vai người đi tìm hiểu, người đã mổ xong muốn chia sẻ, hoặc người đang kể lại một trải nghiệm/tâm trạng cụ thể.

### Phân bổ 8 góc (tổng ~28 câu)

1. **Góc 1: Hỏi review Bác sĩ (3 câu)** — Hỏi tay nghề/khám của BS Tuấn (mổ chính), BS Linh, BS Hoàng Lan (khám). Ai mát tay, ai khám kỹ.
2. **Góc 2: Chi phí & Ưu đãi (3 câu)** — Hỏi gói khám 12 bước **(chỉ trong ngữ cảnh mổ cận/khúc xạ — xem §6)**, ưu đãi SmileDays, giá trọn gói. **Nêu số → phải đọc `fees-promos.md` + in footer; chưa đọc thì hỏi dạng "đang có ưu đãi gì" không kèm số.**
3. **Góc 3: So sánh Công nghệ (3 câu)** — SMILE Pro vs SmartSight, SmartSurfACE cho mắt mỏng, Phakic ICL cho cận nặng.
4. **Góc 4: Dịch vụ & CSVC (3 câu)** — Quy trình trong ngày, phòng ốc, Ortho-K cho trẻ. **Câu Ortho-K không được nhắc khám free** (Ortho-K = T2 có phí); hỏi phí thì để ngỏ/hotline.
5. **Góc 5: Hậu phẫu (3 câu)** — Hồi phục, khô mắt, tái khám, kiêng cữ.
6. **Góc 6: Social proof — Người đã mổ xong (5 câu)** — Chia sẻ trải nghiệm tích cực, kể chi tiết (BS, thị lực, số ngày hồi phục).
7. **Góc 7: Story kể chuyện (4 câu)** — Bài dài hơn hẳn các góc khác (1 đoạn 4-6 câu, kể mạch trải nghiệm thật). Chủ đề: tâm lý lo lắng/rén trước ngày mổ, buổi khám chuyên sâu 12 bước diễn ra thế nào, băn khoăn trước khi quyết định mổ. Luôn đặt bối cảnh ở DND Sài Gòn/DND Trương Định — không dùng tên bệnh viện khác. Kết bài bằng 1 câu hỏi xin chia sẻ/động lực/kinh nghiệm từ mọi người, không phải câu hỏi thông tin khô khan.
8. **Góc 8: So sánh bệnh viện (4 câu)** — Đóng vai người đang tìm hiểu nhiều nơi: đã khám (hoặc định khám) ở 1-2 viện khác — ví dụ Mắt Sài Gòn, Mắt TPHCM, Việt Nhật — và đang cân nhắc thêm DND Sài Gòn để khám/so sánh giá, công nghệ, cách tư vấn. DND luôn xuất hiện như **1 lựa chọn đang xem xét** bên cạnh viện khác, không phải viện đã chốt hay được khen vượt trội — giữ đúng tinh thần "đang tìm hiểu, chưa quyết".

### Ví dụ mode `group`
- "mn có ai mổ cận chỗ bs Tuấn DND Sài Gòn chưa ạ, cho e xin review tay nghề bác với"
- "e thấy bên DND SG đang có smiledays, tc e eo hẹp mổ đc gói nào tốt nhỉ"
- "mình mổ smile pro bên DND Trương Định tuần trước, bs Tuấn mổ cho, dễ chịu hơn mình tưởng mn, tầm 2-3 ngày là đi làm lại đc r"
- (Góc 7 - story) "e vừa đặt lịch mổ cận tuần sau ở DND Sài Gòn xong mà từ hôm qua đến giờ tự nhiên lại thấy rén 😅. lúc đi khám thì quyết tâm lắm, bs bảo mắt e đủ điều kiện, cũng chọn được phương pháp r. về nhà bố mẹ lại hỏi đủ thứ, có đau k, nhỡ sau này có vấn đề thì sao, làm e cũng dao động theo. anh/chị nào từng mổ ở DND SG r cho e xin ít động lực với ạ, k biết trước ngày mổ mn có bị tâm lý giống e k"
- (Góc 7 - story) "mn cho e xin review mổ cận ở DND Sài Gòn với ạ 🙏 tuần trước e đi khám chuyên sâu trước mổ ở đây, bình thường e khá sợ khám mắt vì nhìn máy móc là run, nhưng buổi khám k căng như e lo, mất khá nhiều tg vì qua nhiều bước, có nhỏ thuốc rồi đợi đo lại nên gần cả buổi sáng. bs giải thích tình trạng mắt e khá kỹ và tư vấn e đủ điều kiện mổ smile pro, nhưng e vẫn chưa chốt ngay vì đây là quyết định lớn. ai mổ ở DND SG r cho e xin ít review: thị lực sau mổ ổn k, hồi phục ntn, bệnh viện theo dõi hậu phẫu có kỹ k ạ, e cảm ơn mn nhiều"
- (Góc 8 - so sánh viện) "e cận 5 độ loạn 1, mới khám ở mắt sg đc tư vấn femto pro với smile pro r, giờ muốn khám thêm chỗ khác xem sao. có ai khám ở DND Sài Gòn r k, chi phí khám bên đó tầm nhiêu, có nên qua khám thêm 1 vòng trước khi chốt k ạ"
- (Góc 8 - so sánh viện) "e đang phân vân giữa mắt tphcm với DND Trương Định q3, chưa biết nên khám ở đâu trước, ai đi khám cả 2 chỗ r so sánh giúp e với"

---

# MODE 1B (sub-mode): `/dnd-seeding group story` (hoặc `/dnd-seeding story`)

**Mục đích:** Nhánh con của Mode `group`. Chỉ sinh **~15 bài story kể chuyện** — KHÔNG sinh 7 góc còn lại của Mode 1. Dùng khi chỉ cần content dạng kể chuyện dài để đăng group.

**Kích hoạt:** tham số `story` đứng sau `group` (`group story`), hoặc gõ tắt `story` ngay sau lệnh. Nếu chỉ có `group` (không kèm `story`) → chạy Mode 1 đầy đủ 8 góc như thường.

### Đặc trưng story (kế thừa Góc 7)
- **Bài dài hơn hẳn comment thường:** mỗi bài 1 đoạn 4-6 câu, kể mạch trải nghiệm thật, có cảm xúc.
- **Luôn đặt bối cảnh ở DND Sài Gòn / DND Trương Định** — không dùng tên bệnh viện khác làm nơi mổ (trừ chủ đề 7/15 có thể nhắc viện khác như nơi "đã đi khám trước" rồi mới tới DND).
- **Kết bài bằng 1 câu hỏi xin chia sẻ/động lực/kinh nghiệm** từ mọi người — KHÔNG phải câu hỏi thông tin khô khan.
- Áp dụng đủ Tone & Writing Style + Persona Pool + quy tắc tên bác sĩ như các mode khác.

### Pool 19 chủ đề — xáo trộn mỗi lần chạy, chọn ~15 câu, phân bổ ĐỀU 4 nhóm (~3-4 câu/nhóm)

**Nhóm A — Trước mổ (tâm lý/quyết định):**
1. Tâm lý lo lắng/rén trước ngày mổ
2. Buổi khám chuyên sâu 12 bước diễn ra thế nào
3. Băn khoăn trước khi quyết định mổ
8. Vượt nỗi sợ đụng vào mắt (sợ dao kéo, nhìn máy là run)
9. Chần chừ nhiều năm mới quyết mổ, tiếc sao không làm sớm

**Nhóm B — Sau mổ (hồi phục/đổi đời):**
4. Hành trình hậu phẫu — hồi phục ngày 1/ngày 3, sáng mắt dần
5. Kể chuyện thoát kính sau nhiều năm đeo kính dày
17. Cuộc sống đổi sau mổ (bơi, thể thao, trang điểm, sáng dậy k quờ tìm kính)
10. Cảm động vì được bs/điều dưỡng chăm sóc, dặn dò, hỏi thăm sau mổ

**Nhóm C — Theo đối tượng:**
11. Sinh viên dành dụm tiền mổ, "đầu tư cho đôi mắt"
12. Người tỉnh lên SG mổ trong ngày (Biên Hòa/Long An/Bình Dương)
13. Mẹ có con cận đưa đi Ortho-K, tâm sự làm mẹ — **story này KHÔNG được nhắc khám free** (Ortho-K = T2)
14. Nghề cần bỏ kính (công an/quân đội/phi công/tiếp viên)
6. Dẫn người thân đi mổ/khám (góc người nhà)
16. Kể thay ba mẹ mổ Phaco (đục thủy tinh thể, mắt sáng lại)

**Nhóm D — Y khoa đặc biệt / cách biết đến DND:**
15. Cận nặng từng bị từ chối laser → được tư vấn Phakic ICL
7. Quá trình chọn viện & chốt DND SG
18. Tình cờ biết DND (bạn giới thiệu / xem livestream / lướt fanpage)
19. Tiktoker/KOC quay hành trình review, nhận cashback khi share

### Cách xuất kết quả (mode story)
In **gộp theo 4 nhóm A/B/C/D**, mỗi nhóm là 1 tiêu đề, dưới liệt kê các bài story của nhóm đó. Mỗi lần chạy chọn chủ đề khác nhau trong pool để không trùng ý.

### Ví dụ mode `story`
(2 ví dụ này chính là style Góc 7 — viết bài MỚI mỗi lần, chỉ tham khảo giọng)
- (Nhóm A) "e vừa đặt lịch mổ cận tuần sau ở DND Sài Gòn xong mà từ hôm qua đến giờ tự nhiên lại thấy rén 😅. lúc đi khám thì quyết tâm lắm, bs bảo mắt e đủ điều kiện, cũng chọn được phương pháp r. về nhà bố mẹ lại hỏi đủ thứ, có đau k, nhỡ sau này có vấn đề thì sao, làm e cũng dao động theo. anh/chị nào từng mổ ở DND SG r cho e xin ít động lực với ạ, k biết trước ngày mổ mn có bị tâm lý giống e k"
- (Nhóm B) "mình đeo kính từ năm lớp 6, tới giờ hơn 10 năm cận 6 độ, sáng nào dậy cũng quờ quạng tìm kính mới thấy đường 🥲. tuần trước mổ smile pro bên DND Trương Định, bs Tuấn mổ cho, sáng hôm sau mở mắt ra nhìn rõ luôn mà cứ ngỡ đang mơ. giờ đi tắm, bơi, ngủ dậy đều nhìn rõ, cảm giác lạ lắm mn ạ. ai mổ xong r có bị 'quen tay' đưa lên dụi mắt tìm kính giống mình k huhu"

---

# MODE 2: `/dnd-seeding reply-group "câu hỏi gốc"`

**Mục đích:** Tạo ~20 comment reply vào bài viết của người khác trên group. Đóng vai **người từng trải nghiệm** hoặc **người cũng đang tìm hiểu** mà biết DND, dẫn dắt tự nhiên về DND Sài Gòn.

### Cách hoạt động
- AI đọc `"câu hỏi gốc"` mà user paste vào
- Phân tích ý chính của câu hỏi (hỏi về giá? về BS? về công nghệ? về hồi phục?)
- Sinh ra ~20 comment reply phù hợp ngữ cảnh, tự nhiên

### 10 kiểu reply — chọn theo ngữ cảnh câu hỏi gốc, tổng ~20 item

In section header đúng dạng `### Kiểu N: <tên>` — QA script attribute item theo header này để chấm hạn ngạch.

**Không phải run nào cũng dùng đủ 10 kiểu.** Đọc câu hỏi gốc rồi chọn kiểu nào trả lời đúng thứ người ta đang hỏi; kiểu không hợp thì bỏ, dồn số item sang kiểu hợp.

| Kiểu | Bắt buộc? | Khi nào dùng |
|---|---|---|
| 1-5 | tuỳ ngữ cảnh | Kiểu nào trả lời đúng câu hỏi gốc |
| **6** (mixed) | ✅ **luôn có ≥1** | Mọi thread — sàn chống "reply toàn khen" |
| **7** (hỏi lại, k nhắc DND) | ✅ **luôn có ≥1** | Mọi thread — sàn để thread trông như thread thật |
| 8 (đính chính) | tuỳ ngữ cảnh | **Chỉ khi** bài gốc có nhận định sai cần sửa. Bài hỏi giá thuần → bỏ |
| 9 (quy trình) | tuỳ ngữ cảnh | Chỉ khi người ta hỏi/lo về quy trình, thời gian, hậu cần |
| 10 (đang cân nhắc) | tuỳ ngữ cảnh | Chỉ khi bài gốc đang so sánh nhiều chỗ hoặc chưa quyết |

Kiểu 6 và 7 là sàn cứng vì chúng không phải "nội dung" — chúng tồn tại để thread không toàn khen. Bỏ 2 kiểu này là quay lại đúng fingerprint mà guardrail §7 dựng ra để chặn. QA script fail nếu run ≥10 item mà thiếu 1 trong 2.

**5 kiểu gốc (giữ nguyên cú pháp cũ):**

1. **Trả lời từ kinh nghiệm bản thân** — "mình cx từng bị vậy, cuối cùng chọn mổ bên DND SG..."
2. **Gợi ý/Recommend tự nhiên** — "bạn thử qua DND Trương Định q3 khám xem, mình thấy ổn lắm" (chỉ thêm chữ *free* khi câu hỏi gốc thuộc T0/T-FU — xem §6)
3. **Bổ sung thông tin hữu ích** — "theo mình biết thì bên DND SG đang có smiledays nè, b ib hỏi thử"
4. **Đồng cảm + dẫn dắt** — "e cx sợ vậy nè, hôm mổ thấy dễ chịu hơn e tưởng, bs Tuấn bên DND SG khéo tay lắm"
5. **Tag bạn / Rủ đi cùng** — "cái này giống case đứa bạn mình mổ bên DND SG nè, để mình hỏi rồi rep lại"

**5 kiểu MỚI — lý do: 5 kiểu gốc đều nghiêng tích cực, thread toàn khen là fingerprint dễ nhận:**

6. **Review có điểm chưa hài lòng (mixed)** — BẮT BUỘC có thật ≥1 điểm chưa hài lòng, không phải khen ngụy trang. Điểm dở được phép nói: chờ lâu/phòng đông, khô mắt mấy tuần đầu, chi phí cao hơn dự tính, đi xa bất tiện, quên hỏi bs nên phải gọi lại, nhỏ thuốc nhiều bước dễ quên. Kết: vẫn không quay xe, nhưng **không xoá điểm dở**.
7. **Hỏi lại người đăng (không recommend, KHÔNG nhắc DND)** — chỉ hỏi thêm cho rõ: độ cận bao nhiêu, giác mạc dày bao nhiêu, đã khám chưa. Kiểu này **cấm nhắc DND** — nó tồn tại để thread trông như thread thật.
8. **Đính chính nhầm lẫn kỹ thuật** — sửa nhẹ nhận định sai trong thread (vd "mổ xong hết cận vĩnh viễn", "cận nặng k mổ được", "mổ xong là khỏi đeo kính mãi"). Giọng góp ý, không dạy đời, không quảng cáo. Bản thân câu đính chính **không được chứa** claim bị cấm.
9. **Chi tiết quy trình/hậu cần** — thực dụng: mất bao lâu, có cần người đưa về, nghỉ mấy ngày, mang theo gì, nhỏ thuốc bao lâu. Số liệu quy trình thì được; **mốc hồi phục phải nói theo khoảng**, không số cứng.
10. **Người đang cân nhắc, chưa mổ** — chưa trải nghiệm, đang xem 2-3 chỗ. Kiểu này **không được** claim kết quả sau mổ (chưa mổ thì không có kết quả) và không mang `10/10`.

### Quy tắc riêng mode `reply-group`
- Phải **liên quan trực tiếp** đến câu hỏi gốc, không trả lời lạc đề
- Không nhắc DND quá lộ liễu — tối đa nhắc tên 1 lần/comment, có comment chỉ nói "chỗ mình mổ bên Trương Định q3" mà không nhắc DND
- Một số reply **không nhắc DND** — chỉ trả lời câu hỏi thuần túy, tạo cảm giác tự nhiên cho cả thread. Kiểu 7 luôn thuộc nhóm này
- **Độ dài: đúng 1 câu/reply.** Đây là reply để copy-paste, không phải bài đăng. Ngoại lệ duy nhất: **Kiểu 6** (phải mang điểm dở thật) và **Kiểu 9** (thông tin hậu cần) được tối đa 2 câu.
  > Đừng viết reply 3-4 câu kể cả khi thấy "còn nhiều thứ hay để nói". Câu thứ 2 trở đi làm reply trông như bài PR, không như người thật gõ trên điện thoại. Thà cắt ý còn hơn dài.
- **`10/10` chỉ được xuất hiện ở Kiểu 1**, tối đa 20% số item trong run (~4/20). Kiểu 6-10 không mang `10/10` — xem §7

### Ví dụ mode `reply-group`
Giả sử câu hỏi gốc: _"mọi người ơi cận 5 độ loạn 2 độ mổ smile pro có ổn không ạ"_

> Để ý độ dài: **mọi ví dụ dưới đây đúng 1 câu**, trừ Kiểu 6 và 9 là 2 câu. Đây là mức cần bám — không phải mức tối thiểu để nới ra.

- (Kiểu 1) "case mình cx tương tự bạn nè, cận 4.5 loạn 1.75, mổ smile pro bên DND SG, giờ 10/10 r nha" ← `10/10` hợp lệ vì đây là Kiểu 1 và còn trong hạn ngạch 20%
- (Kiểu 2) "cận 5 loạn 2 thì làm smile pro đc bạn ơi, quan trọng là giác mạc đủ dày nên đi khám chuyên sâu trước đi"
- (Kiểu 2) "bạn qua DND Trương Định q3 khám 12 bước trước mổ cận free luôn á" ← chữ *free* hợp lệ vì câu tự mang ngữ cảnh **mổ cận** (T0). Bỏ 2 chữ "mổ cận" ra là câu này vi phạm §6.
- (Kiểu 4) "e cx loạn 2 độ nè, bs Tuấn bên DND SG bảo e làm smile pro đc"
- (Kiểu 3) "loạn 2 độ thì smile pro máy visumax 800 có OcuLign bù trừ trục loạn thị đó bạn"
- (Kiểu 6 - mixed) "mình mổ smile pro bên DND SG cx cận 5 loạn 2, nói thật hôm khám đông nên chờ hơi lâu với khô mắt mấy tuần đầu hơi phiền. còn lại thì mình k tiếc tiền bỏ ra" ← 2 câu, có điểm dở THẬT (đông + chờ lâu + khô mắt), không xoá đi
- (Kiểu 7 - hỏi lại, k nhắc DND) "bạn khám chuyên sâu chưa v, giác mạc bạn dày bn r?"
- (Kiểu 8 - đính chính) "cho mình góp ý nhẹ, mổ khúc xạ là chỉnh độ hiện tại thôi chứ k phải khỏi cận mãi mãi nha"
- (Kiểu 9 - quy trình) "hôm mình đi thì buổi khám mất gần cả buổi sáng vì nhỏ thuốc giãn xong phải đợi đo lại. nên nhờ ai chở về nha, mắt nhoè k tự đi đc" ← 2 câu, mốc hồi phục nói theo khoảng
- (Kiểu 10 - đang cân nhắc) "e cx đang tìm hiểu giống bạn, tính khám thêm DND Trương Định q3 nữa cho có cái so"

---

# MODE 3: `/dnd-seeding ads`

**Mục đích:** Tạo ~20 comment seeding dưới bài quảng cáo (Facebook Ads) của chính mình, dùng nhiều nick ảo. Mục tiêu: tạo engagement, social proof, kéo người thật comment theo.

### 6 kiểu comment (phân bổ đều)

1. **Hỏi giá / Hỏi chi tiết (4 câu)** — "ad ơi mổ smile pro trọn gói bao nhiêu ạ", "giá này áp dụng đến bao giờ ạ"
2. **Hỏi lịch / Đăng ký (3 câu)** — "e muốn book lịch khám cuối tuần đc k ạ", "ad cho e xin sđt tư vấn vs ạ"
3. **Tag bạn bè (3 câu)** — "@tên ơi cái này hay nè", "tag đứa bạn cận 10 độ vào đây 😂"
4. **Bày tỏ quan tâm (3 câu)** — "ôi ưu đãi này thiệt hả", "e tính mổ lâu r mà chưa dám, giờ thấy ưu đãi ngon quá"
5. **Chia sẻ đã mổ ở đây (4 câu)** — "e mổ bên này r, bs Tuấn mổ cho, ổn lắm mn", "mình mổ tháng trước r, recommend luôn nha"
6. **Hỏi thêm về trải nghiệm (3 câu)** — "ai mổ r cho e xin review với", "mổ có đau k mng", "bao lâu đi làm lại đc ạ"

### Quy tắc riêng mode `ads`
- Comment **ngắn gọn hơn** mode group — 1-2 câu, đúng kiểu comment Facebook Ads
- Một số comment chỉ là emoji hoặc tag bạn — tạo engagement tự nhiên
- **Không comment quá chuyên nghiệp** — phải giống người thật lướt thấy ads rồi comment nhanh
- Có vài comment hỏi giá/hỏi chi tiết đơn giản để admin (chính mình) reply lại, tạo tương tác 2 chiều
- Vài comment **chỉ tag bạn** kèm emoji hoặc 1 từ ngắn: "@bạn nè", "@tên check cái này đi"

### Ví dụ mode `ads`
- "ad ơi mổ smile pro trọn gói hết bao nhiêu ạ"
- "e muốn đk khám mổ cận free đc k ạ, cuối tuần có làm k ad" ← có chữ **mổ cận** nên chữ *free* mới hợp lệ
- "@LanNguyen ê m cận nặng vậy đi khám chỗ này đi 😂"
- "ôi ưu đãi này thật á, rẻ hơn e tưởng nhiều 😳"
- "mình mổ chỗ này tháng trước r nè mn, bs Tuấn mổ xong lúc nào k hay, giờ 10/10 r, recommend lun 👍" ← `10/10` hợp lệ ở mode ads (kiểu 5), giữ ≤20% số item
- "mổ có đau k mng 🥲"
- "e ở bình dương lên mổ trong ngày về luôn đc k ạ"
- "đã inbox ad r ạ ❤️"
- "e tính mổ lâu r mà sợ, giờ thấy ưu đãi ngon quá tính liều lun hihi"
- "@MinhTran xem cái này đi bro"

---

# MODE 4: `/dnd-seeding live (nội dung content live)`

**Mục đích:** Tạo ~20 comment seeding dùng nick ảo để bình luận trực tiếp trên livestream (workshop/hội thảo của DND). Đóng vai người xem live thật, comment real-time tạo không khí sôi động, kéo người thật tương tác theo.

### Cách hoạt động
- AI đọc nội dung content live user paste vào (nguyên văn caption/thông tin sự kiện)
- Tự detect từ nội dung: tên + chức danh bác sĩ diễn giả (không giới hạn BS Tuấn/Linh/Hoàng Lan — có thể là bác sĩ chi nhánh khác như DND Hà Nội), tên/chủ đề hội thảo, loại hội thảo (mổ cận, kiểm soát cận thị trẻ em, phaco...), ưu đãi nếu content có nhắc
- Sinh ~20 comment phù hợp, dùng đúng tên bác sĩ/chủ đề detect được — không bịa thêm bác sĩ ngoài nội dung được cung cấp

### 6 nhóm comment (phân bổ đều ~20 câu)
1. **Hỏi/khen bác sĩ diễn giả (4 câu)** — Hỏi tay nghề, khen chuyên môn dựa trên tên + chức danh bác sĩ detect được trong content.
2. **Hỏi ưu đãi/chi phí (3 câu)** — Hỏi ưu đãi khi tham gia workshop, chi phí mổ/khám liên quan chủ đề buổi hội thảo.
3. **Hỏi về loại hội thảo (4 câu)** — Hỏi hội thảo khác cùng chuỗi chương trình DND (VD: hội thảo mổ cận người lớn, hội thảo kiểm soát cận thị trẻ em, hội thảo phaco...), có tổ chức thường xuyên không, khi nào có buổi tiếp theo.
4. **Hỏi lịch/cách đăng ký (3 câu)** — Hỏi cách đăng ký tham gia, còn nhận đăng ký không, có online không hay phải đến trực tiếp.
5. **Tag bạn bè đi cùng (3 câu)** — "@tên ơi vào coi nè", tag người quen đang cận/quan tâm chủ đề.
6. **Cảm xúc quan tâm/mong chờ (3 câu)** — Bày tỏ hào hứng, đang theo dõi live, mong được giải đáp thắc mắc.

### Quy tắc riêng mode `live`
- Văn phong giống mode `ads`: ngắn 1-2 câu, có emoji, tự nhiên như bình luận real-time khi đang xem trực tiếp
- Dùng ngữ cảnh "đang xem live", "vừa vào coi", "đang nghe bs nói" — không dùng từ ngữ kiểu bài post/bài viết
- Tên bác sĩ/chủ đề hội thảo phải khớp đúng nội dung content live được cung cấp, không tự thêm bác sĩ khác
- **Comment hỏi ưu đãi/chi phí (nhóm 2) chịu luật §6:** hội thảo kiểm soát cận thị trẻ em / Ortho-K / Phaco đều là **T2 có phí** — không comment "khám free" cho các chủ đề này. Chỉ chủ đề **mổ cận/khúc xạ** mới được nhắc gói khám 12 bước free.

### Ví dụ mode `live`
(Giả sử content live nhắc BS.CKII Phạm Thị Hằng và workshop SMILE Pro)
- "bs Hằng nói dễ hiểu quá, nghe xong hiểu rõ luôn á"
- "cho e hỏi bs Hằng khám ở DND Sài Gòn hay chỉ ở Hà Nội ạ"
- "tham gia workshop này có đc ưu đãi gì k ạ 👀"
- "DND có hay tổ chức workshop kiểm soát cận thị cho trẻ em k ạ, con e mới lớp 5 cận tăng nhanh"
- "hội thảo mổ phaco thì bên DND có tổ chức k ạ, mẹ e bị đục thủy tinh thể"
- "muốn đăng ký tham gia thì làm sao ạ, còn nhận k"
- "có phải đến trực tiếp k hay xem online cũng đk ạ"
- "@ThaoNguyen ơi vào coi nè, đúng cái m đang tìm hiểu"
- "đang xem mà thấy đúng vấn đề mình đang gặp luôn 😍"
- "hồi hộp quá, đang nghe bs nói mà thấy đúng tình trạng mắt mình"

---

# MODE 5: `/dnd-seeding maps` · `maps_foreigner` · `koc`

3 mode này viết giọng **review** (Google Maps / KOC) nên nhu cầu khác 4 mode trên. Chúng có **ngoại lệ guardrail** — nhưng ngoại lệ cấp **theo từng cột đã đo**, không miễn cả gói. Xem §7B.

> ⚠️ **Luật phí KHÔNG có ngoại lệ mode nào.** `maps`/`koc` vẫn chịu Luật 0, M2 và footer đầy đủ như mọi mode khác. Nêu thông tin phí mà chưa đọc `fees-promos.md` → vẫn fail.

## MODE 5A: `maps` — review Google Maps tiếng Việt

**Dùng khi:** cần review đặt trên Google Maps profile của bv.

- ~20 review, mỗi cái 2-4 câu, dài hơn comment seeding thường
- Giọng người thật đã đi khám/mổ xong, kể lại trải nghiệm cụ thể: chỗ đậu xe, thời gian chờ, nhân viên hướng dẫn, bs giải thích
- Nêu chi tiết định vị được: `147 Trương Định`, `Q3`, tên bs (theo quy tắc §2)
- Persona xoay như Persona Pool, nhưng **không dùng persona Tiktoker/KOC** ở mode này (để dành cho `koc`)

**Được miễn:** claim hết đau · so sánh viện khác
**KHÔNG miễn:** `10/10` (đo 0 hit — không có nhu cầu) · superlative VN/EN · mọi luật phí

## MODE 5B: `maps_foreigner` — review Google Maps tiếng Anh

**Dùng khi:** cần review tiếng Anh từ persona người nước ngoài sống ở VN.

- ~20 review tiếng Anh, giọng expat/du khách, tự nhiên không dịch cứng
- Nhắc được: giao tiếp tiếng Anh của staff, thủ tục cho người nước ngoài, vị trí trung tâm Q3
- Không viết tiếng Việt lẫn vào

**Được miễn:** claim hết đau · so sánh viện khác · `20/20` · superlative EN
**KHÔNG miễn:** `10/10` (đo 0 hit) · superlative VN · mọi luật phí

## MODE 5C: `koc` — review KOC / vlogger

**Dùng khi:** cần comment/caption giọng KOC đang làm content về hành trình mổ.

- ~20 item, giọng người đang quay vlog/làm content, có nhắc việc ghi hình
- Được dùng persona Tiktoker/KOC làm chủ đạo
- Nhắc cashback share hành trình được, nhưng **không nêu số** nếu chưa đọc `fees-promos.md`

**Được miễn:** claim hết đau · `10/10` (đo 5 hit — có nhu cầu thật)
**KHÔNG miễn:** so sánh viện khác (đo 0 hit) · superlative VN/EN · mọi luật phí

## Vì sao không có Example Bank cho 3 mode này

Có chủ đích. Skill này đang chỉ thị model **bắt chước example**, và chỉ thị đó có hiệu lực đo được (`10/10` 167 hit, `nhẹ nhàng` 281 hit trên corpus cũ). Một example chứa vi phạm-được-miễn nằm trong file dùng chung sẽ thành style reference cho **98% traffic** của 4 mode còn lại — chúng không được miễn gì.

Nên 3 mode này mô tả **bằng luật**, không bằng câu mẫu. Muốn biết giọng thì đọc 3 file mẫu gốc trong scratch, đừng copy example vào đây.

Việc chặn lây nhiễm do **script** cưỡng chế, không do vị trí file: `--check` áp `EXEMPT` theo mode, nên cùng một câu "mổ xong ko đau gì" **pass** ở `maps` và **fail 5C** ở `group`. Fixture `B3d` trong `--selftest` khoá hành vi đó.

---

## Process Flow

### Khi nhận lệnh `/dnd-seeding [mode] [tham số]`:

**Bước 1: Xác định mode** (check theo thứ tự này)

Chỉ đọc **token đầu tiên**, và chỉ phần **trước** dấu ngoặc kép đầu tiên. Bỏ mọi `k=v` ra làm param trước khi so.

- `group story` HOẶC `story` (đứng ngay sau lệnh) → chạy **Mode 1B** (sub-mode story), CHỈ sinh ~15 bài story
- `group` (không kèm `story`) hoặc không có tham số → chạy Mode 1 đầy đủ 8 góc
- `reply-group "..."` → chạy Mode 2, parse câu hỏi gốc từ dấu ngoặc kép
- `ads` → chạy Mode 3
- `live (nội dung content live)` → chạy Mode 4, parse toàn bộ nội dung live, detect bác sĩ/chủ đề/ưu đãi từ đó
- `maps` / `maps_foreigner` / `koc` → chạy Mode 5A / 5B / 5C, áp ngoại lệ §7B đúng theo mode
- token đầu không khớp mode nào → chạy `group`. **Không suy diễn mode từ chữ trong câu hỏi của user.**

**Bước 2: Chọn Persona & Sinh nội dung**
- Chọn ngẫu nhiên 5-6 persona từ Persona Pool
- Sinh đúng số câu theo cấu trúc của mode tương ứng (mode `group` ~28 câu, sub-mode `story` ~15 câu, mode `reply-group`/`ads`/`live` ~20 câu)
- Đảm bảo đa dạng persona, cấu trúc câu, cách xưng hô

**Bước 3: Áp dụng Tone & Viết tắt**
- Viết theo đúng tone Gen Z/Office worker
- Không lặp cấu trúc giữa các câu
- Nội dung phải mới mẻ mỗi lần chạy (Example Bank chỉ tham khảo style)

**Bước 4: Xuất kết quả ra Chat**
- Hiển thị rõ ràng theo nhóm/kiểu để dễ copy
- Mode `reply-group`: hiện lại câu hỏi gốc ở đầu để tiện đối chiếu
- Mode `live`: hiện lại tên bác sĩ/chủ đề hội thảo đã detect được ở đầu để tiện đối chiếu

**Bước 4B: Gác phí trước khi lưu**
- Đối chiếu từng câu có **thông tin phí** (free/0đ/miễn phí/tặng gói/trị giá/số tiền) với luật §6. Câu nào không đủ điều kiện → sửa hoặc bỏ.
- Có nêu thông tin phí → phải **đã đọc `fees-promos.md` trong run này** + in footer `[fees: <updated> · <fee-tier-id>]`. Chưa đọc → bỏ hết thông tin phí, chuyển hotline.
- Chạy `python scripts/qa_seeding.py --check <file>` (hoặc pipe draft qua stdin trước khi ghi). Fail thì sửa rồi chạy lại.

**Bước 5: Lưu file scratch**
Lưu vào: `C:\Users\Admin\.gemini\antigravity-ide\scratch\seeding_<mode>_<timestamp>.md`
(timestamp định dạng `yyyyMMdd_HHmmss`). In đường dẫn file.

---

## Common Mistakes

| Sai lầm | Cách khắc phục |
|---------|----------------|
| Viết hoa đầu câu / chấm phẩy trang trọng | Chữ thường, gõ tự nhiên, bỏ bớt dấu câu — TRỪ tên riêng |
| Viết thường tên riêng: "bs tuấn", "dnd", "dnd sg" | LUÔN viết hoa: bs **Tuấn**, **DND**, **DND SG**, **DND Sài Gòn**, **Trương Định** |
| Câu nào cũng "bv" | Xen kẽ "bv mắt" / "bệnh viện mắt" / "bên viện" cho đa dạng |
| Nhồi từ marketing quảng cáo | Dùng: "máy xịn", "khám kỹ", "ổn áp", "nhanh gọn" |
| **Dùng lại cụm "nhẹ nhàng"** | 281 hit trên corpus cũ = fingerprint. Xoay 6-8 biến thể ở mục Tone, mỗi cụm ≤15% item/run |
| **Claim hết đau: "k đau", "ko hề đau", "chẳng thấy đau"** | 121 hit đang phải xoá. Nói cảm nhận theo hướng dễ chịu/đỡ hơn dự tính, không phủ định đau |
| **Thread reply toàn khen** | Bắt buộc có Kiểu 6 (mixed, có điểm dở thật) + Kiểu 7 (chỉ hỏi lại, k nhắc DND) — xem MODE 2 |
| **So sánh giá/chất lượng vượt trội với viện khác** | Cấm ở group/reply/ads/live: "rẻ hơn", "bằng nửa", "so với viện X". Chỉ `maps`/`maps_foreigner` được miễn |
| Nhắc tên DND quá nhiều trong 1 câu | Tối đa 1 lần/câu, đôi khi chỉ nói "chỗ Trương Định q3" |
| Trùng cấu trúc câu | Đổi chủ ngữ + cách kết câu liên tục |
| Copy nguyên Example Bank | Chỉ tham khảo style — viết câu MỚI mỗi lần |
| Reply không liên quan câu hỏi gốc (mode reply-group) | Phải đọc kỹ câu hỏi gốc, reply đúng ngữ cảnh |
| **Reply dài 3-4 câu (mode reply-group)** | Đúng **1 câu/reply** để copy-paste ngay; chỉ Kiểu 6 và 9 được 2 câu. Reply dài đọc như bài PR, không như người thật gõ trên đt |
| **Xuất đủ 10 kiểu dù câu hỏi gốc không hợp (mode reply-group)** | Chọn kiểu theo ngữ cảnh. Kiểu 8 chỉ khi bài gốc có nhận định sai; Kiểu 9 chỉ khi có hỏi về quy trình. Kiểu 6 và 7 thì luôn giữ |
| Comment ads quá dài/chuyên nghiệp (mode ads) | Comment ngắn 1-2 câu, có emoji, giống comment nhanh trên đt |
| Tất cả comment ads đều khen | Phải xen kẽ hỏi giá, tag bạn, hỏi lịch — đa dạng kiểu tương tác |
| Bịa thêm bác sĩ/chủ đề không có trong content live (mode live) | Chỉ dùng tên bác sĩ/chủ đề đã detect từ nội dung content được paste |
| Dùng từ "bài viết/bài post" cho comment live (mode live) | Dùng ngữ cảnh "đang xem live", "vừa vào coi", "đang nghe bs nói" |
| **Nói "khám free" cho Ortho-K / Phaco / cắt kính / khám bệnh lý / tổng quát** | Free CHỈ cho khám mổ cận-khúc xạ (T0) và tái khám hậu phẫu đã mổ tại DND (T-FU). Xem §6 |
| **Nói "khám free" chung chung, không gắn service** | Mỗi câu phải tự mang ngữ cảnh T0/T-FU. Không có → không nói free |
| **Hứa miễn phí tái khám cho người mổ ở viện khác** | Chỉ người đã mổ tại DND. Ca viện khác: có phí, không báo số, chuyển hotline |
| **Đẩy người lão thị sang cắt kính** | Lão thị điều trị được (Presbyond / Phaco + IOL đa tiêu). Khám lão thị đường khúc xạ = free |
| **Nêu phí mà không in footer** | Có nêu thông tin phí → in `[fees: <updated> · <fee-tier-id>]` ở cuối file, ngày lấy từ `fees-promos.md` |
| **Nêu số phí/số ưu đãi mà chưa đọc `fees-promos.md` trong run đó** | Đây là con bug gốc, chỉ đổi hình. Chưa đọc file → không nêu bất kỳ thông tin phí nào (kể cả chữ "free"), chuyển hotline |
| **Copy số tiền từ `fees-promos.md` ngược lên SKILL.md** | Để số ở 2 nơi là tái tạo class bug. SKILL.md chỉ giữ `fee-tier-id` / `promo-key` |
