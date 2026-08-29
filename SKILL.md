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
| **Mode `reply-group` mà câu hỏi gốc KHÔNG phải mổ cận/khúc xạ** (phaco, lão thị, kiểm soát cận/Ortho-K, cắt kính, glaucoma, võng mạc, lác, mộng, thẩm mỹ, tổng quát) | **`services.md`** — fact pack theo service. Chưa đọc thì không có dữ kiện gì để trả lời ngoài mổ cận, và đó chính là con bug M6 gác |
| Trước khi ghi file scratch | chạy `scripts/qa_seeding.py --check` (pipe draft qua stdin) |
| Muốn biết script gác gì / ngưỡng bao nhiêu | `qa/checks.md` |

`fees-promos.md` là **file duy nhất có số tiền**. SKILL.md chỉ có `fee-tier-id` / `promo-key`.
`services.md` là fact pack **phi-tiền** — có số tiền trong đó là fail `--selftest` (gate M6-E).

## Repo & đồng bộ

Repo GitHub: https://github.com/minhtranquang1993/dnd-seeding (nhánh `main`).

Layout 5 file: `SKILL.md` · `fees-promos.md` · `services.md` · `qa/` · `scripts/`.

- **Push:** copy cả 5 path vào clone local, commit, push.
- **Pull về máy:** ghi đè cả 5 path vào **cả 3 runtime** (đường dẫn macOS):
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
- `/dnd-seeding anti "review xấu"` — Tạo ~20 comment reply vào thread có **review xấu**, giọng khách đã trải nghiệm tốt (MODE 6)
- `/dnd-seeding` (không tham số) — Mặc định chạy mode `group`

**Luật nhận lệnh:** mode token chỉ được nhận ở **vị trí token đầu tiên**, và chỉ **trước** mọi chuỗi trong ngoặc kép. `k=v` (ví dụ `service=phaco`) luôn là param, không bao giờ là mode. Token đầu không khớp mode nào → chạy `group`, không đoán.
> Vì vậy `reply-group "chị nào review maps cho e"` là mode **reply-group** — chữ `maps` nằm trong câu hỏi của user, không phải lệnh.

---

## Context & Reference Data

### 1. Thông tin Bệnh viện & Địa chỉ
- **Tên:** Bệnh viện Mắt Quốc tế DND Sài Gòn (viết tắt: DND Sài Gòn, DND SG, DND Trương Định).
- **Địa chỉ:** 147 - 147B - 147Bis Trương Định, **Phường Nhiêu Lộc**, TP.HCM (Phường 9, Quận 3 cũ).
  > Vẫn nói "q3" trong content seeding được — người ta tìm đường theo Quận 3. Nhưng địa chỉ
  > đầy đủ thì dùng Phường Nhiêu Lộc (cập nhật 2026-08 theo script chat của bệnh viện).
- **Hotline:** 0775.147.147 / 1900 8195.
- **Giờ làm việc:** Thứ 2–7: sáng 08h00–12h00, chiều 13h00–17h00 (**nghỉ trưa 12h–13h**); Chủ nhật: **chỉ sáng** 08h00–12h00.
- **BHYT:** DND **có** hỗ trợ BHYT (Phaco, mộng, cườm nước). Được nói "có BHYT hỗ trợ" — **số tiền hoặc % chi trả thì chuyển hotline** (gate M6-D chặn).

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

> 📎 Mục này chỉ là **danh sách có gì**. Dữ kiện để *viết được reply* (quy trình, thời gian,
> chuẩn bị, mốc tái khám) nằm ở **`services.md`** — mode `reply-group` với câu hỏi không phải
> mổ cận thì bắt buộc đọc file đó.

- **Ortho-K:** Kính đeo đêm kiểm soát cận thị trẻ em. **Khám Ortho-K CÓ PHÍ** (T2).
- **Phaco:** Mổ đục thủy tinh thể, 3-5 phút/mắt, 500.000+ ca. **Khám Phaco CÓ PHÍ** (T2).
- **Thẩm mỹ mắt:** Cắt mí, lấy mỡ bọng, chỉnh sụp mi. **Khám CÓ PHÍ** (T2).
- **Lão thị:** điều trị được — Presbyond (laser) hoặc Phaco + IOL đa tiêu. Người lão thị **không phải chỉ có đường đi cắt kính**. Khám lão thị theo đường khúc xạ/laser = **T0 free**; nếu ca đó đi đường **Phaco + IOL đa tiêu** thì **không báo phí khám → hotline** (chưa có chính sách).
- **Kiểm soát cận thị trẻ em:** 4 hướng — tròng kính KSCT, Ortho-K, atropine nồng độ thấp, ánh sáng đỏ theo chỉ định. **Khám CÓ PHÍ** (T2).
- **Bệnh lý:** glaucoma/cườm nước, võng mạc - dịch kính, lác, mộng. **Khám CÓ PHÍ** (T2).
- **Khám tổng quát:** **CÓ PHÍ** (T2) — gói 12 bước free KHÔNG áp cho tổng quát.

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
| `anti` | Kiểu 1 (khách đã mổ) | ≤20% item/run |

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
7. **Góc 7: Story kể chuyện (4 câu)** — Bài dài hơn hẳn các góc khác (1 đoạn 4-6 câu, kể mạch trải nghiệm thật). Chủ đề lấy từ pool ở **MODE 1B**; nếu lấy chủ đề nhóm "trước mổ" thì **bắt buộc áp luật 3 câu + anti-pattern ở §Nhóm A mở rộng** — không viết bài dừng ở "e lo / e băn khoăn / e chần chừ". Luôn đặt bối cảnh ở DND Sài Gòn/DND Trương Định — không dùng tên bệnh viện khác. Kết bài bằng 1 câu hỏi xin chia sẻ/động lực/kinh nghiệm từ mọi người, không phải câu hỏi thông tin khô khan.
8. **Góc 8: So sánh bệnh viện (4 câu)** — Đóng vai người đang tìm hiểu nhiều nơi: đã khám (hoặc định khám) ở 1-2 viện khác — ví dụ Mắt Sài Gòn, Mắt TPHCM, Việt Nhật — và đang cân nhắc thêm DND Sài Gòn để khám/so sánh giá, công nghệ, cách tư vấn. DND luôn xuất hiện như **1 lựa chọn đang xem xét** bên cạnh viện khác, không phải viện đã chốt hay được khen vượt trội — giữ đúng tinh thần "đang tìm hiểu, chưa quyết".

### Ví dụ mode `group`
- "mn có ai mổ cận chỗ bs Tuấn DND Sài Gòn chưa ạ, cho e xin review tay nghề bác với"
- "e thấy bên DND SG đang có smiledays, tc e eo hẹp mổ đc gói nào tốt nhỉ"
- "mình mổ smile pro bên DND Trương Định tuần trước, bs Tuấn mổ cho, dễ chịu hơn mình tưởng mn, tầm 2-3 ngày là đi làm lại đc r"
- (Góc 7 - story · trục **A9**) "mẹ e cứ gạt 'mắt mũi để yên đó, đụng vào lỡ có j hối k kịp', xong mẹ kể bà cô ở quê mổ xong khô rát cả năm 😔. e hiểu mẹ lo nên k dám nói tiếp, mà e cx mệt cái cảnh trời mưa là mờ kính, đi bơi thì gần như mù, nói ra thì mẹ bảo chịu chút đi. e tìm hiểu cả tháng, chọn đc DND Sài Gòn r mà vẫn chưa dám đặt lịch vì k muốn đi kiểu giấu mẹ. mấy hôm nay e tính rủ mẹ đi cùng buổi khám cho mẹ nghe bs nói trực tiếp, chứ e nói mẹ k tin đâu. mn có ai từng phải thuyết phục ba mẹ vụ này chưa ạ, mn nói kiểu j cho ba mẹ chịu ngồi nghe"
- (Góc 7 - story · buổi khám làm cốt truyện — **tối đa 1 bài/run**, xem §Nhóm A mở rộng) "mn cho e xin review mổ cận ở DND Sài Gòn với ạ 🙏 tuần trước e đi khám chuyên sâu trước mổ ở đây, bình thường e khá sợ khám mắt vì nhìn máy móc là run, nhưng buổi khám k căng như e lo, mất khá nhiều tg vì qua nhiều bước, có nhỏ thuốc rồi đợi đo lại nên gần cả buổi sáng. bs giải thích tình trạng mắt e khá kỹ và tư vấn e đủ điều kiện mổ smile pro, nhưng e vẫn chưa chốt ngay vì đây là quyết định lớn. ai mổ ở DND SG r cho e xin ít review: thị lực sau mổ ổn k, hồi phục ntn, bệnh viện theo dõi hậu phẫu có kỹ k ạ, e cảm ơn mn nhiều"
- (Góc 8 - so sánh viện) "e cận 5 độ loạn 1, mới khám ở mắt sg đc tư vấn femto pro với smile pro r, giờ muốn khám thêm chỗ khác xem sao. có ai khám ở DND Sài Gòn r k, chi phí khám bên đó tầm nhiêu, có nên qua khám thêm 1 vòng trước khi chốt k ạ"
- (Góc 8 - so sánh viện) "e đang phân vân giữa mắt tphcm với DND Trương Định q3, chưa biết nên khám ở đâu trước, ai đi khám cả 2 chỗ r so sánh giúp e với"

---

# MODE 1B (sub-mode): `/dnd-seeding group story` (hoặc `/dnd-seeding story`)

**Mục đích:** Nhánh con của Mode `group`. Chỉ sinh **~15 bài story kể chuyện** — KHÔNG sinh 7 góc còn lại của Mode 1. Dùng khi chỉ cần content dạng kể chuyện dài để đăng group.

**Kích hoạt:** tham số `story` đứng sau `group` (`group story`), hoặc gõ tắt `story` ngay sau lệnh. Nếu chỉ có `group` (không kèm `story`) → chạy Mode 1 đầy đủ 8 góc như thường.

### Đặc trưng story (kế thừa Góc 7)
- **Bài dài hơn hẳn comment thường:** mỗi bài 1 đoạn 4-6 câu, kể mạch trải nghiệm thật, có cảm xúc.
- **Luôn đặt bối cảnh ở DND Sài Gòn / DND Trương Định** — không dùng tên bệnh viện khác làm nơi mổ (trừ trục A13/D7 có thể nhắc "chỗ đã đi khám trước" rồi mới tới DND).
- **Kết bài bằng 1 câu hỏi xin chia sẻ/động lực/kinh nghiệm** từ mọi người — KHÔNG phải câu hỏi thông tin khô khan.
- **Nhóm A còn thêm 3 luật riêng** (luật 3 câu · chi tiết vật lý · anti-pattern) — xem §Nhóm A mở rộng. Bỏ qua là ra đúng loạt bài một màu "e lo / e sợ / e chần chừ".
- Áp dụng đủ Tone & Writing Style + Persona Pool + quy tắc tên bác sĩ như các mode khác.

### Pool chủ đề — xáo trộn mỗi lần chạy, chọn ~15 câu, phân bổ ĐỀU 4 nhóm (~3-4 câu/nhóm)

**Nhóm A — Trước mổ (tâm lý / quyết định):** nhóm này có **pool riêng 18 trục**, không phải liệt kê chủ đề như 3 nhóm còn lại — xem **§Nhóm A mở rộng** ngay sau pool. Chọn 3-4 trục, **mỗi lần chạy phải rơi vào ≥3 cụm khác nhau** (A-I → A-V).

> Lý do tách riêng: Nhóm A là nhóm dễ viết một màu nhất. 5 chủ đề cũ (lo lắng trước ngày mổ · buổi khám 12 bước · băn khoăn quyết định · sợ dao kéo · chần chừ nhiều năm) thực chất là **cùng một câu chuyện** kể bằng 5 nhãn khác nhau: "e lo, e sợ, e chưa quyết". Đọc 3 bài liên tiếp là nhận ra ngay cùng một khuôn.
>
> Cả 5 chủ đề đó **không bị xoá**, chỉ được cụ thể hoá thành tình huống có xung đột: lo lắng trước ngày mổ → **A17** (nghi thức đêm trước) · băn khoăn quyết định → **A15/A16** (bị dí chốt · được trao quyền chọn) · sợ dao kéo → **A5** · chần chừ nhiều năm → **A7** (chi phí cơ hội của trì hoãn). Riêng "buổi khám 12 bước" bị **hạ từ chủ đề xuống bối cảnh** — xem §Luật chọn trục.

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
15. Cận nặng từng bị từ chối laser → được tư vấn Phakic ICL — **góc y khoa** (phương pháp nào phù hợp). Cùng tình huống nhưng kể ở **góc tâm lý** (sợ bị từ chối lần nữa) thì đó là trục **A13** của Nhóm A, không phải bài này. Một run không lấy cả hai.
7. Quá trình chọn viện & chốt DND SG
18. Tình cờ biết DND (bạn giới thiệu / xem livestream / lướt fanpage)
19. Tiktoker/KOC quay hành trình review, nhận cashback khi share

### Cách xuất kết quả (mode story)
In **gộp theo 4 nhóm A/B/C/D**, mỗi nhóm là 1 tiêu đề, dưới liệt kê các bài story của nhóm đó. Mỗi lần chạy chọn chủ đề khác nhau trong pool để không trùng ý. Nhóm A ghi kèm **mã trục** (`A1`…`A18`) sau tiêu đề bài để đối chiếu luật chọn trục.

### Nhóm A mở rộng — 18 trục, 5 cụm

**Vấn đề đang sửa:** 5 chủ đề Nhóm A cũ đều dừng ở **trạng thái cảm xúc** ("lo lắng", "băn khoăn", "chần chừ", "sợ"). Trạng thái cảm xúc không phải nội dung — nó là *nhãn* dán lên nội dung. Viết theo nhãn thì bài nào cũng ra cùng một khuôn: mở bằng "e lo/e sợ", giữa bài kể buổi khám, kết bằng "mn cho e xin động lực".

**Luật thay thế:** mỗi bài Nhóm A phải trả lời được **3 câu** trước khi viết. Không trả lời được cả 3 thì bài đó chưa có nội dung, đừng viết:

1. **Sợ/băn khoăn CÁI GÌ cụ thể?** — không phải "sợ mổ", mà "sợ nằm không yên vì hồi lấy máu đã xỉu", "sợ 20 năm nữa mắt thế nào thì chưa ai trả lời được".
2. **Hai thứ nào đang kéo nhau?** — phải có **xung đột thật**: tiền vs thời gian · mẹ vs bản thân · deadline nghề vs độ cận chưa ổn định · muốn tin bs vs sợ bị bán thêm. Bài chỉ có một chiều "e lo" là bài không có xung đột.
3. **Câu hỏi kết bài hỏi ĐÚNG cái xung đột đó** — không phải "mn cho e xin động lực" dán vào cuối. Câu hỏi phải là câu mà chỉ người từng ở đúng tình huống đó mới trả lời được.

Thêm 1 luật hình thức: mỗi bài cần **≥1 chi tiết vật lý cụ thể** (đồ vật, con số nhỏ, hành động, địa điểm, thời điểm trong ngày) — "tay lạnh ngắt lúc đợi đọc kết quả", "tờ giấy bs ghi để trong tủ 6 tháng", "đặt 3 cái báo thức mà thức tới sáng", "chụp cái ảnh cuối còn đeo kính". Chi tiết vật lý là thứ phân biệt bài người thật gõ với bài mô tả cảm xúc chung chung.

#### Cụm A-I — Nỗi sợ có nội dung (không phải "sợ" chung chung)

| # | Trục | Xung đột / chi tiết cần có |
|---|---|---|
| **A1** | Sợ **mất kiểm soát trong lúc mổ**, không phải sợ đau: sợ nằm không yên, sợ nhắm mắt sai lúc, sợ panic giữa ca | Nền: từng xỉu lúc lấy máu / có rối loạn lo âu / hồi bé nhỏ thuốc giãn là khóc ầm |
| **A2** | Sợ **hậu quả dài hạn không ai trả lời được**: 20-30 năm nữa mắt thế nào, về già mổ Phaco có bị ảnh hưởng | Đã hỏi bs, bs nói theo dõi định kỳ — nhưng câu "20 năm nữa" thì không ai chốt được. Xung đột: muốn một câu chắc chắn vs không tồn tại câu chắc chắn |
| **A3** | Đọc **case biến chứng trên mạng lúc 2h sáng** rồi không ngủ được | Xung đột: lý trí biết đó là số ít vs cái case đó cứ hiện ra. Chi tiết: đọc lúc mấy giờ, đọc ở đâu |
| **A4** | Mắt có **nền bệnh riêng** nên sợ mình là ca ngoại lệ: khô mắt sẵn, viêm bờ mi, cận lệch 2 mắt, nhược thị nhẹ, giác mạc chóp nghi ngờ | Xung đột: mắt mình khác người ta nên review của người khác không dùng được cho mình |
| **A5** | Sợ **dao kéo / máy móc chạm vào mắt** — bản cụ thể hoá của chủ đề cũ | Phải có chi tiết vật lý: đo nhãn áp phụt hơi là giật, không dám tự nhỏ thuốc, cắt tóc gần mắt cũng nhắm chặt |

#### Cụm A-II — Kinh tế & chi phí cơ hội

| # | Trục | Xung đột / chi tiết cần có |
|---|---|---|
| **A6** | **Cộng tiền kính mấy năm qua** rồi so với tiền mổ — phát hiện gần bằng nhau | Xung đột: trả 1 lần thì xót, trả rải ra thì không thấy. Chi tiết: đổi mấy cặp kính, lens, nước ngâm |
| **A7** | **Chi phí cơ hội của việc trì hoãn**: mỗi năm dời lại là thêm 1 năm sống với kính, mà tiền để dành thì bị việc khác chen vào | Xung đột: kế hoạch vs đời sống thật. Chi tiết: đã dời mấy lần, lý do từng lần |
| **A8** | Cân giữa **tiền mổ cho mình vs việc khác của gia đình** (đóng học cho em, sửa nhà, ba mẹ cần khám) | Xung đột thật, không phải "tc eo hẹp" chung chung. Persona sinh viên / người mới đi làm |

#### Cụm A-III — Áp lực từ người khác

| # | Trục | Xung đột / chi tiết cần có |
|---|---|---|
| **A9** | **Ba mẹ phản đối** — "mắt mũi để yên đó", kèm câu chuyện người quen mổ hỏng | Xung đột: hiểu mẹ lo vs mệt cảnh mưa mờ kính. Hướng giải: rủ mẹ đi cùng buổi khám cho mẹ nghe bs nói |
| **A10** | **Bạn bè / đồng nghiệp mỗi người một ý**, người thúc người dội — càng hỏi càng loãng | Chi tiết: hỏi mấy người, mỗi người nói gì trái nhau |
| **A11** | **Chưa dám công khai**: xin nghỉ phép mà không dám khai lý do thật, sợ bị hỏi qua hỏi lại, sợ mổ xong không đạt thì mất mặt | Xung đột: muốn làm âm thầm vs cần người chở về |
| **A12** | **Deadline nghề nghiệp dí**: sơ tuyển công an/quân đội/phi công/tiếp viên, hạn nộp hồ sơ vs độ cận chưa ổn định hoặc chưa đủ tuổi khuyến nghị | Xung đột rõ nhất trong cả pool: thời hạn bên ngoài vs điều kiện y khoa bên trong |

#### Cụm A-IV — Nghi ngờ quy trình & niềm tin

| # | Trục | Xung đột / chi tiết cần có |
|---|---|---|
| **A13** | **Từng bị một nơi từ chối laser** → cạch luôn, giờ đi khám lại mà mang tâm lý "kiểu gì cũng nghe lại câu đó" | Chi tiết: lần trước bs nói gì, lần này ngồi đợi đọc kết quả cảm giác ra sao. Hướng: được tư vấn Phakic ICL nhưng vẫn chưa dám mừng |
| **A14** | Sợ **bị tư vấn lên phương pháp đắt hơn nhu cầu thật** — muốn tin bs mà không có chuyên môn để tự kiểm | Xung đột: muốn tin vs không đủ nền để tin. Không được viết thành tố cáo viện nào |
| **A15** | Sợ **bị dí chốt ngay trong buổi khám**, muốn về nhà nghĩ thêm mà sợ mất suất/mất ưu đãi | Chi tiết: đã chuẩn bị sẵn câu "e về suy nghĩ thêm" trong đầu |
| **A16** | **Bs đưa 2 hướng rồi để tự chọn** → đứng hình, vì cứ nghĩ đi khám là được chỉ định 1 đường | Xung đột: mong được quyết hộ vs được trao quyền quyết. Chi tiết: tờ giấy bs ghi, đọc tới lui cả tuần |

#### Cụm A-V — Nghi thức & mốc thời gian

| # | Trục | Xung đột / chi tiết cần có |
|---|---|---|
| **A17** | **Đêm trước ngày mổ**: đặt 3 báo thức mà thức tới sáng, chụp cái ảnh cuối còn đeo kính, dọn sẵn nhà vì biết mai không nhìn rõ | Không phải "e lo" — là **nghi thức**. Chi tiết vật lý là bắt buộc |
| **A18** | **Ký giấy đồng ý phẫu thuật**: đọc tới dòng rủi ro thì chững lại, dù trước đó đã đọc hết trên mạng | Xung đột: biết trước vs thấy nó in trên giấy có tên mình. ⚠️ Viết là "giấy **đồng ý phẫu thuật**" — chữ "giấy **cam kết**" bị gate 5C `commitment` chặn |

#### Luật chọn trục — chống một màu

- Chọn **3-4 trục**, phải rơi vào **≥3 cụm khác nhau**. 3 bài cùng cụm A-I là đúng lỗi đang sửa, chỉ đổi nhãn.
- **Không quá 1 bài/run** kể chi tiết buổi khám như nội dung chính. Buổi khám được xuất hiện ở nhiều bài, nhưng là **bối cảnh**, không phải cốt truyện. Cũ: 5 chủ đề mà 1 chủ đề dành riêng cho buổi khám → cứ ~20% Nhóm A là bài tả buổi khám.
- **Không quá 1 bài/run** mở đầu bằng cụm cảm xúc trần (`e lo`, `e sợ`, `e băn khoăn`, `e rén`, `e chần chừ`). Các bài còn lại mở bằng **sự việc** — con số, hành động, câu người khác nói, mốc thời gian.
- Câu hỏi kết bài **không được trùng khuôn** giữa các bài trong cùng run. Xoay: hỏi cách xử lý tình huống · hỏi người cùng hoàn cảnh · hỏi cái gì làm họ chốt · hỏi họ nói với ba mẹ thế nào · hỏi họ dựa vào gì để chọn.

#### Anti-pattern Nhóm A — viết thế này là chưa đủ sâu

| ❌ Chưa đủ | Vì sao | ✅ Thay bằng |
|---|---|---|
| "e lo lắm k biết mổ có sao k" | Nhãn cảm xúc, không có nội dung. Không trả lời được câu 1 của luật 3 câu | "e sợ nằm k yên giữa ca, hồi lấy máu e còn xỉu" (A1) |
| "e băn khoăn k biết có nên mổ k" | Không có xung đột — chỉ có 1 chiều | "e cần bỏ kính trước kỳ sơ tuyển mà độ e năm nay còn tăng 0.5" (A12) |
| "e chần chừ mấy năm r" | Trạng thái, không phải sự việc. Chần chừ **vì cái gì** mới là nội dung | "e dời lịch 2 lần, lần đầu lấy lý do công việc, lần 2 thì thật ra là e sợ" (A7) |
| "tc e eo hẹp nên chưa mổ đc" | Chung chung, dùng được cho mọi bài | "tiền mổ của e đang cân với tiền đóng học cho em, mà em e vào cấp 3 năm nay" (A8) |
| "mn cho e xin ít động lực với ạ" ở cuối mọi bài | Câu hỏi rỗng, ai cũng trả lời được nên không ai trả lời | Hỏi đúng xung đột: "mn nói kiểu j cho ba mẹ chịu ngồi nghe ạ" (A9) |
| Kể lại quy trình 12 bước như bài mô tả dịch vụ | Đây là story, không phải bài giới thiệu. Buổi khám là bối cảnh | Chỉ giữ chi tiết nào có cảm xúc gắn vào: tay lạnh lúc đợi kết quả, tờ giấy bs ghi |

#### Bẫy guardrail riêng của Nhóm A — đã test bằng `--check`

Nhóm A là nhóm dễ vấp gate nhất vì nó viết về **nỗi sợ**, mà mô tả nỗi sợ hay kéo theo đúng những cụm bị cấm. Sáu bẫy đã đo:

| Định viết | Gate chặn | Viết thay |
|---|---|---|
| "hôm ký giấy **cam kết** trước mổ" | 5C `commitment` | "hôm ký giấy **đồng ý phẫu thuật**" |
| "e mong **hết cận** sau 10 năm đeo kính" | 5C `cure_myopia` | "e mong **thoát kính** sau 10 năm đeo" |
| "bs nói **k phải là k đau**, chỉ cộm xốn" | 5C `dau_claim` + M3 — regex bắt cả câu **phủ định của phủ định** | "bs nói cảm giác chỉ cộm xốn tầm mấy tiếng đầu" |
| "**so với viện** kia thì bên đây giải thích kỹ hơn" | 5C `compare_other_hospital` | "chỗ e khám trước đo có 10 phút, bên đây đo gần cả buổi" — kể **việc**, không so viện |
| "bs mổ mấy nghìn ca **chưa lỗi ca nào**" | 5C `safety_absolute` | "bs giải thích rõ rủi ro cho e nghe" |
| "e thấy bên đây **khám kỹ nhất** q3" | 5C `superlative_vn` / M7-F | "e thấy bs chịu ngồi giải thích kỹ cho e" |

Trục A2 (sợ hậu quả 20 năm) và A3 (đọc case biến chứng) **được phép nhắc rủi ro/biến chứng** — kể **nỗi sợ của mình** không phải claim y khoa. Nhưng không được kết bài bằng câu trấn an tuyệt đối; kết bằng câu hỏi thật hoặc bằng chính điều bs đã nói ("bs bảo tuỳ tình trạng mắt từng người").



### Ví dụ mode `story`
(viết bài MỚI mỗi lần, chỉ tham khảo giọng — không copy)

**Nhóm A — 2 ví dụ dưới đã qua `--check` PASS.** Đọc kèm luật 3 câu ở §Nhóm A mở rộng: mỗi bài đều nêu **sợ cái gì cụ thể**, có **xung đột hai chiều**, và câu hỏi kết bám đúng xung đột đó.

- (Nhóm A · trục **A13** — từng bị một nơi từ chối) "năm ngoái e đi khám 1 chỗ, bs xem bản đồ giác mạc xong lắc đầu bảo mắt e mỏng quá k bắn laser đc, e về ngồi xe buýt mà mắt đỏ hoe 😔. từ hôm đó e cạch luôn, ai nhắc chuyện mổ mắt là e đổi chủ đề. tuần rồi e mới lấy hết can đảm qua DND Sài Gòn khám chuyên sâu, lúc ngồi đợi bs đọc kết quả tay e lạnh ngắt, cứ nhẩm trước trong đầu là kiểu j cũng nghe lại đúng câu năm ngoái. bs Tuấn đo xong ngồi chỉ cho e giác mạc e dày bn, vì sao đường laser k hợp, còn đường Phakic ICL thì cân nhắc đc, mà e vẫn chưa dám chốt vì lần trước hy vọng r thất vọng. mn ai từng bị 1 nơi từ chối r đi khám lại chỗ khác chưa ạ, mn gỡ cái tâm lý này ntn"
  > Sợ cụ thể: nghe lại đúng câu từ chối. Xung đột: muốn hy vọng vs sợ thất vọng lần hai. Chi tiết vật lý: xe buýt, tay lạnh ngắt. Câu hỏi kết chỉ người từng bị từ chối trả lời được.
- (Nhóm A · trục **A16** — bs đưa 2 hướng để tự chọn) "hôm khám xong bs đưa e 2 hướng, giải thích ưu nhược từng cái r nói tuỳ e chọn, e ngồi đó mà đứng hình lun. e cứ nghĩ đi khám là bs chỉ định 1 đường r mình theo, k nghĩ là mình phải cầm quyết định trong khi mình chả có chuyên môn j. về nhà e mở lại tờ giấy bs ghi, đọc tới lui cả tuần, nghiêng bên này lại thấy tiếc bên kia. e chưa hẹn lại lịch vì sợ chọn xong mấy năm sau lại nghĩ 'hồi đó chọn cái kia có khi hơn'. mn lúc bs đưa nhiều lựa chọn thì mn dựa vào cái j để chốt ạ"
  > Sợ cụ thể: sợ hối vì chính lựa chọn của mình. Xung đột: mong được quyết hộ vs được trao quyền quyết. Bài này **không** mở bằng "e lo/e sợ" — mở bằng sự việc.
- (Nhóm B) "mình đeo kính từ năm lớp 6, tới giờ hơn 10 năm cận 6 độ, sáng nào dậy cũng quờ quạng tìm kính mới thấy đường 🥲. tuần trước mổ smile pro bên DND Trương Định, bs Tuấn mổ cho, sáng hôm sau mở mắt ra nhìn rõ luôn mà cứ ngỡ đang mơ. giờ đi tắm, bơi, ngủ dậy đều nhìn rõ, cảm giác lạ lắm mn ạ. ai mổ xong r có bị 'quen tay' đưa lên dụi mắt tìm kính giống mình k huhu"

---

# MODE 2: `/dnd-seeding reply-group "câu hỏi gốc"`

**Mục đích:** Tạo ~20 comment reply vào bài viết của người khác trên group. Đóng vai **người từng trải nghiệm** hoặc **người cũng đang tìm hiểu** mà biết DND, dẫn dắt tự nhiên về DND Sài Gòn.

### Cách hoạt động
- AI đọc `"câu hỏi gốc"` mà user paste vào
- **Bước 0 — phân loại service (BẮT BUỘC, làm trước khi chọn kiểu).** Xem §Bước 0 ngay dưới
- Sinh ra ~20 comment reply **trả lời đúng service đó**, tự nhiên

### Bước 0 — phân loại service câu hỏi gốc

> ⛔ Bỏ bước này là quay lại đúng con bug đang sửa: hỏi Phaco/cắt kính/lão thị/tổng quát mà
> reply vẫn kéo về mổ cận. QA script gác bằng gate **M6**, không phải chỉ khuyên.

**1. In 2 dòng này ở đầu output** (script parse để gác — sai format là fail M6-A):

```
**Câu hỏi gốc:** <paste nguyên câu hỏi>
**Topic:** <service> / <phase>
```

**2. Bảng service** — đọc câu hỏi, chọn theo ladder, **dừng ở match đầu tiên**:

| service | Dấu hiệu trong câu hỏi |
|---|---|
| `lao_thi` | lão thị, mắt lão, nhìn gần mờ, đeo kính lão, Presbyond, PresbyMAX |
| `phaco` | phaco, thủy tinh thể, đục thủy tinh, cườm khô, mổ cườm, IOL |
| `ksct` | ortho, Ortho-K, kiểm soát cận, kính đêm, đeo đêm, tròng kính KSCT, atropine, trục nhãn cầu |
| `glaucoma` | glaucoma, glocom, tăng nhãn áp, cườm nước, cắt bè, thiên đầu thống |
| `vong_mac` | võng mạc, dịch kính, bong võng mạc, hoàng điểm, đáy mắt |
| `lac` | lác, lé, mắt lệch |
| `mong` | mộng, mộng thịt |
| `tham_my` | cắt mí, sụp mi, bọng mắt, thẩm mỹ mắt, lấy mỡ |
| `kinh` | cắt kính, đo độ, đo mắt, thay kính, mua kính, kính mới, đo kính |
| `tong_quat` | tổng quát, tổng quan, khám định kỳ, kiểm tra sức khỏe mắt |
| `kx` | mổ cận/viễn/loạn, khúc xạ, SMILE, Lasik, SmartSight, SmartSurfACE, CLEAR, Femto, Phakic, ICL |
| `none` | không có dấu hiệu nào |

**Thứ tự ladder có lý do, đừng đảo:**
- `kx` đứng **cuối** — để chữ `mổ` trơn không nuốt service khác. `mổ phaco` phải ra `phaco`,
  không phải `kx`. Cùng cái bẫy §6 #1.
- `lao_thi` đứng **trước** `phaco` — người hỏi lão thị cần nghe Presbyond / IOL đa tiêu, không
  phải bài Phaco thường. (Phí thì vẫn theo §6: `lão thị` + `phaco` → hotline. Hai hệ thống khác nhau.)
- `tong_quat` đứng **sau** các nhóm cụ thể — "khám tổng quát xem có bị cườm không" là câu hỏi về cườm.

**3. `phase`:** câu hỏi có `tái khám` / `sau mổ` / `hậu phẫu` / `mới-vừa-đã mổ` → `fu`, còn lại → `pre`.

> `phase` **không** thay `service`. "mẹ e mới mổ phaco tái khám sao ạ" là `phaco` / `fu` — vẫn
> là câu hỏi về Phaco, và reply nói mốc hậu phẫu **mổ cận** vẫn bị M6-B chặn. Hậu phẫu Phaco
> khác mổ cận thật: thẻ Family 2 năm vs 3 năm, nhịn ăn xét nghiệm, mang thẻ BHYT.

**4. `service` ≠ `kx`/`none` → ĐỌC `services.md`**, lấy section `## <service>` + tiểu mục
`### pre` hoặc `### fu`. Không đọc thì không có dữ kiện, và không có dữ kiện thì chỉ nói được
về mổ cận — đúng con bug.

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

### Kiểu 8 / 9 / 10 nói gì theo service

Ba kiểu này ở trên **chỉ mô tả phiên bản mổ cận** — đó chính là lý do reply hay trôi. Câu hỏi
service khác thì nội dung phải đổi theo, không phải dịch lại bài mổ cận. Dữ kiện lấy ở
`services.md`.

| service | Kiểu 8 đính chính cái gì | Kiểu 9 hậu cần gì | Kiểu 10 đang cân nhắc gì |
|---|---|---|---|
| `phaco` | "nhỏ thuốc cho tan cườm" (không tan được, phải mổ) · "để chín rồi mổ luôn thể" (để chín mổ khó hơn) | nhịn ăn sáng để xét nghiệm nếu mổ trong ngày · mang thẻ BHYT · người lớn tuổi cần người đi cùng | đang xem vài chỗ mổ cho ba mẹ, hỏi loại thủy tinh thể nào hợp |
| `lao_thi` | "lão thị chỉ có nước đeo kính lão" (điều trị được: Presbyond hoặc IOL đa tiêu) | nhỏ tê bề mặt không tiêm · tầm 10-15 phút/mắt · về trong ngày · vài tiếng đầu cộm xốn | đang cân nhắc giữa đường laser và đường thay thủy tinh thể |
| `ksct` | "cho bé đeo kính là xong" (KSCT là kiểm soát tốc độ tăng độ, khác cắt kính) · "Ortho-K hại mắt" | khám 60-90 phút, có nhỏ liệt điều tiết thì 90-120 · **Ortho-K phải ngưng 1 tháng** trước khám | đang so tròng kính KSCT vs Ortho-K vs atropine cho con |
| `kinh` | "đo độ ở đâu chả giống nhau" (đo máy + thử kính khác nhau) | lens mềm ngưng 1 tuần trước đo · đo xong mới ra đơn | đang phân vân cắt kính hay tìm hiểu mổ luôn |
| `glaucoma` | "cườm nước với cườm khô là một" (hai bệnh khác nhau) | cần theo dõi định kỳ, không phải khám 1 lần là xong | đang tìm chỗ theo dõi lâu dài |
| `vong_mac` | "mắt còn nhìn được là chưa sao" (võng mạc hỏng âm thầm) | khám đáy mắt phải nhỏ giãn, mắt nhoè vài tiếng, đừng tự lái xe | tiểu đường nên đi tầm soát định kỳ |
| `lac` | "lác thì phải mổ" (phải khám tìm nguyên nhân trước) | khám tìm nguyên nhân trước rồi bs mới chỉ định | đang tìm hiểu cho con / cho bản thân |
| `mong` | "mộng nhỏ kệ nó" (mộng lan vào tròng đen thì phiền hơn) | có hỗ trợ BHYT (số → hotline) | đang xem mổ ở đâu |
| `tham_my` | "sụp mi chỉ là xấu thôi" (có thể che tầm nhìn) | khám tư vấn trước | đang tìm hiểu cắt mí |
| `tong_quat` | "mắt không mờ thì khỏi khám" (nhiều bệnh tiến triển âm thầm) | khám định kỳ, ra vấn đề thì bs chuyển chuyên sâu | đang tìm chỗ khám định kỳ cho cả nhà |

**Luật phí theo service — đọc kỹ, sai chỗ này là tái tạo bug `:55`:**

| service | Được nói khám free? |
|---|---|
| `kx`, `lao_thi` (đường laser) | ✅ T0 |
| `phaco`, `ksct`, `glaucoma`, `vong_mac`, `lac`, `mong`, `tham_my`, `tong_quat` | ❌ T2 **có phí** |
| `kinh` | ❌ T1 **có phí** — trừ khi người hỏi là **lão thị** |
| `lao_thi` + `phaco` cùng câu | ❌ hotline, chưa có chính sách |

**BHYT:** được nói "có BHYT hỗ trợ" (Phaco, mộng, cườm nước). **Số hoặc % chi trả → hotline**
(gate M6-D chặn).

### Quy tắc riêng mode `reply-group`
- Phải **liên quan trực tiếp** đến câu hỏi gốc, không trả lời lạc đề
- **Bám đúng service đã phân loại ở Bước 0.** Câu hỏi Phaco thì reply nói Phaco; đừng chèn
  SMILE/mổ cận vào cho có. Gate M6-B chặn từng item, M6-C chặn cả run
  - Trôi **không cần nhắc tên** cũng bị chặn: nói giọng mổ cận ("đo bản đồ giác mạc", "ngưng
    lens", "vạt giác mạc", "thoát kính") trong thread Phaco vẫn fail
  - Nhưng cụm **dùng chung** thì được: nhỏ thuốc giãn, mắt nhoè nhờ chở về, khám chuyên sâu,
    nhãn áp — Phaco / võng mạc / khám bé đều nhỏ giãn thật, không tính là trôi
  - Item nhắc **cả hai** service chỉ hợp lệ khi **có dấu hiệu so sánh** ("mẹ e mổ phaco **còn**
    e mổ cận, 2 ca khác nhau"). Rắc tên service vào rồi nói chuyện service khác thì **vẫn fail** —
    nhắc một lần không hợp lệ hoá được nội dung lạc đề
  - Gate xét **từng câu**: một câu so sánh hợp lệ không bảo lãnh được câu lạc đề bên cạnh
  - Nhắc nhãn **hàng xóm** cùng với service đang hỏi thì **không sao** — "mổ phaco xong vẫn phải
    đeo kính lão", "mổ phaco xong 1 tháng mới đo độ cắt kính" là nội dung đúng, không phải lạc đề.
    Gate chỉ gác hướng trôi thật sự rủi ro (chủ yếu là sang **mổ cận**)
- **≥60% item thực chất phải chạm đúng service** (Kiểu 7 không tính vào mẫu số). Trả lời chung
  chung để né token cũng là lạc đề — M6-C bắt
- Không nhắc DND quá lộ liễu — tối đa nhắc tên 1 lần/comment, có comment chỉ nói "chỗ mình mổ bên Trương Định q3" mà không nhắc DND
- Một số reply **không nhắc DND** — chỉ trả lời câu hỏi thuần túy, tạo cảm giác tự nhiên cho cả thread. Kiểu 7 luôn thuộc nhóm này
- **Độ dài: đúng 1 câu/reply.** Đây là reply để copy-paste, không phải bài đăng. Ngoại lệ duy nhất: **Kiểu 6** (phải mang điểm dở thật) và **Kiểu 9** (thông tin hậu cần) được tối đa 2 câu.
  > Đừng viết reply 3-4 câu kể cả khi thấy "còn nhiều thứ hay để nói". Câu thứ 2 trở đi làm reply trông như bài PR, không như người thật gõ trên điện thoại. Thà cắt ý còn hơn dài.
- **`10/10` chỉ được xuất hiện ở Kiểu 1**, tối đa 20% số item trong run (~4/20). Kiểu 6-10 không mang `10/10` — xem §7

### Ví dụ mode `reply-group`

> **Ba ví dụ dưới đây là BA câu hỏi gốc khác nhau, cố ý.** Bản cũ chỉ có đúng 1 ví dụ về SMILE
> Pro — mà mục Tone đã ghi rõ skill đang chỉ thị model bắt chước example và chỉ thị đó có hiệu
> lực đo được (`10/10` 167 hit, `nhẹ nhàng` 281 hit). Một example bank toàn mổ cận **chính là**
> thứ dạy model trả lời câu hỏi Phaco bằng bài mổ cận. Đọc cả ba trước khi viết.

#### Ví dụ A — câu hỏi `kx` (mổ cận)

**Câu hỏi gốc:** _"mọi người ơi cận 5 độ loạn 2 độ mổ smile pro có ổn không ạ"_
**Topic:** `kx` / `pre`

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

#### Ví dụ B — câu hỏi `phaco` (KHÔNG được trả lời bằng bài mổ cận)

**Câu hỏi gốc:** _"mẹ e 68t bị đục thủy tinh thể, mổ phaco ở đâu ổn ạ"_
**Topic:** `phaco` / `pre`

> So với ví dụ A: **không một câu nào nhắc SMILE / mổ cận / 12 bước free.** Persona đổi từ
> người tự đi mổ sang **con cháu dẫn ba mẹ đi**. Hậu cần đổi hẳn: nhịn ăn sáng, thẻ BHYT.

- (Kiểu 1) "mẹ mình cx 70t mổ phaco bên DND Trương Định q3, bs Tuấn mổ, giờ bà đọc báo lại đc r"
- (Kiểu 2) "bạn cho bác qua DND Trương Định q3 khám thử xem, bên đó mổ phaco nhiều"
- (Kiểu 3) "mổ phaco nhanh lắm b, tầm 3-5 phút 1 mắt à, khám với mổ trong ngày luôn đc"
- (Kiểu 3) "phaco bên đó có hỗ trợ BHYT nha, số cụ thể b gọi 0775.147.147 hỏi cho chắc" ← nói "có BHYT" được, **số thì hotline** (M6-D)
- (Kiểu 4) "nhà e cx lo y chang hồi đưa ba đi, mà bs giải thích kỹ nên cũng đỡ căng"
- (Kiểu 6 - mixed) "mẹ mình mổ phaco bên DND SG, nói thật hôm khám đông nên chờ khá lâu, bà lớn tuổi ngồi đợi hơi mệt. còn ca mổ thì nhanh, mình k tiếc" ← điểm dở thật, hợp ngữ cảnh người già
- (Kiểu 7 - hỏi lại, k nhắc DND) "bác nhà b mắt mờ lâu chưa v, có tiểu đường hay huyết áp j k?"
- (Kiểu 8 - đính chính) "cho mình góp ý nhẹ, cườm khô là k nhỏ thuốc cho tan đc đâu b, tới lúc thì phải mổ thôi"
- (Kiểu 9 - quy trình) "hôm dẫn mẹ đi, muốn mổ luôn trong ngày thì phải nhịn ăn sáng để lấy máu xét nghiệm. nhớ mang thẻ BHYT với CCCD nha" ← hậu cần **riêng của Phaco**, không phải bài mổ cận
- (Kiểu 10 - đang cân nhắc) "e cx đang xem vài chỗ cho ba, chưa quyết loại thủy tinh thể nào nên tính đi khám cho bs tư vấn"

#### Ví dụ C — câu hỏi `kinh` (cắt kính — T1 CÓ PHÍ, tuyệt đối không nói free)

**Câu hỏi gốc:** _"mn ơi e muốn đo độ cắt kính mới thì đi đâu uy tín ạ"_
**Topic:** `kinh` / `pre`

> Cạm bẫy ở đây là **phí**: cắt kính là T1 **có phí**, nói "khám free" là vi phạm §6. Và đừng
> biến câu hỏi đo độ thành bài chào mổ cận — gợi mổ tối đa **một câu** ở Kiểu 10.

- (Kiểu 1) "e đo độ cắt kính bên DND Trương Định q3, máy đo xong bs thử kính lại nên đeo êm"
- (Kiểu 2) "bạn qua bên viện mắt q3 đo thử đi, đo độ có phí nhưng đo kỹ hơn tiệm kính"
- (Kiểu 3) "đang đeo lens thì nhớ ngưng trước 1 tuần r hẵng đi đo nha, k là ra sai độ đó"
- (Kiểu 4) "e cx từng cắt kính ở tiệm r nhức đầu hoài, đi đo lại ở bv mới biết lệch độ"
- (Kiểu 6 - mixed) "mình đo bên DND SG, phí đo độ thì có tính chứ k free nha, với hôm đó phải chờ tới lượt hơi lâu. bù lại kính đeo đúng độ, k nhức mắt như cũ" ← nói thẳng **có phí**, đúng T1
- (Kiểu 7 - hỏi lại, k nhắc DND) "b đo độ lần gần nhất cách đây bao lâu r, có thấy nhìn xa mờ thêm k?"
- (Kiểu 8 - đính chính) "đo ở đâu cx như nhau là k đúng đâu b, đo máy xong còn phải thử kính mới ra đúng độ"
- (Kiểu 9 - quy trình) "đo xong họ đưa đơn, mình cầm đơn đi cắt chỗ nào cx đc nha, k bắt buộc cắt tại chỗ"
- (Kiểu 10 - đang cân nhắc) "e cx đang phân vân cắt kính tiếp hay tìm hiểu mổ luôn, chắc đi khám hỏi bs cho rõ" ← **một câu duy nhất** chạm tới mổ, không nhiều hơn

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

# MODE 6: `/dnd-seeding anti "<review xấu>"`

**Mục đích:** Có người đăng **review xấu** về DND trên group/fanpage. Sinh ~20 comment vào thread đó, đóng vai **khách hàng đã trải nghiệm tốt** — kể chuyện của mình, không phản bác, không đấu khẩu.

> ⛔ **Đây KHÔNG phải giọng bệnh viện trả lời khiếu nại.** Không "bệnh viện chúng tôi rất tiếc", không "xin lỗi quý khách", không "bộ phận CSKH sẽ liên hệ". Gate **M7-B** chặn.

### Ba luật cứng của mode

| Luật | Nội dung | Gate |
|---|---|---|
| **Không đấu khẩu** | Không quy kết động cơ (`đối thủ`, `dựng chuyện`, `nick ảo`, `được thuê`) và không phủ nhận lời kể của người đăng (`chắc b hên xui`, `1 sao mà kể như thật`, `acc mới tinh nhỉ`) | **M7-C** |
| **Né hẳn điểm phàn nàn** | Không thừa nhận rồi cân bằng lại. Không `nói thật hôm e đi cx chờ hơi lâu mà...`, không `công nhận hơi đông nhưng...`, không `bù lại`. Kể trải nghiệm tốt của mình, **không nhắc lại điểm người ta phàn nàn** | **M7-E** |
| **Không xếp hạng** | Không `khám kỹ nhất`, `uy tín nhất q3`, `hơn hẳn chỗ cũ`, `viện khác k bằng`. Nêu **lý do cụ thể** ("bs chịu ngồi giải thích", "gần nhà") thay vì so bên nào hơn | **M7-F** + §7C |

**Được đính chính DỮ KIỆN, không được phủ nhận TRẢI NGHIỆM.** "chắc b nhầm lịch nghỉ trưa r, bên đó nghỉ 12h-13h" — hợp lệ, hữu ích. "chắc b hên xui gặp hôm đó thôi" — bị chặn.

### Marker bắt buộc ở đầu output

Cả 3 dòng, và review phải là **blockquote** (mỗi dòng bắt đầu `> `):

```
**Mode:** anti
**Review xấu:**
> <paste nguyên văn review của user>
> <dòng 2 nếu review dài>
**Topic:** <service> / <phase>
```

Vì sao phải blockquote, không phải văn trần:

- Review dán vào thường **nhiều dòng**. Regex một dòng chỉ đọc được dòng đầu → mất chủ đề → M6 tắt im lặng.
- Review hay có gạch đầu dòng số ("1. chờ 2 tiếng"). Không có `>` thì script đếm chúng thành **item của bạn**.
- Vùng review được **miễn** luật §7C (bạn đang trích dẫn, không phải đang nói). Ranh giới vùng đó phải rõ ràng, nếu không nó thành chỗ giấu vi phạm.

Thiếu dòng `**Mode:** anti` → **fail M7-A**, dù có marker review. Không có dòng đó thì cả họ gate M7 không chạy.

`**Topic:**` phân loại bằng đúng bảng service ở MODE 2 Bước 0. Review chung chung ("thái độ kém") → `none`, gate chủ đề tự bỏ qua. Review chạm ≥2 service → gate cũng bỏ qua và in note.

### 6 kiểu comment (~20 item)

In header đúng dạng `### Kiểu N: <tên>` — script attribute item theo header này.

| Kiểu | Số | Nội dung |
|---|---|---|
| **1** | 5 | Khách **đã mổ** kể trải nghiệm của mình — bs nào, phương pháp, thị lực hiện tại |
| **2** | 3 | Khách **đi khám** (chưa mổ) kể buổi khám — bs giải thích ra sao, các bước |
| **3** | 3 | **Người nhà** dẫn ba mẹ / con đi (Phaco, Ortho-K, kiểm soát cận) |
| **4** | 3 | Khách **tái khám / lâu năm** — đi nhiều lần, hồ sơ mắt được lưu, được theo dõi |
| **5** | 3 | Khách **ở tỉnh**, hoặc khách **đã đi nhiều viện rồi chốt DND** |
| **7** | **≥2** | **Hỏi lại người đăng** — trung tính, KHÔNG khen, KHÔNG nhắc DND, KHÔNG kể trải nghiệm bản thân |

**Không có Kiểu 6.** Ở MODE 2, Kiểu 6 nghĩa là "review có điểm chưa hài lòng thật" — mode này **cấm** đúng thứ đó. Số 6 để trống có chủ đích; đừng dùng lại nó cho nghĩa khác.

**Kiểu 5 là kiểu rủi ro nhất.** "Đã đi nhiều viện rồi chốt DND" mời gọi đúng thứ §7C cấm. Viết theo hình "đã xem nhiều nơi, chốt chỗ này **vì lý do cụ thể**", không xếp hạng:
- ❌ "e khám 3 chỗ r mới chốt bên này, tại thấy bs giải thích **rõ nhất**"
- ✅ "e khám 3 chỗ r mới chốt bên này, tại bs chịu ngồi giải thích kỹ cho e"

**Kiểu 7 là sàn cứng, ≥2 item.** Chốt "né hẳn" đã bỏ Kiểu 6, nên Kiểu 7 là **phòng tuyến cấu trúc duy nhất** còn lại chống thread 20/20 toàn khen. Ba điều kiện, gate M7-D kiểm cả ba:

1. Phải là **câu hỏi thật** — `?`, `nhỉ`, `v ạ`, `bao lâu`, `bs nào`, `bn độ`
2. **Không nhắc** DND / Trương Định
3. **Không mang trải nghiệm hay đánh giá của bản thân** — "bên đó ổn lắm, b khám lại chưa v?" vẫn **fail**: khen rồi dán câu hỏi ở đuôi thì vẫn là khen

### Luật kế thừa (không có ngoại lệ nào cho mode này)

- **§6 luật phí** — nêu thông tin phí phải đọc `fees-promos.md` + in footer. Kiểu 3 nói Phaco/Ortho-K là **T2 có phí**, không được nói free.
- **§7C cấm chung** — claim hết đau, superlative, so sánh viện, `cam kết`/`đảm bảo`, `khỏi cận`.
- **Claim an toàn tuyệt đối bị cấm** (họ `safety_absolute`): "an toàn 100%", "chưa nghe ai bị biến chứng", "k có ca nào bị sao", "chưa lỗi ca nào". Thread phòng thủ dễ trượt vào đây nhất, và đây là loại claim rủi ro pháp lý cao nhất skill sinh ra được. Nói được: "bs giải thích rõ rủi ro cho e".
- **`10/10` chỉ ở Kiểu 1**, tối đa 20% item/run.
- **Anti-repeat §7D** — mỗi cụm ≤15% item/run.
- **Độ dài** — 1-2 câu/comment, như MODE 2.
- **Mật độ nhắc DND** — tối đa 1 lần/comment; có comment chỉ nói "chỗ Trương Định q3" hoặc "bên đó"; Kiểu 7 không nhắc.

### Giới hạn đã biết — nói thẳng

Chốt "né hẳn" nghĩa là **18/20 comment đều tích cực**. Đó chính là fingerprint mà §7 dựng ra để chặn. Các lớp giảm nhẹ: sàn Kiểu 7 · anti-repeat · §7C + M7-F · `safety_absolute` · quota `10/10`. **Không xoá được hết** — nếu thread cần trông thật hơn nữa thì phải nới chốt "né hẳn", và đó là quyết định của bạn, không phải của skill.

M7-E cũng **không kín**: nó bắt các hình nhượng bộ phổ biến ("nói thật...", "công nhận...", "bù lại"), nhưng "hôm e đi thì phải ngồi đợi tới trưa, mà bs khám kỹ" thì lọt. Tập cách nói một điểm dở là mở; siết thêm sẽ bắt oan câu hợp lệ.

---

## Process Flow

### Khi nhận lệnh `/dnd-seeding [mode] [tham số]`:

**Bước 1: Xác định mode** (check theo thứ tự này)

Chỉ đọc **token đầu tiên**, và chỉ phần **trước** dấu ngoặc kép đầu tiên. Bỏ mọi `k=v` ra làm param trước khi so.

- `group story` HOẶC `story` (đứng ngay sau lệnh) → chạy **Mode 1B** (sub-mode story), CHỈ sinh ~15 bài story
- `group` (không kèm `story`) hoặc không có tham số → chạy Mode 1 đầy đủ 8 góc
- `reply-group "..."` → chạy Mode 2, parse câu hỏi gốc từ dấu ngoặc kép, rồi **làm Bước 0 phân loại service trước khi chọn kiểu**
- `ads` → chạy Mode 3
- `live (nội dung content live)` → chạy Mode 4, parse toàn bộ nội dung live, detect bác sĩ/chủ đề/ưu đãi từ đó
- `maps` / `maps_foreigner` / `koc` → chạy Mode 5A / 5B / 5C, áp ngoại lệ §7B đúng theo mode
- `anti "review xấu"` → chạy **Mode 6**, parse review xấu từ ngoặc kép, in marker blockquote, sinh 6 kiểu comment
- token đầu không khớp mode nào → chạy `group`. **Không suy diễn mode từ chữ trong câu hỏi của user.**

**Bước 2: Chọn Persona & Sinh nội dung**
- **Mode `reply-group`: làm Bước 0 (phân loại service) TRƯỚC.** Service ≠ `kx`/`none` → đọc `services.md` lấy dữ kiện, rồi mới viết
- Chọn ngẫu nhiên 5-6 persona từ Persona Pool
- Sinh đúng số câu theo cấu trúc của mode tương ứng (mode `group` ~28 câu, sub-mode `story` ~15 câu, mode `reply-group`/`ads`/`live` ~20 câu)
- Đảm bảo đa dạng persona, cấu trúc câu, cách xưng hô

**Bước 3: Áp dụng Tone & Viết tắt**
- Viết theo đúng tone Gen Z/Office worker
- Không lặp cấu trúc giữa các câu
- Nội dung phải mới mẻ mỗi lần chạy (Example Bank chỉ tham khảo style)

**Bước 4: Xuất kết quả ra Chat**
- Hiển thị rõ ràng theo nhóm/kiểu để dễ copy
- Mode `reply-group`: in **`**Câu hỏi gốc:**`** và **`**Topic:** <service> / <phase>`** ở đầu output (bắt buộc — thiếu là fail M6-A)
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
| **Story Nhóm A dừng ở nhãn cảm xúc ("e lo", "e băn khoăn", "e chần chừ")** | Nhãn không phải nội dung. Áp **luật 3 câu** (sợ cái gì cụ thể · hai thứ nào kéo nhau · câu hỏi kết bám xung đột) + **≥1 chi tiết vật lý**. Xem §Nhóm A mở rộng |
| **3 bài Nhóm A cùng một cụm, chỉ đổi nhãn** | Chọn 3-4 trục rơi vào **≥3 cụm khác nhau** (A-I → A-V) |
| **Bài Nhóm A nào cũng tả buổi khám 12 bước** | Tối đa **1 bài/run** lấy buổi khám làm cốt truyện; các bài khác dùng nó làm bối cảnh |
| **Bài Nhóm A nào cũng kết "mn cho e xin ít động lực"** | Câu hỏi rỗng. Hỏi đúng xung đột của bài, mỗi bài một khuôn khác |
| **Viết "ký giấy cam kết" trong story trước mổ** | Gate 5C `commitment` chặn chữ `cam kết`. Viết "giấy **đồng ý phẫu thuật**" |
| **Viết "mong hết cận" / "bs nói k phải là k đau"** | `cure_myopia` và `dau_claim`/M3 chặn. Viết "mong **thoát kính**" · "cảm giác chỉ cộm xốn mấy tiếng đầu" |
| Reply không liên quan câu hỏi gốc (mode reply-group) | Phải đọc kỹ câu hỏi gốc, reply đúng ngữ cảnh |
| **Câu hỏi Phaco / cắt kính / lão thị / Ortho-K / tổng quát mà reply kéo về mổ cận** | Làm **Bước 0** phân loại service trước, đọc `services.md`, rồi viết theo service đó. Gate M6-B/M6-C chặn — xem MODE 2 |
| **Trôi chủ đề không cần nhắc tên** (thread Phaco mà nói "bản đồ giác mạc", "ngưng lens", "vạt giác mạc") | Đó vẫn là giọng mổ cận, M6-B bắt qua `KX_CONTEXT`. Nói hậu cần **của service đang hỏi** |
| **Trả lời chung chung để né gate** ("bên đó ổn lắm", "b ib hỏi thử") | ≥60% item thực chất phải chạm đúng service, M6-C bắt. Chung chung cũng là lạc đề |
| **Thiếu dòng `**Câu hỏi gốc:**` ở đầu output (mode reply-group)** | In cả `**Câu hỏi gốc:**` và `**Topic:**`. Thiếu là fail M6-A — không khai câu hỏi thì không gác được gì |
| **Nêu số / % BHYT** | Nói "có BHYT hỗ trợ" thôi, số thì chuyển hotline 0775.147.147 (M6-D) |
| **Lẫn cườm nước (glaucoma) với cườm khô (Phaco)** | Hai bệnh khác nhau. Cườm khô = đục thủy tinh thể = mổ Phaco. Cườm nước = tăng nhãn áp = thuốc/laser/cắt bè |
| **Lẫn mốc ngưng kính áp tròng** | Lens mềm ngưng ≥ **1 tuần**; Ortho-K ngưng ≥ **1 tháng** |
| **Lẫn thời hạn thẻ Family** | Sau mổ **khúc xạ: 3 năm**; sau mổ **Phaco: 2 năm** |
| **Đưa giá Phaco / Ortho-K / lác / mộng / cườm nước vào `services.md`** | Những giá đó KHÔNG có trong `fees-promos.md` → seeding chuyển hotline. `services.md` là fact pack phi-tiền, gate M6-E fail nếu có số tiền |
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
| **Mode `anti`: dùng giọng bệnh viện trả lời khiếu nại** | Mode này đóng vai **KHÁCH đã trải nghiệm**. Không "bệnh viện chúng tôi", "quý khách", "bộ phận CSKH" — gate M7-B chặn |
| **Mode `anti`: đấu khẩu / quy kết người viết review** | Không "chắc đối thủ", "nick ảo", "chắc b hên xui gặp hôm đó". Được đính chính **dữ kiện** ("chắc b nhầm lịch nghỉ trưa"), không được phủ nhận **trải nghiệm** — gate M7-C |
| **Mode `anti`: thừa nhận điểm phàn nàn rồi cân bằng lại** | Chốt là **né hẳn**: không "nói thật hôm e đi cx chờ hơi lâu mà...", không "công nhận hơi đông nhưng...", không "bù lại". Kể trải nghiệm tốt của mình — gate M7-E |
| **Mode `anti`: xếp hạng ("khám kỹ nhất", "hơn hẳn chỗ cũ")** | §7C cấm superlative + so sánh viện, nhưng regex cũ chỉ phủ `tốt nhất/giỏi nhất/số 1` và so sánh **giá**. Gate M7-F phủ khoảng giữa. Nêu **lý do cụ thể** thay vì xếp hạng |
| **Mode `anti`: review xấu viết văn trần, không blockquote** | Phải là `> ` mỗi dòng. Văn trần làm regex chỉ đọc dòng đầu (M6 mất chủ đề) và biến vùng review thành chỗ giấu vi phạm — gate M7-A |
| **Mode `anti`: Kiểu 7 là câu khen dán câu hỏi ở đuôi** | "bên đó ổn lắm, b khám lại chưa v?" vẫn fail. Kiểu 7 phải trung tính hoàn toàn: không brand, không trải nghiệm bản thân — gate M7-D |
| **Claim an toàn tuyệt đối ("an toàn 100%", "chưa nghe ai bị biến chứng")** | Bị cấm ở **mọi mode** (họ `safety_absolute`). Thread phòng thủ dễ trượt nhất. Nói được: "bs giải thích rõ rủi ro cho e" |
| **Nêu số phí/số ưu đãi mà chưa đọc `fees-promos.md` trong run đó** | Đây là con bug gốc, chỉ đổi hình. Chưa đọc file → không nêu bất kỳ thông tin phí nào (kể cả chữ "free"), chuyển hotline |
| **Copy số tiền từ `fees-promos.md` ngược lên SKILL.md** | Để số ở 2 nơi là tái tạo class bug. SKILL.md chỉ giữ `fee-tier-id` / `promo-key` |
