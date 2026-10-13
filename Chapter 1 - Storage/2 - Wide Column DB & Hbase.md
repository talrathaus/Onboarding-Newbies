# Introduction to HBase :elephant:

> **Note:** this document was renamed earlier to `Wide Column DB & Hbase` to reflect the broader category; the title remains centered on HBase for now.

## Overview
Today’s session dives deeper into column‑oriented databases with a focus on Apache HBase, the Hadoop ecosystem’s wide‑column store. Understanding HBase will help you see how low‑latency random access is provided over massive data sets.

**The emphasis is on HBase’s architecture, core components, and operational model.**

## Goals
- Grasp the columnar database model and why HBase exists.
- Learn the responsibilities of key HBase components (RegionServer, Region, ZooKeeper, HFile, etc.).
- Improve your ability to plan and self‑direct learning.

:warning: **Note:**
- This is a self‑study day; independence and time management are crucial.
- If you can’t explain a concept clearly, you probably need to revaisit it.
- Read the [Exercise](#exercise) before starting so you know what to emphasize.
- Ask your mentor if you’re unsure what to research.

### ⏳ Timeline
Estimated Duration: 3 Days
- Day 1: Learn the concepts of wide column DB and HBASE spesficly; spend the day.
- Day 2-3: Get deep into HBASE spesficly
    - Have a Q&A session at the third day and in between sessions each day

## Core Concepts

## Part 1: Wide Column Databases (General Concepts)

Answer these questions to understand the fundamentals of wide-column databases before focusing on HBase:

1. **Data Model & Structure:**  
   What is a wide-column database, and how does its data model work? Explain the concepts of rows, column families, and flexible schemas. How does this model differ from traditional relational databases and key-value stores?

Wide-column Databases הם NoSQL DB הדומים לDB מסוג key-value, אך הValue עצמו בנוי גם במבנה של Key-Value, ואין חובה שכל השורות יכילו את אותן הColumns (כלומר, אין schema קבועה).
מסדי נתונים אלו מותאמים לfrequent write, ולinfrequent read and edit.
הנתונים נשמרים על גבי הדיסק, המערכת ניתנת להרחבה אופקית בקלות, והיא פועלת במבנה מבוזר.
הdata model נראה ככה:
המידע מחולק לטבלאות.
טבלה מחולקת לקבוצה של שורות - region.
region מחולק לשורות.
שורה מחולקת לRow Key וColumn Family.
בColumn Family יהיה [(column(s ושם] המידע שמור בצורת Key-Value.
Row Key - מזהה יחודי של השורה
Column Family - קבוצה של שורות הממקמות פיזית קבוצה של עמודות ואת הערכים שלהן, לעיתים קרובות משיקולי ביצועים.
Flexible schema: מאחסן נתונים רק כאשר הcolumns קיימים, אידיאלי עבור נתונים בעלי semi-structured data.
זה שונה מKey Value בכך שאפשר לאחסן בתוך ה"Value" שלנו עוד מערכת "Key Value" ואפשר להריץ עליהם queries כאילו זה RDBMS.
זה שונה מRDBMS בכך שהschema לא אחידה וקבועה.  
HMaster - הNameNode של HBase: מנהל את cluster הHBase, מקצה Regionים לRegionServerים, מבצע load balancing ומטפל בschema changes.

1. **Use Cases & Motivation:**  
   Why do wide-column databases exist? In what scenarios are they most useful (for example: large-scale datasets, time-series data, sparse data, or systems requiring high write throughput)?

Wide-Column DBs נוצרו משום שגוגל התמודדה עם בעיה שאף אחד לא פתר קודם לכן: indexing של כל WWW.
הדרישות שלהם היו:
- PB של נתונים - צורך בdistributed system.
- מיליארדי פעולות מדי יום - קריאות וכתיבות רציפות.
- Schema משתנה - נדרשו schemaות מרובות, שונות ומשתנות.
- נתונים דלילים - רוב התאים יהיו ריקים כי האתרים שונים זה מזה.
מסדי נתונים רלציוניים לא יכלו להרחיב אופקית, מאגרי מסמכים עדיין לא היו קיימים, ומאגרי מפתח-ערך היו פרימיטיביים מדי עבור דפוסי הגישה המקוננים והרב-ממדיים הנדרשים.
Column-Wide Databases נוצר להיות אידיאלי עבור:
- Schema משתנה\פורמטים שונים של נתונים.
- Horizontal scaling - מערכות מבוזרות גדולות.
- שליפת נתונים יעילה עבור שאילתות שלא רלוונטיות לכל השורות.
- נתונים הדורשים לעיתים קרובות פעולות קריאה וכתיבה מהירות.

2. **Distributed Design:**  
   How do wide-column databases distribute data across clusters? Explain concepts such as partitioning, replication, and horizontal scalability.

Wide-Column DBs עושים שימוש בpartitioning מבוסס Hash, כאשר נהוג להשתמש באלגוריתמים של Consistent Hashing כדי להשיג חלוקת נתונים מאוזנת [יעני לעשות load balancing בין RegionServers].
הנתונים משוכפלים על פני מספר RegionServers.
היכולת לפצל regions ולהפיצם בין מספר RegionServers משמעותה שDBS מסוג Wide-Column "נועדו" לhorizontal scaling, כלומר, הוספת RegionServers נוספים.

---

### Part 2: Apache HBase (Implementation & Operations)

Answer these five questions to cover HBase’s major areas:

1. **Architecture & Data Model:**  
   Describe the overall architecture of Apache HBase, including tables, rows keyed by row key, column families, region servers, regions, and the storage format (HFile). How do these elements differ from a traditional relational database, and why is schema design driven by access patterns?

המידע מחולק לטבלאות.
region מחולק לשורות.
שורה מחולקת לRow Key וColumn Family.
Row Key - מזהה יחודי של השורה
Column Family - קבוצה של שורות הממקמות פיזית קבוצה של עמודות ואת הערכים שלהן, לעיתים קרובות משיקולי ביצועים.
טבלה מחולקת לקבוצה של שורות - region.
HRegionServer הוא המימוש של הRegionServer, האחראי על ניהול של Regionים, הRegionServer הוא DataNode בDISK.
HFile - הנתונים בHBase מאוחסנים בקובץ של key-value pairs ממוינים.
זה שונה מRDBMS בכך שהschema לא אחידה וקבועה.
הschema מושפעת access pattern כי לא לכל שורה יש את אותה schema.

2. **Components & Storage Flow:**  
   Explain the roles of RegionServers, Regions, MemStore, HFiles, block cache, and the Write-Ahead Log (WAL). How does data flow from a client write to durable storage, and how are reads served from memory and disk structures? Understand what is the actual role of each component and its purpose. In addition, understand the formats of these components.

HRegionServer הוא המימוש של הRegionServer, האחראי על ניהול של Regionים, הRegionServer הוא DataNode.
טבלה מחולקת לקבוצה של שורות - region.
MemStore: רכיה הקולט את פעולות הput האחרונות, יש רק MemStore 1 לכל Column Family.
HFile - הנתונים בHBase מאוחסנים בקובץ של key-value pairs ממוינים בDISK.
Block Cache: שומר בלוקים של נתונים בזיכרון לאחר קריאתם.
WAL: מאחסן נתונים חדשים שטרם נשמרו או עברו commit באחסון קבוע.  
קובצי WAL מכילים רשימה של פעולות עריכה [כולל פעולות הוספה ומחיקה].  
פעולות העריכה נכתבות באופן כרונולוגי; לפיכך, לצורך שמירה קבועה, פעולות הוספה חדשה מתווספות לסוף קובץ הWAL המאוחסן בדיסק.
Write:
WAL-נעשה put למה שאנחנו רוצים לכתוב, כך שזה ישמר בWAL,.
Memstore - העדכון נרשם בmemstore.
ACK - מקבלים עדכון שהעדכון שלנו נשמר בRAM.
Flush - כאשר הWAL נהיה מלא מספיק, נוריד את כל השינויים שלנו לHFile כך שישמרו בDisk.
Read:
WAL - נראה אם מה שאנחנו מחפשים נמצא שם
Memstore - אם לא היה בWAL, נראה אם במקרה מה שאנחנו מחפשים נמחק
HFile - נחפש בHFile

3. **Performance & Maintenance:**  
   What are minor and major compactions, MOB storage, Bloom filters, and caching? How do they affect read/write latency, storage efficiency, and amplification? Discuss the importance of row-key design and hotspot avoidance.

Compactions: הדרך של HBase לנקות אחריו את הHFILEים הלא נחוצים\"dupicates" בכדי להוריד עומס מהזיכרון.
Minor compactions: מרג’וג' של כמו קונפיגורבילית של HFileים קטנים לHFile אחד גדול יותר.
Major compactions: מרג’וג’ של כל קבצי הHFile בregion אחד.
אחסון של Medium-sized Objects בגדלי 100KB-10MB sized objects בHBase מתבצע על ידי הפחתת עומס I/O הכולל עבור column family שהוגדרו על ידי אחסון ערכים גדולים מהסף שהוגדר מחוץ לאזורים הרגילים כדי למנוע splits, merges, וחשוב מכל, minor compactions.
Caching: שמירת מידע חדש בRAM בכדי שיהיה אפשר לשלוף אותו יותר מהר.
כל אלו הם פעולות שבצורה ישירה - שמירה של מידע בRAM, או בצורה עקיפה - מקלים על הDisk, מאפשרים לread/write latency לרדת ולאחסן את המידע בצורה יותר טובה.
היתרון של הrow key design הוא שתמיד יהיה מזהה יחודי לכל שורה ולכן לא צריך לדאוג לקפילויות של ערכים וחיפוש הינו הרבה יותר מהיר.
Hotspotting מתרחש כאשר כמות גדולה של תעבורת לקוחות מופנית לnode יחיד, או למספר מצומצם של nodeים, בתוך cluster.

3. **Fault Tolerance & Coordination:**  
   How does HBase use WAL replay, region reassignment, and coordination via ZooKeeper to handle failures and maintain availability? What happens when a RegionServer crashes?

WAL Replay מאפשר להריץ מחדש את הWAL עבור קבוצת או כל הtables.  
הWAL מסונן כך שיכלול רק את קבוצת הtables שנבחרה.  
ניתן, למפות את הפלט לקבוצת tables אחרת.  
הWALPlayer מסוגל לייצר HFileים לצורך bulk import בשלב מאוחר יותר.
Region reassignment מאפשר לregion לעבר מregionserver אחד לאחר למטרות load balancing.
Zookeeper HBase משתמשת בZooKeeper לצורך leader elections, ניהול leases של שרתים, bootstrapping ותיאום בין הRegionServers.
במקרה של קריסה של שרת RegionServer, הzookeeper ינהל את השרתי regionservers שנשארו ויגרום לregion reassignment, בנוסף, במידה וניתן נשתמש בWAL Replay.

3. **Scalability & Operations:**  
   Discuss how HBase scales horizontally through region splitting and balancing, how it relies on HDFS for durability, and what administrative actions (snapshots, backups, schema changes, recovery) operators perform in production environments.

HBase Horizontal Scaling קורה באמצעות הוספה של RegionServerים ושימוש בRegion Reassignment.
HBase פועל על גבי HDFS ובכך הreplication והביזור שלו ניתנים לשימוש כיתרון כי כל RegionServer הינו DataNode והHMaster הינו NameNode.
Snapshots: שומר שינויים מרגע ההתחלה על טבלה מסוימת.
Backup: עותק של table ששמור מחוץ ל-HBase לצורך התאוששות מאסון.
Schema changes: פשוט להוסיף column חדש.
Recovery: הHMaster מקצה מחדש את הRegions שלו לRegionServers זמינים, ותהליך הReplay משחזר פעולות כתיבה שטרם נשמרו בHFiles.  
במקרה של HMaster failure הZKFC יוודא יוודה שהStandby HMaster יעלה.
### 🔄 Alternatives
Assignment: You are required to research and write a comparative analysis between HBase and an industry alternative.
- Deliverable: A written summary (minimum 1 or 2 sentences).
- Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
- Goal: You must be able to justify why the department uses this tool for our specific environment.

### 🎯 User Story & Scenario
Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.
- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.

## Wrapping Up :trophy:
Go over your answers with your mentor and clarify any uncertainties. Relate HBase concepts back to the broader data platform.

## Action Items
- Identify HBase topics you want to delve into further.
- Collect a list of real‑world HBase deployments or related technologies.
- Prepare questions for the next mentor Q&A session.

## Recommended Resources
- [Official HBase Reference Guide](https://hbase.apache.org/book.html) – the definitive documentation.
- *Hadoop: The Definitive Guide* (O'Reilly) – chapters on HBase.
