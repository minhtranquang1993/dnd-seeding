---
name: dnd-seeding-services
description: >
  Fact pack phi-tiền theo service cho skill dnd-seeding. Dùng để reply-group bám đúng chủ đề
  câu hỏi gốc thay vì trôi về mổ cận. KHÔNG chứa số tiền — mọi con số phí/ưu đãi sống ở
  fees-promos.md.
updated: 2026-08
---

# Fact pack theo service — DND Sài Gòn

> ⛔ **File này KHÔNG được chứa số tiền.** `fees-promos.md` là file duy nhất có tiền.
> Ở đây chỉ có: phương pháp, quy trình, thời gian, mốc tái khám, chuẩn bị trước khám.
> `qa_seeding.py --selftest` chạy gate **M6-E** quét file này bằng `MONEY_TOKEN_RX` — nhét số
> tiền vào đây là fail selftest, không phải chờ ai rà tay.
>
> Giá mổ Phaco, giá kính Ortho-K, giá lác/mộng/cườm nước **cố ý không có ở đây**. Chúng không
> nằm trong `fees-promos.md`, nên seeding **chuyển hotline** khi bị hỏi. Đưa vào là tái tạo
> đúng class bug §6 vừa sửa, chỉ dời chỗ.

**Nguồn:** script chat chính thức của bệnh viện (`quick_replies` export, 142 shortcut).
Không suy diễn ngoài nguồn này. Thiếu dữ kiện → reply nói chung + đẩy hotline, đừng bịa.

**Cách dùng:** `detect_topic()` trả `(phase, service)`. Lấy section `## <service>`, rồi lấy
tiểu mục `### pre` hoặc `### fu` theo `phase`.

**Luật chung cho mọi section:**
- Reply seeding là người thật kể lại, **không** phải tư vấn y khoa. Nói "bs bảo…", "hôm e đi
  thì…", không nói "phương pháp X chỉ định cho…".
- Mọi mốc hồi phục nói theo **khoảng**, không số cứng (§7C).
- Không cam kết kết quả. Không claim hết đau (§7C — 121 hit đang phải xoá).
- Nội dung **mổ** chỉ nhắc bs Tuấn. Nội dung **khám** được nhắc bs Tuấn / bs Linh / bs Hoàng Lan.

---

## phaco

**Là gì:** mổ đục thủy tinh thể (dân gian gọi **cườm khô**), thay thủy tinh thể nhân tạo.
Đây là cách điều trị duy nhất — nhỏ thuốc không làm tan được cườm đã đục.

**Nói được:**
- Mổ nhanh, tầm 3-5 phút mỗi mắt; khám và mổ có thể trong ngày nếu đủ điều kiện.
- Công nghệ Femto Phaco (thay dao cơ học), phục hồi thị lực nhanh sau 1-2 ngày.
- Có nhiều loại thủy tinh thể nhân tạo: đơn tiêu, hai tiêu, ba tiêu — bs tư vấn sau khám.
- **Có hỗ trợ BHYT.** Nói "có BHYT" được; **số tiền / % chi trả → hotline** (M6-D).
- Để lâu thành "cườm chín" thì mổ phức tạp hơn — nên đi khám sớm.
- Bệnh có thể tiến triển âm thầm, hay gặp ở người lớn tuổi.

**Đặc thù khi đi khám (khác mổ cận, đây là chỗ hay bị trôi):**
- Khám Phaco đi kèm **xét nghiệm máu** nếu muốn mổ trong ngày → **nhịn ăn sáng**.
- Mang theo **thẻ BHYT** (mổ cận không cần).
- Thuốc nội khoa đang uống vẫn dùng bình thường, không phải ngưng.

**Cấm:**
- Không nói khám Phaco free — khám Phaco **T2, có phí** (§6). Đây là lỗi cũ ở `:55`.
- Không nhắc BS Phí Duy Tiến (quick_replies có, nhưng luật skill chỉ truyền thông bs Tuấn).
- Không nêu giá thủy tinh thể → hotline.

### pre
Người nhà thường là người hỏi hộ ("mẹ e nhìn mờ…"). Reply nghe như con cháu dẫn ba mẹ đi khám:
kể chuyện đặt lịch, nhắc nhịn ăn sáng, nhắc mang BHYT, nhắc người lớn tuổi cần có người đi cùng.

### fu
Sau mổ Phaco: thẻ Family **2 năm** dùng tái khám (mổ cận là **3 năm** — đừng lẫn).
Tái khám theo lịch bs hẹn. Nói theo khoảng, không tự chế mốc.

---

## lao_thi

**Là gì:** mắt lão, nhìn gần mờ, thường sau 40 tuổi. **Điều trị được** — người lão thị
KHÔNG phải chỉ có đường đi cắt kính (đây là lỗi nhận thức skill đã ghi ở §5).

**Nói được:**
- Hai hướng: **Presbyond / PresbyMAX** (đường laser, cho người giác mạc còn tốt và chưa đục
  thủy tinh thể) hoặc **thay thủy tinh thể nhân tạo đa tiêu** (giải quyết luôn cả cườm về sau).
- Không có phương pháp "tốt nhất cho tất cả", chỉ có phương pháp hợp với mắt từng người.
- Mổ nhỏ thuốc tê bề mặt, không tiêm; tầm 10-15 phút mỗi mắt; về trong ngày, không nằm viện.
- Sau khi hết tê có thể cộm xốn, chảy nước mắt nhẹ như có bụi — vài tiếng là dịu.
- Khám lão thị khảo sát riêng: đo cấu trúc giác mạc, bản đồ giác mạc, đáy mắt, đánh giá độ
  linh hoạt thủy tinh thể còn lại, kiểm tra khả năng thích nghi của não với Presbyond.

**Phí — đọc kỹ, đây là chỗ dễ sai:**
- Lão thị đi đường **khúc xạ/laser** → T0, được nói free.
- Lão thị đi đường **Phaco + IOL đa tiêu** → **chưa có chính sách, KHÔNG báo phí → hotline**.
- Câu nào nhắc cả `lão thị` + `phaco` thì **nhóm chặn thắng** (§6, bẫy #3).

### pre
Persona hợp: người 45-55 đọc điện thoại phải để xa, hoặc con cái hỏi hộ ba mẹ.
Điểm chạm thật: "đeo kính lão bất tiện", "kính hai tròng nhìn chóng mặt".

### fu
Chưa có dữ kiện riêng trong nguồn → nói chung theo lịch bs hẹn, không bịa mốc.

---

## ksct

**Là gì:** kiểm soát cận thị cho trẻ. Không phải "thay kính cho bé nhìn rõ" — là theo dõi và
can thiệp để **hạn chế tốc độ tăng độ** và sự kéo dài trục nhãn cầu.

**Nói được:**
- **4 phương pháp:** tròng kính kiểm soát cận thị · kính áp tròng **Ortho-K** · nhỏ **Atropine**
  nồng độ thấp · liệu pháp ánh sáng đỏ theo chỉ định.
- **Ortho-K:** kính áp tròng cứng **đeo ban đêm**, sáng tháo ra vẫn nhìn rõ cả ngày, không cần
  kính gọng. Không phẫu thuật, thiết kế riêng theo giác mạc từng mắt.
- **Tròng kính KSCT:** vùng giữa cho bé nhìn rõ, xung quanh có vòng vi thấu kính đồng tâm tạo
  tín hiệu quang học trên võng mạc. Nhìn ngoài như kính gọng thường, bé đi học đeo bình thường.
- **Khám KSCT khác khám đo độ:** đo khúc xạ và thị lực, **đo chiều dài trục nhãn cầu**, chụp
  bản đồ giác mạc, kiểm tra điều tiết và phối hợp hai mắt, đánh giá nguy cơ tăng độ.
- **Thời gian khám:** tầm 60-90 phút nếu bé hợp tác; cần nhỏ thuốc liệt điều tiết thì 90-120 phút.
- Bé cần tái khám định kỳ để bs đánh giá hiệu quả.

**Chuẩn bị:** đang đeo **Ortho-K phải ngưng ít nhất 1 tháng** trước ngày khám
(lens mềm chỉ 1 tuần — đừng lẫn hai mốc này).

**Cấm:**
- Không nói khám Ortho-K / KSCT free — **T2, có phí** (§6). Persona "mẹ bỉm" đặc biệt dễ sai chỗ này.
- Không nêu giá kính Ortho-K → hotline.
- Không hứa "chặn đứng tăng độ" — chỉ nói hạn chế/làm chậm.

### pre
Persona hợp: mẹ bỉm, "con e lớp 5 tăng độ nhanh quá". Điểm chạm thật: sợ con tăng độ mỗi năm,
sợ con đeo lens hỏng mắt, hỏi bé mấy tuổi thì đeo Ortho-K được.

### fu
Theo dõi định kỳ trong năm: đo khúc xạ, đo trục nhãn cầu, chụp bản đồ giác mạc theo chỉ định bs.

---

## kinh

**Là gì:** khám đo độ - cắt kính. Đo khúc xạ để có đơn kính, **không** phải khám tiền phẫu.

**Nói được:**
- Đo độ cận/viễn/loạn, thử kính, ra đơn.
- Đang đeo **lens mềm ngưng ít nhất 1 tuần**, **Ortho-K ngưng ít nhất 1 tháng** trước khám.
- Sau mổ khúc xạ tại DND có voucher mua kính — nhưng **không nêu giá trị** → hotline.

**Cấm — chỗ này gắt nhất:**
- **Khám đo độ - cắt kính là T1, CÓ PHÍ.** Tuyệt đối không nói free.
- Có CT hỗ trợ **có điều kiện** — mức hỗ trợ và điều kiện đều ở `fees-promos.md`, chưa đọc
  thì không nêu.
- **Ngoại lệ duy nhất:** người **lão thị** hỏi cắt kính thì vẫn free (§6) — vì lão thị không bị
  đẩy sang đường cắt kính.
- Đừng biến câu hỏi cắt kính thành bài chào mổ cận. Người ta hỏi đo độ thì trả lời đo độ; muốn
  gợi mổ thì chỉ một câu nhẹ ở kiểu 10, không phải cả thread.

### pre
Persona hợp: dân văn phòng thay kính, sinh viên đổi kính mới. Điểm chạm: kính cũ nhức mắt,
nghi tăng độ.

### fu
Không áp dụng — cắt kính không có hậu phẫu.

---

## glaucoma

**Là gì:** cườm nước / tăng nhãn áp / glocom (thiên đầu thống). Khác hẳn cườm khô (Phaco).

**Nói được:**
- Điều trị bằng **thuốc** hoặc **laser**; không được thì mới tính phẫu thuật **cắt bè**.
- Cần bs chuyên khoa khám và theo dõi.
- **PGS.TS.BS Võ Thị Hoàng Lan** có thế mạnh glaucoma, viêm màng bồ đào (bs khám, không mổ).
- Đây là bệnh cần phát hiện sớm, để lâu ảnh hưởng thị lực.

**Cấm:** khám **T2 có phí**, không free. Không nêu giá mổ cắt bè → hotline.
Đừng lẫn **cườm nước** (glaucoma) với **cườm khô** (Phaco) — hai bệnh khác nhau.

### pre
Persona hợp: người trung niên đi khám vì nhức mắt, hoặc có người nhà bị glaucoma.

### fu
Chưa có dữ kiện riêng → theo lịch bs hẹn.

---

## vong_mac

**Là gì:** bệnh lý võng mạc - dịch kính, đáy mắt.

**Nói được:**
- DND có bs chuyên khoa võng mạc.
- **PGS.TS.BS Võ Thị Hoàng Lan**: võng mạc đái tháo đường, thoái hóa hoàng điểm, lỗ rách võng mạc.
- Chẩn đoán bằng **OCT**, chụp mạch huỳnh quang — giúp phát hiện sớm.
- **BSNT Bùi Quang Tuấn** làm can thiệp dịch kính - võng mạc.
- Khám đáy mắt thường phải nhỏ giãn đồng tử, mắt nhoè vài tiếng nên đừng tự lái xe về.

**Cấm:** khám **T2 có phí**, không free.

### pre
Persona hợp: người tiểu đường đi tầm soát, người thấy ruồi bay / chớp sáng.

### fu
Chưa có dữ kiện riêng → theo lịch bs hẹn.

---

## lac

**Là gì:** lác / lé.

**Nói được:**
- Mổ lác đơn thuần có làm tại DND.
- **Phải khám tìm nguyên nhân trước** rồi bs mới chỉ định được — không phải ca nào cũng mổ.

**Cấm:** không nêu giá mổ lác → hotline. Khám T2 có phí.

### pre
Persona hợp: ba mẹ có con bị lác, hoặc người lớn lác từ nhỏ giờ muốn xử lý.

### fu
Chưa có dữ kiện riêng → theo lịch bs hẹn.

---

## mong

**Là gì:** mộng thịt.

**Nói được:** có mổ mộng tại DND; có hỗ trợ BHYT (nói "có BHYT" được, **số → hotline**).

**Cấm:** không nêu giá mổ mộng → hotline. Khám T2 có phí.

### pre
Persona hợp: người làm ngoài trời nhiều, nắng gió.

### fu
Chưa có dữ kiện riêng → theo lịch bs hẹn.

---

## tham_my

**Là gì:** thẩm mỹ mắt — cắt mí, lấy mỡ bọng mắt, chỉnh sụp mi.

**Nói được:** DND có làm. Sụp mi có thể là vấn đề chức năng chứ không chỉ thẩm mỹ.

**Cấm:** khám **T2 có phí**, không free. Không nêu giá → hotline.

### pre
Persona hợp: người muốn cắt mí, hoặc sụp mi che tầm nhìn.

### fu
Chưa có dữ kiện riêng → theo lịch bs hẹn.

---

## tong_quat

**Là gì:** khám tổng quát / tổng quan — kiểm tra sức khỏe mắt định kỳ, không nhắm dịch vụ nào.

**Nói được:**
- Khám và tư vấn các bệnh lý về mắt nói chung.
- Đi khám định kỳ để phát hiện sớm.
- Nếu khám ra vấn đề cụ thể thì bs chuyển hướng chuyên sâu tương ứng.

**Cấm — chỗ hay sai:**
- **Khám tổng quát là T2, CÓ PHÍ.** Không được nói free. Gói 12 bước free **chỉ** cho khám mổ
  cận/khúc xạ, không áp cho tổng quát (§4).
- Có CT hỗ trợ có điều kiện — mức hỗ trợ ở `fees-promos.md`.

### pre
Persona hợp: người đi khám sức khỏe định kỳ, hoặc thấy mắt mỏi mà chưa biết bị gì.

### fu
Không áp dụng.

---

## Dữ kiện dùng chung mọi service

**Địa chỉ:** 147 - 147B - 147Bis Trương Định, **Phường Nhiêu Lộc**, TP.HCM (Phường 9, Quận 3 cũ).

**Giờ làm việc:** Thứ 2 - Thứ 7 sáng 8h00-12h00, chiều 13h00-17h00 (**nghỉ trưa 12h-13h**);
Chủ nhật **chỉ sáng** 8h00-12h00.

**Hotline / Zalo:** 0775 147 147 · 1900 8195.

**Đi khám mang theo:** CCCD hoặc VNeID. Có BHYT thì mang thẻ (Phaco, mộng).

**Ngày khám không nên:** trang điểm mắt, nối mi, đeo trang sức, **tự lái xe** (nhỏ giãn đồng tử
xong mắt nhìn gần mờ và nhạy sáng vài tiếng).

> ⚠️ Nhỏ giãn đồng tử **không phải đặc trưng của mổ cận** — Phaco, khám đáy mắt/võng mạc, khám
> liệt điều tiết cho bé đều nhỏ giãn. Nhắc chuyện nhoè mắt / nhờ người chở về trong reply Phaco
> hay võng mạc là **hợp lệ**, không tính là trôi chủ đề (xem `KX_CONTEXT` trong `qa/checks.md`).

**Ngưng kính áp tròng trước khám:** lens mềm ≥ 1 tuần · Ortho-K ≥ 1 tháng.

**BHYT:** DND **có** hỗ trợ BHYT (Phaco, mộng, cườm nước). Nói "có BHYT" được — **số tiền hoặc
% chi trả thì chuyển hotline** (M6-D). Shortcut `bhyt` cũ trong quick_replies nói "chưa áp dụng"
đã lỗi thời, chốt với user 2026-08: dùng bản có BHYT.

**Các chi nhánh:** DND Sài Gòn (147 Trương Định) · DND Hà Nội · DND Bắc Giang · DND Hải Dương.
Seeding cho DND Sài Gòn thì đừng kể chi nhánh khác trừ khi người hỏi ở tỉnh đó.
