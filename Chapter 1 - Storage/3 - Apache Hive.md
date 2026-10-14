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

פייסבוק עברה מOracle [אחסון מבוסס SQL] לHadoop [אחסון מבוסס MapReduce], וכעת 70,000 השאילתות שהיה עליהם להריץ מדי יום התבצעו לאט מדי, וHadoop אינה תומכת בSQL אלא בMapReduce בלבד וכל המפתחים של פייסבוק שהתרגלו לSQL לא ידעו מה לעשות.

הוא בנוי למטלות על WareHouse - סיכום נתונים, ביצוע שאילתות ad-hoc וניתוח של כמויות גדולות של נתונים, לא למטלות טז"מיות [OLTP].

Hive מוסיף כלים המאפשרים גישה נוחה לנתונים באמצעות SQL, מאפשרים ETL, הפקת reports, ניתוח נתונים, גישה לקבצים המאוחסנים ישירות בHDFS או במערכות אחסון נתונים אחרות, כמו HBase.

2 ההבדלים העיקריים בHive לעומת DBs אחרים הם:

1. Schema on read - הסכמה נאכפת בזמן הקריאה ולא הכתיבה, כך שיש יותר גמישות ומהירות בהכנסת המידע אך זה יכול ליצור שגיאות בruntime כשאנחנו קוראים את המידע ועושים לו Parse.  לעומת זאת, בDB קלאסי שבו הschema היא on write כך שמידע שלא עומד בschema לא נכנס מלחתחילה אך יותר איטי הכתיבה.
2. Seperation of storage and compute - לעומת DB קלאסי שגם מנהל פעולות [שליפות, הנכסות, מחיקות, עריכות…] וגם את האחסון של המידע עצמו, Hive מטפל רק בפעולות ולא עושה את האחסון בעצמו.
### 2. Hive Architecture

Draw the architecture of a production-style Hive environment. Include every component required for a client to submit a query, obtain metadata, execute distributed work, and access table data. Explain the responsibility of each component as well as every connection, protocol, deployment boundary, and important failure scenario.

Your explanation should make clear which responsibilities belong to the catalog, query processing, distributed compute, and storage. Explain which component manages metadata, which components plan and coordinate queries, and which components perform the distributed computation.

- Pay particular attention to **decoupling** in Hive's architecture. Explain which responsibilities can operate independently and why separating metadata management from query execution is useful.

<img width="1160" height="1082" alt="image" src="https://github.com/user-attachments/assets/21226ce9-f814-4c8f-8dbc-45168cc52ba1" />

Catalog:
Thrift Client - לקוח מכל שפה שתומכת בthrift
ODBC - windows software applications clients
JDBC - java application clients
CLI - CLI לשאילתות Hive
Web Interface - ממשק web
Query Processing:
Hive Server - שרת המקשר בין לקוחות לHive עצמו
Hive Driver - המוח של Hive, כאשר משתמש כותב שאילתה, היא נשלחת לcompiler המשתמש בmetadata כדי לקמפל אותה.  
לאחר מכן, הoptimizer משפר את קוד הMapReduce כדי לאפשר ביצוע יעיל יותר.  
לבסוף, הexecutor - מנוע ה-MapReduce, מריץ את התוכנית ומחזיר את התוצאה.
Metastore - המקום בו מאוחסן metadata על טבלאות אלו, כמו שמות DBs והSchemaות, מיקום האחסון, partitions ועוד.
Metastore Server - הגשר בין הלקוח לMetastoreים.
Derby DB - הDB אחסון של הmetadata.
Distributed computation:
Proc and resource management - הצורה שבה המידע מועבד, תלוי גרסת Hive, הרכיב שאיתו הexecutor מתקשר.
Flow: UI->Driver->Compiler [Driver] ->Metastore->Compiler [Driver]->Optimizer [Driver]->Executor [Driver] -> Executor [MapReduce/tez]->UI
הUI שולח שאילתת SQL לdriver שמעביר אותה לCompiler שלוקח metadata מהmetastore בשביל לקחת את השאילתה ולתרגם אותה לMapReduce job.  
משם זה עובר לOptimizer שגורם לסקריפט לרוץ יותר מהר ואז לExecutor שמריץ את הסקריפט ומחזיר תשובה לUI.
הDeployment boundries נקבעים לפי כמות הmapreducers המשתתפים בפעולה - localmode שבו עובד רק reducer אחד לעומת mapreducemode [מאוד יצירתי] שבו עובדים יותר מreducer 1.
“com.mysql.jdbc.exceptions.jdbc4.!CommunicationsException: Communications link failure”
שגיאה זו נגרמת בדרך כלל מכך ששרתי MySQL סוגרים חיבורים לאחר שהחיבור נותר במצב idle למשך זמן מה.  
הרצת הפקודה הבאה בשרת ה-MySQL תפתור את הבעיה:
“set global wait_status=120;”
### 3. Hive Tables and Storage

Choose one Hive table and investigate its complete lifecycle: definition, schema, storage location, file format, data loading, schema changes, querying, and deletion. Demonstrate how its logical definition relates to the files and directories in storage, and explain the important design choices at each stage.

הגדרה, סכמה:
CREATE TABLE {TableName}({Column1Name} {Column1DataType}, {Column2Name} {Column2DataType}, {Column3Name} {Column3DataType},...) ROW FORMAT DELIMITED FIELDS TERMINATED BY ‘{Delimiter}’ STORED AS {FileType};
כאשר ColumnDataType יכול להיות
TinyInt, SmallInt, Int, BigInt, Float, Double, STRING, timestamp, MAP, STRUCT, ARRAY
כאשר FileType יכול להיות
Texfile, Sequencefile, ORCfile, RCfile, Parquetfile וAvrofile
טעינת נתונים ושאילתות:
LOAD DATA INPATH '{Filepath}' INTO TABLE {TableName};
ההתנהגות המדויקת תלויה במיקום המקור ובמערכת הקבצים.  
כאשר קובץ המקור נמצא ב־HDFS, הפעולה עשויה להעביר אותו לתיקיית הטבלה במקום לקרוא כל רשומה ולכתוב אותה מחדש.
לאחר מכן ניתן להריץ שאילתות SQL בשביל לטעון מידע .
Hive מתרגם את השאילתה לתוכנית ביצוע, שיכולה לרוץ באמצעות Tez או MapReduce, בהתאם להגדרות המערכת.
שינוי schema:
ALTER TABLE {TableName} ADD COLUMNS ({ColumnName} {ColumnDataType});
הוספת עמודה להגדרת הטבלה אינה בהכרח משנה את הקבצים הקיימים.  
רשומות ישנות עשויות להחזיר NULL עבור העמודה החדשה, אם הנתונים בקובץ אינם כוללים אותה.
מחיקת טבלה:
DROP TABLE {TableName};
סוגי טבלאות:
Managed Table - מחיקתה מסירה גם את הmetadata וגם את הנתונים.
External Table - מחיקתה מסירה את הmetadata בלבד ומשאירה את קובצי הנתונים.
בנוסף, בmanaged tables, ניתן לשנות את הנתונים, את הproperties שלהם ואת הdata layout אך ורק באמצעות פקודות Hive.  
[ניתן לעקוף זאת, אך הדבר יוביל לבעיות ולתקלות]
השיקולים ביצירת טבלה הם:
1. בחירת סוג הטבלה שיותר מתאים לסיטואציה - האם אתה רוצה שHive תהיה אחראית למחיקת המידע או שהוא רק ימחק אם אתה מוחק אותו דרך מערכת הקבצים
2. סוג הקובץ - איך המידע שמור ומה הפורמט בתוך הקובץ
3. סוג הschema - איך המידע אשקרה נראה, לא נרצה לשמור timestamps כIntים או MAP כSTRING
### 4. Hive Partitioning

Research partitioning in Hive and how Hive implements it. Explain how a partitioned table is defined, how partitions affect the filesystem directory structure, and how partitioning can improve or harm query performance. Include the trade-offs involved in choosing partition columns.

Partitioning בHive זה שיטה לפיצול טבלאות ענק לטבלאות לוגיות קטנות יותר, בהתבסס על ערכי עמודות.  
עבור כל ערך ייחודי נוצרת טבלה לוגית אחת - מחיצה.  
בHive, טבלאות מיוצגות כתיקיות במערכת הקבצים HDFS.
טבלה יכולה לכלול מחיצה אחת או יותר, כאשר כל מחיצה תואמת לתת-תיקייה בתוך התיקייה של הטבלה. 
זה עוזר לנו לחיפוש יותר מהיר באמצעות שאם Hive מזהה מחיצה המתאימה לשאילתה, הוא יכול להשתמש בPartition Pruning ולקרוא רק את התיקייה הרלוונטית, במקום לסרוק את כל הנתונים מכל השנים.
הTrade-off הוא בעצם חיפוש על שאילתות ספציפיות מהיר קצר לעומד חיפוש על שאילתות יותר כלליות יותר איטי.

### 5. Dedicated MapReduce Exercise: WordCount

Explain how the classic MapReduce WordCount program works from input to final output. Describe the mapper input and output, shuffle and sort, reducer input and output, and which operations run in parallel. Use concrete key/value pairs in your explanation. Then explain why executing a multi-stage Hive query with MapReduce can be expensive and how Tez differs.

משפט דוגמא:  
"אנחנו לוקחים" - Node 1  
את המידע ומעבירים" - Node 2  
"אותו הלאה" - Node 3

שלב ראשון - הפיכת המידע לKeyValuePair

|   |   |
|---|---|
|Value|Key|
|1|אנחנו|
|1|לוקחים|
|1|את|
|1|המידע|
|1|ומעבירים|
|1|אותו|
|1|הלאה|

שלב שני - ערבוב המידע לפי Key לNodes
"אותו אנחנו את" - Node 1
"הלאה המידע" - Node 2
"ומעבירים לוקחים" - Node 3

שלב שלישי - ספירת המידע פנים Nodeית
Node 1

| Value | Key   |
| ----- | ----- |
| 1     | אותו  |
| 1     | אנחנו |
| 1     | את    |

Node 2

| Value | Key   |
| ----- | ----- |
| 1     | הלאה  |
| 1     | המידע |

Node 3

| Value | Key      |
| ----- | -------- |
| 1     | ומעבירים |
| 1     | לוקחים   |

שאילתת Hive מורכבת עשויה לבצע JOIN, לאחר מכן GROUP BY ולבסוף פעולת צבירה נוספת - כאשר פעולות אלו דורשות מספר משימות MapReduce נפרדות, כל משימה עלולה להוסיף המתנה בין שלבים וכתיבה וקריאה של נתוני ביניים מהאחסון.
Tez מאפשר להריץ שאילתה כDAG של משימות עיבוד.  
הוא מחבר שלבים בצורה גמישה יותר, יכול לעשות שימוש חוזר במשאבי ביצוע ולהימנע מחלק מכתיבות הביניים ומעלויות האתחול המיותרות.
Tez לא מבטל כל כתיבה לדיסק ולא מבטיח שכל שאילתה תהיה מהירה יותר, אך הוא יכול להפחית את העלויות של ביצוע שאילתות מרובות שלבים.

### 6. Fault Tolerance

Research fault tolerance in Hive. Consider failures in the services involved in metadata management, query coordination, distributed execution, and storage. Explain which failures a query can recover from, which failures cause it to fail, and what makes recovery possible.

התאוששות:
1. שכפול נתונים ב־HDFS.
2. ניסיונות חוזרים של משימות - הexecutors יכולים להריץ מחדש משימות שנכשלו בצומת אחר.
3. High Availability - אפשר להגדיר מספר מופעים של Metastore או של HiveServer2, כך שכשל של מופע אחד לא בהכרח יפסיק את השירות.￼
סבילות לתקלות ב־Hive מבוססת על שילוב בין שכפול נתונים, ניסיונות חוזרים של משימות ויתירות של שירותים.  
תקלות נקודתיות בDataNodes או בעיבוד ניתנות לעיתים קרובות להתאוששות אוטומטית.  
לעומת זאת, אובדן כל עותקי הנתונים הדרושים, כשל מתמשך בשירות קריטי או מיצוי ניסיונות ההתאוששות עלולים לגרום לשאילתה להיכשל.
כלומר, ייתכן שהמערכת תמשיך להיות זמינה, אך שאילתה מסוימת שכבר נכשלה תצטרך להישלח מחדש.

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
