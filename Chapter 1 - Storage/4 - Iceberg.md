# Apache Iceberg

Now that you are familiar with the concepts of catalogs and the metastore,
and understand the critical separation between how data is stored versus how it is logically organized,
it is time to move from theory to the practice of the modern data world.

Meet Apache Iceberg – the table format we use as the storage layer in our lakehouse.
designed to solve the consistency and performance "pains" of legacy directory-based systems.

###⏳ Timeline
Estimated Duration: 2 Days
- Day 1: Independent research and deep dive into the foundations of Iceberg.
- Day 2:
  - (Morning): First Q&A.
  - (End of Day): Question Answering & Final Q&A.

### 📚 Resources
Use the resources listed below and practice searching the internet for questions not answered by the provided documentation.
- [Apache Iceberg Official Docs](https://iceberg.apache.org/docs/latest/#documentation)
- [Apache Iceberg Definitive Guide](http://103.203.175.90:81/fdScript/RootOfEBooks/E%20Book%20collection%20-%202024%20-%20F/CSE%20%20IT%20AIDS%20ML/Apache%20Iceberg%20(2024).pdf)
- [Meap Book - Apache Iceberg](./asstes/Architecting_an_Apache_Iceberg_Lakehouse_v3_MEAP.pdf)

### Guide Questions❓
Please use these questions as a guide for your research, dive in, and deepen your understanding of all concepts.

1. What is Apache Iceberg? 
   Explain the problems it solves compared to Hive tables (schema evolution, partitioning, consistency, performance).


Apache Iceberg הוא open table format עבור מאגרי נתונים אנליטיים עצומים.
Iceberg מוסיף טבלאות למנועי חישוב - בהם Spark, Trino, PrestoDB, Flink, Hive וImpala - באמצעות פורמט טבלאות בעל ביצועים גבוהים, הפועל בדיוק כמו טבלת SQL.

לפני Iceberg, נטפליקס הסתמכה במידה רבה על Hive " - 600,000 Hive ו-250 מיליון partitions".
עם זאת, ככל שנפחי הנתונים גדלו למאות PB, נטפליקס נתקלה בכמה אתגרים עם Hive:
חסר בו ACID וRollback.
שינוי partition schemas או עדכון schemas דורשות כתיבה מחדש של כל הטבלה.
בגלל אתגרים אלו, נטפליקס פיתחה את Iceberg, שתוכנן עם ACID, תאימות בין מנועי עיבוד שונים וmetadata layer המספקת תכונות כמו Rollback, schema evolution וpartition evolution...
פורמט הטבלה הציע לנטפליקס את יכולת ההרחבה והגמישות הדרושות כדי לעמוד בקצב דרישות הנתונים.


2. Describe the Apache Iceberg table architecture. 
   Explain metadata files, manifest files, data files, and snapshots and how they relate to each other.


פורמט טבלה: 
Metadata Layer: טבלת Iceberg עוקבת אחר כל data files שלה באמצעות snapshots וmanifestים של metadata המאוחסנים בקבצים יעודיים לשמירת metadata בצורת JSON ששומרים schmas, partition specs וsnapshots.
כל Snapshot בmetadata מצביע לmanifest list, אשר מפנה לקובץ manifest אחד או יותר המפרט data files [זה הdata layer] בפועל.
הקובץ manifest לא רק יצביע לdata files אלא גם ישמור סטטיסטיקות על הקבצים שהוא מחזיק ומידע על הpartitions של הקבצים.
כאשר רוצים להוסיף מידע, נכתוב data files חדשים, ניצור manifest חדש שיצביע אחרי הקבצים האלו, manifest list חדש שיצביע אחרי כל הmanifestים הקיימים וmetadata file שיצביע על קבצי הmanifest list הקיימים בכדי לשמור גרסאות וכי כל הקבצים בmetadata layer, כלומר, הכל חוץ מהdata files הם Immuntable.



3. What is an Iceberg catalog, and what is its role? Explain what a catalog manages (table namespace, metadata pointers, commits), why it’s required, mention common catalog implementations, and explain how it differs from the Hive Metastore implementation. Describe how catalogs and formats enable multiple compute engines to work on the same data.


Iceberg Catalog מספק גישה לטבלאות Iceberg באמצעות שמות, ומתאם את פרסום השינויים בטבלאות.
תפקידיו העיקריים הם תרגום מזהה טבלה לmetadata העדכניים שלה, ותמיכה בביצוע atomic commits.
הimplementation guide של קטלוג Iceberg מתאר פעולות אלו כחילוץ המיקום של הmetadata, ועדכון מיקום זה באופן אטומי.
Table namespace - מתאים בין שם למיקום פיזי של טבלה
Metadata pointers - מוודא שהpointer לטבלה מצביע על קובץ הmetadata הכי עדכני
Atomic commits - פעולות קורות בצורה מידית, והקטלוג מוודא שהם לא קורות באותו הזמן.
Common implementations: Apache Polaris, Unity Catalog, Apache Lakekeeper, and Apache Gravitino ובגלל שכולם משתמשים בIceberg REST Catalog Specification אז ניתן להחליף אותם אחד בשני בלי לכתוב מחדש את כל הטבלאות.
Iceberg Catalog
Hive Metastore


ממשק המאפשר למנועי שאילתות לאתר ולנהל טבלאות Iceberg.
הוא יכול להשתמש במערכות backends שונות, כגון שרת REST או Hive Metastore.
שירות metadata המאחסן רישומי טבלאות, schemas ומיקומי אחסון.
Purpose
מגדיר כיצד מנועים מתקשרים עם הקטלוג.
שירות שיכול לשמש כמימוש של iceberg catalog.
Difference

הם יכולים לפעול יחד: קטלוג Iceberg מבוסס-REST יכול להשתמש ב-Hive Metastore כמערכת האחורית שלו.

Multiple compute engines עושים שימוש בIceberg catalog משותף, כלומר, שפעולות קריאה וכתיבה מתואמות דרך הcatalog, כך שהengines רואים את המצב העדכני ביותר שעבר commit, דבר המאפשר להם לחלוק data layer משותף ולעשות process באותו הזמן.


4. How does Iceberg handle concurrent reads and writes? 
  Explain snapshot isolation, atomic commits, optimistic concurrency control, and conflict detection.


שימוש בIceberg catalog משותף, פעולות קריאה וכתיבה מתואמות דרך הcatalog, כך שהengines רואים את המצב העדכני ביותר שעבר commit, דבר המאפשר להם לחלוק data layer משותף ולעשות process באותו הזמן.

הבעיה: שאילתה עלולה להתחיל, ובאמצעה, הETL תתחיל לשנות מחיצות.
פעולה זו תגרום לשאילתה להיכשל עם שגיאה, או, תגרום לה לקרוא שילוב של נתונים ישנים וחדשים.
הפתרון: Snapshot Isolation -  כאשר שאילתה מתחילה, המנוע ננעל על הsnapshot הנוכחי של הטבלה.
הוא יראה גרסה עקבית לחלוטין של הטבלה מאותו רגע בזמן למשך כל משך השאילתה.
בינתיים, הETLים יכולים לבצע מספר snapshotים חדשים שלא ישפיעו על הראשון.

Atomic commits - פעולות קורות בצורה מידית, לאחר כל עדכון טבלה והקטלוג מוודא שהם לא קורות באותו הזמן.

Optimistic Concurrency Control, או (OCC) מניח שמספר עסקאות יכולות להסתיים לעתים קרובות מבלי להפריע זו לזו, כלומר, אם מספר משימות מנסות לכתוב לאותה טבלה בו זמנית, אף אחת מהן לא נחסמת, אך כל אחת מהן בודקת התנגשויות לפני ביצוע הcommit ואם נמצאת התנגשות, הכותב פשוט מנסה שוב את הפעולה שלה.

Conflict detection קורה כאשר כותב אחר מעדכן את הmetadata של הטבלה, למשל, על ידי הוספת קבצים חדשים או נתונים סטטיסטיים, מבלי לגעת באותם קבצי data - מצב שניתן לפתור באופן אוטומטי על ידי רענון הmetadata וביצוע חוזר של הcommit.
או כאשר שני כותבים משנים את אותם קובצי data או partitions.
במקרים אלה יהיה צורך בעשייה מחדש של הכתיבה.
הגרסא שתישאר היא הגרסא ששנת את הsnapshot ראשונה בcatalog.
ניתן לצמצם את כמות הפעמים שזה קורה באמצעות הוספת Partial Progress שגורם לcommitים לקרות באמצע הכתיבות המאוד ארוכות.



5. What maintenance operations does Iceberg require, and why? 
   Discuss compaction, snapshot expiration, orphan file cleanup, and metadata cleanup.


Snapshot Expiration:
כל כתיבה לטבלת Iceberg יוצרת snapshot חדש של טבלה.
ניתן להשתמש בsnapshot לשאילתות time travel, או שניתן לעשות recall.
עם זאת, snapshots אלו מצטברות ויש לנקות אותן.

Metadata Cleanup:
Iceberg עוקבת אחר metadata של טבלה באמצעות קבצי JSON.
כל שינוי בטבלה מייצר קובץ metadata חדש כדי לספק אטומיות.
טבלאות עם פעולות commit רבות, כמו אלו שנכתבות על ידי משימות streaming, עשויות להזדקק לניקוי קבצי metadata באופן קבוע.

Orphan Files:
בDistributed Processing Engines, כשלים במשימות או בעבודות עלולים להשאיר קבצים שאינם מופנים על ידי metadata של טבלה, ובמקרים מסוימים ייתכן שתפוגת snapshots רגיל לא תוכל לקבוע שקובץ אינו נחוץ עוד ולמחוק אותו.
צריך למחוק גם אותם.

Data Files Compactions:
Iceberg עוקבת אחר כל קובץ נתונים בטבלה.
קבצי data רבים יותר מובילים לmetadata רבים יותר המאוחסנים בקבצי manifest, וקבצי data קטנים גורמים לכמות מיותרת של metadata ולשאילתות פחות יעילות עקב עלויות פתיחת קבצים.
אז ניקח את הקבצי data ונאחד אותם לקבצים יותר גדולים - בערך כ100MB.


שאלות סקילה 1:

מה קורה בrepartitions
מכיוון שהpartitions נשמרות בקובץ הmanifest, הrepartitioning (הpartiiton evolution) מתבצע פשוט על ידי DROP PARTITION הקיימת וADD PARTITION חדשה המבוססת על השדה החדש - וזאת אך ורק עבור קבצים חדשים (לא ניתן לבצע זאת עבור נתונים קיימים ללא כתיבה מחדש שלהם).

הבדלים בין סטטיסטיקות בHive ובIceberg
Hive statistics:
מספר שורות, מספר קבצים, גודל בbytes
Iceberg Manifest statistics:
פורמט הקובץ, partition scheme, ערכי המינימום/מקסימום, הcount וערכי ה-null עבור העמודות בקובץ נתונים.

מה ההבדל במבנה הכללי של Iceberg מהמבנה הכללי של Hive בגישה לטבלה
Iceberg מטפלת בpartitioning בצורה אוטומתית, נמנעת באופן אוטומטי מקריאת מחיצות מיותרות, למשתמשים אין צורך לדעת כיצד הטבלה מחולקת למחיצות, ואין עליהם להוסיף filterים נוספים לשאילתות שלהם.
מבני המחיצות בIceberg יכולים להתפתח ולהשתנות בהתאם לצורך.

איזה בעיות Iceberg פותר
הם נדרשו לנהל PBs של טבלאות בdata lake, תאימות בין מנועי עיבוד שונים וmetadata layer המספקת תכונות כמו Rollback, schema evolution וpartition evolution.

איזה פורמט הם manifest files
Metadata file - similar to JSON

להסתכל על סוגי הקבצים בmetadata layer
https://vutr.substack.com/p/i-spent-7-hours-diving-deep-into

בכתיבה, איך נראה file metadata חדש
הדבר ייצור קובץ metadata חדש שיצביע על כל הsnapshotים, אך הcatalog יצביע רק על קובץ הmetadata החדש.

מה זה cow
כאשר מעדכנים קובץ נתונים, Iceberg כותבת מחדש את הקובץ כולו.
פעולה זו אינה יעילה, אך היא משרתת מטרה ספציפית: שמירה על קובצי נתונים שלמים המשקפים את המצב העדכני, וביטול הצורך של שאילתות קריאה לבצע פעולות התאמה (reconciliation) או מיזוג כלשהן.

מה זה mor
בעת עדכון רשומה, Iceberg יוצר delete file, המציין: "יש להתעלם מרשומה זו בעת הקריאה", וכותב לקובץ הנתונים החדש רק את השינויים עצמם.
שיטה זו מאיצה באופן משמעותי את פעולות הכתיבה.אבל, בעת ביצוע שאילתה על הנתונים, על Iceberg לבדוק את delete files אלו ולמזג את השינויים עם הנתונים המקוריים, כדי להציג את התמונה העדכנית של הנתונים שלכם.

מה הצורות שאפשר למחוק בהם מידע בIceberg
MOR, COW

תהליך מחיקה בIceberg
Exactly like editing, but either using COW or MOR

מה זה PUFFIN FILES
קבצים שבהם נשמור סטטיסטיקות על טבלאות, כמו כמה ערכים uniq יש בטבלה
משמשים בהם כדי לדעת כמה שורות יש בטבלה כדי לעשות Joinים בצורה יותר טובה [קובץ קטן לקובץ גדול]

איך נראה הcatalog בHive Metastore
External Hive Table

איך השימוש בHive Metastore שונה מהשימוש שלו בIceberg
משמש לאחסון metadata של טבלאות לעומת משמש לאחסון מיקומי טבלאות

באיזה DB משתמשים בשביל הIceberg Catalog
זה תלוי במימוש: JDBC יכול לעבוד עם כל RDBMS, הAWS Glue משתמש בS3, Hive מבוססים HMS וקטלוגים REST עושים שימוש במערכת הקבצים שעליה הם יושבים.

באיזה שרת פונים בRestCatalog
אין פאקינג שרת, הם פונים לקטלוג עצמו

הבדלים בין JDBC Catalog, REST Catalog וHive Metastore server
REST Catalog - several engines or languages need a shared interface.
Hive Catalog - Saved as an external Hive table
JDBC Catalog - Saved as a relational DB [ex - MySQL]
Amazon Glue Catalog - S3

שאלות סקילה 2:

איפה הpuffin files נמצאים
בתוך הdata layer

יתרון שיש לIceberg על Hive מעל S3 - בקשר list
בHive צריך לעשות LIST לכל הs3 ולמצוא את כל הקבצים הרלוונטים לטבלה לעומת בIceberg שאפשר למצוא רק את הmetadata file באמצעות הcatalog ומשם למצוא ביותר קלות את כל קבצי הטבלה.

מה השמות של סוגי delete files
Positional - מחיקה לפי מיקום; Equality – מחיקה לפי ערך

איך מגדירים אם להשתמש בcow או mor ואיפה
write.delete.mode, write.update.mode, write.merge.mode בcatalog

איפה delete files נשמרים
כpuffin files בdata/deletes.puffin/ [בmanifest]

מה זה Data File Compaction
אז ניקח את הקבצי data ונאחד אותם לקבצים יותר גדולים - בערך כ100MB.

איך מטריגים כל אופטימיזציה
Table tb = SparkActions.get().expireSnapshots(tb).expireOlderThan(tsToExpire).execute(); 

Old metadata files cannot be deleted manually and only with write.metadata.delete-after-commit.enabled=true

Table tb = SparkActions.get().deleteOrphanFiles(tb).execute();

Table tb = SparkActions.get().rewriteDataFiles(tb).filter(Expressions.equal("date", "2020-08-18")).option("target-file-size-bytes", Long.toString(500 * 1024 * 1024)).execute();

לעבור על כל האופטימיזציות שוב
Snapshot Expiration: כל כתיבה לטבלת Iceberg יוצרת snapshot חדש של טבלה.
עם זאת, snapshots אלו מצטברות ויש לנקות אותן.
Metadata Cleanup: טבלאות עם הרבה שינויים, עשויות להזדקק לניקוי קבצי metadata ישנים באופן קבוע.
Orphan Files: בDistributed Processing Engines, כשלים במשימות או בעבודות עלולים להשאיר קבצים שאינם מופנים על ידי metadata של טבלה, וצריך למחוק אותם.
Data Files Compactions: ניקח את הקבצי data ונאחד אותם לקבצים יותר גדולים.

מה זה RemoveOrphanFiles
בDistributed Processing Engines, כשלים במשימות או בעבודות עלולים להשאיר קבצים שאינם מופנים על ידי metadata של טבלה, ובמקרים מסוימים ייתכן שתפוגת snapshots רגיל לא תוכל לקבוע שקובץ אינו נחוץ עוד ולמחוק אותו.
צריך למחוק גם אותם.

לדרג סדר פעולות אופטימיזציה לפי יעילות (יעילות יעני יהיה יותר טוב להריץ אחד אחרי השני) - ולהסביר
Delete Orphan Files - They are a burden and can be deleted without any of the other files being hcanged
Compact Data Files - In order for there to be less manifest files in total, there needs to be a reduction in the amount of data files.
Manifest Rewriting - Same for compact data files reason but about manifest lists.
Expire Snapshots - Exact same explanation
Remove Old Metadata files - bla bla bla.

איך לעשות Recovery לmetadata בHDFS\S3
לא נכון - RewriteDataFiles יכול לכתוב מחדש לפי הcatalog והטבלה
בHDFS אפשר להשתמש בsnapshots ישנים בכדי לשחזר ובS3 נשתמש בshards.

איך לרשום טבלה לIceberg אחרי שעשית לה DROP
drop_backup - the original table will be retained as backup if configured

מה יש בDB של catalog 
Table name, namespace name, and filepath.

מה עושים עם catalog נמחק
REGISTER tables/WRITE files

מה הcatalog הממומש - ליים
REST adapter

להסתכל על הDB - ליים
Tablename, tablenamespace, filepath
יש גם DB נוסף של attributes ששם ניתן לראות איזה טבלה אנחנו בה

שאלות סקילה 3:

איזה DB זה - ליים
Postgress

איזה סוג קובץ הוא manifest
AVROOOOOOOOOOOOOOOOOOOOOOO

Types of delete files: 
Positional Delete Files: Store the exact location of deleted records in specific files.
Equality Delete Files: These store the values of deleted records, a description of what to remove.

איפה אני מגדיר אם טבלה היא mor/cow
CREATE TABLE catalog.people ( id int, first_name string, last_name string ) TBLPROPERTIES ( 'write.delete.mode'='copy-on-write', 'write.update.mode'='merge-on-read', 'write.merge.mode'='merge-on-read' ) USING iceberg; 
או
ALTER TABLE catalog.people SET TBLPROPERTIES ( 'write.delete.mode'='merge-on-read', 'write.update.mode'='copy-on-write', 'write.merge.mode'='copy-on-write' ); 

איפה delete files נשמרים
בdata layer

איזה Compactions יש


מה זה bin-pack, sort, z-order compactions
binPack
compaction טהור - כתיבת קבצים קטנים לקבצים גדולים, ללא תלות בסדר הרשומות.
Sort
compaction תוך מיון הרשומות לפי שדה אחד או יותר.
zOrder
Sort compaction אבל הענקת משקל שווה לכל השדות לפיהם מתבצע המיון.

מה זה manifest compactions
Iceberg משתמש בmetadata בmanifest list ובmanifest files שלו כדי להאיץ את תכנון השאילתות ולגזום קבצי נתונים מיותרים.
Manifest files נדחסים אוטומטית לפי סדר הוספתם, מה שהופך את השאילתות למהירות יותר כאשר תבנית הכתיבה מתיישרת עם מסנני קריאה.
כאשר תבנית הכתיבה של טבלה אינה מתיישרת עם תבנית השאילתה, ניתן לכתוב מחדש את הmetadata כדי לקבץ מחדש data files לmanifest באמצעות rewriteManifests.

### 🔄 Alternatives
Assignment: You are required to research and write a comparative analysis between Iceberg and an industry alternative.
- Deliverable: A written summary (minimum 1 or 2 sentences).
- Add real life usecase 
- Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
- Goal: You must be able to justify why the department uses this tool for our specific environment.

### 🎯 User Story & Scenario
Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.
- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.
