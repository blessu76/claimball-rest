---
title: Chúng tôi kiểm tra thế nào để dấu điểm rơi luôn nói đúng sự thật
description: Dấu điểm rơi chỉ hữu ích khi nó đúng. Đây là cách chúng tôi kiểm tra rằng nó hiển thị đúng những ô thực sự được tô.
summary: Dấu điểm rơi của Claimball chỉ có ích khi nó đúng, nên chúng tôi kiểm tra rằng nó khớp với những ô thực sự được tô. Chúng tôi chơi nhiều ván mô phỏng đầy đủ với các hạt giống ngẫu nhiên khác nhau và so sánh từng dấu với kết quả, đồng thời cố ý phá quy tắc để xác nhận bài kiểm tra thất bại. Trò chơi vẫn đang thử nghiệm và sắp ra mắt trên iOS và Android.
slug: marker-keeps-its-word
lang: vi
translation_of: en
category: devlog
keywords: Claimball, dấu điểm rơi, kiểm thử, chơi công bằng, nhật ký
copy_review: iris 2026-11-14
---
Dấu điểm rơi cho biết bóng sẽ rơi ở đâu, nên nó phải đúng mọi lúc. Đây là cách nó được kiểm tra trong các bản dựng thử nghiệm nội bộ TestFlight, chưa được phát hành cho công chúng.

## Một lời hứa trên màn hình

Nếu dấu chỉ một ô mà trò chơi lại tô ô khác, bạn sẽ thôi tin nó, và trò chơi sẽ có cảm giác không công bằng. Vì vậy dấu phải khớp với những gì thực sự xảy ra.

## Một quy tắc cho cả hai

Dấu và cú đánh thực tế phải khớp nhau. Chúng tôi kiểm tra bằng cách chơi các ván mô phỏng đầy đủ, lặp lại nhiều lần với các hạt giống ngẫu nhiên khác nhau, rồi so sánh từng dấu với những ô thực sự được tô. Chúng phải khớp mọi lúc.

## Kiểm tra chính bài kiểm tra

Một bài kiểm tra không bao giờ thất bại thì chẳng chứng minh được gì. Vì vậy chúng tôi cũng cố ý phá quy tắc, chẳng hạn chỉnh một giá trị nhích nhẹ, và đảm bảo bài kiểm tra phát hiện và thất bại.

## Cả đối thủ và quy tắc đặc biệt

Phép so sánh tương tự chạy với từng đối thủ AI và với các biến thể của Thử thách hằng ngày, vì chúng thay đổi tốc độ và hành vi.

## Vẫn thành thật về giới hạn

Những kiểm tra này chạy trên các ván mô phỏng. Chơi trên điện thoại thật là một vòng kiểm thử riêng.

## Tiếp theo là gì

Claimball vẫn đang thử nghiệm và sắp ra mắt trên iOS và Android. Hiện chưa có ngày phát hành.

## Câu hỏi thường gặp

### Vì sao dấu điểm rơi phải chính xác?
Nếu dấu chỉ một ô mà trò chơi lại tô ô khác, bạn sẽ thôi tin nó, và trò chơi sẽ có cảm giác không công bằng.

### Các bạn kiểm tra dấu thế nào?
Chúng tôi chơi các ván mô phỏng đầy đủ nhiều lần với các hạt giống ngẫu nhiên khác nhau và so sánh từng dấu với những ô thực sự được tô. Chúng phải khớp mọi lúc.

### Bài kiểm tra có bao gồm đối thủ và Thử thách hằng ngày không?
Có. Phép so sánh tương tự chạy với từng đối thủ AI và với các biến thể của Thử thách hằng ngày, vì chúng thay đổi tốc độ và hành vi. Những kiểm tra này chạy trên các ván mô phỏng, còn chơi trên điện thoại thật là một vòng kiểm thử riêng.

### Claimball đã phát hành chưa?
Chưa. Trò chơi vẫn đang thử nghiệm và sắp ra mắt trên iOS và Android. Hiện chưa có ngày phát hành.
