---
title: "SQL Injection (SQLi)"
date: 2026-04-19T22:54:34-04:00
draft: true
# Layout settings
showTableOfContents: true
# Project metadata
category: "Lab" # Web, Pwn, Crypto, Research
difficulty: "Medium"
tools: ["burp"]
# Featured image (drop feature.jpg in the folder)
feature: "feature.jpg"
---

### SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
#### Description

 This lab contains a SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out a SQL query like the following:
 
```sql
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```



To solve the lab, perform a SQL injection attack that causes the application to display one or more unreleased products.

#### Steps
##### Step 1: Understanding the mechanism
When you click on a category like `Accessories`, the application makes a request to: `filter?category=Accesories`


Behind the scenes, the database executes a query that looks something like this: 
```sql
`SELECT * FROM products WHERE category = 'Gifts' AND released = 1`
```
The `released = 1` condition is what hides the unreleased products from regular users, the main goal is to break out (or ignore) this logic so the database ignore the restriction and returns everything
##### Steps 2: Intercept the Request
1. Using Burp Suite Proxy Tab, turn Intercept on
2. In your browser, click on `Accessories` (or any other category) on the labs Homepage
3. Burp Suite will catch the GET request that looks like this![](Pasted%20image%2020260420001356.png)

##### Steps 3: Craft and Inject the Payload
You need to inject a logical statement that is always true, and then comment out the rest of the original query. The classic payload for this is `' OR 1=1--`

- `'` closes the string literal for the category.
- `OR 1=1` is a statement that always evaluates to true.
- `--` is the SQL comment indicator, which tells the database to ignore the rest of the query (specifically the `AND released = 1` part).

1. In Burp Suite, right-click the intercepted request and select **"Send to Repeater"** (`Ctrl+R`). This allows you to test the payload safely.
2. Go to the **Repeater** tab.
3. Modify the first line of the request to append the payload to the category parameter. You should URL-encode the spaces. Your request should now look like this: `GET /filter?category=Gifts'+OR+1=1-- HTTP/1.1`
#####  Step 4: Execute and Verify
1. In the Repeater tab, click **"Send"**.
2. Look at the Response panel on the right. You should see a `200 OK` status. If you render or search the HTML, you will notice it now contains details for unreleased products that were previously hidden.
3. To officially clear the lab, you must trigger this in the browser. You can either:
    - Go back to the **Proxy** tab, modify the intercepted request exactly as you did in Repeater, and click **"Forward"**.
    - Turn Intercept off, and simply paste the payload directly into your browser's URL bar: `https://YOUR-LAB-ID.web-security-academy.net/filter?category=Gifts'+OR+1=1--`
Once the page loads with the injected payload, the "Congratulations, you solved the lab!" banner will appear. Document this payload in your notes and mark today's system repetition as complete.![](Pasted%20image%2020260420002942.png)