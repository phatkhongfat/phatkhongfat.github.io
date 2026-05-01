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
### Giới thiệu chung
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
	- **Bản chất bảo mật:** Thay vì lúc nào cũng bắt người dùng nhập 3, 4 bước (gây ức chế), hệ thống sẽ đánh giá Rủi ro (Risk-based) dựa trên Vị trí và Hành vi.
    - **Cách hoạt động:** 
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
#### Phân loại theo đối tượng giao tiếp (Entity Context)
Bảo mật hệ thống đòi hỏi các chiến lược khác biệt tùy thuộc vào thực thể chủ động thực hiện quá trình truy cập.
- **Xác thực Giữa Người và Máy (Human-to-Machine - H2M):**
    - **Đặc điểm:** Thao tác xác thực được kích hoạt và thực hiện bởi người dùng vật lý.
    - **Đánh giá rủi ro:** Mục tiêu hàng đầu của các kỹ thuật tấn công phi kỹ thuật (Social Engineering), Phishing, và dò quét thông tin tự động (Credential Stuffing / Brute-force).
- **Xác thực Giữa Máy và Máy (Machine-to-Machine - M2M):**
    - **Đặc điểm:** Giao tiếp tự động giữa các thành phần phần mềm, dịch vụ API hậu trường (Backend services), hệ thống CI/CD hoặc mạng lưới thiết bị IoT mà không có sự can thiệp của con người.
    - **Đánh giá rủi ro:** Việc rò rỉ các khóa tĩnh (Hardcoded secrets / Long-lived API Keys) trong mã nguồn hoặc kho lưu trữ (như GitHub) là hiểm họa lớn nhất.
#### Phân loại theo chiều xác minh (Verification Direction)
Tiêu chí này phản ánh cấp độ tin cậy được thiết lập trong kênh truyền thông mạng, đặc biệt quan trọng trong kiến trúc Không tin cậy (Zero Trust).
- **Xác thực một chiều (One-way Authentication):**
    - **Đặc điểm:** Yêu cầu phía Client (thực thể yêu cầu truy cập) phải cung cấp bằng chứng danh tính cho Server. Chiều ngược lại (Server chứng minh với Client) thường chỉ dừng ở mức độ xác minh chứng chỉ SSL/TLS chung của tên miền.
    - **Đánh giá rủi ro:** Vẫn tồn tại rủi ro tấn công **Man-in-the-Middle (MitM)** nếu chứng chỉ Public Key Infrastructure (PKI) bị lợi dụng hoặc thiết bị Client bị lây nhiễm các chứng chỉ gốc (Root CA) giả mạo.
- **Xác thực hai chiều (Mutual Authentication / mTLS):**
    - **Đặc điểm:** Cả Client và Server đều bắt buộc phải trình diễn và xác minh Chứng chỉ số (Digital Certificates) của nhau thông qua cơ chế mật mã bất đối xứng (Asymmetric Cryptography) ngay tại tầng giao vận (Transport Layer) trước khi kênh trao đổi dữ liệu (Application Layer) được thiết lập.
    - **Đánh giá an toàn thông tin:** Khởi tạo một đường ống bảo mật (Secure Tunnel) cực kỳ vững chắc. Ngăn chặn tuyệt đối các kỹ thuật MitM, nghe lén (Sniffing), và giả mạo (Spoofing).

## Kiểm soát truy cập (Access Control - AuthZ)
### Giới thiệu chung
Nếu Xác thực (Authentication - AuthN) là hệ thống cửa từ để xác định "Bạn là ai?", thì K**iểm soát truy cập (Authorization/Access Control - AuthZ)** là hệ thống khóa từ bên trong các phòng ban để trả lời câu hỏi: **"Bạn được phép làm gì đối với tài nguyên này?"**.
Việc triển khai sai lệch Access Control là nguyên nhân cốt lõi dẫn đến các lỗ hổng nghiêm trọng như **IDOR** (Insecure Direct Object Reference) hay **Privilege Escalation** (Leo thang đặc quyền) trong bảo mật ứng dụng Web.
Dưới đây là phân tích kỹ thuật về 4 mô hình kiểm soát truy cập nền tảng.
### Các mô hình kiểm soát truy cập
#### **Kiểm soát truy cập tùy ý (DAC - Discretionary Access Control)**
Đây là mô hình phi tập trung, trong đó **chủ sở hữu (Owner) của tài nguyên có toàn quyền quyết định** ai được phép truy cập vào tài nguyên đó.
![](Pasted%20image%2020260429053634.png)
- **Cơ chế hoạt động:** Quyền truy cập thường được lưu trữ dưới dạng Access Control Lists (ACLs). Ví dụ điển hình nhất là hệ thống phân quyền file trên hệ điều hành (như chmod trên Linux) hoặc tính năng Share folder trên Google Drive.
- **Kiến trúc:** Ở cấp độ lập trình hướng đối tượng (ví dụ với Java), tư duy quản lý truy cập theo kiểu DAC thể hiện qua việc thiết lập chuẩn xác các access modifier. Việc thiết kế hệ thống an toàn đòi hỏi ưu tiên sử dụng `private` thay vì `protected` hoặc `public` cho các trạng thái nội tại của class. Cách tiếp cận này đảm bảo đóng gói (encapsulation) nghiêm ngặt, buộc mọi sự tương tác phải đi qua các luồng (methods) đã được kiểm duyệt, ngăn chặn truy cập trái phép trực tiếp vào vùng nhớ.
- **Rủi ro bảo mật:** Rất khó để quản lý ở quy mô lớn. Một người dùng bất cẩn có thể chia sẻ (share) dữ liệu nhạy cảm ra toàn mạng lưới (Public) mà hệ thống quản trị trung tâm khó phát hiện kịp thời. Không chống lại được mã độc: Nếu máy tính nhiễm Malware, Malware đó sẽ chạy với toàn bộ đặc quyền DAC của người dùng hiện tại.
#### **Kiểm soát truy cập bắt buộc (MAC - Mandatory Access Control)**
Trái ngược với DAC, MAC là mô hình quản lý tập trung và cực kỳ khắt khe, nơi **chính sách truy cập do Hệ thống/Quản trị viên cấu hình và áp đặt**. Chủ sở hữu tài nguyên không thể tự ý thay đổi.
- **Cơ chế hoạt động:** Dựa trên việc dán nhãn (Labeling). Mỗi tài nguyên (Files, Databases) được gắn nhãn độ mật (Confidential, Secret, Top Secret) và mỗi người dùng/tiến trình được cấp một mức độ tiếp cận tương ứng (Clearance). Hệ thống sẽ đối chiếu hai nhãn này trước khi cấp quyền (áp dụng các mô hình toán học như Bell-LaPadula để bảo mật luồng thông tin).
- **Ứng dụng thực tế:** Thường được cấu hình sâu ở tầng hệ điều hành (SELinux, AppArmor) hoặc trong các môi trường quân sự, chính phủ.
- **Rủi ro/Hạn chế:** Cực kỳ phức tạp trong việc thiết lập và duy trì. Triển khai MAC sai cách có thể làm tê liệt luồng hoạt động bình thường của ứng dụng.

#### **Kiểm soát truy cập dựa trên vai trò (RBAC - Role-Based Access Control)**
Đây là tiêu chuẩn công nghiệp (De facto standard) được sử dụng trong khoảng 90% các hệ thống phần mềm doanh nghiệp và ứng dụng Web hiện nay.
- **Cơ chế hoạt động:** Quyền hạn không được gán trực tiếp cho User, mà được gán cho các **Roles (Vai trò)**. Sau đó, User được cấp một hoặc nhiều Role.
    - _Luồng:_ User → Role → Permission.
- **Ưu điểm:** Tối ưu hóa việc vận hành (Operational Efficiency). Khi nhân sự thay đổi phòng ban, quản trị viên chỉ cần thu hồi Role cũ và cấp Role mới, hệ thống tự động kế thừa hàng trăm quyền tương ứng mà không cần chỉnh sửa ACL thủ công.
- **Rủi ro bảo mật (Role Explosion):** Khi hệ thống phát triển, số lượng các "ngoại lệ" tăng lên, dẫn đến việc phải tạo ra vô số Role mới (ví dụ: tạo riêng Role `Admin_Read_Only_Weekend`). Điều này phá vỡ cấu trúc RBAC, gây khó khăn cho việc Audit (kiểm toán bảo mật) và dễ dẫn đến lỗ hổng cấp sai quyền.