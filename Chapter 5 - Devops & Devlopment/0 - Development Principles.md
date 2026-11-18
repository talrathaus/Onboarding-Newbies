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

4. What are the most common **programming** styles/paradigms (ex: Object-Oriented), what are the differences, and when should each be used?

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

2. Define the role of a **Pull Request (PR) / Merge Request**.
What is **squshing**? Why is it common practice to squash commits before the final merge?
Find how can you **apply specific fixes** from one branch to another without merging the entire history?
What is the process for **safely undoing** a merged PR using git revert?

3. Explain the difference between **CLI (Command Line Interface)** and
   **UI (User Interface)** applications.  
   What are the benefits of each?

4. What is the difference between a **compiler** and an **interpreter**?  
   Provide examples of languages that use each approach.

5. What is **event-driven programming**?  
   Explain how it differs from procedural execution and where it is commonly used.


> ⚠️ **Recommended exercise**  Please organzie your time and consider trying this git exercise [https://learngitbranching.js.org/]()
---

# Python & API Foundations

### ❓ Guide Questions

1. What is **Python**, and what are its main characteristics compared to other
   programming languages (for example c#)?  
   Discuss readability, ecosystem, and runtime behavior.
compare python uniuqe data type like Tuple vs. List.


2. What is a **REST API**?  
   Explain the core concepts such as resources, HTTP methods, and stateless communication.

3. **What is the Global Interpreter Lock (GIL) in Python?**  
   Explain:
   - What the GIL is and why it exists  
   - How it affects multi-threading and CPU-bound vs I/O-bound tasks  
   - Differences (if any) in how the GIL behaves across Python versions  
   - What Python 3.14 introduces regarding optionally disabling the GIL and why this is significant  
   - Common strategies to work around its limitations (e.g., multiprocessing)

4. What is a linter? read and explain about Ruff.

5. What are e2e testings? What are **tests** in software development, and why are they important?  
   Explain unit tests, integration tests, and the role of automated testing. What are **mocks**, and why are they used in testing?  
   Compare **pytest** with other Python testing frameworks and explain its advantages.

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

