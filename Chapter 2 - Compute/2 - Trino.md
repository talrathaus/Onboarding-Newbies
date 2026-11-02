# Introduction to Trino 🐰

## Overview
Today’s session introduces Trino, a distributed SQL query engine designed for high-performance analytics across multiple data sources. Unlike traditional databases, Trino does not store data itself. Instead, it queries data where it already resides, enabling fast interactive analysis across large and diverse datasets.

**The emphasis is on Trino’s architecture, distributed execution model, and how it integrates with modern data platforms.**

## Goals
- Understand what Trino is and where it fits in a modern data architecture.
- Learn how Trino executes distributed queries across workers.
- Explore how Trino connects to multiple data sources and federates queries.
- Improve your ability to research distributed data systems independently.

:warning: **Note:**
- This is a self-study day; independence and time management are crucial.
- If you can’t explain a concept clearly, you probably need to revisit it.
- Ask your mentor if you’re unsure what to research.

### ⏳ Timeline
Estimated Duration: 3 Days

- Day 1: Learn the fundamentals of distributed SQL engines and Trino’s role in the data ecosystem.
- Day 2: Dive deeper into Trino architecture, connectors, and query execution.
- Day 3: Review performance optimization and operational concepts, followed by a Q&A session.

---

## Core Concepts

### Part 1: Distributed SQL Engines (General Concepts)

Answer these questions to understand the broader category of distributed query engines before focusing on Trino specifically.

1. **Role in the Data Architecture:**  
   What is a distributed SQL query engine, and where does it sit in a modern data architecture? How does it differ from storage systems such as data lakes or databases?

מנוע שאילתות (Query Engine) הוא כלי המשמש לגישה למקור נתונים, שתפקידו להריץ ולעבד שאילתות מול אותו מקור נתונים.
המונח SQL מציין שהפעולה מתבצעת באמצעות שפת SQL או שפה דמוית-SQL.
המונח "מבוזר" (Distributed) מעיד על כך שהארכיטקטורה תוכננה לאפשר הרחבה או צמצום (scaling) בהתאם לצורך, מה שמאפשר למערכת להתמודד עם מאגרי נתונים בהיקף נרחב.

זה יהיה ברמה הכי גבוהה, באמת.

הוא שונה בכך שהוא מתמקד אך ורק בביצוע השאילתות – זה כל מה שהוא עושה, בחיי.

2. **Motivation & Use Cases:**  
   Why do organizations use distributed SQL engines? In what scenarios are they preferred (for example: interactive analytics on large datasets, federated queries across multiple systems, or querying data lakes)?

בצעו שאילתות על כמויות עצומות של נתונים ביעילות באמצעות שאילתות מבוזרות – אם אתם עובדים עם טרה-בייטים או פטה-בייטים של נתונים, סביר להניח שאתם משתמשים בכלים המקיימים אינטראקציה עם Hadoop ו-HDFS.
עבדו מול סוגים שונים של מקורות נתונים.
מחסני נתונים (Data Warehousing) ואנליטיקה: ניתוח נתונים, צבירת כמויות גדולות של נתונים והפקת דוחות – OLAP.

3. **Distributed Query Processing:**  
   How do distributed query engines typically execute queries across multiple nodes? Explain concepts such as parallel processing, data shuffling, and shared-nothing architectures.

השאילתה מומרת לייצוג מובנה הנקרא עץ תחביר מופשט (AST), לאחר מכן, כלי אופטימיזציה מנתח את התוכנית הלוגית ומנסה לשפר אותה.
לאחר יצירת התוכנית הלוגית, המנוע ממיר את התוכנית הלוגית הממוטבת לתוכנית פיזית.
לאחר מכן, המשימות בתוכנית יחולקו לכל עובד, והן יעובדו במקביל; לאחר מכן, מתרחש שלב ערבוב, המבטיח שכל השורות של אותו מפתח קבוצה ישולבו.
הנתונים מחולקים מחדש בין עובדים בהתבסס על ה-hash של מפתח הקיבוץ.
התערובת תמיד הכרחית לחישוב התוצאה הסופית.
אם נתוני הביניים הופכים גדולים מדי מכדי להתאים לזיכרון, המנוע עלול לגלוש לדיסק, אשר כותב נתונים מאוחסנים זמניים לפני מיזוגם מאוחר יותר.
השאילתה הסתיימה 😊

ארכיטקטורת shared-nothing היא שכל רכיב או צומת פועלים באופן עצמאי ויש להם משאבים ייעודיים משלהם, כגון מעבדים, זיכרון ואחסון.

---

### Part 2: Trino (Implementation & Operations)

Answer these questions to cover Trino’s major architectural and operational concepts.

1. **Purpose & Position in the Data Stack:**  
   What is Trino, and where does it sit in the data architecture? Explain its role as a distributed MPP SQL engine, how it differs from storage systems, and when it should be used instead of other query engines.

Trino is an open-source, distributed SQL query engine.
It was designed and written from the ground up to efficiently query data against disparate data sources of all sizes, ranging from gigabytes to petabytes.
Trino breaks the false choice between having fast analytics using an expensive commercial solution or using a slow “free” solution that requires excessive hardware.

Trino executes queries in memory across a cluster of workers, returning results quickly without persisting intermediate state.
It has no storage layer of its own and stays intentionally stateless between queries.
Spark, by contrast, builds execution plans as DAGs, which lets it handle iterative computation, shuffle-heavy joins, and multi-step pipelines that would be impractical to express as a single SQL statement.


2. **Architecture & Query Execution:**  
   How is Trino architected, and how does it execute queries in a distributed environment? Discuss the roles of the Coordinator and Workers, stages and tasks, data exchanges, and the execution model.

Trino is a distributed query engine that processes data in parallel across multiple servers.
There are two types of Trino servers: coordinators and workers.
A Trino cluster consists of several Trino nodes - one coordinator and zero or more workers.
Users connect to the coordinator with their SQL query tool.
The coordinator collaborates with the workers.
The coordinator and the workers access the connected data sources.
This access is configured in catalogs.
Processing each query is a stateful operation.
The workload is orchestrated by the coordinator and spread in parallel across all workers in the cluster.
Each node runs Trino in one JVM instance, and processing is parallelized further using threads.
Any Trino server in a specific Trino cluster is considered a node.


The Trino coordinator is the server that is responsible for parsing statements, planning queries, and managing Trino worker nodes.
For development or testing purposes, a single instance of Trino can be configured to perform both roles.
The coordinator keeps track of the activity on each worker and coordinates the execution of a query.
The coordinator creates a logical model of a query involving a series of stages, which is then translated into a series of connected tasks running on a cluster of Trino workers.
Coordinators communicate with workers and clients using a REST API.

A Trino worker is a server in a Trino installation, which is responsible for executing tasks and processing data.

Worker nodes fetch data from connectors and exchange intermediate data with each other.
The coordinator is responsible for fetching results from the workers and returning the final results to the client.
When a Trino worker process starts up, it advertises itself to the discovery server in the coordinator, which makes it available to the Trino coordinator for task execution.
Workers communicate with other workers and Trino coordinators using a REST API.


3. **Connectors & Catalogs:**  
   How does Trino integrate with external systems through connectors and catalogs? Explain what connectors are responsible for, how catalogs are configured, and how Trino can federate queries across multiple data sources.

Catalogs define and name a configuration for connecting to a data source, allowing users to query the connected data.
Each catalog’s configuration specifies a connector to define which data source the catalog connects to.

Connectors translate data from a data source into Trino schemas, tables, columns, rows, and data types.
A connector is specific to a data source and is used in catalog configurations to define which data source the catalog connects to.

The create() method of the connector factory receives a config map, containing all properties from the catalog properties file. It can be used to configure the connector, but because all the values are strings, they might require additional processing if they represent other data types. It also doesn’t validate if all the provided properties are known. This can lead to the connector behaving differently than expected when a connector ignores a property due to the user making a mistake in typing the name of the property.
To make the configuration more robust, define a Configuration class. This class describes all the available properties, their types, and additional validation rules.

Federated queries use data stored in multiple systems and databases. Trino can connect to and query all of them in unison. This approach uses joins to combine the disparate data with a single SQL query. 

4. **Governance & Workload Management:**  
   How does Trino handle governance and workload management? Discuss resource groups, concurrency control, memory limits, access control (RBAC), and multi-tenant isolation.

Resource groups are a powerful concept in Trino used to limit resource utilization on the system. The resource group configuration consists of two main pieces: the resource group properties and the selector rules. A resource group is a named collection of properties that define available cluster resources. You can think of a resource group as a separate section in the cluster that is isolated from other resource groups. The group is defined by CPU and memory limits, concurrency limits, queuing priorities, and priority weights for selecting queued queries to run. 

System access control enforces authorization at the global Trino level and allows you to configure access for catalogs and rules for the principals used. Trino also separates the principal for authentication from the user who is running queries. For example, multiple users may share a principal for authenticating, but run queries as themselves. By default, Trino allows any principal who can authenticate to run queries as anyone else.

5. **Query Optimization & Performance:**  
   How does Trino optimize query performance? Explain cost-based optimization, statistics usage, join strategies, predicate pushdown, partition pruning, spilling, and caching behavior.

6. **High Availability & Multi-Cluster Routing:**  
   How does Trino Gateway enable high availability and workload isolation across multiple Trino clusters? Explain how it provides a single entry point, performs rule-based query routing and load balancing, monitors cluster health, and enables failover and multi-cluster isolation beyond what a single Trino coordinator can support.


איך קוראים לשלב הראשונה שמגיע מהלקוח לcoord
statement

שם של מבנה נתונים שאותה שעברה parse
split/statement, depends on what we was talking about

מה predicate pushdown עושה
Uses the filter sooner, typically resulting from a condition to omit unnecessary rows.

מה predicate pushdown עושה בHive over HDFS with Parquet
Trino will read the Parquet metadata to only use relevant rows.

Trino statistics
For a table:
row count
For each column in a table:
data size
nulls fraction
distinct value count
low/high value

איך הcoord עושה scheduling ומתי
כל stage הוא מחלק לtaskים והוא שולח task ה[split+op] כאשר נוצר Physical plan.
הcoord יודע מה כל worker עושה באמצעות heartbeat.

Physical plan vs logical plan
Post-optimization vs Pre-optimization.

FINISHING
Query will be FINISHED only when the client has consumed all of the nextURIs [attribute returns the next batch of query results].
If it's not able to keep up, the query will stay in FINISHING state until all the segment locations are retrieved.
Join hints
JOIN hints are used to specify which join algorithm should be used (if possible) by the optimiser.

יותר קטן מtask - כל ה3
Task->1 or more Driver->1 or more Operator with 1 or more Split

עוד חלקים של הcoord
Catalogs, Connectors, SPI, logical planner, physical planner

Session properties
A configuration property that can be temporarily modified by a user for the duration of the current connection session to the Trino cluster.
There are two types of session properties:
System session properties - apply to the whole cluster
Catalog session properties - set on a per-catalog basis
Session properties are tied to the current session, so a user can have multiple connections to a cluster that each have different values for the same session properties.

Input BLOCKED / Output BLOCKED
Input - an operator is idle because it is waiting for upstream data to arrive.
Output - an operator is frozen because downstream operators or clients cannot consume its data fast enough.

Client Tags
Information about the client and the CLI user.
Separate multiple tags with commas
 The tags can be used as input for Resource groups.

2 types of caching
Trino accesses files directly on object storage and remote file system storage.
Two cache managers are available:
Alluxio caches files on local disks.
Memory caches files on the Java heap.

Client protocol
The Trino client protocol is an HTTP-based protocol that allows clients to submit SQL queries and receive results.
The protocol is a sequence of REST API calls to the coordinator of the Trino cluster.

External routing service vs Internal routing service
Internal Routing Service - Routing rules are defined locally inside a configuration file (such as a YAML file) directly accessible by the Trino Gateway. 
External Routing Service - Trino Gateway sends request headers, parameters, and metadata via an HTTP POST request to an independent, external web service, which responds with a target routing group.
Do we define the rules manually for a trino gateway or does a separate entity do that.
Noisy neighbors - איך פותרים
A service that has multiple customers [tenants] can be multitenant.
A benefit of multitenant systems is that resources can be pooled and shared among tenants.
The noisy neighbor problem occurs when one tenant's performance is degraded because of the activities of another tenant. 
The noisy neighbor problem also occurs when each tenant consumes only a small portion of the system's capacity, but the combined resource usage of many tenants can result in a peak in overall usage. [not relevant since each cluster has independent resources here]

Trino Gateway [crazy subtle foreshadowing] - a load balancer, proxy server, and configurable routing gateway for multiple Trino clusters 
Trino gateway is a middleman that checks routes “statements” into clusters, and if a cluster becomes unavailable, it will stop routing statements into said cluster.
It also handles the noisy neighbors problem so that none of the clusters reach a maximum capacity whilst sharing their resources


בעית הרשאות - איך פותרים
System access control - enforces authorization at a global level, before any connector-level authorization. You can use one of the built-in implementations in Trino, or provide your own.

FTE - סוגים
Fault-tolerant execution is a mechanism in Trino that enables a cluster to mitigate query failures by retrying queries or their component tasks in the event of failure. With fault-tolerant execution enabled, intermediate exchange data is spooled and can be reused by another worker in the event of a worker outage or other fault during query execution. 

2 types - task retry and query retry

האם FTE הוא תחליף לDisk Spill
Yes and no - yes, as in it will do some form of fault tolerance; no, as in if you run out of RAM,m there’s no backup.

TrinoUI
Trino provides a Web UI for monitoring a Trino cluster and managing queries.
The Web UI is accessible on the coordinator via HTTP or HTTPS, using the configured port number.

Concurrency, concurrency limit, parallelism, parallelism limit
The number of tasks that can be run in parallel - lower = more tasks concurrently but creates greater overhead.


---

### 🔄 Alternatives
Assignment: You are required to research and write a comparative analysis between Trino and an industry alternative.

- Deliverable: A written summary (minimum 1–2 paragraphs).
- Add a real-life use case.
- Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competing technologies.
- Goal: You must be able to justify why the department uses this tool for our specific environment.

---
### 🎯 User Story & Scenario
Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.
- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.
---


## Wrapping Up :trophy:
Go over your answers with your mentor and clarify any uncertainties. Relate Trino concepts back to the broader data platform and how distributed query engines interact with storage systems and processing frameworks.

---

## Action Items
- Identify Trino topics you want to explore further.
- Search examples of industray usage of Trino.
- **Bonus** - what is the rabbit's name?
- Prepare questions for the next mentor Q&A session.

---

## Recommended Resources
- [Official Trino Documentation](https://trino.io/docs/current/) – the primary reference guide.
- [Trino: The Definitive Guide (O'Reilly)](https://dokumen.pub/trino-the-definitive-guide-sql-at-any-scale-on-any-storage-in-any-environment-2nbsped-109813723x-9781098137236.html)
- [Official Trino Gateway Documentation](https://trinodb.github.io/trino-gateway/)
