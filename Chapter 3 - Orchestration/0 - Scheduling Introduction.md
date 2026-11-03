# Orchestration Fundamentals:
## Overview
This section will go over the fundamentals of _orchestration_, consisting of _scheduling_ and _resource management_.

**We will focus on general concepts such as scheduling algorithms, preemptive vs non-preemptive scheduling and prioritization.**

## Goals
- Develop a foundational understanding of how scheduling is done.
- Learn the common terminology used by most schedulers.
- Introducing the day-to-day challenges of an infrastructure administrator.
- Practice planning a self-study day and estimating time for learning.

:warning: **Note:**
- This is a self-study day. Independence and time management are essential.
- Many newcomers struggle with self-study; take a moment to plan your day and stick to it.
- Understand the **big picture** of each concept. If you can't explain it, you probably haven't learned it.
- Be prepared to describe how concepts relate to one another and to real-world scenarios.
- When in doubt about what you need to learn, ask your mentor.

### Core Concepts

Think through the following questions; by answering them you’ll touch every major topic listed above:

1. **Scheduling Basics:** Why can’t we just use a simple sleep() command or a basic cron job to manage a modern data workflows? What is the difference between a Time-based trigger and an Event-based trigger? Give a real-world data example for each, In general scheduling, why do we use a DAG to represent a workflow instead of just a simple list of instructions?
מתזמן משימות הוא מערכת שלמה שנועדה לנהל, לאחסן, לעקוב ולבצע משימות בקנה מידה גדול.
בניגוד ל-Cron, שמחליט רק מתי משימה צריכה להריץ, מתזמן משימות מנהל את כל מחזור החיים של המשימה.
הוא מטפל ביצירת משימות, התמדה, קביעת סדרי עדיפויות, ניסיונות חוזרים, ניטור, ביצוע ומדרגיות.
ניתן לחשוב על מתזמן משימות כפלטפורמת ניהול משימות חכמה, בהשוואה למשימת cron, שהיא טיימר פשוט.

טריגר מבוסס זמן: מבוצע אוטומטית בזמנים מוגדרים מראש.
טריגר מבוסס אירועים: מבוצע אוטומטית כאשר אירוע מסוים מתרחש.

אנו משתמשים ב-DAGs מכיוון שיש להם:
- צמתים מייצגים משימות, כגון קליטת נתונים, הרצת טרנספורמציה או אימון מודל.
- קצוות מייצגים תלויות. קצה ממשימה א' למשימה ב' מציין ש-B לא יכולה להתחיל עד ש-A תסתיים.
- נקודות התחלה וסיום מסמנות היכן העבודה מתחילה ומסתיימה.
- ענפים מקבילים מאפשרים למשימות ללא תלויות משותפות לפעול בו זמנית.
- מטא-נתונים ויומני רישום עוקבים אחר סטטוס, היסטוריה ותוצאות לצורך צפייה וניפוי שגיאות.

2. **Scheduling Algorithms & Types:** Compare First-In-First-Out (FIFO), Shortest Job First (SJF) and Round Robin (RR), how do they handle varying workflows? Define Preemptive vs. Non-preemptive scheduling, If a "Critical" job enters the queue while a "Low" priority job is already running, what happens in both scenarios? What is "Starvation" in priority scheduling, and how does the concept of Aging fix it? what are other common algorithms to fix starvation?

FIFO - קוף רואה עבודה, קוף עושה עבודה, קוף רואה עבודה הבאה, קוף עושה את העבודה הבאה אחרי העבודה הראשונה שנעשתה, בעיה - אם קוף רואה עבודה גדולה אז קוף רואה עבודות קטנות שלוקחות זמן קצר, קוף עושה עבודה גדולה קודם, מאט עבודות קטנות.

SJF - קוף מקבל עבודות, קוף מעריך איזו עבודה היא הקצרה ביותר, קוף מבצע ממוין ברשימת עבודות עולה, בעיה - אם קוף מקבל עבודה ממש גדולה, עבודה גדולה לא מבוצעת ומקבלת עומס, קוף צריך גם להעריך כמה זמן לוקחות עבודות, לוקח זמן.

RR - קוף מקצה עבודות לזמן ולא לזמן לעבודות; כל העבודות מקבלות חלק שווה של משאבים; בעיה - החלפת הקשר.

תזמון מקדים מקצה את המעבד לתהליך לתקופה מוגדרת, בעוד שתזמון לא מקדים מקצה את המעבד לתהליך עד שהוא מסיים או נכנס למצב המתנה.

בתזמון לא מקדים, שום דבר לא ישתנה לאחר שהוא התחיל ולא יהיה אכפת לו משינוי העדיפויות, בהשוואה לתזמון מקדים, שבו הקצאת המשאבים גמישה, ומשימות העדיפות הדחופות יותר יגזל את המשאבים.

רעב הוא משימה שנמצאת בעדיפות נמוכה, ומשימות חדשות יותר עם עדיפות גבוהה יותר תמיד מגיעות כדי לקחת משאבים מהמשימה בעלת העדיפות הנמוכה יותר.
זה נפתר על ידי הזדקנות, מכיוון שהזדקנות היא טכניקה שמעלה מעת לעת את העדיפות של תהליך המתנה.
פתרון נוסף לרעב הוא RR, שבו רעב אינו מתרחש עקב אופן הקצאת המשאבים.

3. **Resource Allocation & Scheduling:** Explain Dominant Resource Fairness (DRF). Why is it more "fair" to look at CPU and RAM usage rather than just task count? Compare Static Allocation to Dynamic Allocation. Which one is safer for the system, and which one is more efficient for the cluster? What is Capacity Scheduling, and how does it provide "guaranteed lanes" for different departments?

המשאב הדומיננטי של משתמש הוא המשאב שיש לו את החלק הגדול ביותר ממנו. DRF מיייש הוגנות מקסימלית-מינימלית על חלקים דומיננטיים - משווה את החלק הדומיננטי של המשתמשים.
ספירת המשימות עשויה לא לייצג את השימוש בפועל במשאבים - משתמש יכול לבצע משימה אחת בשנה, אך משימה זו דורשת יותר CPU ו-RAM מכל המשימות של 30 משתמשים שמריצים 20 משימות קטנות ביום.

הקצאה סטטית משמשת להקצאת משאבים במהלך תהליך קומפילציה של נתונים בגודל קבוע.
המהדר מקצה משאבים למשתנים הקיימים בתוכנית.
זה מאפשר גישה יעילה למשאבים.
הקצאה דינמית משמשת להקצאת משאבים במהלך תהליך ביצוע הנתונים.
זה מאפשר הקצאה לישויות כאשר התוכנית פועלת בפעם הראשונה.
זה מקצה שטח וגודל מדויקים לתוכן הדינמי, ולכן ההקצאה מתבצעת במהלך זמן ריצה, מה שמפחית את בזבוז השטח.
סכמת הקצאה סטטית מהירה ובטוחה יותר אך פחות יעילה בהשוואה להקצאה דינמית.

תזמון קיבולת מוגדר כתהליך של תיאום משאבים כדי להבטיח שימוש יעיל בהם. זה כרוך בתכנון משימות תחזוקה על סמך כשלים באשכול או צרכים תפעוליים מבלי לזרז את התהליך.

4. **Cluster Utilization:** What are idle resources in a cluster, and why are they considered a problem from a utilization perspective? What are our options when we want to improve cluster resource usage on job based or non job based clusters (at least provide 3)? what are the advantages and disadvantages of each option (at least 2)?

הסוד ליכולת הרחבה (סקיילביליות) לפי דרישה הוא, שבכל מצב נתון, נדרשים משאבים זמינים – מאגר של משאבים פנויים שמהם ניתן לשאוב כדי לספק כל תוספת נדרשת למשאבים.
הם מהווים בעיה, מכיוון שאנו שואפים לנצל את מלוא המשאבים העומדים לרשותנו.

1. קנה מידה אוטומטי - אפשר לאשכול להוסיף/להסיר צמתים ולהוסיף/להסיר עותקים בהתאם לעומס. עבור משימות, ניתן לשנות את קנה המידה לאפס כאשר אין תור. אתה משלם רק עבור מה שאתה משתמש בו, וזה אוטומטי, אבל צמתים חדשים לוקחים דקה להתחיל, וזה יכול להתנדנד כל הזמן.
2. תזמון חכם יותר / אריזת סלים - ארזו משימות בצורה הדוקה יותר במקום להשאיר צמתים חצי ריקים. כלים כמו מילוי חוזר ב-Slurm, Karpenter, או הסרת התזמון ב-Kubernetes. ניצול טוב בהרבה מבלי לקנות חומרה נוספת ואין צורך לשנות את הקוד שלך, אבל חלק מהמשימות בעלות עדיפות נמוכה עלולות לחכות זמן רב יותר, ואתה עלול לקבל שכנים רועשים באותו צומת.
3. התאמה לגודל הנכון + התחייבות יתר - תקן את בקשות המעבד/זיכרון RAM - רוב הצוותים מבקשים יותר מדי. לאחר מכן תוכל לבצע התחייבות יתר ולערבב משימות אצווה עם שירותים ארוכי טווח על אותם צמתים.
זהו הניצחון המהיר ביותר בעלויות, ואתה משתמש בכל הפער שכבר שילמת עבורו, אבל אם אתה מקצץ יותר מדי, אתה מקבל OOMs ומצערת, ואם אתה משתמש במופעים נקודתיים/ניתנים למניעה, עבודות יכולות להיסגר באמצע הריצה.

5. **Users Perspective:** Why is Idempotency the most important concept for a developer to understand when writing scheduled jobs? what is an Exponential Backoff when jobs fail? What is Backfilling, and how does it relate to the "Optimistic" approach of keeping resources busy?

אידמפוטנטיות היא כאשר, לא משנה כמה פעמים תעשו משהו, התוצאה שלו לא תשתנה ותהיה זהה לביצוע פעם אחת.
זה חשוב כי אנחנו רוצים שאם נתזמן את אותה משימה לרוץ פעמיים בשעה 20:00, אז אנחנו רוצים שהיא תרוץ פעם אחת כדי לא לבזבז משאבים.

אלגוריתם ה-backoff האקספוננציאלי מגדיל את זמן ההמתנה בין ניסיונות חוזרים באופן אקספוננציאלי לאחר כל כישלון, מה שעוזר לנהל עומס ברשת ולמנוע ניסיונות חוזרים מסונכרנים.

תזמון Backfill מאפשר למשימות אחרות להשתמש במשבצות המשימות השמורות, כל עוד המשימות האחרות אינן מעכבות את תחילתה של משימה אחרת, מה שמאפשר למשימות מקבילות גדולות לפעול מבלי לנצל מספיק משאבים.


### Real-World Context
Rather than focusing on one technology, think about how these ideas show up in schedulers, such as the linux scheduler or the trino task scheduler.

## Wrapping Up :trophy:
Discuss your answers and any areas of confusion with your mentor. Reflect on how these general concepts will help when you later when using scheduled jobs.

## Additional Topics from Review
- A deep dive into sheduling algorithms.
- What are the different obsolescence algorithms widely used? where could they also be implemented? what are some scheduling algorithms without preemption and aging that solve starvation?

## Action Items
- Review your notes and identify topics you want to explore deeper.
- Collect a list of real-world schedulers and their algorithms.
- Prepare questions for the upcoming mentor Q&A session.

## Recommemded Resources
- [Priority Scheduling Slurm](https://slurm.schedmd.com/priority_multifactor.html)
- [Operating Systems Scheduling Stanford University](https://web.stanford.edu/~ouster/cgi-bin/cs140-spring14/lecture.php?topic=scheduling)
