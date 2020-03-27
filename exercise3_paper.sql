/* Question1 ~
提供每个区域销售额 (total_amt_usd) 最高的销售代表的姓名。*/
SELECT t2.sales_name, t2.region_name, t2.total_orders
FROM (
SELECT region_name, MAX(total_orders) max_orders
FROM (
SELECT sr.name sales_name, r.name region_name, SUM(o.total_amt_usd) total_orders
FROM region r
JOIN sales_reps sr
ON r.id = sr.region_id
JOIN accounts a
ON sr.id = a.sales_rep_id
JOIN orders o
ON a.id = o.account_id
GROUP BY 1,2
ORDER BY 3 DESC) t1
GROUP BY 1) t3
JOIN (
SELECT sr.name sales_name, r.name region_name, SUM(o.total_amt_usd) total_orders
FROM region r
JOIN sales_reps sr
ON r.id = sr.region_id
JOIN accounts a
ON sr.id = a.sales_rep_id
JOIN orders o
ON a.id = o.account_id
GROUP BY 1,2
ORDER BY 3 DESC) t2
ON t2.region_name = t3.region_name AND t2.total_orders = t3.max_orders

/* Question2 ~
对于具有最高销售额 (total_amt_usd) 的区域，
总共下了多少个订单 （total count orders） ？*/
SELECT r.name region_name, SUM(o.total_amt_usd) total_sales, SUM(o.total) count_orders
FROM region r
JOIN sales_reps sr
ON r.id = sr.region_id
JOIN accounts a
ON sr.id = a.sales_rep_id
JOIN orders o
ON a.id = o.account_id
GROUP BY 1
ORDER BY 2 DESC

/* Question3 ~
对于购买标准纸张数量 (standard_qty) 最多的客户
（在作为客户的整个时期内），有多少客户的购买总数依然更多？*/
SELECT a.name, SUM(o.total) total_orders
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY 1
HAVING SUM(o.total) > (SELECT total_orders
FROM (SELECT a.name, SUM(o.standard_qty) total_std, SUM(o.total) total_orders
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1) sub)
ORDER BY 2

/*Question4 ~
对于（在作为客户的整个时期内）总消费 (total_amt_usd) 最多的客户，
他们在每个渠道上有多少 web_events？*/
SELECT a.name, w.channel, COUNT(*) count_channel
FROM web_events w
JOIN accounts a
ON w.account_id = a.id AND a.name =
(SELECT name FROM(SELECT a.name, SUM(o.total_amt_usd) total_spent
FROM web_events w
JOIN accounts a
ON w.account_id = a.id
JOIN orders o
ON a.id = o.account_id
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1) t1)
GROUP BY 1,2
ORDER BY 3 DESC

/*Question5 ~
对于总消费前十名的客户，
他们的平均终身消费 (total_amt_usd) 是多少?*/
SELECT AVG(total_spent) avg_amt
FROM (
SELECT a.name, SUM(o.total_amt_usd) total_spent
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10) t1

/*Question6 ~
比客户的平均每订单消费高的企业，
它们的平均终身消费 (total_amt_usd) 是多少？*/
SELECT AVG(avg_amt)
FROM (
SELECT a.id, AVG(o.total_amt_usd) avg_amt
FROM orders o
JOIN accounts a
ON a.id = o.account_id
GROUP BY 1
HAVING AVG(o.total_amt_usd) >
(SELECT AVG(o.total_amt_usd) avg_all
FROM orders o))t1
