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

שאלות אבל סקילה
איך docker עובד על windows
Before Windows 10 2004 (and the equivalent Server version), it would essentially use Hyper-V with a “hidden” Linux VM.

Since the release of WSL2, it simply uses whatever flavour of Linux you’ve installed in WSL, and uses that kernel.

מה זה הimage בתכלס על המחשב
A bunch of read-only layers managed by the DockerD

איך עושים "CD" בdocker
WORKDIR

איזה עוד פקודה יש בdockerfile להריץ פקודות שהם לא CMD
RUN, the main difference is:
RUN Command: RUN command will execute the default command when we are building the image and commit the image changes for the next step.
There can be more than 1 RUN command to aid in the process of building a new image.
CMD Command: CMD commands will just set the default command for the new container, which will not be executed at build time.
If a Dockerfile has more than 1 CMD command, then all of them are ignored except the last one.


פקודות בDockerfile
FROM - import base image
EXPOSE - expose port of container at runtime
RUN - run command during image building process.
CMD - specifies the command that will run upon container start
ENV - set environment variable
COPY - copy files from host to container
VOLUME - create a mount point as  a volume inside a container
WORKDIR - “cd” but for Docker
ARG - set variables passed to the Dockerfile during build time
LABEL - add metadata to image
STOPSIGNAL
ONBUILD
ENTRYPOINT
MAINTAINER
ADD
HEALTHCHECK
SHELL
USER

מה זה docker run -it
Create and run a new container from an image
  -i, --interactive                      Keep STDIN open even if not attached
  -t, --tty                              Allocate a pseudo-TTY

איך רואים את כל הfs של הcontainer בפקודה
docker exec -it myserver /bin/bash
ls -lsa

איך dockerfile ללא baseimage ולמה
FROM scratch - empty base image
Why:
Smaller image size
That’s kinda it the rest are other advantages that come from that

האם אפשר יותר מbaseimage 1
Yes - it’s called Multi-Stage Builds.

מה זה docker compose
Docker Compose is a tool for defining and running multi-container applications.

פקודות בdocker
run            Create and run a new container from an image
exec           Execute a command in a running container
ps             List containers
build          Build an image from a Dockerfile
pull           Download an image from a registry
push           Upload an image to a registry
images         List images
login          Authenticate to a registry
logout         Log out from a registry
search         Search Docker Hub for images
version        Show the Docker version information
info           Display system-wide information
compose        READ ABOVE
container      Manage containers
image          Manage images
plugin         Manage plugins
volume         Manage volumes
commit         READ BELLOW
cp             Copy files/folders between a container and the local filesystem
create         Create a new container
diff           Inspect changes to files or directories on a container's filesystem
events         Get real time events from the server
history        Show the history of an image
import         Import the contents from a tarball to create a filesystem image
inspect        Return low-level information on Docker objects
kill           Kill one or more running containers
logs           Fetch the logs of a container
pause          Pause all processes within one or more containers
port           List port mappings or a specific mapping for the container
rename         Rename a container
restart        Restart one or more containers
rm             Remove one or more containers
rmi            Remove one or more images
start          Start one or more stopped containers
stats          Display a live stream of container(s) resource usage statistics
stop           Stop one or more running containers
tag            Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
top            Display the running processes of a container
update         Update configuration of one or more containers
  
למה kaniko טוב ומתי להשתמש [לא לסיים ב"CICD, K8S", לתת דוגמה]
container image building designed for Dockerfile-based image creation.

איך מגדירים bind mount וvolume
Bind mount: … -v HOSTDIR:CONTDIR
Volume: docker volume create [OPTIONS] [VOLUME] 

Use case של bridge
Docker Bridge Networks are used for developing web applications with backend services, deploying microservices to a single host, setting up a local development environment, running continuous integration (CI) pipelines, and testing service-to-service communication.

Port forwarding in Docker
docker run -p CONTAINERPORT:HOSTPORT IMAGE

מה זה commit בdocker
Create a new image from a container's changes


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
