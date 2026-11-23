# Docker Foundations

Docker is a platform for running applications in isolated environments called containers.

It introduces a standardized way to package and execute software across different environments, without depending on the underlying system configuration.

Instead of installing dependencies directly on a machine, applications are bundled into portable units that can run consistently wherever Docker is available.

---

### ⏳ Timeline
Estimated Duration: 1 Day

Day 1 – Docker Core Concepts  
- Containers vs Virtual Machines  
- Images, Containers, Dockerfile  
- Networking & Storage  
- Security & Isolation  
- Build strategies (Docker, Kaniko, DinD)

---

### 📚 Resources
- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kaniko Documentation](https://github.com/GoogleContainerTools/kaniko)
- [OCI Specification](https://opencontainers.org/)

---

# Docker Core Concepts

### ❓ Guide Questions

1. **What is Docker and what problems does it solve?**  
   Explain what a container is, how it differs from a virtual machine, and why containers are useful in modern systems (portability, consistency, isolation).

הסיבה שיש לנו את Docker היא כדי לשתף את האפליקציות שלנו ולשכפל את סביבת האפליקציה שלנו על מכונה אחרת בצורה קלה יותר מאשר מכונות וירטואליות נפרדות לכל סביבה ואפליקציה חדשות.

מכולה היא התוכנה עצמה של התמונה, שהיא תמונת מצב של התוכנה שלנו וכל התלויות שלה, שנבנית על ידי Dockerfile - הקוד שאומר ל-Docker כיצד לבנות את התמונה.
ההבדל העיקרי בין מכולות Docker לבין אשכול של מכונות וירטואליות הוא שמשאבים משותפים ישירות עם המארח, ו-Docker מתקשר באופן טבעי עם מחשב המארח, בעוד שבמכונות וירטואליות היא צריכה לאתחל מערכת הפעלה שלמה ולשמור את המשאבים הללו ולתקשר דרך היפר-ויזור למחשב המארח.

מכולות שימושיות במערכות המודרניות שלנו מכיוון שהן ניידות להפליא [קלות כמו יצירת Dockerfile], והן נותנות תוצאות עקביות על פני מכונות וירטואליות שונות הודות לאופן שבו הן מבודדות את הפרויקט תוך כדי יכולת להפיק תועלת ממחשב מארח חזק מאוד.

2. **What are the core Docker components and how do they interact?**  

הרכיב העיקרי של Docker הוא מנוע Docker, המורכב מ: לקוח Docker CLI - שאליו המשתמש שולח את בקשותיו/פקודותיו, Daemon של Docker - השרת שאיתו ה-CLI מקיים אינטראקציה, והם מתקשרים דרך REST API.
מנוע Docker מאפשר לך לנהל את המכולות, התמונות ונפחי הנתונים של Docker.
מנוע Docker מחולק לשני תת-רכיבים: הלקוח [שדיברנו עליו קודם] והמארח, שהוא הדמון, ניהול המכולות [containerd] וניהול התמונות.
מאגר Docker - שרת מרוחק, רישום של תמונות שממנו תוכל לקבל את התמונות שלך.
נפחי נתונים עוזרים לך לאחסן את הנתונים שלך במכולות שלך.
<img width="750" height="395" alt="image" src="https://github.com/user-attachments/assets/33f51719-4aab-4277-8345-fee1b555343f" />


3. **How do networking and storage work in Docker?**  
   Explain:
   - Container networking (bridge, host, ports)  
   - Communication between containers  
   - Volumes vs bind mounts  
   - When to use persistent storage

רשת גשר: רשת Docker המוגדרת כברירת מחדל, המאפשרת למכולות באותו מארח לתקשר.
היא מספקת בידוד רשת, מקצה לכל מכולה כתובת IP משלה ותומכת בתקשורת דרך כתובות IP או שמות מכולה באמצעות DNS של Docker.
רשת מארח: מאפשרת למכולות לשתף את מחסנית הרשת של המארח ישירות, באמצעות כתובת ה-IP, הממשקים והניתוב שלו.
פעולה זו עוקפת את בידוד הרשת, ה-NAT ומיפוי הפורטים של Docker.
תקשורת מכולה: Docker מאפשר למכולות לתקשר זו עם זו ועם עומסי עבודה חיצוניים, בין אם במארח יחיד ובין אם בין מספר מארחים באשכול.

אמצעי אחסון: אחסון המנוהל על ידי Docker שקיים באופן עצמאי ממכולות ותמונות.
הנתונים נשארים גם לאחר שמכולה נעצרת או מוסרת, וניתן לעשות שימוש חוזר באמצעי אחסון על ידי מכולות אחרות.
מתאים ביותר לאחסון קבוע וליישומים בעלי מצב.

חיבורי קשירה: רכיב ספריות מארח ישירות למכולות, כאשר השינויים משתקפים משני הצדדים.
מתאים ביותר לזרימות עבודה של פיתוח ולאחסון זמני, אך דורש ניהול ידני של ספריות מארח.
ההבדל העיקרי: אמצעי אחסון מנוהלים על ידי Docker והם הטובים ביותר עבור נתונים מתמשכים, בעוד ש-bind mounts מחברים ישירות ספריות מארח למכולות.

4. **What are the security and isolation risks in Docker?**  
   Discuss:
   - Namespaces and cgroups (high-level)  
   - Running containers as root vs non-root  
   - Image vulnerabilities and best practices

Docker בנוי על תכונות של ליבת לינוקס (Linux kernel) המבודדות תהליכים ושולטות במשאבים.
מרחבי שמות (Namespaces) מעניקים לכל קונטיינר תצוגה מבודדת משלו על המערכת (תהליכים משלו, רשת, נקודות עיגון/mounts וכו').
קבוצות בקרה (Control Groups או cgroups) מגבילות ועוקבות אחר השימוש במשאבים (מעבד, זיכרון, קלט/פלט).

Docker Root: כברירת מחדל, קונטיינרים פועלים לעתים קרובות כמשתמש root.
קבצים שנוצרים בספריות מארח מותקנות הופכים לבעלות root, מה שעלול למנוע ממשתמשים רגילים לשנות או למחוק אותם.
דבר זה עלול לגרום לשגיאות הרשאה ולכשלים בבנייה.

Docker Non-Root: מפעיל קונטיינרים תחת משתמש רגיל במקום root.
קבצים שנוצרים בספריות מותקנות נמצאים בבעלות אותו משתמש, מה שמקל על שינוי ומחיקה מהמארח.
זה גם מפחית את סיכוני האבטחה על ידי הגבלת הרשאות קונטיינרים.
ההבדל העיקרי: לקונטיינרים של root יש הרשאות מוגברות אך עלולים לגרום לבעיות בעלות על קבצי מארח.
קונטיינרים שאינם root מספקים אבטחה טובה יותר ומונעים בעיות רבות הקשורות להרשאות.

תמונות בסיס לא מאובטחות: תמונות בסיס הן הבסיס של קונטיינרים.
שימוש בתגים לא מוצמדים כגון ubuntu:latest או node:alpine יכול להציג פגיעויות בלתי צפויות מכיוון שהתמונה עשויה להשתנות עם הזמן.
שימוש בגרסאות תמונה ספציפיות ומהימנות מסייע בשמירה על אבטחה ועקביות.
gh0stEdit - פגיעות גישה מבוססת שכבות: פגיעות המאפשרת לתוקפים לתפעל שכבות תמונה של Docker מבלי לבטל את חתימת התמונה או להפעיל סריקות אבטחה סטטיות או דינמיות. זה עלול להקשות על זיהוי שינויים זדוניים.

שיטות עבודה מומלצות לתמונות:
- שמרו על תמונות קונטיינר מינימליות.
- השתמשו בתמונות בסיס מהימנות.
- עדכנו את התמונות שלכם לעתים קרובות.
- סרוקו תמונות מקומית במהלך הפיתוח.

5. **How are Docker images built in different environments?**  
   Compare:
   - Standard Docker build  
   - Docker-in-Docker (DinD)  
   - Kaniko  
   Explain when each approach is used (e.g., CI/CD pipelines, Kubernetes).

בניית Docker סטנדרטית:
CLI - פקודת בניית Docker -> DockerD בונה את התמונה שנתנו לה.
זוהי התמונה המוגדרת כברירת מחדל.

DinD - בתוך מכל Docker יחיד, ייווצרו תת-מכולות עבור כל מכל ומכולה עבור מכל DinD.
הוא משמש בעיקר בצינורות CI/CD.

Kaniko - מבצע כל הוראה ברצף, ויוצר שכבות ביניים שניתן לאחסן במטמון באופן אופציונלי, והתמונה הסופית נדחפת לאחר מכן לרישום שצוין.
הוא בנוי גם עבור צינורות CI/CD וגם עבור פודי Kubernetes, מכיוון שיש לו אינטגרציה מקורית עם שניהם.

---

### 🔄 Alternatives
Assignment: Compare two virtualization approaches:

- Virtual Machines (VMs) vs Containers

Deliverable:
- 1–2 sentences comparison  
- Include a real-world use case for each

Goal:
Understand the trade-offs between full virtualization and container-based isolation.

---

### 🎯 User Story & Scenario

Assignment: Describe a real-world usage of Docker.

Deliverable (2 paragraphs):

- Describe a service (e.g., API) that is packaged using Docker  
- Explain how it is built (Dockerfile), stored (registry), and deployed  
- Describe briefly how containers help ensure consistency across environments
