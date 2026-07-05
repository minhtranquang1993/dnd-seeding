---
name: seeding-dnd
description: >
  Tạo danh sách ~20 content seeding ngắn dạng câu hỏi cho Bệnh viện Mắt Quốc tế DND Sài Gòn.
  Trigger khi user gõ "/seeding-dnd", "seeding-dnd", "content seeding dnd", hoặc yêu cầu
  tạo ý tưởng/câu hỏi đi seeding cho DND.
---

# Seeding DND Skill 👁️

Tạo content seeding tự nhiên cho Bệnh viện Mắt Quốc tế DND Sài Gòn (147 Trương Định, Quận 3, TP.HCM) với 3 chế độ khác nhau tùy mục đích sử dụng.

## When to Use

- `/seeding-dnd group` — Tạo ~20 bài đăng seeding trên group mổ cận
- `/seeding-dnd reply-group "câu hỏi gốc"` — Tạo ~20 comment reply vào bài người khác trên group
- `/seeding-dnd ads` — Tạo ~20 comment seeding dưới bài quảng cáo của mình
- `/seeding-dnd` (không tham số) — Mặc định chạy mode `group`

---

## Context & Reference Data

### 1. Thông tin Bệnh viện & Địa chỉ
- **Tên:** Bệnh viện Mắt Quốc tế DND Sài Gòn (viết tắt: DND Sài Gòn, DND SG, DND Trương Định).
- **Địa chỉ:** 147 - 147B - 147Bis Trương Định, Võ Thị Sáu, Quận 3, TP.HCM.
- **Hotline:** 0775.147.147 / 1900 8195.
- **Giờ làm việc:** Thứ 2–7: 08h00–17h00, Chủ nhật: 08h00–12h00.

### 2. Đội ngũ Bác sĩ
- **BSNT Bùi Quang Tuấn (Giám đốc):** 13 năm kinh nghiệm, BS Nội trú ĐH Y Dược Huế, 10 năm Trưởng khoa DND Hà Nội trước khi vào làm GĐ DND Sài Gòn. Chuyên Phaco, khúc xạ, dịch kính - võng mạc. Nổi tiếng khéo tay, tận tâm, hàng chục nghìn ca thành công.
- **ThS.BS Lê Thị Thu Hà (Trưởng khoa Khúc xạ):** 12 năm, Thạc sĩ ĐH Y Hà Nội. Chuyên gia kiểm soát cận thị trẻ em + phẫu thuật laser hiện đại. Nhẹ nhàng, chu đáo.
- **ThS.BS Hoàng Mai Linh:** >7 năm nhãn khoa.
- **PGS.TS.BS Võ Thị Hoàng Lan:** Chuyên gia khúc xạ.
- **BS.CKII Nguyễn Đăng Dũng:** Sáng lập hệ thống DND, ~40 năm, 300.000+ ca, tiên phong Phaco & khúc xạ VN.

### 3. Công nghệ Phẫu thuật
- **SMILE Pro (VISUMAX 800, Carl Zeiss - Đức):** 8-10 giây/mắt, vết mổ 2mm, định tâm tự động, phục hồi 24h, ít khô mắt.
- **SmartSight (SCHWIND ATOS):** Không tạo vạt, rạch 2mm, bảo tồn giác mạc.
- **SmartSurfACE (SCHWIND AMARIS 750S):** Laser không chạm, không vạt, không hút chân không, phù hợp giác mạc mỏng/sợ dao kéo.
- **Femto-LASIK / Femto-Pro (FEMTO LDV Z8):** Laser tạo vạt chính xác.
- **Phakic ICL:** Đặt thấu kính nội nhãn cho cận nặng (18-20 diop) hoặc giác mạc quá mỏng.
- **CLEAR:** Phương pháp kết hợp riêng DND.
- **Crosslinking:** Làm bền vững giác mạc, kết hợp thêm.

### 4. Ưu đãi SmileDays 2026
- Khám chuyên sâu 12 bước miễn phí (trị giá 1.000.000đ, kể cả Ortho-K).
- Hỗ trợ đến 50%++ chi phí mổ cận, giá chỉ từ 13 triệu/2 mắt.
- Cashback 3.000.000đ khi share hành trình. Thẻ Family 5.000.000đ.
- Miễn phí tái khám & đồng hành hậu phẫu 3 năm. Check-in nhận quà mùa hè.

### 5. Dịch vụ khác
- **Ortho-K:** Kính đeo đêm kiểm soát cận thị trẻ em.
- **Phaco:** Mổ đục thủy tinh thể, 3-5 phút/mắt, 500.000+ ca.
- **Thẩm mỹ mắt:** Cắt mí, lấy mỡ bọng, chỉnh sụp mi.

---

## Persona Pool

Xáo trộn persona mỗi lần chạy. Không dùng quá 3 câu cùng 1 persona.

| Persona | Cách nói đặc trưng |
|---------|---------------------|
| **Sinh viên** | "e là sv", "ba mẹ cho tiền mổ", "tc eo hẹp" |
| **Dân văn phòng** | "e làm văn phòng", "ngồi máy tính cả ngày", "sợ khô mắt" |
| **Mẹ bỉm** | "con e cận tăng nhanh", "cho bé đi khám ortho-k", "con mới lớp 5" |
| **Người tỉnh lên SG** | "e ở biên hòa/bình dương/long an", "lên sg mổ về luôn trong ngày" |
| **Tiktoker / KOC** | "e muốn quay review", "share đc cashback 3tr k", "làm content" |
| **Người cận nặng** | "e cận 12 độ", "giác mạc mỏng", "bs bảo k bắn laser đc" |
| **Người đã mổ xong** | "mình mới mổ tuần trước", "tái khám đạt 1.5/1.5", "thoát kính r" |

---

## Tone & Writing Style (Áp dụng cho TẤT CẢ modes)

- **Viết tắt tự nhiên (xen kẽ, không dùng hết):**
  `e` (em), `mn`/`mng` (mọi người), `bs` (bác sĩ), `bv` (bệnh viện), `đc` (được), `k`/`ko` (không), `q3` (quận 3), `j` (gì), `r` (rồi), `vs` (với), `cx` (cũng), `tc` (tài chính), `ntn` (như thế nào), `đt` (điện thoại)
- **Phong cách:**
  - Chữ thường (lowercase) là chính
  - Ngắn gọn, 1-2 ý/câu
  - Biểu cảm: `hihi`, `huhu`, `hic`, `ạ`, `mn ơi`, `nha`, `nè`, `hen`, `á`, `lun`
  - **CẤM** từ marketing: "đẳng cấp quốc tế", "đồng bộ hiện đại", "tiên phong", "trải nghiệm đỉnh cao"
  - Thay bằng: "máy xịn", "khang trang", "nhiệt tình", "nhanh gọn", "ổn áp"
  - Thỉnh thoảng thiếu dấu chấm cuối câu hoặc lỗi chính tả nhẹ
- **Đa dạng cấu trúc:**
  - Đổi chủ ngữ: e, mình, tui, đứa bạn e, bạn e, con e
  - Đổi cách kết: nhỉ, k ạ, thế nào, ai chưa, cho e hỏi, ai biết k
  - Không 2 câu liên tiếp bắt đầu cùng 1 từ

---

# MODE 1: `/seeding-dnd group`

**Mục đích:** Tạo ~20 bài đăng mới trên các group review mổ cận (Hội mổ cận, Hội review SMILE Pro...). Đóng vai người đi tìm hiểu hoặc người đã mổ xong muốn chia sẻ.

### Phân bổ 6 góc (tổng 20 câu)

1. **Góc 1: Hỏi review Bác sĩ (3 câu)** — Hỏi tay nghề BS Tuấn, BS Hà, BS Dũng. Ai mát tay, ai khám kỹ.
2. **Góc 2: Chi phí & Ưu đãi (3 câu)** — Hỏi khám 12 bước 0đ, SmileDays giảm 50%, giá trọn gói.
3. **Góc 3: So sánh Công nghệ (3 câu)** — SMILE Pro vs SmartSight, SmartSurfACE cho mắt mỏng, Phakic ICL cho cận nặng.
4. **Góc 4: Dịch vụ & CSVC (3 câu)** — Quy trình trong ngày, phòng ốc, Ortho-K cho trẻ.
5. **Góc 5: Hậu phẫu (3 câu)** — Hồi phục, khô mắt, tái khám, kiêng cữ.
6. **Góc 6: Social proof — Người đã mổ xong (5 câu)** — Chia sẻ trải nghiệm tích cực, kể chi tiết (BS, thị lực, số ngày hồi phục).

### Ví dụ mode `group`
- "mn có ai mổ cận chỗ bs tuấn dnd sài gòn chưa ạ, cho e xin review tay nghề bác với"
- "e thấy bên dnd sg đang smiledays giảm 50%, tc tầm 25tr mổ đc gói nào tốt nhỉ"
- "mình mổ smile pro bên dnd trương định tuần trước, bs tuấn mổ cho, nhẹ nhàng lắm mn, 2 ngày đi làm lại r"

---

# MODE 2: `/seeding-dnd reply-group "câu hỏi gốc"`

**Mục đích:** Tạo ~20 comment reply vào bài viết của người khác trên group. Đóng vai **người từng trải nghiệm** hoặc **người cũng đang tìm hiểu** mà biết DND, dẫn dắt tự nhiên về DND Sài Gòn.

### Cách hoạt động
- AI đọc `"câu hỏi gốc"` mà user paste vào
- Phân tích ý chính của câu hỏi (hỏi về giá? về BS? về công nghệ? về hồi phục?)
- Sinh ra ~20 comment reply phù hợp ngữ cảnh, tự nhiên

### 5 kiểu reply (phân bổ đều ~4 câu/kiểu)

1. **Trả lời từ kinh nghiệm bản thân** — "mình cx từng bị vậy, cuối cùng chọn mổ bên dnd sg..."
2. **Gợi ý/Recommend tự nhiên** — "bạn thử qua dnd trương định q3 khám free xem, mình thấy ổn lắm"
3. **Bổ sung thông tin hữu ích** — "theo mình biết thì bên dnd sg đang có smiledays giảm 50% nè"
4. **Đồng cảm + dẫn dắt** — "e cx sợ vậy nè, nhưng mổ xong thấy nhẹ nhàng lắm, bs tuấn bên dnd sg khéo tay lắm"
5. **Tag bạn / Rủ đi cùng** — "cái này giống case đứa bạn mình mổ bên dnd sg nè, để mình hỏi rồi rep lại"

### Quy tắc riêng mode `reply-group`
- Phải **liên quan trực tiếp** đến câu hỏi gốc, không trả lời lạc đề
- Không nhắc DND quá lộ liễu — tối đa nhắc tên 1 lần/comment, có comment chỉ nói "chỗ mình mổ bên trương định q3" mà không nhắc DND
- Một số reply **không nhắc DND** — chỉ trả lời câu hỏi thuần túy, tạo cảm giác tự nhiên cho cả thread
- Độ dài: ngắn hơn mode group, 1-3 câu/reply (comment thường ngắn hơn bài đăng)

### Ví dụ mode `reply-group`
Giả sử câu hỏi gốc: _"mọi người ơi cận 5 độ loạn 2 độ mổ smile pro có ổn không ạ"_

- "case mình cx tương tự bạn nè, cận 4.5 loạn 1.75, mổ smile pro bên dnd sg, giờ 10/10 r nha"
- "cận 5 loạn 2 thì làm smile pro đc bạn ơi, quan trọng là giác mạc đủ dày, bạn đi khám chuyên sâu trước đi"
- "bạn qua dnd trương định q3 khám 12 bước free luôn á, bs sẽ tư vấn phương pháp phù hợp cho bạn"
- "e cx loạn 2 độ nè, bs tuấn bên dnd sg bảo e làm smile pro đc, mổ xong k thấy loạn nữa lun"
- "loạn 2 độ thì smile pro máy visumax 800 xử lý tốt lắm bạn, nó có OcuLign bù trừ trục loạn thị"

---

# MODE 3: `/seeding-dnd ads`

**Mục đích:** Tạo ~20 comment seeding dưới bài quảng cáo (Facebook Ads) của chính mình, dùng nhiều nick ảo. Mục tiêu: tạo engagement, social proof, kéo người thật comment theo.

### 6 kiểu comment (phân bổ đều)

1. **Hỏi giá / Hỏi chi tiết (4 câu)** — "ad ơi mổ smile pro trọn gói bao nhiêu ạ", "giá này áp dụng đến bao giờ ạ"
2. **Hỏi lịch / Đăng ký (3 câu)** — "e muốn book lịch khám cuối tuần đc k ạ", "ad cho e xin sđt tư vấn vs ạ"
3. **Tag bạn bè (3 câu)** — "@tên ơi cái này hay nè", "tag đứa bạn cận 10 độ vào đây 😂"
4. **Bày tỏ quan tâm (3 câu)** — "ôi giảm 50% thiệt hả", "e tính mổ lâu r mà chưa dám, giờ thấy ưu đãi ngon quá"
5. **Chia sẻ đã mổ ở đây (4 câu)** — "e mổ bên này r, bs tuấn mổ cho, ổn lắm mn", "mình mổ tháng trước r, recommend luôn nha"
6. **Hỏi thêm về trải nghiệm (3 câu)** — "ai mổ r cho e xin review với", "mổ có đau k mng", "bao lâu đi làm lại đc ạ"

### Quy tắc riêng mode `ads`
- Comment **ngắn gọn hơn** mode group — 1-2 câu, đúng kiểu comment Facebook Ads
- Một số comment chỉ là emoji hoặc tag bạn — tạo engagement tự nhiên
- **Không comment quá chuyên nghiệp** — phải giống người thật lướt thấy ads rồi comment nhanh
- Có vài comment hỏi giá/hỏi chi tiết đơn giản để admin (chính mình) reply lại, tạo tương tác 2 chiều
- Vài comment **chỉ tag bạn** kèm emoji hoặc 1 từ ngắn: "@bạn nè", "@tên check cái này đi"

### Ví dụ mode `ads`
- "ad ơi mổ smile pro trọn gói hết bao nhiêu ạ"
- "e muốn đk khám free đc k ạ, cuối tuần có làm k ad"
- "@LanNguyen ê m cận nặng vậy đi khám chỗ này đi 😂"
- "ôi giảm 50% thật á, chỉ từ 13tr thui hả 😳"
- "mình mổ chỗ này tháng trước r nè mn, bs tuấn mổ nhẹ nhàng lắm, giờ 10/10 r, recommend lun 👍"
- "mổ có đau k mng 🥲"
- "e ở bình dương lên mổ trong ngày về luôn đc k ạ"
- "đã inbox ad r ạ ❤️"
- "e tính mổ lâu r mà sợ, giờ thấy ưu đãi ngon quá tính liều lun hihi"
- "@MinhTran xem cái này đi bro"

---

## Process Flow

### Khi nhận lệnh `/seeding-dnd [mode] [tham số]`:

**Bước 1: Xác định mode**
- Không có tham số hoặc `group` → chạy Mode 1
- `reply-group "..."` → chạy Mode 2, parse câu hỏi gốc từ dấu ngoặc kép
- `ads` → chạy Mode 3

**Bước 2: Chọn Persona & Sinh nội dung**
- Chọn ngẫu nhiên 5-6 persona từ Persona Pool
- Sinh đúng ~20 câu seeding theo cấu trúc của mode tương ứng
- Đảm bảo đa dạng persona, cấu trúc câu, cách xưng hô

**Bước 3: Áp dụng Tone & Viết tắt**
- Viết theo đúng tone Gen Z/Office worker
- Không lặp cấu trúc giữa các câu
- Nội dung phải mới mẻ mỗi lần chạy (Example Bank chỉ tham khảo style)

**Bước 4: Xuất kết quả ra Chat**
- Hiển thị rõ ràng theo nhóm/kiểu để dễ copy
- Mode `reply-group`: hiện lại câu hỏi gốc ở đầu để tiện đối chiếu

**Bước 5: Lưu file scratch**
Lưu vào: `/Users/minhtqm1993/.gemini/antigravity-ide/scratch/seeding_<mode>_<timestamp>.md`
(timestamp định dạng `yyyyMMdd_HHmmss`). In đường dẫn file.

---

## Common Mistakes

| Sai lầm | Cách khắc phục |
|---------|----------------|
| Viết hoa, chấm phẩy trang trọng | Chữ thường, gõ tự nhiên, bỏ bớt dấu câu |
| Nhồi từ marketing quảng cáo | Dùng: "máy xịn", "khám kỹ", "ổn áp", "nhẹ nhàng" |
| Nhắc tên DND quá nhiều trong 1 câu | Tối đa 1 lần/câu, đôi khi chỉ nói "chỗ trương định q3" |
| Trùng cấu trúc câu | Đổi chủ ngữ + cách kết câu liên tục |
| Copy nguyên Example Bank | Chỉ tham khảo style — viết câu MỚI mỗi lần |
| Reply không liên quan câu hỏi gốc (mode reply-group) | Phải đọc kỹ câu hỏi gốc, reply đúng ngữ cảnh |
| Comment ads quá dài/chuyên nghiệp (mode ads) | Comment ngắn 1-2 câu, có emoji, giống comment nhanh trên đt |
| Tất cả comment ads đều khen | Phải xen kẽ hỏi giá, tag bạn, hỏi lịch — đa dạng kiểu tương tác |
