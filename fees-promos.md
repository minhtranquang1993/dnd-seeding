---
name: dnd-seeding-fees-promos
description: Nguồn duy nhất chứa SỐ TIỀN cho skill dnd-seeding — phí khám theo tier và ưu đãi mổ. SKILL.md chỉ giữ pointer (fee-tier-id / promo-key), không giữ số.
updated: 2026-07
---

# Phí khám & ưu đãi — DND Sài Gòn

> **Ngày cập nhật: 2026-07.** Con số trong footer `[fees: 2026-07 · <tier>]` phải khớp ngày này.
>
> **File này là nơi duy nhất trong skill có số tiền.** SKILL.md chỉ chứa `fee-tier-id` và `promo-key` trỏ về đây. Đừng copy số ngược lên SKILL.md — để số ở 2 nơi là tái tạo đúng class bug đang sửa, chỉ dời chỗ.

## 1. Phí khám theo tier

| fee-tier-id | Phí | Sau CT 50% | Áp cho | Được nói free? |
|---|---|---|---|---|
| **T-FU** | **0đ** | — | Tái khám hậu phẫu, **đã mổ tại DND**, trong 3 năm | ✅ |
| **T0** | **0đ** — gói khám chuyên sâu 12 bước, trị giá **1.000.000đ** | — | Khám mổ cận/viễn/loạn, **lão thị** (đường khúc xạ/laser), **Phakic ICL** | ✅ |
| **T1** | 160.000đ | 80.000đ | Khám đo độ - cắt kính | ❌ |
| **T2** | 350.000đ | 175.000đ | Phaco · Ortho-K/kiểm soát cận · võng mạc-dịch kính, glaucoma · thẩm mỹ mắt · khám tổng quát | ❌ |
| **hotline** | không báo số | — | Mổ viện khác đến tái khám · lão thị đi đường Phaco + IOL đa tiêu · ambiguous · không detect được service | ❌ |

**Điều kiện CT 50%:** (check-in/share post **HOẶC** đánh giá 5\* Google Maps) **VÀ** (like fanpage **HOẶC** quan tâm Zalo OA DND).

**Hotline khi không báo số:** 0775.147.147 / 1900 8195.

## 2. Mapping promo-key → tier

`promo-key` là nhóm dịch vụ trong bucket table của SKILL.md. Bảng này là chỗ duy nhất nối nhóm đó với số tiền.

| promo-key | fee-tier-id | Số tiền | Được nói free? |
|---|---|---|---|
| `fu_dnd` | T-FU | 0đ | ✅ |
| `fu_other` | hotline | không báo số | ❌ |
| `kx` | T0 | 0đ (gói 12 bước, trị giá 1.000.000đ) | ✅ |
| `kinh` | T1 | 160.000đ · CT 50% → 80.000đ | ❌ |
| `pc` | T2 | 350.000đ · CT 50% → 175.000đ | ❌ |
| `or` | T2 | 350.000đ · CT 50% → 175.000đ | ❌ |
| `khac` | T2 | 350.000đ · CT 50% → 175.000đ | ❌ |
| `lt_phaco` | hotline | không báo số — **chưa có chính sách** | ❌ |
| `ambiguous` | hotline | không báo số | ❌ |
| `none` | hotline | không báo số | ❌ |

> `lt_phaco` = lão thị đi đường **Phaco + IOL đa tiêu**. Chốt 2026-07: **không báo phí khám, chuyển hotline** — chưa có chính sách giá cho đường này. Lão thị đi đường khúc xạ/laser vẫn là `kx` → T0 free.

## 3. Ưu đãi mổ (SmileDays 2026)

> **Upstream là `dnd-ads/promotions.md`.** Bảng dưới là bản đồng bộ tính đến **2026-07** để skill seeding không phải nêu số mà chưa đọc file nào. Ưu đãi mổ đổi thì sửa upstream trước, rồi đồng bộ xuống đây kèm ngày.

| promo | Số | Ghi chú |
|---|---|---|
| Hỗ trợ chi phí mổ cận | đến **50%++** | giá chỉ từ **13 triệu/2 mắt** |
| Cashback share hành trình | **3.000.000đ** | |
| Thẻ Family | **5.000.000đ** | |
| Khám chuyên sâu 12 bước | **miễn phí**, trị giá **1.000.000đ** | CHỈ cho khám mổ cận/khúc xạ (gồm lão thị đường laser, Phakic ICL) — xem §1 |
| Miễn phí tái khám hậu phẫu | **0đ**, **3 năm** | CHỈ người đã mổ tại DND |
| Check-in nhận quà mùa hè | — | không có số |

## 4. Luật dùng file này

1. **Chưa đọc file này trong run đó → không được nêu bất kỳ thông tin phí nào**, kể cả dạng chữ (`free`, `miễn phí`, `tặng gói khám`, `trị giá 1.000.000đ`, `0đ`). Chưa đọc thì chuyển hotline.
2. Có nêu thông tin phí → **bắt buộc** in footer `[fees: 2026-07 · <fee-tier-id>]` ở cuối file.
3. Footer khai tier nào thì con số/claim trong draft phải khớp tier đó. Script `qa_seeding.py --check` tự đọc file này và đối chiếu — lệch là fail.
4. Sửa số ở đây thì **phải** cập nhật `updated:` ở frontmatter và dòng "Ngày cập nhật" — footer check so ngày với 2 chỗ đó.
