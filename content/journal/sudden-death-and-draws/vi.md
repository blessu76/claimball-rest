---
title: Ván hòa kết thúc thế nào trong Claimball
description: Trước đây ván hòa kết thúc bằng một kết quả gây khó hiểu. Đây là cách đột tử hoạt động hiện nay, và những gì đã thay đổi trong các bản dựng thử nghiệm mới nhất.
summary: Trong Claimball, ván hòa sẽ chuyển sang đột tử và điểm tiếp theo quyết định ván. Người ghi điểm quyết định lấy một ô của đối thủ nếu cần, nên bảng hiện 30–28 thay vì 29–29 và màn hình kết quả luôn khớp với số cuối cùng.
slug: sudden-death-and-draws
lang: vi
category: devlog
translation_of: en
published: 2026-11-03T21:05+09:00
keywords: Claimball, đột tử, hòa, trò chơi giải trí, nhật ký
copy_review: iris 2026-11-14
---
Một ván Claimball kéo dài 90 giây trên lưới ô vở, và phần lớn thời gian một bên đơn giản là giữ nhiều lãnh thổ hơn khi đồng hồ dừng. Bài viết này nói về trường hợp còn lại: ván đấu kết thúc với tỉ số ngang nhau.

## Chuyện gì xảy ra khi hòa

Khi hết giờ mà số ô bằng nhau, ván đấu chuyển sang đột tử. Đồng hồ dừng lại và điểm kế tiếp quyết định ván đấu. Nếu đến giây thứ 90 bóng vẫn còn trên không, ván đấu chờ bóng rơi xuống rồi mới tính.

## Lỗi chúng tôi đã sửa

Trong các bản dựng thử nghiệm, một trận đột tử có thể kết thúc với số ô vẫn ngang nhau, ví dụ 29–29, trong khi màn hình kết quả báo bạn thua. Người thắng được xác định đúng, nhưng con số trên màn hình không thể hiện điều đó, nên cảm giác rất sai.

Đầu tiên chúng tôi cho kết quả như vậy hiển thị là hòa. Sau đó chúng tôi quyết định đột tử không bao giờ được trông như hòa: người ghi điểm quyết định giờ sẽ lấy một ô từ đối thủ nếu cần, để bàn chơi hiển thị 30–28 thay vì 29–29. Màn hình kết quả luôn khớp với con số cuối cùng.

## Cũng có trong các bản dựng thử nghiệm mới nhất

Logo và con số Combo tối đa giờ giữ đúng thứ tự trong các ngôn ngữ viết từ phải sang trái như tiếng Ả Rập, và trang Ghi chú phát hành của trang web liệt kê những gì đã thay đổi trong từng bản dựng.

## Tiếp theo là gì

Claimball vẫn đang thử nghiệm và sắp ra mắt trên iOS và Android. Hiện chưa có ngày phát hành.

## Câu hỏi thường gặp

### Điều gì xảy ra khi một ván Claimball kết thúc hòa?
Khi hết giờ mà số ô bằng nhau, ván chuyển sang đột tử. Đồng hồ dừng lại và điểm tiếp theo quyết định ván.

### Nếu bóng vẫn còn trên không ở giây thứ 90 thì sao?
Ván chờ bóng rơi xuống rồi mới tính.

### Đột tử có thể kết thúc mà trông như hòa không?
Không. Giờ đây người ghi điểm quyết định lấy một ô của đối thủ nếu cần, nên bảng hiện 30–28 thay vì 29–29.

### Claimball đã phát hành chưa?
Chưa. Claimball vẫn đang thử nghiệm và sắp ra mắt trên iOS và Android, chưa có ngày phát hành.
