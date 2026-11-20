---
title: Vòng lặp trận đấu chuyển sang động cơ game
description: Hoạt ảnh bảng đấu giờ chạy trên động cơ game, và trận đấu tạm dừng khi bạn rời khỏi ứng dụng.
summary: Chúng tôi đã chuyển vòng lặp hoạt ảnh của bảng đấu chính sang động cơ game Flame, để việc tính thời gian nằm ở một chỗ duy nhất. Trò chơi vẫn chạy như trước. Nếu bạn rời khỏi ứng dụng khi đang đấu, trận đấu sẽ tạm dừng và chờ bạn bấm Tiếp tục. Trò chơi vẫn đang thử nghiệm và sắp có trên iOS và Android.
slug: match-loop-and-pause
lang: vi
category: devlog
translation_of: en
keywords: Claimball, động cơ game, tạm dừng, trận đấu, nhật ký
copy_review: iris 2026-11-20
---
Người chơi không thấy luật mới ở đây. Đây là thay đổi bên trong giúp bảng đấu chạy ổn định.

## Một vòng lặp cho bảng đấu

Hoạt ảnh bảng đấu trước đây chạy bằng bộ đếm thời gian riêng. Bây giờ nó chạy trên động cơ game Flame, động cơ này điều khiển các khung hình của bảng từ một chỗ.

## Rời ứng dụng, quay lại thì đang tạm dừng

Nếu có cuộc gọi đến, thông báo hiện lên, hoặc bạn chuyển sang ứng dụng khác, trận đấu sẽ tạm dừng. Khi quay lại, bấm Tiếp tục để chơi tiếp. Trong lúc bạn đi vắng, không có gì di chuyển.

## Vẫn là trò chơi đó

Điểm số, luật chơi, dữ liệu lưu và mua hàng không thay đổi. Bảng đấu trông và chơi giống như trước.

## Vẫn đang thử nghiệm

Chúng tôi vẫn đang kiểm tra vòng lặp mới trên điện thoại thật.

## Bước tiếp theo

Claimball vẫn đang thử nghiệm và sắp có trên iOS và Android. Chưa có ngày phát hành.

## Câu hỏi thường gặp

### Luật chơi có thay đổi không?
Không. Điểm số, luật chơi, dữ liệu lưu và mua hàng vẫn giữ nguyên. Chỉ có cách chạy hoạt ảnh bảng đấu được chuyển đi.

### Nếu tôi rời đi giữa trận thì sao?
Trận đấu sẽ tạm dừng. Hãy bấm Tiếp tục khi bạn quay lại.

### Claimball đã phát hành chưa?
Chưa. Trò chơi vẫn đang thử nghiệm và sắp có trên iOS và Android, nhưng chưa có ngày phát hành.
