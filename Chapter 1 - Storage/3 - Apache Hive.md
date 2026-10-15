# Apache Hive 🐝

## Overview

Hive includes several cooperating responsibilities. As you research, distinguish catalog and metadata management, SQL planning, distributed compute, and storage. Identify which Hive or Hadoop component performs each responsibility and how the components interact with one another.

> **Mental model:** HMS answers *“What is the table and where is it?”* The query engine answers *“How will this query run?”* Storage answers *“Where are the bytes?”*

### ⏳ Timeline
Estimated duration: 2 Days 

Complete the research assignments, record the sources you used and the questions that remain open, and review your findings with your mentor.

## Research Assignments

### 1. Hive's Purpose and Place in the Ecosystem

Research why Apache Hive was created and where it fits in the Hadoop ecosystem. Explain the types of workloads it is designed for, the abstractions it adds above distributed storage, and how its approach differs from traditional database systems.
 
י פייסבוק עברה מOracle [אחסון מבוסס SQL] לHadoop [אחסון מבוסס MapReduce], וכעת 70,000 השאילתות שהיה עליהם להריץ מדי יום התבצעו לאט מדי, וHadoop אינה תומכת בSQL אלא בMapReduce בלבד וכל המפתחים של פייסבוק שהתרגלו לSQL לא ידעו מה לעשות.
 
י הוא בנוי למטלות על WareHouse - סיכום נתונים, ביצוע שאילתות ad-hoc וניתוח של כמויות גדולות של נתונים, לא למטלות טז"מיות [OLTP].

י Hive מוסיף כלים המאפשרים גישה נוחה לנתונים באמצעות SQL, מאפשרים ETL, הפקת reports, ניתוח נתונים, גישה לקבצים המאוחסנים ישירות בHDFS או במערכות אחסון נתונים אחרות, כמו HBase.

י 2 ההבדלים העיקריים בHive לעומת DBs אחרים הם:

י 1. Schema on read - הסכמה נאכפת בזמן הקריאה ולא הכתיבה, כך שיש יותר גמישות ומהירות בהכנסת המידע אך זה יכול ליצור שגיאות בruntime כשאנחנו קוראים את המידע ועושים לו Parse.  לעומת זאת, בDB קלאסי שבו הschema היא on write כך שמידע שלא עומד בschema לא נכנס מלחתחילה אך יותר איטי הכתיבה.

י 2. Seperation of storage and compute - לעומת DB קלאסי שגם מנהל פעולות [שליפות, הנכסות, מחיקות, עריכות…] וגם את האחסון של המידע עצמו, Hive מטפל רק בפעולות ולא עושה את האחסון בעצמו.
### 2. Hive Architecture

Draw the architecture of a production-style Hive environment. Include every component required for a client to submit a query, obtain metadata, execute distributed work, and access table data. Explain the responsibility of each component as well as every connection, protocol, deployment boundary, and important failure scenario.

Your explanation should make clear which responsibilities belong to the catalog, query processing, distributed compute, and storage. Explain which component manages metadata, which components plan and coordinate queries, and which components perform the distributed computation.

- Pay particular attention to **decoupling** in Hive's architecture. Explain which responsibilities can operate independently and why separating metadata management from query execution is useful.

<img width="1160" height="1082" alt="image" src="https://github.com/user-attachments/assets/21226ce9-f814-4c8f-8dbc-45168cc52ba1" />
 

י Catalog:

י Thrift Client - לקוח מכל שפה שתומכת בthrift

י ODBC - windows software applications clients 

י JDBC - java application clients 

י CLI - CLI לשאילתות Hive 

י Web Interface - ממשק web 

י Query Processing: 

י Hive Server - שרת המקשר בין לקוחות לHive עצמו 

י Hive Driver - המוח של Hive, כאשר משתמש כותב שאילתה, היא נשלחת לcompiler המשתמש בmetadata כדי לקמפל אותה.  
לאחר מכן, הoptimizer משפר את קוד הMapReduce כדי לאפשר ביצוע יעיל יותר.  
לבסוף, הexecutor - מנוע ה-MapReduce, מריץ את התוכנית ומחזיר את התוצאה. 

י Metastore - המקום בו מאוחסן metadata על טבלאות אלו, כמו שמות DBs והSchemaות, מיקום האחסון, partitions ועוד. 

י Metastore Server - הגשר בין הלקוח לMetastoreים. 

י Derby DB - הDB אחסון של הmetadata. 

י Distributed computation: 

י Proc and resource management - הצורה שבה המידע מועבד, תלוי גרסת Hive, הרכיב שאיתו הexecutor מתקשר. 

י Flow: UI->Driver->Compiler [Driver] ->Metastore->Compiler [Driver]->Optimizer [Driver]->Executor [Driver] -> Executor [MapReduce/tez]->UI 

י הUI שולח שאילתת SQL לdriver שמעביר אותה לCompiler שלוקח metadata מהmetastore בשביל לקחת את השאילתה ולתרגם אותה לMapReduce job.   

י משם זה עובר לOptimizer שגורם לסקריפט לרוץ יותר מהר ואז לExecutor שמריץ את הסקריפט ומחזיר תשובה לUI. 

י הDeployment boundries נקבעים לפי כמות הmapreducers המשתתפים בפעולה - localmode שבו עובד רק reducer אחד לעומת mapreducemode [מאוד יצירתי] שבו עובדים יותר מreducer 1. 

י “com.mysql.jdbc.exceptions.jdbc4.!CommunicationsException: Communications link failure” 

י שגיאה זו נגרמת בדרך כלל מכך ששרתי MySQL סוגרים חיבורים לאחר שהחיבור נותר במצב idle למשך זמן מה.   

י הרצת הפקודה הבאה בשרת ה-MySQL תפתור את הבעיה: 

י “set global wait_status=120;”
### 3. Hive Tables and Storage

Choose one Hive table and investigate its complete lifecycle: definition, schema, storage location, file format, data loading, schema changes, querying, and deletion. Demonstrate how its logical definition relates to the files and directories in storage, and explain the important design choices at each stage.
 

י הגדרה, סכמה: 

י CREATE TABLE {TableName}({Column1Name} {Column1DataType}, {Column2Name} {Column2DataType}, {Column3Name} {Column3DataType},...) ROW FORMAT DELIMITED FIELDS TERMINATED BY ‘{Delimiter}’ STORED AS {FileType}; 

י כאשר ColumnDataType יכול להיות 

י TinyInt, SmallInt, Int, BigInt, Float, Double, STRING, timestamp, MAP, STRUCT, ARRAY 

י כאשר FileType יכול להיות 

י Texfile, Sequencefile, ORCfile, RCfile, Parquetfile וAvrofile 

י טעינת נתונים ושאילתות: 

י LOAD DATA INPATH '{Filepath}' INTO TABLE {TableName}; 

י ההתנהגות המדויקת תלויה במיקום המקור ובמערכת הקבצים.   

י כאשר קובץ המקור נמצא ב־HDFS, הפעולה עשויה להעביר אותו לתיקיית הטבלה במקום לקרוא כל רשומה ולכתוב אותה מחדש. 

י לאחר מכן ניתן להריץ שאילתות SQL בשביל לטעון מידע . 

י Hive מתרגם את השאילתה לתוכנית ביצוע, שיכולה לרוץ באמצעות Tez או MapReduce, בהתאם להגדרות המערכת. 

י שינוי schema: 

י ALTER TABLE {TableName} ADD COLUMNS ({ColumnName} {ColumnDataType}); 

י הוספת עמודה להגדרת הטבלה אינה בהכרח משנה את הקבצים הקיימים.   

י רשומות ישנות עשויות להחזיר NULL עבור העמודה החדשה, אם הנתונים בקובץ אינם כוללים אותה. 

י מחיקת טבלה: 

י DROP TABLE {TableName}; 

י סוגי טבלאות: 

י Managed Table - מחיקתה מסירה גם את הmetadata וגם את הנתונים. 

י External Table - מחיקתה מסירה את הmetadata בלבד ומשאירה את קובצי הנתונים. 

י בנוסף, בmanaged tables, ניתן לשנות את הנתונים, את הproperties שלהם ואת הdata layout אך ורק באמצעות פקודות Hive.   

י [ניתן לעקוף זאת, אך הדבר יוביל לבעיות ולתקלות] 

י השיקולים ביצירת טבלה הם: 

י 1. בחירת סוג הטבלה שיותר מתאים לסיטואציה - האם אתה רוצה שHive תהיה אחראית למחיקת המידע או שהוא רק ימחק אם אתה מוחק אותו דרך מערכת הקבצים 

י 2. סוג הקובץ - איך המידע שמור ומה הפורמט בתוך הקובץ 

י 3. סוג הschema - איך המידע אשקרה נראה, לא נרצה לשמור timestamps כIntים או MAP כSTRING
### 4. Hive Partitioning

Research partitioning in Hive and how Hive implements it. Explain how a partitioned table is defined, how partitions affect the filesystem directory structure, and how partitioning can improve or harm query performance. Include the trade-offs involved in choosing partition columns.
 

י Partitioning בHive זה שיטה לפיצול טבלאות ענק לטבלאות לוגיות קטנות יותר, בהתבסס על ערכי עמודות.   

י עבור כל ערך ייחודי נוצרת טבלה לוגית אחת - מחיצה.   

י בHive, טבלאות מיוצגות כתיקיות במערכת הקבצים HDFS. 

י טבלה יכולה לכלול מחיצה אחת או יותר, כאשר כל מחיצה תואמת לתת-תיקייה בתוך התיקייה של הטבלה.  

י זה עוזר לנו לחיפוש יותר מהיר באמצעות שאם Hive מזהה מחיצה המתאימה לשאילתה, הוא יכול י להשתמש בPartition Pruning ולקרוא רק את התיקייה הרלוונטית, במקום לסרוק את כל הנתונים מכל השנים. 

י הTrade-off הוא בעצם חיפוש על שאילתות ספציפיות מהיר קצר לעומד חיפוש על שאילתות יותר כלליות יותר איטי.

### 5. Dedicated MapReduce Exercise: WordCount

Explain how the classic MapReduce WordCount program works from input to final output. Describe the mapper input and output, shuffle and sort, reducer input and output, and which operations run in parallel. Use concrete key/value pairs in your explanation. Then explain why executing a multi-stage Hive query with MapReduce can be expensive and how Tez differs.
 

י משפט דוגמא:   

י "אנחנו לוקחים" - Node 1   

י את המידע ומעבירים" - Node 2   

י "אותו הלאה" - Node 3
 

י שלב ראשון - הפיכת המידע לKeyValuePair


| Value | Key      |
| ----- | -------- |
| 1     | אנחנו    |
| 1     | לוקחים   |
| 1     | את       |
| 1     | המידע    |
| 1     | ומעבירים |
| 1     | אותו     |
| 1     | הלאה     |
 

י שלב שני - ערבוב המידע לפי Key לNodes 

י "אותו אנחנו את" - Node 1 

י "הלאה המידע" - Node 2 

י "ומעבירים לוקחים" - Node 3
 

י שלב שלישי - ספירת המידע פנים Nodeית 

י Node 1

| Value | Key   |
| ----- | ----- |
| 1     | אותו  |
| 1     | אנחנו |
| 1     | את    |
 

י Node 2

| Value | Key   |
| ----- | ----- |
| 1     | הלאה  |
| 1     | המידע |
 

י Node 3

| Value | Key      |
| ----- | -------- |
| 1     | ומעבירים |
| 1     | לוקחים   |
 

י שאילתת Hive מורכבת עשויה לבצע JOIN, לאחר מכן GROUP BY ולבסוף פעולת צבירה נוספת - כאשר פעולות אלו דורשות מספר משימות MapReduce נפרדות, כל משימה עלולה להוסיף המתנה בין שלבים וכתיבה וקריאה של נתוני ביניים מהאחסון. 

י Tez מאפשר להריץ שאילתה כDAG של משימות עיבוד.   

י הוא מחבר שלבים בצורה גמישה יותר, יכול לעשות שימוש חוזר במשאבי ביצוע ולהימנע מחלק מכתיבות י הביניים ומעלויות האתחול המיותרות. 

י Tez לא מבטל כל כתיבה לדיסק ולא מבטיח שכל שאילתה תהיה מהירה יותר, אך הוא יכול להפחית את העלויות של ביצוע שאילתות מרובות שלבים.

### 6. Fault Tolerance

Research fault tolerance in Hive. Consider failures in the services involved in metadata management, query coordination, distributed execution, and storage. Explain which failures a query can recover from, which failures cause it to fail, and what makes recovery possible.
 

י התאוששות: 

י 1. שכפול נתונים ב־HDFS. 

י 2. ניסיונות חוזרים של משימות - הexecutors יכולים להריץ מחדש משימות שנכשלו בצומת אחר. 

י 3. High Availability - אפשר להגדיר מספר מופעים של Metastore או של HiveServer2, כך שכשל של מופע אחד לא בהכרח יפסיק את השירות. 

י סבילות לתקלות ב־Hive מבוססת על שילוב בין שכפול נתונים, ניסיונות חוזרים של משימות ויתירות של שירותים.   

י תקלות נקודתיות בDataNodes או בעיבוד ניתנות לעיתים קרובות להתאוששות אוטומטית.   

י לעומת זאת, אובדן כל עותקי הנתונים הדרושים, כשל מתמשך בשירות קריטי או מיצוי ניסיונות ההתאוששות עלולים לגרום לשאילתה להיכשל. 

י כלומר, ייתכן שהמערכת תמשיך להיות זמינה, אך שאילתה מסוימת שכבר נכשלה תצטרך להישלח מחדש.

### שאלות סקילה 1

**י מה זה mapreduce**

י map produce שזה בעצם פונקציה שפועלת על כל האיברים בסדרה במקביל

**י איך mapreduce עובד**

י 3 שלבים:

י 1. Map: כל worker node מפעיל את פונקציית הMap על הנתונים המקומיים וכותב את הפלט לאחסון זמני.
הmaster node מוודא שרק עותק אחד של נתוני הקלט הכפולים יעובד.

י 2. Shuffle: כל worker node מבצעים חלוקה מחדש של הנתונים בהתבסס על output keys (שנוצרו על ידי פונקציית הMap), כך שכל הנתונים המשויכים למפתח מסוים ממוקמים באותו צומת עבודה.

י 3. Reduce: הworker nodes מעבדים במקביל כל קבוצה של נתוני פלט, עבור כל מפתח.

**י איזה חלק בecosystem הוא hive**

י SQL Query Engine

**י מה השם של הweb interface**

י WebHCat

**י מה זה thrift**

י thrift זה IDL שזה שפת תכנות המאפשרת לתוכנית או לאובייקט, הכתובים בשפת תכנות אחת, לתקשר עם תוכנית אחרת הכתובה בשפת תכנות לא ידועה.

**י למה בחרו בthrift בHadoop Ecosystem**

י אפשר להשתמש בThrift גם עבור RPC.

י מכיוון שHadoop מבצע RPCs רבים, קיימת אפשרות להשתמש בThrift כדי לשפר את הביצועים.

**י למה בחרו בthrift בHive**

י גם Hive עושה הרבה RPCs וזה גם אחיד עם שאר הecosystem.

**י מה הCLI השני בHive [לא HiveCLI]**

י Beeline

**י מה ההבדל בין 2 הCLIs של Hive - על מה כל אחד מהם מבוסס**

י HiveCLI הוא הCLI הדיפולטיבי והיותר ישן של Hive, הוא מובנה בתוך hive ומובנה Java.

י Beeline הוא חדש יותר ומתחבר לHive דרך הHiveServer, מבוסס JDBC ודומה ללקוח thrift.

**י האם הdriver והserver רכיבים שונים בhive**

י כן, הם רכיבים נפרדים.

**י מה הOutput של SQL לאחר קומפילציה**

י DAG

**י איך קוראים לרכיב שלוקח "compiled SQL" בhive והופך אותו לmapreduce job**

י Planner לוקח את הDAG והופך אותו לmapreduce job

**י איזה עוד executors יש חוץ מmapreeduce/mapreducev2**

י Spark, Tez - בתכלס שניהם יותר טובים לווק, Tez יותר מתאים ללהחליף את Mapreduce בuse case הזה וSpark יותר מהיר.

**י איך למחוק מידע בטלבה external ושהמיגע גם ימחק**

י ALTER TABLE addresses_text SET TBLPROPERTIES ('external.table.purge'='true');

**י מה ההבדל השני בין external וmanaged**

י managed גורם לhive להניח שהוא מנהל גם את המידע לעומת external שלא, כך שניתן לערוך את המידע בmanaged table באמצעות פקודות Hive.

**י מה זה DerbyDB**

י פרויקט Java-י של RDMBS מapache שניתן להשתמש בו כDB זמני לtesting [המטרה שלו]

**י האם נשתמש בDerbyDB במערכת prod**

י לא, זה מוצר שהפסיקו להמשיך וכי לא היה לו High availability והוא מוצר של Single Process Storage, כלומר, הוא יודע להתמודד רק עם לקוח אחד בכל רגע 

**י מה המצב בשלישי של HMS [חוץ מlocal וremote]**

י Embedded

**י ההבדל בין local HMS וremote HMS**

י Embeded - הכל לוקלי - מהDriver עד הmetastore והDB, הDB בהכרח יהיה Derby.

י Local - הDriver והMetastore לוקליים, רק הDB יהיה בנפרד וכנראה לא יהיה DerbyDB.

י Remote - הMetastoreים והDB נמצאים גם בם במכונות וירטואליות נפרדות מהDriver.

**י מה זה Avi load balancer***

**י סוגי אופטימיזציות בHive**

י מאחד את הטרנספורמציות השונות יחד, ממיר JOINים רבים לפעולה אחת, מפצל משימות כך שניתן יהיה לארגן את החלקים באופן שיאפשר ביצוע מהיר יותר,כמו הפעלת filters לפני ביצוע הtransform.

**י למה רק HMS 1**

אין בהכרח רק אחד, אפשר לעשות יותר מאחד, דווקא מומלץ שיהיה יותר מHive Metastore Server אחד כי הוא stateless ורק מאפשר תקשורת עם הMetastore.

**י למה יש metastore server**

**י שלא כל Driver ידע איפה על הMetastoreים נמצאים [בRemote HMS architecture].**

י האיזה דרכים הביזור של metastore server קורה

**י לקוח בוחר metastore באופן אקראי, אם הmetastore הזה אינו זמין, הלקוח בוחר באופן אקראי אחד אחר.**

**י מה זה metastore ERD***

### שאלות סקילה 2 

**י למה הHiveCLI לא עובר דרך הHiveServer**

י 

**י באיזה פרוטוקול הHiveCLI מתשקר עם הDriver**

י 

**י HiveServer1 VS HiveServer2**

י 

**י מה זה הIL של HiveQL**

י 

**י מה מאפשר לHive לנהל את הManaged Table**

י 

**י למה הHive MetaStore Server קיים בתכלסססססס**

י 

**י מה הUse Case של Remote VS Local HMS**

י 

**י למה Hive הוא לא DB**

י 

**י איך Hive יודע לקרוא סוגי קבצים לא טקסטואלים**

י 

**י מה זה Parquet**

י 

**י מה זה avro, orc [בקצרה]**

י 

**י איך נראות תיקיות בpartitioning**

י 

**י איך להוסיף partition לmetastore**

י 

## Optional Hands-On

Complete the [Docker Compose lab](./Hive%20Hand%20On%20(optional)/README.md) to inspect catalog and query services separately, create an external table, run `EXPLAIN`, and observe metadata and data lifecycles.

## Trainee Completion Checklist

- [ ] I can explain why Hive exists and the workloads for which it is designed.
- [ ] I can draw Hive's architecture and distinguish catalog, query processing, compute, and storage.
- [ ] I can explain decoupling between metadata management and query execution.
- [ ] I can trace the lifecycle of a Hive table from its logical definition to its physical data.
- [ ] I can explain how Hive partitioning is represented in the table definition and filesystem.
- [ ] I can explain WordCount, especially shuffle and sort, and compare MapReduce with Tez.
- [ ] I can explain how Hive's components handle failures and where fault tolerance comes from.
- [ ] I recorded the sources I used and my remaining questions for the mentor.

## Recommended Resources

- [MapReduce video](https://youtu.be/cvhKoniK5Uo?si=MGoozk3SU-uOCGEA) — **Recommended viewing while learning about MapReduce.** It provides a visual explanation to reinforce the map, shuffle and sort, and reduce stages.

Review your research and checklist with your mentor. The chapter is complete when you can explain the system in your own words and diagnose a problem by layer instead of only saying that “Hive is broken.”
