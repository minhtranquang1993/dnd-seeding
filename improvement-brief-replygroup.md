# Improvement Brief: `reply-group` bám sát câu hỏi gốc theo service

## Hiện trạng (baseline, đo trên SKILL.md + qa_seeding.py)

**Vấn đề user báo:** reply-group trả lời câu hỏi nào cũng kéo về mổ cận / khúc xạ.

**Nguyên nhân, đọc từ code:**

1. MODE 2 (`SKILL.md:356-422`) **không có bước phân loại service** trước khi chọn kiểu reply.
   Skill nhảy thẳng từ "AI đọc câu hỏi gốc" → "chọn 1 trong 10 kiểu". Không có chỗ nào hỏi
   "câu này thuộc nhóm dịch vụ nào".
2. **Cả 10 kiểu đều được mô tả bằng ngôn ngữ mổ cận.** Kiểu 1 "chọn mổ bên DND SG";
   kiểu 8 (đính chính) chỉ liệt kê 3 nhầm lẫn, cả 3 về mổ khúc xạ; kiểu 9 (quy trình) chỉ
   có nhỏ thuốc giãn + nhờ chở về; kiểu 10 "chưa mổ, đang xem 2-3 chỗ".
3. **Toàn bộ block ví dụ (`SKILL.md:406-422`) dùng đúng 1 câu hỏi gốc** về SMILE Pro.
   Mục Tone ghi rõ skill đang chỉ thị model bắt chước example, và chỉ thị đó có hiệu lực
   đo được (`10/10` 167 hit, `nhẹ nhàng` 281 hit). Một bộ example toàn mổ cận là style
   reference cho mọi câu hỏi.
4. **Skill không có dữ kiện để trả lời service khác.** §5 "Dịch vụ khác" chỉ có 4 dòng một
   câu cho Ortho-K / Phaco / thẩm mỹ / lão thị. Không có quy trình, thời gian, mốc tái khám,
   phương pháp — nên kể cả khi model muốn bám câu hỏi, nó không có gì để nói ngoài mổ cận.
5. **QA script không gác chủ đề.** `check_new_angles` (`qa_seeding.py:1080`) chỉ kiểm kiểu
   6/7 có mặt, kiểu 6 có điểm dở thật, kiểu 7 không nhắc brand, và 10/10. Không có gate nào
   đối chiếu nội dung reply với câu hỏi gốc.

**Cái đã có sẵn và dùng lại được:** §6 đã có bucket table service-aware
(`kx`/`kinh`/`pc`/`or`/`khac`/`lt_phaco`/`fu_*`) và `detect_bucket()` (`qa_seeding.py:656`)
đã cưỡng chế nó cho luật phí. Khung phân loại **đã tồn tại và đã được test** — nó chỉ chưa
được dùng để lái nội dung.

**Nguồn dữ liệu mới:** `quick_replies_..._1786000138.xlsx` (142 shortcut, Downloads) — script
chat chính thức của bệnh viện. Rút được dữ kiện cho Phaco, lão thị, kiểm soát cận thị/Ortho-K,
cắt kính, tổng quát, lác, mộng, cườm nước, trả góp, mốc tái khám, ngưng lens.

## Mục tiêu cải thiện (đo được)

1. Câu hỏi Phaco / cắt kính / tổng quát / lão thị / Ortho-K sinh ra reply **nói đúng service
   đó**, không trôi sang SMILE/mổ cận.
2. Reply mang **dữ kiện thật của DND** cho service đó, không nói chung chung.
3. Thất bại này **không thể tái phát im lặng** — QA script fail, không chỉ là chữ trong SKILL.md.

## Quyết định đã chốt với user (Gate 1)

| Câu | Chốt |
|---|---|
| BHYT (quick_replies mâu thuẫn: `bhyt` nói chưa áp dụng, `GIÁPHACO` nói chi trả 80-100%) | **Có BHYT — được nhắc.** Shortcut `bhyt` coi như bản cũ đã lỗi thời |
| Địa chỉ / giờ làm việc | **Cập nhật cả 2** theo quick_replies: Phường Nhiêu Lộc (Q3 cũ), nghỉ trưa 12h-13h, CN chỉ sáng |
| Bác sĩ cho reply Phaco | **Chỉ BS Tuấn**, giữ luật hiện tại. KHÔNG thêm BS Phí Duy Tiến, KHÔNG thêm BS Thu Hà (memory: BS Hà đã nghỉ) |
| Phạm vi | **SKILL.md + QA script cưỡng chế** |

## Hướng đề xuất

### A. `services.md` — fact pack theo bucket (file mới, thứ 5)

Layout hiện tại 4 file. Thêm file thứ 5, cùng cơ chế "mandatory read" như `fees-promos.md`.

**Bất biến phải giữ: `fees-promos.md` là file DUY NHẤT có số tiền.** `services.md` chứa dữ kiện
phi-tiền: phương pháp, quy trình, thời gian, mốc tái khám, chuẩn bị trước khám. Giá mổ Phaco
(9tr-40tr), giá kính Ortho-K (18-21tr), lác (9.9tr), mộng (3.95-4.6tr), cườm nước (3-6.5tr)
trong quick_replies **không** được đưa vào — chúng không nằm trong `fees-promos.md`, nên
seeding chuyển hotline. Đưa vào là tái tạo đúng class bug §6 vừa sửa, chỉ dời chỗ.

Mỗi topic (§C1) có: nói được gì · reply nghe như người thật ra sao · cấm gì.
Section trong `services.md` khớp 1-1 với nhãn `service` của `detect_topic()` để người sửa skill
không phải tự map — `## phaco`, `## lao_thi`, `## ksct`, `## kinh`, `## glaucoma`, `## vong_mac`,
`## lac`, `## mong`, `## tham_my`, `## tong_quat`. Mỗi section có 2 tiểu mục theo `phase`:
`### pre` (chuẩn bị, quy trình khám) và `### fu` (mốc tái khám, hậu phẫu).

### B. MODE 2 — thêm Bước 0 phân loại + bảng thích ứng kiểu

- Bước 0: đọc câu hỏi gốc → xác định **`(phase, service)`** (bảng §C1, không phải bucket phí) → in ra đầu file.
- Bảng "kiểu N nói gì theo service": kiểu 8/9/10 hiện chỉ có phiên bản mổ cận; bổ sung phiên
  bản cho phaco / lao_thi / ksct / kinh / glaucoma / vong_mac / lac / mong / tham_my / tong_quat.
- Thêm block ví dụ cho **2 câu hỏi gốc mới** (Phaco, cắt kính) bên cạnh ví dụ SMILE hiện có,
  để example bank không còn một màu.
- In `**Câu hỏi gốc:**` và `**Topic:** <service> / <phase>` ở đầu output theo format cố định (script parse được).

### C. QA script — gate M6 `topic-fit`

#### C1. `TOPIC` — nhãn chủ đề riêng, KHÔNG dùng lại bucket phí (ISSUE-2)

`detect_bucket()` là bảng phân loại **phí**, và nó gộp những thứ mà topic-fit cần tách:
`lt_phaco` gộp lão thị + Phaco vào một ô vì cả hai cùng route hotline. Dùng nó để gác chủ đề
thì reply về Phaco sẽ thoả câu hỏi lão thị và ngược lại — đúng chỗ user đang than.

Nên tách: `detect_bucket()` **giữ nguyên, không sửa** (fee logic đã test kỹ, đụng vào là
regression). Thêm hàm mới `detect_topic()` chạy độc lập, trả nhãn hẹp hơn:

| topic | Token nhận diện (bỏ dấu bằng `norm()` sẵn có) |
|---|---|
| `kx` | `mổ cận`, `mổ viễn`, `mổ loạn`, `mổ khúc xạ`, `khúc xạ`, `smile`, `lasik`, `smartsight`, `smartsurface`, `clear`, `femto`, `phakic`, `icl` |
| `phaco` | `phaco`, `thủy tinh thể`, `đục thủy tinh`, `cườm khô`, `mổ cườm`, `iol` |
| `lao_thi` | `lão thị`, `presbyond`, `presbymax`, `mắt lão`, `nhìn gần mờ`, `đeo kính lão` |
| `ksct` | `ortho`, `ortho-k`, `orthok`, `kiểm soát cận`, `kính đêm`, `đeo đêm`, `tròng kính ksct`, `atropine`, `trục nhãn cầu` |
| `kinh` | `cắt kính`, `đo độ`, `đo mắt`, `thay kính`, `mua kính`, `kính mới`, `đo kính` |
| `glaucoma` | `glaucoma`, `glocom`, `tăng nhãn áp`, `cườm nước`, `cắt bè`, `thiên đầu thống` |
| `vong_mac` | `võng mạc`, `dịch kính`, `bong võng mạc`, `hoàng điểm`, `đáy mắt` |
| `lac` | `lác`, `lé`, `mắt lệch` |
| `mong` | `mộng`, `mộng thịt` |
| `tham_my` | `cắt mí`, `sụp mi`, `bọng mắt`, `thẩm mỹ mắt`, `lấy mỡ` |
| `tong_quat` | `tổng quát`, `tổng quan`, `khám định kỳ`, `kiểm tra sức khỏe mắt` |
| `none` | không khớp gì |

**Không còn ô `khac` gộp (ISSUE-2).** Bản trước dồn võng mạc + glaucoma + lác + mộng + thẩm mỹ
+ tổng quát vào một ô. Như vậy M6-B chỉ chặn được trôi sang mổ cận, còn hỏi lác mà reply nói
cườm nước thì **pass** — vẫn đúng cái user đang than, chỉ hẹp hơn một bậc. Sáu nhóm này khác
nhau cả về phương pháp lẫn cách người ta hỏi, nên tách.

Bảng phí §6 vẫn gộp chúng thành `khac`/T2 và **không sửa** — hợp lý ở đó, vì cả sáu **cùng một
mức phí**. Nhưng phí giống nhau không có nghĩa nội dung giống nhau. Đây chính là lý do topic
phải là bảng riêng, không phải bucket phí dùng lại.

#### C1b. `fu` không phải topic — nó là pha (ISSUE-1)

"mẹ e mới mổ phaco tái khám sao ạ" vẫn là câu hỏi **về Phaco**. Nếu `fu` là một nhãn đứng riêng
và được miễn M6-B, thì reply trôi sang hậu phẫu **mổ cận** vẫn pass — mà hướng dẫn hậu phẫu
Phaco / Ortho-K / lão thị khác hẳn mổ cận (nhịn ăn xét nghiệm, mốc tái khám, thẻ Family 2 năm
vs 3 năm). Đúng class lỗi đang sửa, chỉ nằm ở nhánh hậu phẫu.

Nên `detect_topic()` trả **tuple `(phase, service)`**:
- `phase` ∈ {`fu`, `pre`} — có token hậu phẫu (`tái khám`, `sau mổ`, `hậu phẫu`, `mới/vừa/đã mổ`) hay không
- `service` = nhãn ở bảng C1, hoặc `none`

`fu` + `phaco` → `("fu", "phaco")`. **M6-B áp trên `service`, không quan tâm `phase`** — nên câu
hỏi tái khám Phaco vẫn bị gác. Chỉ khi `service == "none"` (hậu phẫu trơn, không nêu mổ gì) mới
bỏ qua M6-B, vì lúc đó không có gì để trôi khỏi.

`phase` không vô dụng: nó chọn *khía cạnh* trong `services.md` (§A) — `fu` thì lấy mục mốc tái
khám, `pre` thì lấy mục chuẩn bị trước khám. Nhưng nó không nới gate.

**Ladder cho `service`:** `lao_thi` → `phaco` → `ksct` → `glaucoma` → `vong_mac` → `lac` →
`mong` → `tham_my` → `kinh` → `tong_quat` → `kx` → `none`.

- `kx` đứng **cuối** để `mổ` trơn không nuốt nhóm khác — cùng cái bẫy §6 đã ghi ở "Ba cái bẫy hay sai" #1.
- `lao_thi` đứng **trước** `phaco`: người hỏi lão thị cần nghe Presbyond / IOL đa tiêu, không
  phải bài Phaco thường. Fee vẫn route `lt_phaco` → hotline như cũ; hai hệ thống không gọi nhau.
- `tong_quat` đứng **sau** các nhóm cụ thể: "khám tổng quát xem có bị cườm không" là câu hỏi về cườm.

#### C1c. `kx_context` — drift lexicon, bắt trôi không cần token (ISSUE-2 vòng 2)

M6-B chỉ bắt được khi item mang token service **khác**. Nhưng phần lớn drift thật không nhắc
"SMILE" — nó nói *giọng* mổ cận: "nhỏ thuốc giãn xong nhờ người chở về", "đo bản đồ giác mạc",
"chờ giác mạc ổn", "k dụi mắt sau laser", "ngưng lens 1 tuần trước". Những câu này không mang
token `kx` nào nên bị M6-B **bỏ qua** — đúng loại drift mà kiểu 9 (quy trình) hiện sinh ra, vì
kiểu 9 trong SKILL.md chỉ có đúng phiên bản mổ cận.

Nên thêm `KX_CONTEXT` — cụm **chỉ đúng với khúc xạ**, rút từ chính example block hiện có
(`SKILL.md:406-422`) và mục kiểu 9:

`bản đồ giác mạc` · `độ dày giác mạc` · `giác mạc mỏng` · `giác mạc dày` · `sau laser` ·
`vạt giác mạc` · `ngưng lens` · `ngưng kính áp tròng` · `thoát kính` · `k đeo kính nữa` · `12 bước`

**Cụm nào dùng chung nhiều service thì KHÔNG vào list.** Tiêu chí loại: nếu Phaco / võng mạc /
khám trẻ em cũng nói cụm đó một cách hợp lệ thì loại.

| Cụm bị loại | Lý do |
|---|---|
| `nhỏ thuốc giãn` | Phaco, võng mạc/đáy mắt, khám liệt điều tiết cho bé đều nhỏ giãn. Quick_replies xác nhận: `LỊCHPHACO` và `qt-ksct` đều nhắc |
| `chở về` + `mắt nhoè` | Hệ quả của nhỏ giãn, nên thừa hưởng đúng vấn đề trên. Lời dặn "đừng tự lái xe" là chung cho mọi ca có giãn đồng tử |
| `khám chuyên sâu` | Phaco, Ortho-K, lão thị đều dùng đúng chữ này |
| `nhãn áp` | Glaucoma dùng nhiều hơn khúc xạ |

Sau khi loại, list chỉ còn cụm mà đọc lên là biết đang nói mổ cận: cấu trúc giác mạc (`bản đồ`,
`độ dày`, `vạt`), laser, ngưng lens trước đo khúc xạ, và mục tiêu bỏ kính. Danh sách ngắn có
chủ đích — gate hẹp mà đúng đáng tin hơn gate rộng mà hay báo nhầm.

**M6-B mở rộng:** `service` câu hỏi ∉ {`kx`, `none`}, item mang token service khác **hoặc** cụm
`KX_CONTEXT`, mà không mang token service câu hỏi → **FAIL**.

Escape hatch giữ nguyên: item mang cả token service câu hỏi thì pass, kể cả có `KX_CONTEXT`
(so sánh hợp lệ).

#### C2. Rule

#### C1d. "Item thực chất" — chống lách bằng câu rỗng (ISSUE-1 vòng 2)

M6-C ngưỡng 20% quá dễ: 20 item, 4 câu đúng chủ đề + 16 câu chung chung không mang token nào
vẫn pass — đúng cái user đang than, chỉ đổi hình từ "trôi sang mổ cận" thành "nói chung chung".

Nên phân loại item trước khi tính tỉ lệ:

| Loại | Định nghĩa | Vào mẫu số M6-C? |
|---|---|---|
| **neutral** | Item thuộc Kiểu 7 (hỏi lại, cấm nhắc DND) — nhận theo section header | ❌ |
| **substantive** | Mọi item còn lại | ✅ |

**M6-C sửa lại:** trong nhóm **substantive**, tỉ lệ item mang token service câu hỏi phải
**≥ 60%** khi `service` ∉ {`kx`, `none`}. Kiểu 7 nằm ngoài mẫu số vì nó tồn tại để *không*
nhắc gì — ép nó mang token là phá sàn chống "thread toàn khen" ở §7.

60% chứ không 100%: kiểu 6 (mixed) và kiểu 10 (đang cân nhắc) có quyền nói về trải nghiệm
chung mà không lặp tên service ở mọi câu. Nhưng 60% có nghĩa **đa số câu trả lời thật phải
chạm đúng service**, không còn lách được bằng 16 câu rỗng.

Ngưỡng 20% cũ giữ lại làm gì? Không — bỏ hẳn, thay bằng 60% trên mẫu số hẹp hơn. Hai ngưỡng
cùng lúc là hai nguồn sự thật.

| Rule | Hành vi |
|---|---|
| M6-A | Mọi draft `reply-group`, **bất kể số item**, thiếu `**Câu hỏi gốc:**` → **FAIL**. Không khai câu hỏi thì M6-B/C không có gì để đối chiếu (ISSUE-3) |
| M6-B | `service` của câu hỏi ∉ {`kx`, `none`}, item mang token service **khác** hoặc cụm `KX_CONTEXT` (§C1c), mà **không** mang token service câu hỏi → **FAIL** (drift) |
| M6-C | Full run (≥10 item), trong nhóm **substantive** (§C1d), tỉ lệ item mang token service câu hỏi < **60%** → **FAIL** (trả lời chung chung / lạc đề) |
| M6-D | Nhắc BHYT kèm số (`%`, tiền) → **FAIL**. Được nói "có BHYT hỗ trợ", số thì hotline |
| M6-E | `services.md` chứa token tiền → **FAIL** trong `--selftest` (ISSUE-4) |

**M6-B giờ gác mọi cặp service, không riêng "trôi sang `kx`" (ISSUE-2).** Hỏi lác mà reply nói
cườm nước → FAIL, vì `lac` ≠ `glaucoma`. Bản trước cả hai cùng ô `khac` nên lọt.

**M6-A áp cho mọi độ dài, không riêng full run.** Fixture reply-group cũ
(`SELFTEST_DRAFT_GOOD`, `M5_GOOD`, `M5_CONTEXT`, `_FB_HEAD`) sẽ được **thêm marker vào**, không
miễn trừ theo tên. Miễn theo tên là tạo một lớp draft mà gate không nhìn — đúng cái
`SELFTEST_MODE_EXEMPT` được viết ra để chống.

**M6-E chi tiết:** scan `services.md` bằng `MONEY_TOKEN_RX` sẵn có, cộng thêm `\d+ *(đ|đồng|vnd)`.
Allowlist các số **không phải tiền**: giờ (`8h`, `12h00`), thời lượng (`3-5 phút`, `60-90 phút`,
`24h`), mốc thời gian (`1 ngày`, `1 tuần`, `1 tháng`, `3-6 tháng`, `3 năm`, `2 năm`), độ cận
(`-20 diop`, `18 độ`), tuổi (`6-18 tuổi`), kích thước (`2mm`). Cách hẹp và kiểm được: allowlist
theo **hậu tố đơn vị** ngay sau số, không theo giá trị.

**Cố tình hẹp, để gate đáng tin:**
- M6-B escape hatch: item mang **cả hai** service token (so sánh hợp lệ, vd "mẹ e mổ phaco còn e mổ cận") thì pass
- Item không mang token service nào thì bỏ qua. Kiểu 7 (hỏi lại) tồn tại để không nhắc gì
- `service == "kx"` **không** kích hoạt M6-B. Câu hỏi mổ cận mà nhắc phaco là hành vi hợp lệ
  của kiểu 8/10 (đính chính, so sánh) — gác chiều đó mua coverage bằng giá false positive
- `service == "none"` không kích hoạt M6-B, kể cả khi `phase == "fu"` — không có gì để trôi khỏi
- M6-C mẫu số **loại Kiểu 7**: kiểu đó tồn tại để không nhắc gì, ép nó mang token là phá sàn §7

### D. Context & Reference Data — sửa theo chốt Gate 1

Địa chỉ, giờ làm việc, BHYT. Không đụng phần bác sĩ.

## Phạm vi

**Trong:** `SKILL.md` (MODE 2, §1 địa chỉ/giờ, §5 dịch vụ, Common Mistakes, Mandatory reads,
Repo & đồng bộ) · `services.md` (mới) · `scripts/qa_seeding.py` (M6 + fixtures).

**Ngoài — cố ý không đụng:**
- `fees-promos.md` — không có số mới; bất biến "1 file có tiền" giữ nguyên
- §6 luật phí, `detect_bucket()`, `free_exam_allowed()` — dùng lại, không sửa logic
- §7 guardrail, anti-repeat, quota 10/10
- Mode `group` / `story` / `ads` / `live` / `maps` / `koc`
- Danh sách bác sĩ

## Rủi ro regression

| Rủi ro | Chặn bằng |
|---|---|
| M6 false-positive trên reply-group mổ cận đang chạy tốt | `service == "kx"` không kích hoạt M6-B; fixture GOOD/M5_GOOD hiện có phải còn pass sau khi thêm marker |
| **Tách 6 nhãn làm M6-B chặt hơn → false-positive mới** | Escape hatch (item mang cả 2 token) áp cho mọi cặp, không riêng cặp có `kx`. Item không mang token service nào vẫn bỏ qua |
| **Ladder 11 bậc khó suy luận khi sửa sau này** | Ladder ghi thành một hằng số list có thứ tự trong script, không phải chuỗi `if/elif` rải rác; fixture khoá 3 cặp dễ lẫn: `lão thị+phaco`, `tổng quát+cườm`, `mổ+ortho` |
| **M6-C 60% ép reply lặp tên service tới mức máy móc** | Mẫu số loại Kiểu 7; ngưỡng 60% chứ không 100% để kiểu 6/10 còn chỗ thở. Fixture khoá: draft tự nhiên có 12/20 item chạm service → PASS |
| **`KX_CONTEXT` false-positive trên cụm dùng chung** | List chỉ chứa cụm đặc-hiệu-khúc-xạ. `nhỏ thuốc giãn`, `chở về`+`mắt nhoè`, `khám chuyên sâu`, `nhãn áp` bị loại có chủ đích (bảng §C1c) — cả bốn đều hợp lệ cho Phaco/võng mạc/khám bé. Fixture chống over-fire cho 3 service |
| Thêm `**Câu hỏi gốc:**` phá `parse_items()` | Dòng không khớp ITEM_RX/SECTION_RX/ITEM_HEADER_RX; chạy selftest xác nhận số item không đổi |
| `detect_topic()` lệch `detect_bucket()` gây 2 nguồn sự thật về service | Hai hàm trả lời **hai câu hỏi khác nhau** (phí vs chủ đề) và không gọi nhau. Ghi rõ trong docstring; fixture khẳng định `lão thị + phaco` → bucket `lt_phaco` nhưng service `lao_thi` |
| services.md có số tiền → thành copy thứ 2 của bảng phí | M6-E cưỡng chế trong `--selftest`, không chỉ rà tay |
| Fact pack sai lệch với thực tế bệnh viện | Chỉ lấy dữ kiện từ quick_replies (nguồn của bệnh viện), không suy diễn |
| Sync thiếu runtime (đã xảy ra: 3 runtime 3 version) | Cập nhật mục "Repo & đồng bộ" từ 4 → 5 path |

## Acceptance criteria

- [ ] `--selftest` xanh, gồm fixture M6 mới:
      drift FAIL (hỏi Phaco, reply SMILE) · on-topic PASS · thiếu marker FAIL ·
      BHYT+số FAIL · `lão thị + phaco` → service `lao_thi` không phải `phaco` ·
      escape hatch (item mang cả 2 token) PASS
- [ ] **ISSUE-1:** "mẹ mới mổ phaco tái khám sao" → `("fu", "phaco")`; reply nói hậu phẫu
      **mổ cận** → FAIL M6-B. Hậu phẫu trơn ("mới mổ tuần trước, kiêng gì ạ") → `("fu", "none")`,
      không kích hoạt M6-B
- [ ] **ISSUE-2:** hỏi lác, reply nói cườm nước → FAIL M6-B (bản cũ pass vì cùng ô `khac`).
      Sáu nhãn tách (`glaucoma`/`vong_mac`/`lac`/`mong`/`tham_my`/`tong_quat`) mỗi nhãn có
      ≥1 fixture nhận diện đúng
- [ ] **ISSUE-2 vòng 2 (drift không token):** câu hỏi Phaco, reply nói "đo bản đồ giác mạc" /
      "chờ giác mạc ổn sau laser" — **không** chứa chữ SMILE/LASIK/mổ cận nào → vẫn FAIL M6-B
      qua `KX_CONTEXT`
- [ ] **ISSUE-1 vòng 3 (cụm dùng chung không được false-positive):** reply hợp lệ cho câu hỏi
      **Phaco** / **võng mạc** / **khám bé** có nhắc `nhỏ thuốc giãn`, `mắt nhoè nhờ chở về`,
      `khám chuyên sâu`, `nhãn áp` mà không trôi sang khúc xạ → **PASS**. Đây là fixture chống
      over-fire, phải có cho cả 3 service
- [ ] **ISSUE-1 vòng 2 (lách bằng câu rỗng):** 20 item hỏi Phaco, 4 item nói Phaco + 16 item
      chung chung không token → **FAIL** M6-C (bản 20% cũ pass). Cùng draft đó nâng lên 12 item
      nói Phaco → PASS
- [ ] Kiểu 7 không bị tính vào mẫu số M6-C: draft toàn item Phaco + 2 item Kiểu 7 trung tính → PASS
- [ ] Fixture cũ `SELFTEST_DRAFT_GOOD` / `M5_GOOD` / `M5_CONTEXT` vẫn PASS sau khi thêm marker
- [ ] `SELFTEST_BUCKETS` (19 case) không đổi kết quả — bằng chứng `detect_bucket()` không bị đụng
- [ ] Draft mẫu câu hỏi Phaco: reply nói Phaco, `--check` PASS
- [ ] Draft mẫu câu hỏi Phaco nhưng reply nói SMILE: `--check` FAIL đúng mã M6-B
- [ ] Draft mẫu câu hỏi cắt kính: `--check` PASS, không có claim free (T1)
- [ ] M6-E chạy trên `services.md` thật: PASS
- [ ] Reviewer APPROVE
