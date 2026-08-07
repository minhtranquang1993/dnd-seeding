# QA gates — `scripts/qa_seeding.py`

Mọi con số ngưỡng dưới đây đọc từ script, không phải chép tay. Sửa ngưỡng thì sửa script trước rồi cập nhật bảng này; `--docsync` gác riêng bảng bucket ở SKILL.md §6.

## Cách chạy

| Lệnh | Dùng khi |
|---|---|
| `python scripts/qa_seeding.py --selftest` | sau mọi lần sửa script hoặc sửa POLICY |
| `cat draft.md \| python scripts/qa_seeding.py --check` | **trước khi ghi scratch** — đây là đường chính |
| `python scripts/qa_seeding.py --check draft.md` | check file đã ghi |
| `python scripts/qa_seeding.py --docsync SKILL.md` | sau khi sửa bảng bucket hoặc POLICY |
| `python scripts/qa_seeding.py --heldout qa/heldout.tsv` | sau khi sửa token/bucket logic |
| `python scripts/qa_seeding.py --baseline <dir>` | đo lại corpus (cần corpus đầy đủ) |
| `--mode <mode>` | ép mode thay vì tự detect |
| `--fees <path>` | trỏ tay tới `fees-promos.md`; mặc định script **tự tìm** |
| `--no-auto-fees` | tắt auto-locate (chỉ để test đường degrade) |

Draft phải qua `--check` **trước** khi ghi file. Ghi trước rồi check thì script chỉ thấy lịch sử, không gác được cái đang xuất.

`--check` không kèm FILE thì đọc stdin. Pipe rỗng → **exit 2 kèm `FAIL: empty input`**, không phải PASS: một gate xanh mà chưa soi gì thì tệ hơn là không có gate.

## Các gate

| Code | Loại | Gác gì | Ngưỡng |
|---|---|---|---|
| `M2` | fail | Câu nói khám free mà service không thuộc T0/T-FU | 0 vi phạm |
| `M3` | fail | Claim hết đau (regex mở rộng) | 0 hit |
| `M5` | fail | Góc reply mới: Kiểu 6 phải có điểm dở thật, Kiểu 7 không nhắc brand, 10/10 chỉ ở Kiểu 1 | **Kiểu 6 + 7** bắt buộc khi run ≥10 item; Kiểu 8/9/10 optional → note |
| `M6-A` | fail | Draft `reply-group` thiếu dòng `**Câu hỏi gốc:**` | **mọi độ dài**, không riêng full run |
| `M6-B` | fail | Item trôi khỏi service câu hỏi: mang token service khác, **hoặc** giọng khúc xạ (`KX_CONTEXT`), mà không nhắc service đang hỏi | 0 item; xét **theo từng câu**; service `kx`/`none` không kích hoạt |
| `M6-C` | fail | Tỉ lệ item **thực chất** chạm service câu hỏi quá thấp (trả lời chung chung / lạc đề) | **≥60%**, mẫu số **loại Kiểu 7**; chỉ áp run ≥10 item |
| `M6-D` | fail | Nhắc BHYT kèm số hoặc % | 0 item — "có BHYT" thì được, số thì hotline. **Chạy cho mọi service**, kể cả `kx`/`none`: đây là luật phí mang số hiệu M6, không phải luật chủ đề |
| `M6-E` | fail (`--selftest`) | `services.md` chứa token tiền | 0 hit |
| `5A` | fail | `10/10` ngoài góc được phép, hoặc vượt hạn ngạch | ≤20% item/run, `live` = 0 |
| `5A` | fail / warn | Mode không khai được (`unknown`): có `10/10` → **fail** (không có luật nào xử được); không có `10/10` → warn | khai `**Mode:** <tên>` hoặc `--mode` |
| `5C` | fail | Cấm chung: hết đau · superlative VN/EN · so sánh viện · cam kết · khỏi cận | 0 hit |
| `FOOTER-A` | fail | Có nêu thông tin phí mà **không có footer** | bắt buộc có footer |
| `FOOTER-B` | fail | Footer khai tier không khớp con số/claim trong draft | xem dưới |
| `ANTIREP` | warn / fail | 1 cụm lặp quá nhiều item trong run | warn >15%, **block >30%** |
| `PARSE` | warn | Không parse được item nào → rơi về check toàn văn | — |
| `POLICY` | warn | Còn slot chính sách chưa chốt | hiện tại: không còn |

## M6 — topic fit (`reply-group` bám câu hỏi gốc)

Gác đúng một lỗi: **hỏi service A, trả lời service B.** Dựng vì MODE 2 không có bước phân loại,
10 kiểu reply đều viết bằng ngôn ngữ mổ cận, và example bank cũ chỉ có 1 câu hỏi gốc (SMILE Pro).

**`detect_topic()` TÁCH KHỎI `detect_bucket()`, có chủ đích.**

| | `detect_bucket()` | `detect_topic()` |
|---|---|---|
| Trả lời câu hỏi | "cái này **giá** bao nhiêu?" | "cái này **về** cái gì?" |
| Võng mạc / glaucoma / lác / mộng / thẩm mỹ / tổng quát | gộp `khac` (**đúng** — cùng T2) | 6 nhãn **riêng** (đúng — nội dung khác nhau) |
| `lão thị` + `phaco` | `lt_phaco` → hotline | `lao_thi` (nói Presbyond / IOL đa tiêu) |
| Hậu phẫu | `fu_dnd` / `fu_other` | `(phase='fu', service=<vẫn giữ>)` |

Hai hàm **không gọi nhau**, fee ladder **không bị sửa** (bằng chứng: `--heldout` 28/28 và
`SELFTEST_BUCKETS` không đổi). Cùng giá không có nghĩa cùng nội dung — dùng bucket phí để gác
chủ đề thì reply về cườm nước sẽ thoả câu hỏi về lác.

**`phase` không thay `service`.** "mẹ mới mổ phaco tái khám sao" là `(fu, phaco)`. Nếu `fu` là
nhãn đứng riêng và được miễn M6-B thì reply trôi sang hậu phẫu *mổ cận* vẫn pass — mà hậu phẫu
Phaco khác thật (thẻ Family 2 vs 3 năm, nhịn ăn xét nghiệm, thẻ BHYT). Chỉ `service == none`
(hậu phẫu trơn) mới bỏ qua M6-B.

**`KX_CONTEXT` — bắt trôi không cần token.** Drift thật ít khi nói "SMILE"; nó nói *giọng* mổ
cận. List chỉ chứa cụm **đặc hiệu khúc xạ**: bản đồ/độ dày/vạt giác mạc · sau laser · ngưng
lens · thoát kính · 12 bước.

Cụm **cố ý loại** khỏi list, vì service khác cũng nói hợp lệ:

| Cụm bị loại | Lý do |
|---|---|
| `nhỏ thuốc giãn` | Phaco, võng mạc/đáy mắt, khám liệt điều tiết cho bé đều nhỏ giãn (nguồn: `LỊCHPHACO`, `qt-ksct`) |
| `chở về` + `mắt nhoè` | hệ quả của nhỏ giãn → thừa hưởng đúng vấn đề trên |
| `khám chuyên sâu` | Phaco, Ortho-K, lão thị dùng đúng chữ này |
| `nhãn áp` | glaucoma dùng nhiều hơn khúc xạ |
| `ngưng lens` / `ngưng kính áp tròng` | **`services.md` bảo phải làm vậy** cho `kinh` (trước đo độ) và `ksct` (Ortho-K trước khám). Gác nó là để gate cãi nhau với chính file tham chiếu |

Gate hẹp mà đúng đáng tin hơn gate rộng mà báo nhầm: false-positive ở đây sẽ dạy người viết
nhồi tên service vào mọi câu.

**Escape hatch — phân biệt theo NGHĨA của từ nối, không theo vị trí.** Item nhắc **cả hai**
service chỉ hợp lệ khi:

- có **cụm so sánh rõ ràng** ở bất kỳ đâu: `khác với`, `so với`, `so sánh`, `trong khi`,
  `k giống`, `thì khác`, hoặc `2 ca ... khác nhau`; **hoặc**
- có **từ nối tương phản** nằm **giữa hai lần nhắc service**: `chứ (k) phải`, hoặc `còn` +
  **chủ thể**, và phần nối phải chạy **thẳng vào** lần nhắc thứ hai — không vượt dấu phẩy,
  **không có động từ vị ngữ** chen giữa.

`cũng` **không phải** dấu hiệu so sánh. Nó nghĩa là "also", **bám ngược** vào thứ vừa nhắc, nên
tự nó không nối được hai vế: "phaco **cũng** cần bs khám kỹ" là nói *về phaco*, còn phần lạc đề
đến ở clause riêng — đúng hình dạng bypass.

`còn` cần **hai** điều kiện:
1. theo sau là **chủ thể** (`e`, `chị gái em`, `mẹ`…). `còn` + động từ là trạng từ "vẫn", bám
   ngược y như `cũng`: "phaco **còn cần** bs khám kỹ…" là bypass.
2. từ chủ thể tới service thứ hai chỉ được chứa **từ nối tiếp danh ngữ** — xưng hô (`gái`, `ấy`,
   `nó`), thời gian (`năm ngoái`, `hôm trước`), thể (`đã`, `mới`, `vừa`, `rồi`), và `đi`
   (trong "đi mổ cận"). Tối đa 6 từ.

**Đây là allowlist, không phải blacklist — cố ý.** Blacklist (cấm `thấy`, `nghĩ`, `cần`…) **fail
open**: mỗi động từ quên liệt kê là một lỗ. Reviewer đã tìm ra `khám`, và còn `đo`, `tư vấn`,
`kiểm tra`… — tiếng Việt nhiều vị ngữ hơn số ai đó chịu khó kể. Allowlist **fail closed**: từ lạ
nghĩa là "không phải so sánh" → M6-B bắn → người viết sửa lại câu. Với một gate mà việc duy nhất
là bắt lạc đề, fail closed là hướng an toàn.

**Độ dài không tách được hai hình** — đuôi hợp lệ "gái em năm ngoái " = 17 ký tự, đuôi bypass
" thấy cần khám kỹ " = 18. Nên luật xét **nội dung** đuôi, không xét độ dài.

`chứ` phải là dạng **`chứ (k) phải`**. `chứ` trơn là tiểu từ diễn ngôn, không nối 2 service.
Sau `chứ k phải` là danh ngữ mô tả service kia ("chứ k phải chỉnh giác mạc như mổ cận") nên
không áp allowlist chủ thể — chỉ cần không vượt dấu phẩy.

**Drift là THEO CẶP SERVICE, không phải "mọi nhãn khác đều là drift".** Bug gốc là reply trôi
sang **mổ cận**, nên `SERVICE_DRIFT_TARGETS` chỉ liệt kê hướng trôi thật sự rủi ro:

| Câu hỏi | Bị gác khi trôi sang |
|---|---|
| `phaco` · `lao_thi` · `ksct` · `kinh` · `tong_quat` | `kx` |
| `glaucoma` · `vong_mac` · `lac` · `mong` · `tham_my` | `kx`, `phaco` |

Nhãn **hàng xóm** nhắc **cùng với** service đang hỏi thì **không phải drift** — đó là nội dung
đúng. Ba câu dưới đây từng bị fail oan khi luật còn là "mọi nhãn khác":

- "mẹ e mổ phaco xong **vẫn phải đeo kính lão** để đọc sách" → IOL đơn tiêu thì đúng là vậy
- "mổ phaco xong 1 tháng bs mới cho **đo độ cắt kính** đọc lại" → mốc khám khúc xạ hậu phẫu thật
- "mẹ e vừa mổ phaco, bs dặn đi **khám tổng quát** định kỳ" → dặn dò thật

Gate bắn vào đúng câu trả lời đúng thì người viết sẽ cắt bớt dữ kiện lâm sàng thật — hại hơn là lợi.
Câu nhắc hàng xóm mà **không** nhắc service đang hỏi thì vẫn bị bắt: đó mới là lạc đề thật.

**Sau khi hatch khớp, phần đuôi vẫn bị soi.** Bất kể khớp bằng đường nào, đoạn sau mention #2
không được mang **drift mới**:

> ❌ "mổ phaco **khác với** mổ cận nha b, e mổ cận SMILE xong thoát kính, 12 bước xong về luôn"

Trước đây chỉ đường closing-marker có luật này, nên 3 đường kia (`khác với`, `chứ k phải`, `còn`)
— vốn là cách mở lời tự nhiên hơn — đi thẳng qua. Đuôi được tính **sau** cụm token của chính
mention #2 ("mổ cận SMILE" là một lần gọi tên, không phải gọi tên rồi tái phát).

**M6-B xét drift THEO TỪNG CÂU trong item, không xét cả item.** Một câu so sánh hợp lệ không
"bảo lãnh" được câu lạc đề bên cạnh:

> ❌ "mổ phaco với mổ cận khác nhau. **e mổ cận SMILE xong thoát kính luôn**" — câu 1 là so sánh
> hợp lệ, nhưng câu 2 là lời kể về mổ cận, vẫn FAIL.

Hatch tồn tại để cho phép **đối chiếu**, không phải để dán một câu so sánh vào đầu rồi lạc đề ở
câu sau.

**Cả ba đường đều fail-closed và đều ANCHOR vào mention #2**, tìm **trong gap** giữa hai lần
nhắc service (không phải toàn item):

| Đường | Điều kiện |
|---|---|
| `khác với` / `so với` / `so sánh` / `trong khi` / `thì khác` | phải nối tới service #2 qua bridge allowlist |
| `2 ca khác nhau` | từ chỉ khác biệt phải **ngay sau** `2 ca` |
| `chứ (k) phải` | nối tới service #2 qua bridge allowlist (≤4 từ) |
| `còn` + chủ thể | nối tới service #2 qua tail allowlist danh ngữ (≤6 từ) |

| Ví dụ | Kết quả | Vì sao |
|---|---|---|
| "mẹ e mổ phaco **còn e mổ cận**" | ✅ pass | chủ thể chạy thẳng vào service #2 |
| "mẹ em mổ phaco **còn chị gái em năm ngoái mổ cận**" | ✅ pass | đuôi toàn từ nối danh ngữ |
| "mẹ mổ phaco **còn em đi mổ cận**" | ✅ pass | `đi mổ` là cách nói bình thường |
| "mổ phaco **khác với** mổ cận nha b" | ✅ pass | marker nối thẳng tới service #2 |
| "…thay thủy tinh thể **chứ k phải** chỉnh giác mạc như mổ cận" | ✅ pass | bridge hợp lệ |
| "phaco **cũng** cần bs khám kỹ, e mổ cận…" | ❌ FAIL | `cũng` bám ngược vào phaco |
| "phaco **còn cần** bs khám kỹ, e mổ cận…" | ❌ FAIL | `còn` + động từ = "vẫn" |
| "phaco **còn e thấy cần khám kỹ** mổ cận…" | ❌ FAIL | chen vị ngữ — không cần dấu phẩy vẫn bị bắt |
| "phaco **còn e khám kỹ** mổ cận…" · "**còn e đo mắt rồi** mổ cận…" | ❌ FAIL | `khám`/`đo` không có trong allowlist |
| "phaco **còn cái này** phải hỏi bs kỹ, e mổ cận…" | ❌ FAIL | `cái`/`bên`/`người` không phải chủ thể đối chiếu |
| "phaco **chứ không phải cứ khám là** mổ cận…" | ❌ FAIL | `cứ`/`khám` không có trong bridge — phủ định *cách khám*, không đối chiếu service |
| "phaco **khác với hôm trước**, e mổ cận…" | ❌ FAIL | so sánh **thời gian**, không phải service |
| "phaco **so với chỗ khác** thì ổn, e mổ cận…" | ❌ FAIL | so sánh **nơi**, không phải service |
| "phaco bên đó có **2 ca mổ khác giờ** buổi sáng, e mổ cận…" | ❌ FAIL | `2 ca … khác giờ` là lịch mổ |
| "phaco có triệu **chứng** mờ dần, e mổ cận…" | ❌ FAIL | `chứ` là substring của `chứng` — phải có ranh giới từ |
| "…đo bản đồ giác mạc kỹ lắm, **còn lại** thì yên tâm" | ❌ FAIL | `còn` không nằm giữa 2 mention |

Vì sao phải chặt: `còn` / `cũng` là mấy từ phổ biến nhất tiếng Việt, và `chứ` nằm trong `chứng`
/ `chứa`. Tìm chúng trên **toàn item** hoặc không có ranh giới từ thì hatch mở gần như luôn, và
bypass "rắc token + thêm từ nối" quay lại nguyên vẹn.

> **Đã thử 4 cách, 3 cách đầu sai** — ghi lại để đừng ai nới lại:
> (a) tìm từ nối trên **toàn item** — mở gần như luôn;
> (b) tách bằng **vị trí** (từ nối phải sát mention #2) — không được, so sánh thật cũng đặt từ
> nối ngay sau mention #1 y hệt bypass;
> (c) **blacklist vị ngữ** — fail **open**, quên `khám` là thủng, mà tiếng Việt còn `đo`,
> `tư vấn`, `kiểm tra`…;
> (d) **allowlist + anchor vào mention #2 + tìm trong gap** — cách đang dùng, fail **closed**.
> Từ lạ = "không phải so sánh" → M6-B bắn → người viết sửa câu. Với gate chuyên bắt lạc đề,
> fail closed là hướng an toàn.
>
> Mẫu chung của cả 3 lần sai: **chỗ nào chấp nhận "văn bản tự do" thì chỗ đó thành bypass.**
> `SELFTEST_COMPARE` giữ 28 ca để nếu ai nới luật thì sập ngay.

## Footer 2 lớp

Đây là cơ chế chặn partial-load: model đọc SKILL.md mà **không** đọc `fees-promos.md` rồi tự bịa phí.

- **Lớp (a):** draft có nêu thông tin phí mà thiếu footer `[fees: <ngày> · <tier>]` → **fail**.
- **Lớp (b):** có footer → script tự đọc `fees-promos.md` và đối chiếu:
  - ngày trong footer phải khớp `updated:` của file
  - tier khai phải tồn tại trong file
  - draft claim free thì tier khai phải được phép free
  - **mọi con số trong câu báo phí phải nằm dưới tier đã khai** — đây là lớp bắt được ca "đã đọc file mà vẫn nói sai", read-receipt không bắt được

Tier hợp lệ trong footer: `T-FU` · `T0` · `T1` · `T2` · `PROMO` (chỉ nêu số ưu đãi mổ) · `hotline`. Nhiều tier thì cách nhau dấu phẩy.

**Script không giữ bản copy nào của số tiền.** Nó parse bảng từ `fees-promos.md` lúc chạy. Nếu file mất, lớp (b) hạ xuống **warn** chứ không im lặng pass.

## Ngoại lệ theo mode

`maps` / `maps_foreigner` / `koc` được miễn **theo từng cột đã đo**, không miễn cả gói:

| Mode | Miễn | KHÔNG miễn |
|---|---|---|
| `maps` | claim hết đau, so sánh viện | `10/10`, superlative |
| `maps_foreigner` | claim hết đau, so sánh viện, `20/20`, superlative EN | `10/10` |
| `koc` | claim hết đau, `10/10` | so sánh viện, superlative |

Luật phí **không** có ngoại lệ mode nào. `maps`/`koc` vẫn chịu M2 + footer đầy đủ.

## Fixture trong `--selftest`

| Block | Kiểm |
|---|---|
| A | bucket detection + M2 trên 19 ca, gồm 4 ca collision bắt buộc |
| B | mỗi họ regex phải bắn trên probe của chính nó |
| B2 | disclaimer không phải vi phạm ("khám phaco **có phí**, k thuộc gói free") |
| B3 | phân biệt *nêu* phí vs *hỏi* phí — chỉ nêu mới cần footer |
| B3b | footer lớp (b) cấp draft, đối chiếu với `fees-promos.md` thật |
| B4 | sàn hạn ngạch `10/10` — instance đầu trong run ngắn phải hợp lệ |
| B5 | ranh giới đính chính — Kiểu 8 được phép nhắc niềm tin sai để sửa nó |
| E2 | run đủ 10 item có sàn 6+7 mà **không** có 8/9/10 → phải PASS (kiểu chọn theo ngữ cảnh) |
| C–F | draft biết-sai phải fail **đúng gate**, draft đúng phải pass |
| G | M6 topic-fit: drift có token · drift bằng `KX_CONTEXT` · **3 ca chống over-fire** (Phaco/võng mạc/khám bé nhắc nhỏ giãn → PASS) · hậu phẫu mang service · escape hatch · M6-A · M6-D · M6-C 2 chiều |
| G2 | `detect_topic()` ladder — 15 ca, gồm `lão thị + phaco` → `lao_thi` (khác bucket `lt_phaco`), `mổ ortho-k` → `ksct` (không phải `kx`), `khám tổng quát xem có cườm` → `phaco` |
| G3 | `services.md` không có token tiền (M6-E) |

Cặp fixture khoá **sàn M5 là 6+7 cụ thể**, không phải "bất kỳ góc mới nào": `E2` chứng minh thiếu 8/9/10 vẫn pass, còn negative `full run with 8/9/10 but no 6 or 7` chứng minh 3 góc kia không thay thế được cặp chống-toàn-khen.

Fixture negative kiểm cả **code gate nào bắn**, không chỉ "có fail hay không". Fail sai gate = fixture xanh mà gate thật đang hỏng.

## Held-out set

`qa/heldout.tsv` — nhãn gán từ chính sách bệnh viện, **không** đọc từ token list trong script. Nếu nhãn suy ra từ regex thì test chỉ chứng minh regex khớp chính nó.

Đang có 28 ca. Cột `source`: `real` (verbatim từ output cũ) · `collision` (4 ca bắt buộc của brief) · `written` (viết thêm cho bucket mà corpus local không chạm tới).

**Giới hạn đang có:** chỉ 4/217 file output nằm trên máy này, nên 6 slot `real` đang là `written`. Baseline `--baseline` vì vậy chưa reproduce được số của brief (121/167/16/5/5). Khi có corpus đầy đủ thì thay 6 slot đó và chạy lại.
