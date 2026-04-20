---
title: "Tổng quan về an toàn thông tin"
date: 2026-04-19T18:58:58-04:00
showTableOfContents: true
category: "Research" 
difficulty: "Easy"
feature: "feature.jpeg"
draft: true
---
Để xây dựng hoặc vận hành một hệ thống an toàn, bạn không thể chỉ dựa vào may mắn. Vấn đề cốt lõi nằm ở việc hiểu rõ các cơ chế bảo vệ và những nguy cơ thực tế. Bài viết này sẽ tập trung phân tích 3 khía cạnh kỹ thuật then chốt trong bảo mật hệ thống:

-  Cơ chế xác thực (Authentication): Các mô hình từ mật khẩu, Token đến xác thực đa yếu tố (MFA).

-  Kiểm soát truy cập (Access Control): Cách triển khai phân quyền dựa trên vai trò (RBAC) hoặc thuộc tính (ABAC).

-  Quản trị rủi ro: Phân biệt rõ ràng giữa Hiểm họa (Threats), Điểm yếu (Vulnerabilities) và cách đánh giá Rủi ro (Risks) trong thực tế. 
## Cơ chế xác thực (AuthN)
**AuthN - là viết tắt của Authentication**, là một quy trình an toàn thông tin nhằm đảm bảo chỉ người dùng được cấp quyền mới có thể truy cập vào thông tin, hệ thống hoặc những tài nguyên khác. Quá trình này yêu cầu thông tin người dùng đưa vào trùng khớp với thông tin được lưu trong hệ thống. 
![](Pasted%20image%2020260420193323.png)
### Một số loại mô hình xác thực
#### Phân loại theo yếu tố
- **Knowledge Factor:**  Dựa trên thông tin bí mật mà chỉ thực thể hợp lệ mới biết. *Ví dụ:*  Mật khẩu (Password), Mã PIN, Câu hỏi bảo mật.
- **Possession Factor:** Yêu cầu người dùng chứng minh họ đang sở hữu một thiết bị vật lý cụ thể. *Ví dụ:* Điện thoại nhận tin nhắn SMS OTP, ứng dụng Authenticator, Google Authenticator), Khóa bảo mật phần cứng (YubiKey), Thẻ từ (Smart card).  
- **Inherence Factor:** Yếu tố sinh trắc học - Các đặc điểm vật lý gắn với cơ thể. *Ví dụ:* FaceID, vân tay
- **Location Factor:** Đặc điểm địa lý hiện tại của bạn. *Ví dụ:* Địa chỉ IP, định vị GPS, mạng Wi-Fi đang kết nối
- **Behavior Factor:** Thói quen, cử chỉ đặc trưng khi thao tác. *Ví dụ:* Tốc độ và lực gõ phím, quỹ đạo di chuyển chuột
#### Phân loại theo số lượng yếu tố
Dựa vào việc kết hợp các yếu tố ở mục trên, ta có thể phân loại như sau:
- **Xác thực đơn yếu tố (SFA - Single Factor Authentication):** Chỉ sử dụng 1 yếu tố duy nhất để đăng nhập. Thường gặp nhất là chỉ sử dụng Username + Password. Mức độ bảo mật tương đối thấp.
- **Xác thực hai yếu tố (2FA - Two-Factor Authentication):** Sử dụng 2 yếu tố thuộc 2 nhóm khác nhau. *Ví dụ:* Mật khẩu + Mã OTP gửi về điện thoại.
- 