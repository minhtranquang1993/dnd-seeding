---
name: dnd-seeding
description: >
  Tạo danh sách ~20 content seeding ngắn dạng câu hỏi cho Bệnh viện Mắt Quốc tế DND Sài Gòn.
  Trigger khi user gõ "/dnd-seeding", "dnd-seeding", "seeding-dnd", "content seeding dnd", hoặc yêu cầu
  tạo ý tưởng/câu hỏi đi seeding cho DND.
---

# Seeding DND Skill 👁️

Tạo content seeding tự nhiên cho Bệnh viện Mắt Quốc tế DND Sài Gòn (147 Trương Định, Quận 3, TP.HCM) với 3 chế độ khác nhau tùy mục đích sử dụng.

## Repo

Skill này được đồng bộ với repo GitHub riêng: https://github.com/minhtranquang1993/dnd-seeding (nhánh `main`, chỉ có file `SKILL.md`).
- **Push cập nhật lên repo:** copy `SKILL.md` vào clone local của repo trên, commit, push.
- **Pull về máy:** lấy `SKILL.md` từ repo trên, ghi đè vào `C:\Users\Admin\.claude\skills\dnd-seeding\SKILL.md`.

## When to Use

- `/dnd-seeding group` — Tạo ~28 bài đăng seeding trên group mổ cận
- `/dnd-seeding reply-group "câu hỏi gốc"` — Tạo ~20 comment reply vào bài người khác trên group
- `/dnd-seeding ads` — Tạo ~20 comment seeding dưới bài quảng cáo của mình
- `/dnd-seeding` (không tham số) — Mặc định chạy mode `group`

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
| **Người tìm hiểu nhiều viện** | "e đi khám 2-3 chỗ r", "đang cân nhắc mổ ở đâu", "so sánh giá/công nghệ mấy viện" |

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

# MODE 1: `/dnd-seeding group`

**Mục đích:** Tạo ~28 bài đăng mới trên các group review mổ cận (Hội mổ cận, Hội review SMILE Pro...). Đóng vai người đi tìm hiểu, người đã mổ xong muốn chia sẻ, hoặc người đang kể lại một trải nghiệm/tâm trạng cụ thể.

### Phân bổ 8 góc (tổng ~28 câu)

1. **Góc 1: Hỏi review Bác sĩ (3 câu)** — Hỏi tay nghề/khám của BS Tuấn (mổ chính), BS Linh, BS Hoàng Lan (khám). Ai mát tay, ai khám kỹ.
2. **Góc 2: Chi phí & Ưu đãi (3 câu)** — Hỏi khám 12 bước 0đ, SmileDays giảm 50%, giá trọn gói.
3. **Góc 3: So sánh Công nghệ (3 câu)** — SMILE Pro vs SmartSight, SmartSurfACE cho mắt mỏng, Phakic ICL cho cận nặng.
4. **Góc 4: Dịch vụ & CSVC (3 câu)** — Quy trình trong ngày, phòng ốc, Ortho-K cho trẻ.
5. **Góc 5: Hậu phẫu (3 câu)** — Hồi phục, khô mắt, tái khám, kiêng cữ.
6. **Góc 6: Social proof — Người đã mổ xong (5 câu)** — Chia sẻ trải nghiệm tích cực, kể chi tiết (BS, thị lực, số ngày hồi phục).
7. **Góc 7: Story kể chuyện (4 câu)** — Bài dài hơn hẳn các góc khác (1 đoạn 4-6 câu, kể mạch trải nghiệm thật). Chủ đề: tâm lý lo lắng/rén trước ngày mổ, buổi khám chuyên sâu 12 bước diễn ra thế nào, băn khoăn trước khi quyết định mổ. Luôn đặt bối cảnh ở DND Sài Gòn/DND Trương Định — không dùng tên bệnh viện khác. Kết bài bằng 1 câu hỏi xin chia sẻ/động lực/kinh nghiệm từ mọi người, không phải câu hỏi thông tin khô khan.
8. **Góc 8: So sánh bệnh viện (4 câu)** — Đóng vai người đang tìm hiểu nhiều nơi: đã khám (hoặc định khám) ở 1-2 viện khác — ví dụ Mắt Sài Gòn, Mắt TPHCM, Việt Nhật — và đang cân nhắc thêm DND Sài Gòn để khám/so sánh giá, công nghệ, cách tư vấn. DND luôn xuất hiện như **1 lựa chọn đang xem xét** bên cạnh viện khác, không phải viện đã chốt hay được khen vượt trội — giữ đúng tinh thần "đang tìm hiểu, chưa quyết".

### Ví dụ mode `group`
- "mn có ai mổ cận chỗ bs tuấn dnd sài gòn chưa ạ, cho e xin review tay nghề bác với"
- "e thấy bên dnd sg đang smiledays giảm 50%, tc tầm 25tr mổ đc gói nào tốt nhỉ"
- "mình mổ smile pro bên dnd trương định tuần trước, bs tuấn mổ cho, nhẹ nhàng lắm mn, 2 ngày đi làm lại r"
- (Góc 7 - story) "e vừa đặt lịch mổ cận tuần sau ở dnd sài gòn xong mà từ hôm qua đến giờ tự nhiên lại thấy rén 😅. lúc đi khám thì quyết tâm lắm, bs bảo mắt e đủ điều kiện, cũng chọn được phương pháp r. về nhà bố mẹ lại hỏi đủ thứ, có đau k, nhỡ sau này có vấn đề thì sao, làm e cũng dao động theo. anh/chị nào từng mổ ở dnd sg r cho e xin ít động lực với ạ, k biết trước ngày mổ mn có bị tâm lý giống e k"
- (Góc 7 - story) "mn cho e xin review mổ cận ở dnd sài gòn với ạ 🙏 tuần trước e đi khám chuyên sâu trước mổ ở đây, bình thường e khá sợ khám mắt vì nhìn máy móc là run, nhưng buổi khám nhẹ nhàng hơn e tưởng, mất khá nhiều tg vì qua nhiều bước, có nhỏ thuốc rồi đợi đo lại nên gần cả buổi sáng. bs giải thích tình trạng mắt e khá kỹ và tư vấn e đủ điều kiện mổ smile pro, nhưng e vẫn chưa chốt ngay vì đây là quyết định lớn. ai mổ ở dnd sg r cho e xin ít review: thị lực sau mổ ổn k, hồi phục ntn, bv theo dõi hậu phẫu có kỹ k ạ, e cảm ơn mn nhiều"
- (Góc 8 - so sánh viện) "e cận 5 độ loạn 1, mới khám ở mắt sg đc tư vấn femto pro với smile pro r, giờ muốn khám thêm chỗ khác xem sao. có ai khám ở dnd sài gòn r k, chi phí khám bên đó tầm nhiêu, có nên qua khám thêm 1 vòng trước khi chốt k ạ"
- (Góc 8 - so sánh viện) "e đang phân vân giữa mắt tphcm với dnd trương định q3, chưa biết nên khám ở đâu trước, ai đi khám cả 2 chỗ r so sánh giúp e với"

---

# MODE 2: `/dnd-seeding reply-group "câu hỏi gốc"`

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

# MODE 3: `/dnd-seeding ads`

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

### Khi nhận lệnh `/dnd-seeding [mode] [tham số]`:

**Bước 1: Xác định mode**
- Không có tham số hoặc `group` → chạy Mode 1
- `reply-group "..."` → chạy Mode 2, parse câu hỏi gốc từ dấu ngoặc kép
- `ads` → chạy Mode 3

**Bước 2: Chọn Persona & Sinh nội dung**
- Chọn ngẫu nhiên 5-6 persona từ Persona Pool
- Sinh đúng số câu theo cấu trúc của mode tương ứng (mode `group` ~28 câu, mode `reply-group`/`ads` ~20 câu)
- Đảm bảo đa dạng persona, cấu trúc câu, cách xưng hô

**Bước 3: Áp dụng Tone & Viết tắt**
- Viết theo đúng tone Gen Z/Office worker
- Không lặp cấu trúc giữa các câu
- Nội dung phải mới mẻ mỗi lần chạy (Example Bank chỉ tham khảo style)

**Bước 4: Xuất kết quả ra Chat**
- Hiển thị rõ ràng theo nhóm/kiểu để dễ copy
- Mode `reply-group`: hiện lại câu hỏi gốc ở đầu để tiện đối chiếu

**Bước 5: Lưu file scratch**
Lưu vào: `C:/tmp/seeding_<mode>_<timestamp>.md`
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
