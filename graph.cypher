// Create the graph: (Customer)-[:RAISED]->(Ticket)-[:ABOUT]->(Product)
CREATE (asha:Customer {name: "Asha Rao"}),
       (liam:Customer {name: "Liam Chen"}),
       (priya:Customer {name: "Priya Nair"}),
       (cs:Product {name: "CloudSync"}),
       (ip:Product {name: "InvoicePro"}),
       (t1:Ticket {ticket_id: "T1", issue: "Login fails after password reset", status: "resolved"}),
       (t2:Ticket {ticket_id: "T2", issue: "Sync stuck at 90%", status: "open"}),
       (t3:Ticket {ticket_id: "T3", issue: "PDF export missing line items", status: "resolved"}),
       (t4:Ticket {ticket_id: "T4", issue: "Unknown", status: "open"}),
       (asha)-[:RAISED]->(t1), (liam)-[:RAISED]->(t2),
       (asha)-[:RAISED]->(t3), (priya)-[:RAISED]->(t4),
       (t1)-[:ABOUT]->(cs), (t2)-[:ABOUT]->(cs),
       (t3)-[:ABOUT]->(ip), (t4)-[:ABOUT]->(ip);

// Query: customers who raised tickets about more than one distinct product
MATCH (c:Customer)-[:RAISED]->(:Ticket)-[:ABOUT]->(p:Product)
WITH c, COUNT(DISTINCT p) AS product_count
WHERE product_count > 1
RETURN c.name AS customer, product_count;
