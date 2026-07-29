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
| `5A` | fail | `10/10` ngoài góc được phép, hoặc vượt hạn ngạch | ≤20% item/run, `live` = 0 |
| `5A` | fail / warn | Mode không khai được (`unknown`): có `10/10` → **fail** (không có luật nào xử được); không có `10/10` → warn | khai `**Mode:** <tên>` hoặc `--mode` |
| `5C` | fail | Cấm chung: hết đau · superlative VN/EN · so sánh viện · cam kết · khỏi cận | 0 hit |
| `FOOTER-A` | fail | Có nêu thông tin phí mà **không có footer** | bắt buộc có footer |
| `FOOTER-B` | fail | Footer khai tier không khớp con số/claim trong draft | xem dưới |
| `ANTIREP` | warn / fail | 1 cụm lặp quá nhiều item trong run | warn >15%, **block >30%** |
| `PARSE` | warn | Không parse được item nào → rơi về check toàn văn | — |
| `POLICY` | warn | Còn slot chính sách chưa chốt | hiện tại: không còn |

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

Cặp fixture khoá **sàn M5 là 6+7 cụ thể**, không phải "bất kỳ góc mới nào": `E2` chứng minh thiếu 8/9/10 vẫn pass, còn negative `full run with 8/9/10 but no 6 or 7` chứng minh 3 góc kia không thay thế được cặp chống-toàn-khen.

Fixture negative kiểm cả **code gate nào bắn**, không chỉ "có fail hay không". Fail sai gate = fixture xanh mà gate thật đang hỏng.

## Held-out set

`qa/heldout.tsv` — nhãn gán từ chính sách bệnh viện, **không** đọc từ token list trong script. Nếu nhãn suy ra từ regex thì test chỉ chứng minh regex khớp chính nó.

Đang có 28 ca. Cột `source`: `real` (verbatim từ output cũ) · `collision` (4 ca bắt buộc của brief) · `written` (viết thêm cho bucket mà corpus local không chạm tới).

**Giới hạn đang có:** chỉ 4/217 file output nằm trên máy này, nên 6 slot `real` đang là `written`. Baseline `--baseline` vì vậy chưa reproduce được số của brief (121/167/16/5/5). Khi có corpus đầy đủ thì thay 6 slot đó và chạy lại.
