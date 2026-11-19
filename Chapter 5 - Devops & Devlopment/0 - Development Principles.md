# Software Development Foundations & Python Basics

Before building data pipelines or services, it is important to understand the
core principles of modern software development.

This module introduces the development practices, conventions, and tools that
are commonly used in professional engineering environments.

The goal is not only to learn *what the tools are*, but also *why they exist*
and how they help create maintainable, scalable, and collaborative systems.

---

### ⏳ Timeline
Estimated Duration: 2 Days

Day 1 – Software Development Principles 
- Development principles and clean architecture
- Development workflows and collaboration
- Testing approaches and design paradigms

Day 2 – Python internals  
- Python ecosystem and development patterns
- REST APIs and Python frameworks
- Testing, mocking, and service design

---

### 📚 Resources
Use the resources below and practice researching additional information online.

- [Clean Python - Sunil Kapil](https://edu.anarcho-copy.org/Programming%20Languages/Python/Clean%20Python.pdf)
- [SOLID Principles Overview](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design)
- [Python Official Documentation](https://docs.python.org/3/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)

---

# Software Development Principles

### ❓ Guide Questions

1. What are **Clean Code principles**, and why are they important in software development?  
   Explain ideas such as readability, maintainability, and the principle of  
   **“Leave the codebase cleaner than you found it.”**

Clean code Principles
Minimize Dependencies (Loose Coupling)
Avoid tightly linking classes or modules. When classes depend too much on each other, changes in one can ripple through others, making updates and debugging difficult.
בתכלס, כמה שפחות coupling כמה שיותר טוב
Group Related Responsibilities (High Cohesion)
Ensure that elements within a class or module work towards a single, clear purpose. High cohesion makes components easier to understand and modify.
כמה שיותר cohesion כמה שיותר טוב
Keep Changes Local (Locality)
Design systems so that changes, fixes, or feature additions can be isolated to a specific area, without affecting unrelated parts of the codebase.
לעשות ששינויים בקוד ישנו רק במקום אחד
Make Components Replaceable (Removability)
Build components that can be removed or swapped out without significant rewrites to the surrounding system.
לעשות שלהחליף רכיב זה קל
Keep it Small (Small Components)
Divide the system into smaller, focused pieces. Each component should ideally handle one task to maintain clarity and reusability.
לעשות שרכיבים יהיו כמה שיותר קטנים

Readability - קריאות - עד כמה הקוד שכתבת אשקרה קריא לבנאדם אחר שלא עבד על הcodebase אףפעם
Maintainability - תחזוקתיות -  עד כמה קל לתחזק את הקוד, עד כמה קל למצוא בו שגיאות וכמה קל לתקן בו ולהוסיף בו דברים.
“Leave the codebase cleaner than you found it.” - אם זה לא שבור לא לתקן את זה, לא צריך להוסיף שיט שלא עושה כלום ועושה את הקוד פחות קריא ממה שהיה לפניך, "לא להיות ההוא שצריך לקרוא לו למילואים רק כדי להבין מה הוא עשה" - א. מטוק, מסא"א.

2. What are the **SOLID principles**?  
   Describe each principle and explain how they help create maintainable
   object-oriented systems.

SOLID:
Single Responsibility Principle (SRP)
Each class should do only one thing. A class with multiple responsibilities becomes hard to understand and maintain.
מטרה אחת לכל פונקציה\קומפוננטה
Open/Closed Principle (OCP)
Code should allow for extension without requiring modification. For example, you should be able to add new features by creating new classes rather than editing existing ones.
"לא צריך לעשות ניתוח לב פתוח בשביל לשים מעיל" - נ. קפלן, מסא"א.
Liskov Substitution Principle (LSP)
Subclasses should work seamlessly in place of their parent classes. Violating this makes inheritance unreliable.
לברבז אמבטיה ולברבז הבית לא יהיה את אותו parent class
Dependency Inversion Principle (DIP)
High-level modules shouldn’t rely on low-level modules. Both should depend on abstractions (interfaces), not specific implementations.
כלב יורש מיונקים ולא יונקים יורשים מכלב
Interface Segregation Principle (ISP)
Keep interfaces small and focused. Don’t force classes to implement methods they don’t need.
KISS אבל רק לinterfaceים ולא לליטרלי כל שאר הקוד שלך

3. Explain the **KISS principle** and its importance in software design.
Why does simple and intuitive software scale well?  
   Why do overly complex systems tend to fail over time?

KISS זה Keep It Simple Stupid, בתכלס אומר לעשות שיט כמה שיותר פשוט וכמה שיתר אינטואטיבי וזה בדרכלל יהיה עדיף על פתרון מסובך שקשה להבין כי ככה אפשר להיכנס לcodebase יותר מהר ולעשות תיקונים ביותר קלות.
גם כי קשה לעשות תיקונים וגם בגלל הOverhead בין רכיבים.

4. What are the most common **paradigms / programming** (ex. Object Orianted) styles, what are the differences and when should each be used

 - תכנות מונחה-עצמים עושה שימוש בobjectים כדי לייצג data וmethodות.
בתכנות מונחה-עצמים, התוכנות משתמשות בעצמים המתקשרים זה עם זה; תקשורת זו מאפשרת לשנות את הנתונים בתוך העצמים ולפעול באופן התואם את רצון המשתמש.
הודות לאופן שבו תוכנן התכנות מונחה-העצמים, הוא מסייע למפתח בכך שהוא מאפשר שימוש חוזר בקוד - הן על ידי חלקים אחרים בתוכנה והן על ידי אנשים אחרים.
Some may claim the goat.

Procedural - תכנות פרוצדורלי הוא פשוט מורכב מרשימת הוראות למחשב, המנחות אותו לבצע פעולות מסוימות בדרך מוגדרת.
The most basic one

Those are the main 2

Declarative - תכנות דקלרטיבי הוא שבה כותבים את הלוגיקה של חישוב, מבלי לכתוב במלואו את זרימת הבקרה שלו, בתכלס הוא paradigm מאוד גדול שבתוכו יש את:
Function Oriented - תכנות פונקציונלי זה כאשר תוכניות נבנות על ידי יישום וחיבור פונקציות.
הגדרות פונקציה הן עצי ביטויים הממפים ערכים לערכים אחרים, ולא רצף של משפטי ציווי המעדכנים את מצב הריצה של התוכנית.
פונקציות מטופלות כישויות מהשורה הראשונה, כלומר ניתן לקשור אותן לשמות (כולל מזהים מקומיים), להעביר אותן כארגומנטים ולהחזיר אותן מפונקציות אחרות, בדיוק כמו כל סוג נתונים אחר.
קל לתחזק וקריא מאוד.

Imperative -  תכנות אימפרטיבי מספק הוראות ספציפיות לגבי האופן שבו יש לבצע חישובים.
בדומה לאופן שבו הimperative mood בשפות טבעיות מביעה פקודות, תוכנית אימפרטיבית מורכבת מפקודות שהמחשב נדרש לבצע.
תכנות אימפרטיבי מתמקד בתיאור אופן הפעולה של התוכנית - צעד אחר צעד - ולא בתיאורים ברמה גבוהה של התוצאות הצפויות ממנה.

5. What is **Test Driven Development (TDD)**?  
   Explain the development cycle and how it improves code reliability.

פיתוח מונחה-בדיקות הוא טכניקה לבניית תוכנה, המכווינה את תהליך הפיתוח באמצעות כתיבת בדיקות.
התהליך מורכב מחזרה על שלושה צעדים פשוטים:
כתיבת בדיקה עבור הפונקציונלית הבאה שצריך להוסיף.
כתיבת הקוד הפונקציונלי, עד אשר הבדיקה עוברת בהצלחה.
ביצוע Refactoring - שיפור מבנה הקוד, הן החדש והן הקיים.

זה משפר את הreliability של הקוד כי בסוף אתה כותב קוד שהמטרה שלו היא לפתור את הtestים שעשית וככה:
אי אפשר "לרמות" - או שהקוד שלך עובר את הtestים או שלא.
יש לך אינטרס לעשות את הקוד כמה שיותר קצר.
ובנוסף לאחרכך אתה תעשה refactor לקוד הזה כדי שהוא יהיה כמה שיותר סולידי וכמה שיותר נקי.


---

# Development Workflows & Architecture Concepts

### ❓ Guide Questions

1. Explain the difference between a **Pull Request (PR)**, **Code Review (CR)**,
   and **Design Review (DR)**.  
   Why are these processes important in team development?

PR - “A pull request proposes merging code changes from one branch into another. As a collaborative feature, pull requests give you a place to discuss and review work before it becomes part of a project.” - [github/about-pull-requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests)
CR - “A code review is a peer review of code that helps developers ensure or improve the code quality before they merge and ship it.” - [gitlab/what-is-code-review](https://about.gitlab.com/topics/version-control/what-is-code-review/)
DR - “A design review is a milestone within a product development process whereby a design is evaluated against its requirements in order to verify the outcomes of previous activities and identify issues before committing to—and, if need be, to re-prioritise—further work.” - [wikipedia/Design_review](https://en.wikipedia.org/wiki/Design_review)

בתכלס: בDR עוברים על העיצוב עצמו של המערכת ועל הרכיבים שלה ולא על הקוד עצמו, בCR עוברים על הקוד עצמו והאם הוא כתוב בצורה SOLIDית ונקייה [בנוסף מוודאים שהוא עובד ועוד כל מיני שיטים וגם זה עוזר שעוד מישהו מסתכל על הקוד שנתב לפני שהוא עובר שימוש] ובPR עוברים על שינויים שנעשו לקוד לפני שהוא נהיה חלק מהbranch החדש המרכזי יותר.

2. Define the role of a **Pull Request (PR) / Merge Request**.
What is **squshing**? Why is it common practice to squash commits before the final merge?
Find how can you **apply specific fixes** from one branch to another without merging the entire history?
What is the process for **safely undoing** a merged PR using git revert?

לוודא שלא מכניסים קוד חרא לprod ושעוד מישהו יסתכל עליו לפני שהוא עובר לprod.

“Squashing allows you to combine multiple commits in your branch's history into a single commit. This can help keep your repository's history more readable and understandable.” - [github/squashing-commits](https://docs.github.com/en/desktop/managing-commits/squashing-commits-in-github-desktop)
בתכלס, כל הcommits של הPR יראו כcommit 1.
זה עוזר לנראות.

Cherrypicking:
Given one or more existing commits, apply the change each one introduces, recording a new commit for each. This requires your working tree to be clean (no modifications from the HEAD commit).

התהליך של ביטול PR שכבר מורג'ג' הוא: יצירת revert PR - כלומר, יצירת PR המכיל את השינויים ההפוכים לאלו שהופיעו ב-PR המקורי שמוזג.

3. Explain the difference between **CLI (Command Line Interface)** and
   **UI (User Interface)** applications.  
   What are the benefits of each?

CLI is like pew pew am haker, UI is 60.
[[I'm not the only autistic one thinking this](https://www.reddit.com/r/opencode/comments/1w0up6l/comment/p6g1g8g/)]

CLI הוא בעצם ממשק שורת פקודה - כשמפחיד ליצור ממשק משתמש גרפי, משתמשים בפקודות דמויות מעטפת שעושות את מה שאתה רוצה לעשות.
[I'm assuming you all meant to compare CLI and GUI because CLI is just a form of UI so there's no actual comparisson to be done]
GUI הוא בעצם ממשק משתמש גרפי - כמו גרפיקה ואנימציות וכדומה כפתור אדום, כפתור כחול, כפתור גדול, כפתור קטן.

4. What is the difference between a **compiler** and an **interpreter**?  
   Provide examples of languages that use each approach.

Compiled languages לוקחות את הקוד כולו ועושות compilation אותו לexecutable file.
הן מהירות יותר בזמן הריצה ובטוחות יותר, אך קשה יותר לבצע בהן debugging, והcompilation עצמו בדרך כלל מוסיף זמן לתהליך.
דוגמאות: C#, Java ו-Rust [אומייגאד, Rust???!!!11!1!!].

Interpreted languages מתרגמות את הקוד שורה אחר שורה לשפת מחשב; קל יותר לבצע בהן debugging, אך הן איטיות יותר.
דוגמאות: Python, Ruby ו-JavaScript.

5. What is **event-driven programming**?  
   Explain how it differs from procedural execution and where it is commonly used.

תכנות מונחה אירועים הוא פרדיגמה שבה זרימת התוכנית נקבעת על ידי אירועים חיצוניים.
UI Events ממקלדות ועכברים, משטחי מגע ומסכי מגע, וקלטים מחיישנים חיצוניים הם מקרים נפוצים.
אירועים עשויים להיווצר גם באופן תכנותי, כגון מהודעות מתוכניות אחרות, התראות משרשורים אחרים או אירועי רשת אחרים.
תכנות מונחה אירועים הוא הפרדיגמה הדומיננטית המשמשת ביישומי GUI ובשרתי רשת.
ביישום מונחה אירועים, בדרך כלל יש לולאת אירועים שמאזינה לאירועים ולאחר מכן מפעילה פונקציית קריאה חוזרת כאשר אחד מאירועים אלה מזוהה.

בתכלס, פרדיגמת התכנות המשמשת ליצירת UI.

> ⚠️ **Recommended exercise**  Please organzie your time and consider trying this git exercise [https://learngitbranching.js.org/]()
---

# Python & API Foundations

### ❓ Guide Questions

1. What is **Python**, and what are its main characteristics compared to other
   programming languages (for example c#)?  
   Discuss readability, ecosystem, and runtime behavior.
compare python uniuqe data type like Tuple vs. List.

פייתון היא interpreted language, משמעות הדבר היא שאין צורך לקמפל אותה לפני ההרצה.
הinterpreter מריץ את קוד הפייתון כמעט על כל מחשב, בשל כך, פייתון איטית יותר מcompiled languages, כגון C, מכיוון שהיא אינה מתורגמת לקוד מכונה לפני ההרצה.
עם זאת, הדבר מאפשר למתכנת לשנות את הקוד ולראות במהירות את התוצאה.
פייתון היא שפת תכנות רב-תכליתית.
פייתון משמשת לעיתים קרובות לבניית אתרי אינטרנט, לאוטומציה של משימות שגרתיות, וליצירת תרשימים וגרפים.
מכיוון שהיא פשוטה ללמידה, אנשים שאינם מומחים למחשבים – כגון מנהלי חשבונות וחוקרים – לומדים לעיתים קרובות את שפת פייתון.
בתכלס, קוד פייטון נלקח מpy לpyc ומpyc הוא נהיה לקוד מכונה שרץ על הPVM.

פייתון היא שפה קריאה מאוד, ונהנית מקהילה וecosystem גדולות ופעילות במיוחד.
פייתון היא שפה מגניבה למדי ולכן היא כוללת טיפוסי נתונים ייחודיים, כמו tuples – שהם מעין רשימות, אך מסומנים באמצעות סוגריים עגולים `()` במקום סוגריים מרובעים `[]`.
כמו כן, הם immutable וhashable – מה שאומר שניתן להשתמש בהם כמפתחות בdictionaries או כאיברים בsets או בfrozensets; בנוסף, הם מעט מהירים יותר וצורכים פחות זיכרון.
lists הם בתכלס מערכים מדמ"חים קלאסיים.


2. What is a **REST API**?  
   Explain the core concepts such as resources, HTTP methods, and stateless communication.

REST API הוא השאר שאקח אחרי פרק זה

REST API הוא ממשק המאפשר לשתי מערכות לתקשר זו עם זו בצורה סטנדרטית.
הוא פועל לפי עקרון האדריכלות של REST, שהופך את חילופי הנתונים לפשוטים, עקביים ובלתי תלויים בפלטפורמה.
מכיוון שממשקי REST API בנויים על טכנולוגיות אינטרנט מבוססות, הם כיום אחת הדרכים הנפוצות ביותר לחבר מערכות תוכנה.

משאב ב-REST API הוא אובייקט עם סוג, נתונים משויכים, קשרים למשאבים אחרים וקבוצת מתודות הפועלות עליו.

זה דומה למופע אובייקט בשפת תכנות מונחית עצמים, עם ההבדל החשוב שרק כמה מתודות סטנדרטיות מוגדרות עבור המשאב (מתודות HTTP GET, POST, PUT, DELETE סטנדרטיות), בעוד שלמופע אובייקט יש בדרך כלל מתודות רבות.

חוסר מצב הוא עקרון ליבה של REST המבטיח שכל בקשה מלקוח לשרת תהיה עצמאית ואינה מסתמכת על בקשות קודמות.

3. **What is the Global Interpreter Lock (GIL) in Python?**  
   Explain:
   - What the GIL is and why it exists  
   - How it affects multi-threading and CPU-bound vs I/O-bound tasks  
   - Differences (if any) in how the GIL behaves across Python versions  
   - What Python 3.14 introduces regarding optionally disabling the GIL and why this is significant  
   - Common strategies to work around its limitations (e.g., multiprocessing)

“GIL זה לא רק מספר" - נ. קפלן, מסא"א.

GIL בתכלס אומר שפייטון יכול להיות רק singlethreaded ואין באמת multithreading בפייטון.
הוא הוקם כדי לנהל את המערכות הפנימיות של פייתון - כמו זיכרון וספירת הפניות - ללא תנאי מרוץ, ובלי ה-GIL, פייתון עלולה לקרוס או לפגוע בנתונים.

ריבוי-הליכים: אינו באמת מקביל; במקום זאת, העיבוד קופץ בין הליכים מהר מאוד.
משימות הקשורות לקלט/פלט: ה-GIL משתחרר בעת המתנה לקלט/פלט, כך שהליכים יכולים לעבור בצורה חלקה.
משימות הקשורות למעבד: הליכים לא יפעלו במקביל - ה-GIL מבטיח הפעלה אחת בלבד בכל פעם, אפילו במעבדים מרובי ליבות.
ב-PY3.13 ניתן היה להשבית את GIL ובמקום זאת להשתמש בגרסה חופשית של הליכים, מה שאפשר לפייתון ריבוי הליכים.

שלוש הדרכים העיקריות לעקיפת הבעיה הן:
שימוש בריבוי עיבודים: לתהליכים נפרדים יש רישומי GIL נפרדים, כך שהקוד שלך יכול להשתמש באופן מלא בליבות מרובות.
השתמש בהרחבות C או בספריות כמו NumPy: עבודה כבדה מתרחשת מחוץ לקוד הבייט של פייתון, תוך עקיפת ה-GIL.
שקול את asyncio: נהדר למשימות קלט/פלט ללא תהליכים מתקדמים.

4. What is a linter? read and explain about Ruff.

כלי "לינטר" (Linter) הוא כלי לניתוח סטטי, הסורק את קוד המקור מבלי להריץ אותו, במטרה לאתר שגיאות פוטנציאליות, חריגות ממוסכמות סגנוניות ודפוסי קוד חשודים.
כיום, לכל שפת תכנות קיימים כלי לינטר משלה, והם הפכו לחלק בלתי נפרד מכל תהליך פיתוח מקצועי.

Ruff הוא כלי לניתוח סטטי של קוד בשפת Python, המספק ניתוח מהיר ומקיף של הקוד שלכם.
הכלי בוחן את הקוד מול קבוצה של כללים מוגדרים מראש ושיטות עבודה מומלצות (best practices), ובכך מסייע לזהות ולתקן בעיות בשלב מוקדם של מחזור הפיתוח.
Ruff כולל מספר רב של כללים מובנים המכסים מגוון רחב של תקני כתיבת קוד ושיטות עבודה מומלצות, מה שהופך אותו לכלי מקיף להבטחת איכות הקוד שלכם.

5. What are e2e testings? What are **tests** in software development, and why are they important?  
   Explain unit tests, integration tests, and the role of automated testing. What are **mocks**, and why are they used in testing?  
   Compare **pytest** with other Python testing frameworks and explain its advantages.

בדיקות E2E הן מתודולוגיה לבדיקות תוכנה שמעריכה את הפונקציונליות המלאה וזרימת הנתונים של יישום או תוכנה.
יישום תוכנה יכול להיות מורכב מתת-מערכות או שירותים המיושמים כמוצר או שירות שלם.
בדיקות E2E מאמתות את היישום כולו על ידי בדיקת כל הרכיבים והאינטגרציות עם מערכות, שירותים, מקורות נתונים וממשקי API אחרים.
הן חשובות כי, כמו, מה אם המוצר שלנו נכשל בprod, כמו שאנחנו צריכים לבדוק אותו לפני הprod כי כמו "hi" - א. מטוק, מס"א.

בדיקות יחידה עוסקות בבדיקת פונקציה/חלק ספציפיים של הפונקציה שלנו; הן קטנות, ומטרתן היחידה היא לבדוק אם הפונקציה עובדת.
בדיקות אינטגרציה דומות לבדיקות E2E אך קטנות יותר; הן בדרך כלל בודקות רכיב שלם או את האינטגרציה בין פונקציות מסוימות.

בדיקות אוטומטיות הן הנוהג של שימוש בכלי תוכנה כדי להריץ את הבדיקות שלך באופן אוטומטי, במקום שאדם ילחץ עליהן ידנית.
כך שתוכל לבדוק שאפליקציה עדיין עובדת בכל פעם שהקוד משתנה.
זה לא מחליף בודקים; במקום זאת, זה מוריד את הבדיקות החוזרות ונשנות, הניתנות לסקריפט, מהצלחת שלהם כדי שהם יוכלו להקדיש זמן לעבודה שרק אדם יכול לעשות.

בדיקות נתונים מחקות את התנהגותן של תלויות אמיתיות כדי לבודד ולבדוק יחידות קוד ספציפיות.
בניגוד לאובייקטים אמיתיים, בדיקות נתונים הן קלות משקל, ניתנות להגדרה, ולעתים קרובות משמשות לאימות האינטראקציות בין רכיבים - ולכן הן משמשות בבדיקות.

pytest הוא הסטנדרט בתעשייה לבדיקות פייתון מכיוון שהוא מבטל קוד בסיסי, מציע מתקנים מודולריים רבי עוצמה ומתגאה במערכת אקולוגית של מעל 800 תוספים.
בעוד ש-unittest המובנה של Python אינו דורש התקנה כלל וכלים מיוחדים כמו Robot Framework או Behave משמשים גם עבור אנשים שאינם מפתחים, pytest מספק את האיזון הטוב ביותר בין פשטות וגמישות עבור רוב פרויקטי Python.

---

### 🔄 Alternatives
Assignment: Research and briefly compare **two development approaches or tools** mentioned above.

Examples:
- FastAPI vs Flask
- Interpreted languages vs compiled languages

Deliverable:
- A short written comparison (1–2 sentences).
- Include a **real-life use case** for each alternative.

Goal:
Be able to explain **why a specific tool or development approach would be chosen in a real system.**

---

### 🎯 User Story & Scenario
Assignment: Based on your research, describe a small example of a **Python service or tool**.

Deliverable:
Two short paragraphs describing:

- A realistic scenario where a Python service is required.
- How testing (pytest), mocking, and clean code practices would be applied.

