# Explore A Component From Our Stack & Knowledge Sharing 🐘 

## **Topics Covered**
- Overview of a selected **Data Stack sub-component** (e.g., Hbase-Memstore, Trino-Coordinator, Spark-Driver, HBase-Meta-Table, Airflow Scheduler, etc.)
- The **problem the sub-component solves** within a technology
- Core **architecture and main components**
- How the technology **integrates with the rest of the Data Stack**
- Typical **data flow and operational usage**
- Key **advantages, limitations, and trade-offs**

> ⚠️ **Note:**
> This task is meant to help you explore the data ecosystem and practice technical communication.  
> Start by asking your **mentor which Data Stack sub-component you should focus on** before you begin your preparation.

### ⏳ Timeline
Estimated Duration: 1 Day

- **First Half of the Day**
  - Ask your mentor which **Data Stack component** you should explore.
  - Research the selected technology and understand:
    - What problem it solves
    - Its architecture and main components
    - Where it fits within a typical **data pipeline**
    - How it interacts with other tools in the stack.

- **Second Half of the Day**
  - Prepare a **20-minute technical presentation** about the technology.
  - Include:
    - A short **introduction to the problem space**
    - The **architecture and core concepts**
    - Example **use cases within a data platform**
    - Integration with other **data tools**
  - Present your findings to the **entire team**.

## Overview
The purpose of this exercise is to help you become familiar with **different parts of the Data Stack** while also practicing the ability to **explain technical systems clearly**.

Your presentation should focus on:
- **What the technology does**
- **Why it exists**
- **How it works**
- **Where it fits in the broader Data Stack**

### 📊 Presentation Requirements

As part of your **20-minute presentation**, you must include the following sections:

https://docs.google.com/presentation/d/1DOP2u-QE0noMQ6JXyMSpLcxqochaOLS2pPdPFG3UPrE/edit?usp=sharing

למצוא איך מנתבים בין excuters יעני מה החוקים?
אוטומתית ככה [כאשר task_create_missing_queues = true]:
```
task_routes = ([
    ('feed.tasks.*', {'queue': 'feeds'}),
    ('web.tasks.*', {'queue': 'web'}),
    (re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),
],)
```
או לעשות את זה ידנית ככה (example) [כאשר task_create_missing_queues = false]:
```
from kombu import Queue

app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('default',    routing_key='task.#'),
    Queue('feed_tasks', routing_key='feed.#'),
)
app.conf.task_default_exchange = 'tasks'
app.conf.task_default_exchange_type = 'topic'
app.conf.task_default_routing_key = 'task.default'
```

איך הפורמט של task נראה? ואיך הסלרי יודע למצוא את הקוד בייס שלו ולדעת מה להריץ?
Task זה callable בpython שניתן לקרוא לו ב:
```
result = FUNCNAME.delay(args)
```
לא בהכרח בכפורמט args

למה שאני לא אשתמש ב kubernetes executor באיירפלואו במקום בסלרי
מוריד את הoverhead של להקים pod ולמחוק אותו מחדש באמצעות שימוש בworkerים שתמיד למעלה [הסברתי את זה אחרי שהלכת]
תוליך אותי את כל ה flow מ airflow scheduler להרצה של task ב celery
הscheduler מזהה DAGRun שאמור לרוץ, מפצל לTaskInstanceים, בודק אם כל הdependencies מולאו, הוא מעביר את זה לExecutor, במקרה הזה הExecutor הוא CeleryExecutor והוא יעביר את זה לMessageBroker שנדבר ומשם Worker ידגום את הQueue ויקח את הTask ויבצע אותו

אם אני מגדיר concurrency=8, מה בפועל ירוץ בתוך הworker?
אם אתה מגדיר בDAG שהConcurrencyLimit = X וכרגע הConcurrency==X אז הScheduler לא ישלח את הTaskInstance לExecutor מלחתחילה

מי בפועל שולח את ה taskים ל queue?
באירפלו הExecutor, בCelery רגיל זה יהיה הלקוח

איך ה queue ממש מנוהל? טכנולוגיות/אוביקטים בתוך הטכנולוגיה וכו'
תלוי Message Broker - זה יכול להיות RabbitMQ, Redis, Amazon SQS, Zookeeper, Kafka, GC PubSub

איך ניתן לשלוט בעומסים? מה קורה אם worker של celery מריץ יותר מדי taskים?
??? A Celery Worker only executes 1 task at a time

איך ניתן למנוע noisy neighbors? ברמת ה worker/ התור וכו
ואיך celery מתמודד איתן אם בכלל?
לכל worker יש משאבים משלו ולכן עליה בצורך במשאבים של תור אחד לא תשפיע על תורים אחרים ורק תשפיע על אותו תור

מה קורה אם ה- worker לא זמין? מה קורה ל taskים שהוא כבר משך, ומה קורה לשאר ה taskים שמתוזמנים
יש retry שבו הtask ינוסה ע"י worker אחר ויעבור לתור אחר [קונפיגורבילי] לתחקור

איך עובד תהליך ה acknowlagement על ה tasks?
Workerים עושים ack כדי לציין שהtask טופלה.
חוסר עשיית הack יגרום לכך שהtask ישלח מחדש לעובד אחר.
המועד המדויק שבו task נחשבת לכישלון משתנה בהתאם לtransport.
איך עובד מנגנון הדגימה של בריאות ה task שרץ
הפוך, הworker נמצא בEvent & Consumer Loops שמוודאים שהוא דוגם את הQueue כאשר הוא פנוי ויש timeout לכל task ככה שאם הtask לא מסתיים הוא עושה fail לtask ואם הworker לא חוזר לloop הוא עובר recycle [פשוט הפעלה מחדש]

איך אפשר לבצע scale out?
אתה מוסיף עוד workerים [???]

האם יש tasks שהיית ממליץ לא להעלות על סלרי?
Task אם צורך במשאבים שמשתנה בזמן הרצה אולי, בכללי פחות מומלץ taskים כבדים אבל אפשר לעבוד אם אתה מגדיר worker עם יותר משאבים לtaskים כאלו מראש


#### 🔄 Alternatives
**Assignment:** Research and present a comparative analysis between the selected tool (for example **S3**) and at least one industry alternative.

- **Deliverable:** A written summary (**minimum 1–2 sentences**).
- **Focus:** Compare:
  - Performance
  - Architecture
  - Specific **pain points** this tool solves compared to legacy systems or competitors
- **Goal:** Demonstrate that you understand **why the department uses this tool** in our specific environment.

#### 🎯 User Story & Scenario
**Assignment:** Based on your research and understanding of the department's pipeline, define a concrete **use case** for this technology.

- **Deliverable:** A written **example scenario/story** (approximately **two paragraphs**).
- **Data Flow:** Map the **data flow** and explain how this tool integrates with the other components in our **Data Stack**.

Expect the team to ask **advanced or in-depth technical questions** during the Q&A.  
You do not need to know everything, but you should understand the **core concepts well enough to discuss them confidently**.

## Wrapping Up :trophy:
After the presentation, discuss the feedback and questions with your mentor.

Make sure you can:
- Explain the **core idea of the technology**
- Describe its **architecture at a high level**
- Understand **when and why it is used**
- Recognize its **strengths and limitations** within our **Data Stack**
