# Spark Fundamentals

## Overview
This is a self-study day on the fundamentals of **Apache Spark** — the compute layer of our datalake platform.

**You'll focus on general concepts: Spark's architecture and execution model, planning & optimization, shuffle & joins, memory management, and how Spark is configured and tuned in our environment (PySpark on Kubernetes).**

The goal is not to memorize definitions. For each concept, aim to explain the **big picture in your own words** and connect it to the others — in the oral exam you'll be asked to reason, not recite.

## Goals
- Build a foundational mental model of how Spark **plans and executes** a job.
- Learn the core terminology (Driver, Executor, Job/Stage/Task, DAG, Shuffle, Catalyst, partition…) well enough to use it fluently.
- Understand how Spark **manages memory** and how it's **configured** — especially in a multi-tenant, PySpark-on-Kubernetes setup.
- Practice planning a self-study day and estimating your own learning time.

:warning: **Note:**
- This is a self-study day. Independence and time management are essential.
- Many newcomers struggle with self-study; take a moment to plan your day and stick to it.
- Understand the **big picture** of each concept. If you can't explain it, you probably haven't learned it.
- Be prepared to describe how concepts relate to one another and to real-world scenarios.
- Skim the [assignments](#-alternatives) and the exercise in Core Concept 1 before diving in, so you know what to focus on.
- When in doubt about what you need to learn, ask your mentor.

### Core Concepts

Think through the following. Treat them as a **rough map of the territory**, not a checklist — they point you at the areas to research, and in the oral exam the examiner will drill deeper into each. If you've truly done the research you'll be able to follow those deeper questions; if you only skimmed the outline, it will show.

1. **Spark Architecture & Execution:** What are the main components of Spark, and what is the role of each? Where can the Driver and Executors run, and what does `spark-submit` do? What is the difference between a transformation and an action? What is lazy execution in Spark? What happens between calling an action and work running on the executors — how does the work break down, and what causes those boundaries? What is a DAG, and how does Spark use it, both to schedule work and to achieve fault tolerance? What is the difference between `SparkContext` and `SparkSession`? Go over [this file](assets/where_do_i_run.py) and, for each line, comment on where it runs.

שלושת הרכיבים העיקריים הם הSpark Driver, הSpark Executor והCluster Manager.
הDriver הוא הmaster, בעוד שהExecutor הוא הslave ביחסי master-slave.
האפליקציה מתקשרת עם הDriver באמצעות סשן; לאחר שהDriver מבין וממטב את השאילתה, הוא מפצל אותה לTaskים ומקצה אותן לExecutorים.
הDriver מחלק את כל הנתונים שניתנו לכל Task לפני הקצאת הTask; אם Task תיכשל, הDriver יצטרך להקצות מחדש את הTask לExecutor אחר.
הDriver מתכנן Task ומוודא שהיא מבוצעת; עם זאת, לעתים רחוקות הוא ייגע בנתונים עצמם.
ה-Executor יכול לעבד מספר Taskים במקביל - מספר Taskים כמספר הCPU Cores שיש ל-Executor.
Data Shuffle מתרחש כאשר מספר Executors מערבבים את הנתונים ביניהם כדי להפוך את הTaskים שלהם ליעילות יותר; זה קורה גם לאחר שכל הTaskים מסיימות לפעול במקביל, ואם יש תוצאה [כלומר, צפוי פלט], היא נשלחת חזרה ל-Driver. איסוף כל הנתונים המתקבלים מכל ה-Executors לתוך Executor אחד הוא גם Task, וביצוע כל פעולה על נתונים אלה הוא Task.
סקריפט ה-spark-submit משמש להפעלת יישומים בCluster.
Cluster Manager הוא יישום המספק את המשאבים לביצוע, וזה יקרה בדרך כלל מתחת למכסה המנוע.
Cluster Manager הוא בדרך כלל K8S, YARN, standalone או Mesos.
ה-Driver וה-Executor יכולים לפעול ב-3 deployment modes:
1. Local deployment mode - הDriver ו-Executor במחשב שלי
2. Client Deployment Mode - הDriver במחשב שלי ו-Executors במרכז הנתונים/ענן
3. Cluster deployment Mode - הDriver ו-Executor במרכז הנתונים/ענן
Transformations הן לוגיקה עסקית שאנו רוצים להחיל על הנתונים שלנו; הן עצלניות, כלומר הן לא קורות אלא אם כן Spark צריך לבצע אותן [באמצעות Action].
שני סוגי הTransformations הם: Transformations צרות - Filter, Select, Create new col, Cast, וTransformations רחבות - Group By, Sort, Join
Actions הן דרישות לתוצאות; אלו הן פעולות שמניעות את החישוב עצמו.
דוגמאות כוללות Collect, Count, Save, Take, Show.
ההבדל הוא באופי הכפייה של Actions לעומת האופי העצל של Transformations.
Lazy Evaluation היא תכונה ב-Spark, אשר מעכבת ביצוע Transformations עד שAction מבוצעת.
לאחר הפעלת Action, Spark יריץ כמה אופטימיזציות על השאילתה שלנו, כמו העברת Transformations כמו filter לנקודה המוקדמת ביותר האפשרית, יישום אופטימיזציות של Catalyst Optimizer, ויישום אופטימיזציות של CPU וזיכרון של Tungsten.
לאחר סיום ה-RDD, ה-Driver מחלק את כל הנתונים שניתנו לTaskים לפני הקצאת הTaskים הללו ל-Executors שבהם הן יפעלו.

3 הStageים הקונקרטיים הם:
1. פתרון הlogical plan
ה-catalyst optimizer מוודא שכל ההפניות שלך הגיוניות - זוהי סדרה של אימותים.
2. אופטימיזציה של הlogical plan שלך
ה-catalyst optimizer מגלה מספר תוכניות לוגיות יעילות, כלומר, מתי לסנן את הנתונים שלך, ומיישם אופטימיזציות אחרות כגון constant folding וpredicate pushdown.
3. תרגום לphysical plan
כיום קיימות מספר optimized logical plans - חלקן אופטימליות יותר מאחרות בהתאם למשאבים שלך.
Spark בוחן את הCluster שלך, מחשב כמה משאבים וזמן ביצוע תוכניות שונות דורשות, ולאחר מכן בוחר את התוכנית היעילה ביותר מבחינת עלות בהתחשב במשאבים הזמינים שלך.
DAG הוא Spark Job שיש לה Stage אחד או יותר, וכל Stage מחולק לTask אחת או יותר.
DAGs הם job - "התמונה הגדולה" בפועל ש- Spark צריכה לבצע. Task יכולה להיות מקבילה או רציפה; Stageים הם רציפים, וTaskים יכולות לפעול במקביל.
דשדוש נתונים הוא גבול בין Stageים.
אנו יכולים להשתמש ב- DAG לfault tolerance מכיוון שאם פעולה כלשהי מתרחשת ופתאום קורס RDD כלשהו, בעזרת Cluster Manager, נזהה את המחיצה ב- DAG שלנו שבה מתרחש האובדן.
הוא משמש גם לתזמון מכיוון שמדובר ב"תוכנית" מכוונת ולא מעגלית [אציקלית].
[לפני Spark 2.0] הSparkContext הוא נקודת הכניסה עבור יישומי Spark.
הוא מייצג את החיבור לcluster של Spark, ואחראי על תיאום וניהול המשאבים הנדרשים לביצוע Taskים.
SparkContext מסייע בהגדרת הסביבה ומשמש כשער לגישה ל-API ברמה הנמוכה (low-level API) של Spark.
[החל מגרסה 2.0 של Spark] הSparkSession מהווה נקודת כניסה מאוחדת לקריאת נתונים, יצירת DataFrames, עבודה עם Spark SQL ושימוש ב-Dataset API.
ה-SparkSession מאגד את הפונקציונליות של SparkContext,‏ SQLContext ו-HiveContext לכדי אובייקט יחיד, ובכך מספק ממשק עקבי ויעיל יותר לעבודה עם Spark.
שני ​​ההבדלים העיקריים ביניהם הם היקף התמיכה ב-API שמציע SparkSession בהשוואה ל-SparkContext, וכן הפישוט של הממשק ב-SparkSession.



2. **Spark Planning & Optimization:** Logical vs. Physical Planning — walk through the transition from Logical Plan to Physical Plan. What is the fundamental difference between Rule-Based (RBO) and Cost-Based (CBO) optimization, and what are the common kinds of optimizations used? What is AQE? Why is running `ANALYZE TABLE` recommended for performant CBO? And what is whole-stage code generation?

המעבר מLogical Planning לPhysical Planning הוא זה:
1. פתרון הLogical Plan שלך
מייעל ה-Catalyst מוודא שכל ההפניות שלך הגיוניות - זוהי סדרה של אימותים.
2. אופטימיזציה של הLogical Plan שלך
מייעל ה-Catalyst מגלה מספר Logical Plans יעילות, כלומר, מתי לסנן את הנתונים שלך, ומיישם אופטימיזציות אחרות כגון logical folding [החלפת קבועים שנשמרו כ-2*3 ב-6 בלבד] וpredicate pushdown [הפיכת המסננים מוקדמים יותר].
3. תרגום לPhysical Plan
כיום קיימות מספר Logical Plans ממוטבות - חלקן אופטימליות יותר מאחרות בהתאם למשאבים שלך.
Spark בוחן את הCluster שלך, מחשב כמה משאבים וזמן ביצוע תוכניות שונות דורשות, ולאחר מכן בוחר את התוכנית היעילה ביותר מבחינת עלות בהתחשב במשאבים הזמינים שלך.
RBO מיישמת קבוצה של כללים מוגדרים מראש כדי למטב את תוכנית השאילתה.
כללים אלה מזהים דפוסים מסוימים בשאילתה ומחליפים אותם בחלופות ממוטבות.
דוגמה: predicate pushdown, logical folding וכו'.
CPO מעריכה את העלות של תוכניות שאילתה שונות על סמך סטטיסטיקות, תפוצה ומשאבים זמינים.
לאחר מכן היא תבחר את התוכנית עם העלות הנמוכה ביותר.
דוגמה: סידור מחדש של צירופים, בחירת אינדקס וכו'.
כדי לאפשר זאת, עלינו להגדיר את spark.sql.cbo.enabled ל-true.
כמו כן, הגדרות בודדות כמו spark.sql.cbo.joinReorder.enabled

אופטימיזציות נפוצות ש-Spark מבצע הן:
* Spark מפזר עיבוד נתונים על פני מספר מבצעים.
חלוקה היא האופן שבו Spark מפזר נתונים, מה שהופך אותה אולי לטכניקת האופטימיזציה הבסיסית ביותר.
* אחסון במטמון והתמדה - עצרו חישוב מחדש של אותו הדבר
* צירופי שידור: ביטול ערבובים יקרים
* צירופים יוצרים צווארי בקבוק בביצועים ביישומי Spark עקב ערבוב נתונים.
* סידור: אופטימיזציה של העברת נתונים
* פורמטים עמודתיים: אופטימיזציה של אחסון ואחזור
* קבצי UDF וקטוריים: האצת פונקציות מותאמות אישית
* שימוש ב-DataFrame API, המספק הזדמנויות אופטימיזציה טובות יותר מאשר RDDs.
* ביצוע ספקולטיבי - ביצוע ספקולטיבי מפעיל משימות גיבוי עבור משימות איטיות, תוך קבלת תוצאות מהמשימות שמסתיימות ראשונות.

AQE מחשב מחדש אופטימיזציות מסוימות [אופטימיזציות מחדש] ממטב השאילתה בעת שינויים גדולים במהלך ביצוע השאילתה.
הפקודה ANALYZE TABLE אוספת סטטיסטיקות אודות טבלה ספציפית אחת או כל הטבלאות במסד נתונים מסוים, אשר ישמשו את ממטב השאילתות כדי למצוא תוכנית ביצוע טובה יותר לשאילתה; סטטיסטיקות אלו מאוחסנות בקטלוג.
יצירת קוד Java בשלב שלם היא אופטימיזציה פיזית של שאילתה ב-Spark SQL אשר משפרת את ביצועי הביצוע של שאילתה על ידי כיווץ עץ שאילתה לפונקציה ממוטבת אחת.



3. **Spark Shuffle & Joins:** Compare the different kinds of joins — when will Spark use each, and how can we tell Spark to prefer one over another? What is join reordering? Why is "broadcasting" considered a high-risk, high-reward optimization? What is a *Narrow* transformation and a *Wide* transformation? Why do some operations require a shuffle? What exactly is written in a shuffle?

Inner Join – זהו סוג הJoin ברירת המחדל ב-Spark SQL.
הוא בוחר שורות שיש להן ערכים תואמים בשתי הטבלאות (או הישויות).


Left Join – מחזיר את כל הערכים מהטבלה השמאלית ואת הערכים התואמים מהטבלה הימנית; אם אין התאמה, יתווסף הערך NULL.
סוג זה מכונה גם Left Outer Join.

Right Join – מחזיר את כל הערכים מהטבלה הימנית ואת הערכים התואמים מהטבלה השמאלית; אם אין התאמה, יתווסף הערך NULL.
סוג זה מכונה גם Right Outer Join.

Full Join – מחזיר את כל הערכים משתי הטבלאות, כאשר בצד שבו אין התאמה מתווספים ערכי NULL.
סוג זה מכונה גם Full Outer Join.

Cross Join – מחזיר את המכפלה הקרטזית של שתי טבלאות.

Semi Join – מחזיר ערכים מהצד השמאלי שיש להם התאמה בצד הימני.
סוג זה מכונה לעיתים Left Semi Join.

Anti Join – מחזיר ערכים מהטבלה השמאלית שאין להם התאמה בטבלה הימנית.
סוג זה מכונה לעיתים Left Anti Join.

Syntax: relation [ Join Type/blank for inner ] JOIN…

Join reordering – תהליך שבו משנים את סדר החיבורים כך שהרכיב הקטן יותר תמיד יחובר אל הרכיב הגדול יותר; זאת במטרה לחסוך במשאבי חישוב.
במקרים של מספר חיבורים, הם יסודרו מחדש על פי אותו עיקרון.

Broadcast Join – סוג של חיבור שבו סט נתונים קטן עובר broadcast לכל ה-Executors.
הדבר מאפשר לבצע חיבור יעיל מול סט נתונים גדול יותר, מבלי לעשות shuffle ברחבי הרשת.
שיטה זו כרוכה בסיכון גבוה, שכן היא פועלת היטב (וללא שגיאות מסוג OOM) רק כאשר הנתונים יכולים להיכנס לזיכרון של כל ה-Executors; עם זאת, היא מציעה תועלת רבה, שכן הביצועים יהיו מהירים הרבה יותר.

Narrow Transformations – מצב שבו הנתונים הדרושים לחישוב הרשומות בpartition מסוימת של הparent RDD נמצאים כולם במחיצה אחת בלבד; אין צורך ב-shuffling (העברת נתונים בין צמתים).
Wide Transformations – מצב שבו הנתונים הדרושים לחישוב הרשומות במחיצה מסוימת עשויים להימצא במספר parent partitions – במקרה זה, נדרש ביצוע של data shuffling.
בשלב ה-shuffle, נכתבים שני קבצים עבור כל task:
shuffle_0_X.data    ← כל הpartitions ממשימת הmap מספר X, משורשרות יחד
shuffle_0_X.index   ← הbyte offsets לצורך חיפוש מהיר


4. **Tungsten, Abstractions & Memory:** What is an RDD? Why did Spark move away from RDDs in favor of DataFrames/Datasets? Explain how Tungsten uses off-heap memory to avoid Garbage-Collection pauses. Why is it a bad idea to give one executor a lot of resources (the "Fat Executor" problem)? What is the difference between Execution/Storage memory and overhead memory, and what happens when a task exceeds its allotted execution memory? In PySpark specifically, where does the Python worker's memory live relative to the JVM heap — and why can heavy Python UDFs cause memory trouble the JVM heap won't show? On Kubernetes, how does all of this relate to `memoryOverhead` and to a pod being `OOMKilled`?

RDD - מערך נתונים מבוזר גמיש, כלומר הוא בלתי ניתן לשינוי, וזה עוזר להפוך את Spark לסובלני תקלות; ניתן לתקשר אותו עם הנתונים רק דרך ממשק ה-API של RDD.
הוא הוחלף משום שהוא אינו מאופטם כברירת מחדל ו"קשה לכתוב אותו".
DataFrames - אלטרנטיבה ל-API דמוי SQL ל-RDD, מאופטם על ידי Catalyst Optimizer.
DataSet - מאופטםת עוד יותר, רק עבור Scala, מאופטם גם על ידי Catalyst Optimizer.
Tungsten הוא מאפטם שמייצר קוד מאופטם במטרה לשפר את יעילות המעבד והזיכרון של משימות Spark.
בגלל האופטימיזציות של Tungsten, יש פחות לחץ על GarbageCollector מכיוון שהוא משתמש בניהול Off-heap, מה שמפחית הקצאת אובייקטים קבועה.

Fat Executor הוא מבצע שיש לו משאבים גדולים/מקסימליים; הרעיון הבסיסי של מבצע זה הוא לספק הקצאת משאבים מקסימלית לכל משימה.
למרות שהוא טוב לעומסי עבודה עתירי CPU/זיכרון, הוא גרוע במקביליות, ומגביר את הסיכון לבעיות GC אם הוא גדול מדי.

זיכרון תקורה משמש לפעולות פנימיות של Spark כגון סידור/ביטול סידור של נתונים, מאגרים ברשת לפעולות ערבוב וצרכים אחרים ברמת JVM.

זיכרון ביצוע:
משמש לחישובים פעילים: הפעלת משימות, ערבוב (מיון, גיבוב, צבירת נתונים), צירופים וכל חישוב המוגדר בעבודות Spark שלך.
מאגרים לקריאת נתונים ולפעולות ערבוב נמצאים כאן.
זיכרון אחסון:
משמש לאחסון נתונים במטמון: כאשר אתה קורא ל-.cache() או .persist() ב-DataFrame או RDD, מחיצות הנתונים מאוחסנות כאן (ב-RAM כברירת מחדל).
זה מכיל גם משתני שידור.
אחסון במטמון מסייע להאיץ אלגוריתמים איטרטיביים ומערכי נתונים הנגישים לעתים קרובות על ידי הימנעות מחישוב מחדש.
אם זיכרון הביצוע אינו מספיק גם לאחר שאילת נתונים מהאחסון, Spark ישפוך נתונים לדיסק המקומי של הצומת, מה שיוביל לביצועים איטיים יותר עקב תקורה של קלט/פלט.

זיכרון ה-worker של Python הוא מאזור תקורת הזיכרון, וכאשר מגיעה למגבלת הזיכרון, ה-worker מתחיל לכתוב לדיסק.
ייתכן שה-Heap של ה-JVM עצמו תקין, אך הקצאות זיכרון מחוץ לHeap (לoff-heap), תהליכי workers של Python, או ספריות Native, גרמו לקונטיינר לחרוג מהמגבלה שלו.
ב-Kubernetes, הפרמטר `spark.kubernetes.memoryOverheadFactor` קובע כמה זיכרון יוקצה לשימושים שאינם ב-JVM (כגון תהליכי עובד של Python, הפועלים מחוץ ל-Heap). לכן, אם ערך זה נמוך מדי, הדבר עלול לגרום לכך ש-Pods המריצים תהליכי עובד של Python ייתקלו בשגיאת OOM.



5. **Spark Skew, Partitioning & Caching:** What is data skew, and how can it be solved? What is the difference between `repartition(n)` and `coalesce(n)`? What are the Spark `StorageLevel`s? What is the difference between `cache` and `persist`? Why are UDFs (especially in Python) bad, and how does Spark address the serde bottleneck with UDFs?

Data Skew הוא כאשר מעבדים מערך נתונים ב-Spark, מקבצים את הנתונים לפי מפתח, כל מחיצה צריכה להיות שווה בערך בגודלה, אולם, אם מופע אחד של המפתח מופיע בתדירות גבוהה בהרבה, הנתונים המשויכים למפתח זה עלולים להגיע למחיצה אחת, מה שמוביל לחוסר איזון.

זה גורם ל-3 בעיות:
1. יצירת נחשלים - משימות שמעבדות מחיצות גדולות יותר יהיו איטיות יותר.
2. חוסר איזון במשאבים - חלק מהצמתים באשכול עשויים להיות מנוצלים פחות או יותר בעוד שאחרים עמוסים.
3. שגיאות של Out of Memory - מחיצות skewed עשויות לדרוש יותר זיכרון מהזמין.

הפתרונות:
Salting - הוספת רכיב אקראי למפתחות הskewed, יצירת מפתחות ייחודיים מרובים כדי לפזר את הנתונים בצורה שווה יותר על פני המחיצות.
פיצול Skewed data - זיהוי המפתחות הskewed ועיבודם בנפרד. טכניקה זו מאפשרת לך לטפל בנתונים הskewed מבלי להשפיע על שאר מערך הנתונים.
הגדלת מספר המחיצות - על ידי הגדלת מספר המחיצות, תוכל לפזר את הנתונים בצורה שווה יותר על פני האשכול, ולהפחית את העומס על כל מחיצה בודדת.

הטרנספורמציה repartition(N) משמשת להגדלה או להקטין את מספר המחיצות ב-DataFrame ל-N.
יתרונות:
* חלוקת נתונים שווה: מכיוון שהיא מערבבת את כל הנתונים, repartition() נוטה ליצור מחיצות חדשות בגודל שווה בערך.
חסרונות:
* יקר: הפעולה המלאה הופכת אותה לפעולה עתירת משאבים וגוזלת זמן.

טרנספורמציה coalesce(N) משמשת בעיקר להפחתת מספר המחיצות ב-DataFrame ל-N.
יתרונות:
* מהיר יותר להפחתת מחיצות: מהיר משמעותית מ-repartition() כאשר המטרה היא רק להקטין את ספירת המחיצות.
חסרונות:
* יכול להוביל למחיצות לא אחידות: מכיוון שהוא ממזג מחיצות קיימות ללא ערבוב מלא, אם המחיצות המקוריות היו לא אחידות בגודלן, המחיצות המאוחדות עשויות גם הן להיות לא אחידות. זה יכול להשפיע על פעולות עוקבות אם הן רגישות להטיית נתונים.
* בעיקר עבור הקטנת מחיצות: האופטימיזציה העיקרית שלו זורחת כאשר shuffle=False (ברירת המחדל) ואתה מצמצם מחיצות.

StorageLevel הוא flag המלווה כל RDD; הוא רושם האם להשתמש בזיכרון, האם לשחרר את ה-RDD לדיסק אם הוא נופל מהזיכרון, האם לשמור את הנתונים בזיכרון בפורמט סידורי ספציפי ל-Java, והאם לשכפל את מחיצות ה-RDD על צמתים מרובים.

פונקציות מוגדרות משתמש הן שגרות הניתנות לתכנות על ידי המשתמש הפועלות על שורה אחת.
הם גרועים בפייתון בגלל שהפונקציות המובנות של Spark:
* רצות בתוך ה-JVM
* וקטוריזציה
* אופטימיזציה על ידי Catalyst
* נהנות מיצירת קוד
* תומכות בדחיפה למטה של פרדיקטים
* גיזום עמודות מיותרות
וUDFים של python:
* שוברים את כל האמור לעיל
* מאלצים את Spark לבצע סדרה של כל שורה
* שולחים אותה ל-worker של פייתון
* מחכים שפייתון תסיים
* מבצעים סדרה של הפלט שוב
* שולחים אותו בחזרה
* חוזרים על זה מיליוני פעמים
אז הם גרועים 😔
פתרון: כתבו את ה-UDF בפונקציות Spark מקוריות.


6. **Configuration & Tuning:** What configs would you expect to set for a typical job, and how do they shape its parallelism and memory? What is dynamic allocation, and what does it rely on (keeping in mind there is no external shuffle service on Kubernetes)? When the same setting is defined in more than one place — in the SparkSession, injected by Airflow, and in `spark-defaults` — how does Spark decide which one wins, and which settings can't be changed once the application has started? If a tenant sets a config and it seems to have no effect, how would you investigate — and how do you check what configuration a running application actually has?

הגדרות חשובות:
* spark.executor.memory: מגדיר את הזיכרון עבור כל תהליך executor. spark.driver.memory: מציין את כמות הזיכרון עבור תהליך ה-driver. 
* spark.executor.cores: מגדיר את מספר הליבות עבור כל תהליך executor. 
* spark.driver.cores: מגדיר את מספר הליבות עבור תהליך ה-driver. 
* spark.default.parallelism: מציין את רמת המקביליות (parallelism) כברירת מחדל. 
* spark.executor.instances: מציין את מספר מופעי ה-executor. 
* spark.yarn.am.cores: מציין את מספר הליבות עבור ה-Application Master ב-YARN. 
* spark.yarn.executor.memoryOverhead: מציין את הזיכרון הנוסף (overhead) עבור כל executor ב-YARN. 
* spark.yarn.executor.cores: מגדיר את מספר הליבות עבור כל executor ב-YARN. 
* spark.yarn.maxAppAttempts: מציין את המספר המרבי של ניסיונות הרצה עבור יישום ב-YARN. 
* spark.yarn.queue: מציין את התור (queue) עבור היישום ב-YARN. 
* spark.dynamicAllocation.enabled: מאפשר/מבטל הקצאת משאבים דינמית. 
* spark.dynamicAllocation.minExecutors: מגדיר את המספר המזערי של executors עבור הקצאה דינמית. 
* spark.dynamicAllocation.maxExecutors: מגדיר את המספר המרבי של executors עבור הקצאה דינמית. 
* spark.sql.shuffle.partitions: מציין את מספר המחיצות (partitions) עבור פעולות shuffle ב-SQL. 
* spark.shuffle.spill: מאפשר/מבטל העברת נתונים לדיסק (spilling) במהלך פעולות shuffle. 
* spark.shuffle.spill.compress: מאפשר/מבטל דחיסה של נתונים המועברים לדיסק במהלך פעולות shuffle. 
* spark.driver.maxResultSize: מגדיר את הגודל המרבי של תוצאות שה-driver יכול לצבור לפני שחרורן. 
* spark.executor.heartbeatInterval: מציין את המרווח הזמני עבור אותות "פעימת לב" (heartbeats) בין ה-executor לבין ה-driver. 
* spark.network.timeout: מגדיר את זמן הקצוב (timeout) לתקשורת רשת בין צמתים (nodes).


Spark מספק מנגנון להתאמה דינמית של המשאבים שהיישום שלך צורך, בהתאם לעומס העבודה. משמעות הדבר היא שהיישום שלכם יכול להחזיר משאבים לאשכול (cluster) כאשר אינם בשימוש, ולבקש אותם שוב במועד מאוחר יותר, בעת הצורך. תכונה זו שימושית במיוחד כאשר מספר יישומים חולקים משאבים באשכול ה-Spark שלכם.
תכונה זו מושבתת כברירת מחדל, והיא זמינה בכל מנהלי האשכולות הפועלים במודל "גרגור גס" (coarse-grained) – כלומר: במצב Standalone, במצב YARN, במצב Mesos (במודל גרגור גס) ובמצב Kubernetes (K8s).


Standalone – מנהל אשכולות פשוט המגיע כחלק מ-Spark, ומקל על הקמת אשכול.
Apache Mesos – מנהל אשכולות כללי, המסוגל להריץ גם Hadoop MapReduce ויישומים מסוג שירות (service applications). (נחשב למיושן/Deprecated).
Hadoop YARN – מנהל המשאבים ב-Hadoop 3.
Kubernetes – מערכת בקוד פתוח לאוטומציה של פריסה, התאמת קנה מידה (scaling) וניהול של יישומים המבוססים על מכולות (containers).


ל-Airflow יש את העדיפות הגבוהה ביותר, אחריו מגיע ה-SparkSession, ולבסוף ה-spark-default – ככל שההגדרה ספציפית יותר, כך גוברת יכולתה לדרוס הגדרות אחרות.
לא ניתן לשנות את ה-SparkSession במהלך ריצת היישום.


אם הוגדרה תצורה כלשהי, יש לוודא תחילה מול ה-tenant (הישות המשתמשת) שההגדרה אכן נשמרה, ולאחר מכן לבדוק האם היא נדרסה על ידי אחת משלוש האפשרויות שהוזכרו.



### Real-World Context
Rather than focusing on one technology in isolation, think about how these ideas show up across distributed processing frameworks — how other engines handle the same problems, and what the *core concepts* of distributed processing are.

## :arrows_counterclockwise: Alternatives

Assignment: research and write a short comparative analysis between Spark and an industry alternative.

- **Deliverable:** a written summary (a sentence or two).
- **Focus:** compare performance, architecture, and the specific "pain points" Spark solves. Cover **Trino** specifically — it's the ad-hoc / analytical query engine that sits alongside Spark in our datalake — and, for historical context, how Spark improved on **MapReduce**.
- **Goal:** be able to justify **when we reach for Spark vs. Trino** in our environment — and when you would *not* use Spark at all.

## :dart: User Story & Scenario

Assignment: based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.

- **Deliverable:** a written example/story (~two sentences).
- **Requirement:** describe a real-world scenario (e.g. a specific client requirement) where Spark is the optimal solution.

## Wrapping Up :trophy:
Discuss your answers and any areas of confusion with your mentor. Reflect on how these general concepts will help when you later write code and support clients.

## Additional Topics from Review
- A deeper dive into Spark internals: what other optimizations does Spark implement? How does Spark's memory allocation work end to end?
- What other well-known processing frameworks exist? Which use cases does Spark fit — and when should you *not* use it?

## Action Items
- Review your notes and identify topics you want to explore deeper.
- Collect a list of real-world use cases for Apache Spark.
- Prepare questions for the upcoming mentor Q&A session.

## Recommended Resources
- [Apache Spark Documentation](https://spark.apache.org/documentation.html)
