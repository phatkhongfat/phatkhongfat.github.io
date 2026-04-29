
### Newly Introduced Vulnerabilities

#### VULN-001: Reflected Cross-Site Scripting (XSS) in Application Submission
- **Vulnerability:** Reflected Cross-Site Scripting (XSS)
- **Vulnerability Type:** Security
- **Severity:** High
- **Source Location:** `/home/kali/Exploit/apply-online/rest/class-applyonline-rest-functions.php` (Line 84)
- **Line Content:** `if( !in_array($file_ext, $allowed_types) ) $errors->add('file_type', sprintf(esc_html__( 'Invalid file %1$s. Allowed file types are: %2$s', 'apply-online' ), $val['name'], implode (',', $allowed_types)));`
- **Description:** The plugin's REST API returns error messages that include the unsanitized filename of an uploaded file. If a file with a malicious name is uploaded and triggers an error, the malicious payload is returned and rendered via `innerHTML` in `public/js/applyonline-public.js`.
- **Recommendation:** Use `textContent` instead of `innerHTML` to render messages in `public/js/applyonline-public.js`.

#### VULN-002: Insecure Deserialization in Extension Update Mechanism
- **Vulnerability:** Insecure Deserialization
- **Vulnerability Type:** Security
- **Severity:** High
- **Source Location:** `/home/kali/Exploit/apply-online/class-addons-update.php` (Line 153)
- **Line Content:** `return @unserialize( $request['body'] );`
- **Description:** The `AOL_BootStrap` class performs an `unserialize()` operation on the body of a remote response. This can lead to Remote Code Execution (RCE) via PHP Object Injection if the remote server is compromised.
- **Recommendation:** Use `json_decode()` instead of `unserialize()` for handling remote data.

#### VULN-003: Stored Cross-Site Scripting (XSS) in Ad Features
- **Vulnerability:** Stored Cross-Site Scripting (XSS)
- **Vulnerability Type:** Security
- **Severity:** Medium
- **Source Location:** `/home/kali/Exploit/apply-online/public/class-applyonline-public.php` (Line 330)
- **Line Content:** `$metas.= $row_start.$val['label'].$separator.$val['value'].$row_close;`
- **Description:** Ad features are stored and rendered without proper escaping, allowing an admin or manager to inject malicious scripts.
- **Recommendation:** Use `esc_html()` when outputting feature labels and values.

#### VULN-004: Broken Security Logic (No-op Sanitization)
- **Vulnerability:** Broken Security Logic
- **Vulnerability Type:** Security
- **Severity:** Low
- **Source Location:** `/home/kali/Exploit/apply-online/includes/applyonline-functions.php` (Line 880)
- **Line Content:** `preg_replace('[^a-z0-9\s]/i', "", $str);`
- **Description:** The function `aol_sanitize_text_field` fails to assign the result of `preg_replace` or return a value, making it a no-op.
- **Recommendation:** Fix the function logic to assign and return the result.
