# Airflow Fundamentals:
## Overview
This section will go over the fundamentals of _`Apache Airflow`_, consisting of the client side, and the backend.

**We will focus on general concepts of Airflow, the flow of the tasks and how does client code look like.**

## Goals
- Master the fundamental Airflow abstractions and authoring models.
- Understand the core backend architecture, the responsibilities of each component, and how they evolve from Airflow 2 to Airflow 3.
- Trace the end-to-end lifecycle of a `Dag` and `TaskInstance`, from code parsing and `Dag` synchronization (including `DAGBundles`) to `Scheduler` critical loops and `Worker` execution.
- Evaluate the mechanics of data and state passing, distinguishing between metadata sharing, global configuration, and resource-efficient patterns.
- Compare Airflow’s orchestration approach against industry alternatives to justify its usage in production data pipelines.

### :warning: **Note:**
- This is a self-study day. Independence and time management are essential.
- Many newcomers struggle with self-study; take a moment to plan your day and stick to it.
- Understand the **big picture** of each concept. If you can't explain it, you probably haven't learned it.
- Be prepared to describe how concepts relate to one another and to real-world scenarios.
- When in doubt about what you need to learn, ask your mentor.

### Core Concepts

Think through the following questions; by answering them you’ll touch every major topic listed above:


1. **Airflow User API & Concepts:** Explain the difference between a DAG and a DagRun? How do tasks share small metadata versus global configuration? What is Jinja Templating, and why would you use {{ ds }} instead of Python's datetime.now()? Contrast the TaskFlow SDK with Classic Operators. How does the TaskFlow SDK handle XComs differently than the old xcom_pull method? What are Assets? What types of Operators exist? Why is it not recommended to run any time consuming code in top level dag code? How does this affect the DAG Processor's performance? What is a Hook? what is the connection between Hooks, Connections and Operators?

DAG Run הוא אובייקט המייצג מופע של ה-DAG בזמן.
XCom הוא שכבת אחסון קטנה בתוך המטא-דאטה של Airflow שבה משימות יכולות להשאיר ערכים עבור משימות אחרות לאסוף.
משתנים הם מושג תצורת זמן הריצה של Airflow - מאגר מפתחות/ערכים כללי שהוא גלובלי וניתן לבצע שאילתה עליו מהמשימות שלך, ולהגדיר אותו בקלות דרך ממשק המשתמש של Airflow, או להעלות אותו בכמות גדולה כקובץ JSON.

Jinja הוא מנוע תבניות מהיר, אקספרסיבי וניתן להרחבה. מצייני מיקום מיוחדים בתבנית מאפשרים כתיבת קוד הדומה לתחביר Python.
Airflow ממנף את Jinja Templating, שיכול להיות עוצמתי בשילוב עם פקודות מאקרו.
{{ ds }} הוא משתנה בתבנית, ומכיוון שהפרמטר env של BashOperator בתבנית עם Jinja, תאריך ההתחלה של מרווח הנתונים יהיה זמין כמשתנה סביבה בשם DATA_INTERVAL_START בסקריפט Bash שלך.

TaskFlow דואג להעברת קלט ופלט בין המשימות שלך באמצעות XComs עבורך, כמו גם חישוב תלויות באופן אוטומטי.
זה נותן לך אובייקט המייצג את ה-XCom עבור התוצאה (XComArg) שתוכל להשתמש בו לאחר מכן כקלט למשימות או אופרטורים במורד הזרם.
XComs "נדחפים" ו"נמשכים" במפורש אל/מהאחסון שלהם באמצעות המתודות xcom_push ו-xcom_pull ב-Task Instances.

נכס Airflow הוא קיבוץ לוגי של נתונים. משימות יצרן במעלה הזרם יכולות לעדכן נכסים, ועדכוני נכסים תורמים לתזמון DAGs צרכניים במורד הזרם.

אופרטור הוא מבחינה מושגית תבנית למשימה מוגדרת מראש שניתן פשוט להגדיר באופן הצהרתי בתוך ה-DAG שלך.

BashOperator, PythonOperator, EmailOperator, SimpleHttpOperator, MySqlOperator, PostgresOperator, MsSqlOperator, OracleOperator, JdbcOperator, DockerOperator, HiveOperator, S3FileTransformOperator, PrestoToMySqlOperator, SlackAPIOperator

יש להימנע מכתיבת קוד ברמה העליונה שאינו נחוץ ליצירת אופרטורים ולבניית יחסי DAG ביניהם בגלל החלטת העיצוב עבור מתזמן Airflow וההשפעה של מהירות ניתוח הקוד ברמה העליונה הן על הביצועים והן על יכולת ההרחבה של Airflow.

Hook הוא ממשק ברמה גבוהה לפלטפורמה חיצונית המאפשר לך לתקשר איתה במהירות ובקלות מבלי שתצטרך לכתוב קוד ברמה נמוכה שפוגע ב-API שלה או משתמש בספריות מיוחדות.
לעתים קרובות הם גם אבני הבניין מהן בנויים אופרטורים.
הם משתלבים עם חיבורים כדי לאסוף אישורים, ולרבים מהם יש conn_id ברירת מחדל; לדוגמה, PostgresHook מחפש אוטומטית את החיבור עם conn_id של postgres_default אם לא תעביר אחד.

2. **Airflow Backend & Architecture:** What are the different components in the Airflow architecture? Define the roles of each component. Why is the `Executor` considered a mechanism/logic rather than a standalone service? Explain the `Deferrable Operator`. Which component makes these possible, and how do they save money/resources in a Big Data stack? What are `Airflow Providers`? and what are the main changes between Airflow 3 and Airflow 2?

מתזמן: מטפל הן בהפעלת זרימות עבודה מתוזמנות והן בשליחת משימות למבצע להפעלה.
מבצע: מטפל במשימות רצות. בהתקנת ברירת המחדל של Airflow, פעולה זו מפעילה את כל מה שבתוך המתזמן, אך רוב המבצעים המתאימים לייצור דוחפים בפועל את ביצוע המשימות אל העובדים.
שרת אינטרנט: מציג ממשק משתמש שימושי לבדיקה, הפעלה וניפוי באגים של התנהגות DAGs ומשימות.
תיקיית קבצי DAG: נקראת על ידי המתזמן והמבצע (וכל עובד שיש למבצע).
מסד נתונים של מטא-נתונים: משמש את המתזמן, המבצע ושרת האינטרנט לאחסון מצב.

אופרטורים תופסים משבצת עובד מלאה למשך כל הזמן שהם פועלים, גם אם הם במצב סרק.
אופרטור דחוי הוא אופרטור שנכתב עם היכולת להשעות את עצמו ולשחרר את העובד כאשר הוא יודע שעליו להמתין, ולהעביר את משימת חידושו למשהו שנקרא טריגר. כתוצאה מכך, בזמן שהוא מושעה (נדחה), הוא לא תופס משבצת עובד, ולאשכול שלך יהיו הרבה פחות משאבים מבוזבזים על מפעילים או חיישנים שאינם פעילים.
ניתן להרחיב את היכולות של Apache Airflow על ידי התקנת חבילות נוספות, הנקראות ספקים.

ב-Airflow 2, כל הרכיבים דיברו עם מסד הנתונים של המטא-דאטה, דבר שלא תמיד אפשרי או מאובטח, בהשוואה ל-Airflow 3, שיש לו שירות API עבור מעבדי קבצי DAG, ה-Triggers וה-Workers.
הוא גם הוסיף תזמון מונחה אירועים וניהול גרסאות של DAG.

3. **Airflow Security:** How does the airflow security model look like? both arcihtecture-wise and client-wise? how can I integrate airflow with different authentication backends and types? (as if LDAP or SSO), what are the available permissions that exist in airflow (find place in docs)?

מודל האבטחה של Airflow כולל סוגים שונים של משתמשים עם גישה ויכולות שונות; זו הסיבה של-Airflow יש את סוגי המשתמשים הבאים:
מנהלי פריסה - אחראים כלליים על ההתקנה, האבטחה והתצורה של Airflow - הרמה הגבוהה ביותר.
מחברי DAG - אחראים על יצירת DAGs ושליחתם ל-Airflow.
משתמשי UI מאומתים - משתמשים שיכולים לגשת לממשק המשתמש ול-API של Airflow ולקיים איתם אינטראקציה - הרמה הנמוכה ביותר.
לכן, מחברי DAG כותבים רק קבצי DAG; לקוחות מקיימים אינטראקציה רק ​​עם שרת ה-API, ומנהל הפריסה [Nati] מטפל בכל פריסת Airflow.

{הכנס תמונה פה אחרכך}

ניתן להוסיף SSO/LDAP על ידי הוספת ספק OAuth2 בקובץ airflow.cfg.
ההרשאות הקיימות הן:
can_create
can_read
can_edit
can_delete

4. **Airflow Task Lifecycle:** What is the full flow of a Dag from being written to being run? What happens when the `Dag Processor` encounters your file? How is `Jinja` parsing different in Dag processing than execution time? At which state does the `Scheduler` stop managing the task, and hand it over to the `Executor`? What is the flow when a task gets to a `Worker`? When does it start running?

אתה כותב את קובץ הפייתון עם ה-DAG בפנים; מעבד ה-DAG קורא אותו, מבצע סדרה שלו, ומכניס אותו למסד הנתונים של המטא-דאטה; המתזמן מבצע סריקה במסד הנתונים כדי לבדוק אם ה-DAGRun אמור להתבצע; ה-executor מקצה משאבים למשימות בתור, ולאחר מכן ה-worker מבצע את ה-DAG.

מעבד ה-DAG מעביר תת-תהליך כדי להריץ את סקריפט הפייתון שלך ומעביר סדרה של מפת המשימות המתקבלת למטמון מסד נתונים, וזה מה ששרת האינטרנט וה-Scheduleur קוראים ממנו.

תבניות Jinja נשארות כמחרוזות גולמיות ולא מעובדות במהלך זמן הניתוח מכיוון שהקשר זמן הריצה עדיין לא קיים, והן מעובדות על ידי ה-worker בזמן הביצוע רק אם הן שייכות לשדות תבנית מוצהרים.

ה-Scheduleur מעביר משימה מתוזמנת לתור ומעביר פקודת CLI פנימית ל-Executor, תוך העברת מעקב פעיל אחר מחזור החיים שלה עד לדיווח סטטוס חדש.

ה-Worker אוסף את הפקודה מהתור, מפעיל תת-תהליך מבודד שמושך מטא-דאטה ומציג שדות Jinja, ומפעיל רשמית את מצב ה-"רץ" ברגע שהוא מבצע את הלוגיקה הפנימית של האופרטור.

5. **Airflow Critical Sections:** What is the `'Critical Section'` of the `Scheduler`? Describe the 4 primary `Critical Sections` (`Dag Run` Creation, `Dag Run` Scheduling, `TaskInstance` Creation, `Task` Scheduling).

מקטע קריטי זה הוא המקום שבו מופעי TaskInstance עוברים ממצב מתוזמן ומועברים לתור ל-executor, תוך הקפדה על גבולות המקבילות והמאגר השונים.

יצירת DAGRun: מזהה DAGs שעתידים לביצוע על סמך לוחות זמנים או טריגרים, ולאחר מכן מוסיפה רשומת DagRun חדשה למסד הנתונים.

תזמון DAGRun: מנטר מצבי DagRun פעילים, מתאם את התקדמות זרימת העבודה ברמת המאקרו עד שהיא נפתרת להצלחה או כישלון.

יצירת TaskInstance: יוצר מופעים של כל משימה בודדת המוגדרת בתוך ריצת DAG חדשה שנוצרה, ומגדיר אותה למצב התחלתי במסד הנתונים.

תזמון משימות: מעריך תלויות משימות, כללי טריגרים ומאגרי משאבים זמינים, ולאחר מכן דוחף משימות מתאימות ל-Executor לצורך ביצוע עובדים.

### Real-World Context
Rather than focusing on one technology, think about how data workflows are scheduled, and think about when running and orchestrating data workflows.

## 🔄 Alternatives

Assignment: You are required to research and write a comparative analysis between Airflow and an industry alternative.

    Deliverable: A written summary (minimum 1 or 2 sentences).
    Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
    Goal: You must be able to justify why the department uses this tool for our specific environment.

## 🎯 User Story & Scenario

Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.

    Deliverable: A written summary example/story (two sentences approx.).
    Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
    Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.


## Wrapping Up :trophy:
Discuss your answers and any areas of confusion with your mentor. Reflect on how these general concepts will help when you later when using scheduled jobs.

## Additional Topics from Review
- A deep dive into the Airlfow database and the inner workings of Airflow.
- A deep dive into bugs solved and unsolved inside Airflow.

## Action Items
- Review your notes and identify topics you want to explore deeper.
- Collect a list of real-world schedulers and their algorithms.
- Prepare questions for the upcoming mentor Q&A session.

## Completion Checklist

- You understand the airflow architecture and can explain in detail what each component does
- You understand airflow on the applicative side, where you know how to author dags
- You understand how airflow manages it's security
- You understand what happens to the task from start to end
- You understand at each tasks state what happens to it and can tell where it is stuck if it is

## Recommemded Resources
- [Airflow Docs](https://airflow.apache.org/docs/)
