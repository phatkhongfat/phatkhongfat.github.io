---
title: Tổng quan về an toàn thông tin
date: 2026-04-19T18:58:58-04:00
showTableOfContents: true
category: Research
difficulty: Easy
feature: feature.jpeg
draft: false
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
- **Xác thực đa yếu tố (MFA - Multiple-Factor Authentication):** Hệ thống yêu cầu từ 2 yếu tố trở lên. Về mặt kỹ thuật, 2FA là một tập con của MFA. Tuy nhiên, trong môi trường doanh nghiệp hiện đại, MFA thường bao hàm một khái niệm thông minh hơn: Adaptive MFA (MFA thích ứng).
	- Bản chất bảo mật: Thay vì lúc nào cũng bắt người dùng nhập 3, 4 bước (gây ức chế), hệ thống sẽ đánh giá Rủi ro (Risk-based) dựa trên Vị trí và Hành vi.
    - Cách hoạt động: 
		- Bạn đăng nhập ở công ty (IP quen thuộc, máy tính cty cấp): *Hệ thống chỉ đòi 1FA (Mật khẩu).
		- Bạn đăng nhập ở quán cà phê (IP lạ): *Hệ thống đòi 2FA (Mật khẩu + OTP).
        - Hệ thống phát hiện tài khoản của bạn đăng nhập từ một quốc gia khác vào lúc 3 giờ sáng: *Hệ thống kích hoạt MFA, đòi hỏi (Mật khẩu + OTP + Xác thực khuôn mặt/FaceID).*
#### Phân loại theo cơ chế lưu trữ trạng thái (Statefulness)
Tiêu chí đánh giá dựa trên cơ chế duy trì và quản lý phiên làm việc của máy chủ sau bước xác thực ban đầu, ảnh hưởng trực tiếp đến khả năng mở rộng và hiệu năng của hệ thống
- **Xác thực có trạng thái (Stateful Authentication):** Máy chủ chịu trách nhiệm toàn quyền lưu trữ và quản lý trạng thái phiên. Sau khi xác thực, một `Session ID` định danh được tạo ra và lưu tại bộ nhớ máy chủ (RAM, Database hoặc Cache server), đồng thời gửi về phía Client (thường qua `Set-Cookie`).
	- **Điểm mạnh:** Cung cấp khả năng kiểm soát tuyệt đối. Quản trị viên có thể thu hồi (revoke) quyền truy cập hoặc buộc đăng xuất (force logout) một phiên làm việc ngay lập tức bằng cách xóa bản ghi trên máy chủ.
	- **Rủi ro:** Đây là mục tiêu điển hình của các cuộc tấn công CSRF (Cross-Site Request Forgery) do trình duyệt mặc định đính kèm Cookie trong các truy vấn.
- **Xác thực phi trạng thái (Stateless Authentication):** Máy chủ không lưu trữ bất kỳ thông tin nào về phiên làm việc. Trạng thái xác thực được đóng gói kèm theo chữ ký điện tử (Signature) vào một Token (tiêu biểu là **JSON Web Token - JWT**). Client lưu trữ Token này và đính kèm vào Header của mỗi truy vấn API tiếp theo.
	- **Điểm mạnh:** Giảm thiểu hoàn toàn rủi ro CSRF nếu Token được truyền qua HTTP Header (`Authorization: Bearer <token>`).
	- **Rủi ro:** Bề mặt tấn công dịch chuyển sang phía Client. Nếu Token được lưu tại Local Storage, hệ thống đối mặt với nguy cơ XSS (Cross-Site Scripting) cao. Nhược điểm chí mạng là khó khăn trong việc thu hồi Token trước khi hết hạn (Expiration), đòi hỏi phải xây dựng thêm cơ chế Deny List/Blacklist, vô hình trung làm mất đi tính "phi trạng thái" ban đầu.
#### Phân loại theo nguồn quản lý định danh (Identity Management)
Tiêu chí này đánh giá ranh giới trách nhiệm trong việc lưu trữ dữ liệu xác thực (Credentials) và quy trình xác minh danh tính.
- **Xác thực cục bộ (Local / Isolated Identity):** Hệ thống đóng vai trò khép kín, tự duy trì cơ sở dữ liệu người dùng (Username/Password) và tự thực hiện logic so khớp xác thực.
    - **Rủi ro:** Trách nhiệm bảo vệ dữ liệu nhạy cảm hoàn toàn thuộc về đội ngũ phát triển nội bộ. Nếu cơ sở dữ liệu bị xâm nhập (Data Breach), hậu quả là cực kỳ nghiêm trọng. Đòi hỏi việc triển khai chuẩn xác các hàm băm kháng GPU (như **Argon2, PBKDF2, bcrypt**) kết hợp với Kỹ thuật thêm muối (Salting) và Pepper.
    - **Khuyến nghị ứng dụng:** Chỉ nên áp dụng cho các hệ thống nội bộ quy mô nhỏ, có độ nhạy cảm thấp hoặc các thiết bị độc lập không có kết nối ra bên ngoài.
- **Định danh liên kết / Xác thực ủy quyền (Federated / Delegated Identity):** Tách biệt hoàn toàn máy chủ cung cấp dịch vụ (Service Provider - SP) và máy chủ cung cấp danh tính (Identity Provider - IdP). Các tiêu chuẩn giao tiếp phổ biến bao gồm **SAML 2.0, OAuth 2.0** và **OpenID Connect (OIDC)**.
    - **Điểm mạnh:** Thu hẹp bề mặt tấn công nội bộ. Rủi ro quản lý mật khẩu được chuyển giao cho các IdP uy tín (Google, Microsoft, Okta), những đơn vị có sẵn cơ sở hạ tầng bảo mật mạnh mẽ và khả năng giám sát dị thường liên tục.    
    - **Rủi ro:** Phát sinh lỗ hổng từ việc cấu hình sai lệch (Misconfiguration) trong luồng giao tiếp giữa SP và IdP. Các rủi ro thường gặp bao gồm rò rỉ mã ủy quyền (Authorization Code Leakage) qua Open Redirect, hoặc thiếu cơ chế xác minh tham số `state` để chống CSRF trong luồng OAuth.
