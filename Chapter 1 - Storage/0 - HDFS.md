# Hadoop Distributed File System (HDFS) :elephant:

## Overview
This session focuses on the core concepts of HDFS, the distributed storage layer of the Hadoop ecosystem. Understanding its architecture will help you appreciate how big data clusters store and manage massive datasets across many machines.

**Study the key components, design decisions, and how they work together to provide fault-tolerant, scalable storage.**

## Goals
- Learn the architecture and roles of HDFS components (NameNode, DataNode, etc.).
- Understand how HDFS handles storage, replication, and availability.
- Understand the disadvantages of HDFS, including potential bottlenecks, performance issues, and other possible challenges.
- Practice planning a self-study day and managing your time.

:warning: **Note:**
- This is a self-study day; independence and time management matter.
- Focus on grasping the full picture of each concept; if you can’t explain it, you haven’t learned it.
- When in doubt, consult your mentor about what to study.

### ⏳ Timeline
Estimated Duration: 3 Days
- Day 1-3: Learn the concepts of HDFS: purpose, historical context, architecture, fault tolerance and the client protocol: how reads and writes are performed.
    - Have a Q&A session on the third day and in between sessions every day

## Core Concepts

Consider the following five questions to cover the major HDFS topics:

1. **Architecture & Roles:**  Describe HDFS’s overall architecture, including NameNode(s), DataNodes, blocks, and how the namespace and metadata are managed. Explain how DataNodes send block reports, and why these mechanisms matter for everyday operations.
   
Blocks: קובץ HDFS מחולק למקטעים של 128 מגהבייט, הנקראים "בלוקים" (blocks), וככל הניתן, כל מקטע מאוחסן ב-DataNode שונה.
DataNodes: מאחסנים את המידע עצמו ב-HDFS בצורת blockים, העבדים.
NameNode: מאחסן metadata כגון מספר הblock, ובאיזה rack ואיזה DataNode(-ים) מאוחסן המידע עצמו, הmaster.
How namespaces are managed: NameNode מנהל את מרחב השמות של מערכת הקבצים. כל שינוי במרחב השמות או במאפייניו נרשם על ידי NameNode.
What are block reports: דוח שהDataNodes בcluster של Hadoop שולחים לNameNode, המכיל metadata על blocks הנשמרים באותו node.
מרווח הזמן של block reports נקבע על ידי ההגדרה dfs.blockreport.intervalMsec; כברירת מחדל - 6 שעות.
    משתמש בBlock reports למטרות הבאות
עיבוד block reportראשוני: עבור דוח ראשון מ-DataNodes שנרשמו זה עתה, המערכת מוסיפה את כל הreplicas התקינים.
עדכון מידע על blockים: המיפוי המקשר בין DataNode לבין הBlockים שלו מתעדכן ב-NameNode.  
    הblock report החדש מושווה לדוח הקודם, והמידע מתעדכן בהתאם.
זה משנה כי זה מראה שהמערכת מחדשת את עצמה כשיש בעיות
   
2. **Storage & Fault Tolerance:**  Explain how HDFS divides files into blocks, uses replication (default factor three), and how it detects and recovers from node failures.
   
משתמש בשכפול (default factor 3),  
לקוח כותב נתונים לקובץ HDFS עם replication factor של 3, הNameNode שולף רשימה של DataNodes, רשימה זו מכילה את הDataNodes שיארחו עותק של אותו block.
לאחר מכן, הלקוח כותב לDataNode הראשון:
הDataNode הראשון מתחיל לקבל את הנתונים בחלקים, כותב כל חלק למאגר המקומי שלו ומשכפל את אותו חלק לDataNode השני ברשימה.
הDataNode השני, מתחיל לקבל כל חלק של block, כותב אותו למאגר שלו, ואז מעביר אותו לDataNode השלישי.
הDataNode השלישי כותב את הנתונים למאגר המקומי שלו.
כך, DataNode יכול לקבל נתונים מהDataNode הקודם בpipeline ובו-זמנית להעביר נתונים לDataNode הבא בpipeline.
באופן זה, הנתונים מועברים בשיטת pipelining מDataNode אחד לשני.

כשל ב-NameNode:
במערכות Hadoop מודרניות, קיימים שני NameNodeים: active וstandby.
הstandby NameNode מבצע checkpoint תקופתית של מרחב השמות namespace של הactive NameNode.
הNameNodes חייבים להיות מסונכרנים זה עם זה בכל עת ולהחזיק באותם metadata.
זיהוי כשל בNameNode מתרחש כאשר הDataNode אינו מקבל תגובה לheartbeat שהוא שולח מדי 3 שניות (פרמטר הניתן להגדרה).
במקרה שבו ה-NameNode הפעיל קורס או מפסיק לפעול, ה-NameNode הסביל ייקח על עצמו את האחריות למתן שירות ללקוחות, ללא כל הפרעה.

כשל ב-DataNode:
DataNode שולח באופן רציף heartbeat לNameNode, מדי 3 שניות.
אם הNameNode אינו מקבל אות "heartbeat" מDataNode הactive במשך 10 דקות (כברירת מחדל), הוא יחשיב את אותו node כמת.
בשלב הזה, הNameNode יבדוק אילו נתונים היו באותו צומת כושל ויזום תהליך של replication.
3. **Block Placement & Performance:** How does HDFS replicate across nodes? Discuss how block placement, snapshots, and checksums contribute to performance and data integrity.
מדיניות המיקום של HDFS קובעת שיש למקם עותק אחד במכונה המקומית אם הכותב נמצא על DataNode, או בDataNode אקראי באותו rack שבו נמצא הלקוח, אם אינו נמצא על DataNode.  
עותק נוסף בDataNode הנמצא בrack מרוחק, ואת העותק האחרון בDataNode אחר באותו rack.
snapshots הם מעקב על השינויים שיעשו לאותו metadata של tree/subtree. 
זה לא מעתיק את את המידע.
שימושים נפוצים בsnapshots כוללים גיבוי נתונים והתאוששות מערכת.
כאשר לקוח יוצר קובץ ב-HDFS, הוא checksum עבור כל block בקובץ ומאחסן סכומים אלו בקובץ נסתר נפרד, באותו namespace של HDFS.
בעת שליפת תוכן הקובץ, הלקוח מוודא שהנתונים שהתקבלו מכל DataNode תואמים לchecksum המאוחסן, אם אין התאמה, הלקוח יכול לבחור לשלוף את הblock מDataNode אחר המחזיק בreplica של אותו block.
   
4. **High Availability:**  Outline HDFS High Availability (Active/Standby NameNode, JournalNodes). How do these features improve scalability and uptime? Don’t forget the role of ZooKeeper in coordinating HA and keeping track of leases. 

Active/Standby NameNode: ראה שאלה 2 - "כשל ב-NameNode"  
כדי שהStandby NameNode ישמור על סנכרון, שני הNameNodeים מתקשרים עם קבוצה של daemons הנקראים JournalNodes (או JNs).
כאשר הActive NameNode מבצע שינוי כלשהו בnamespace, הוא מתעד את השינוי באופן durably ברוב הJNs הללו.
הStandby NameNode מסוגל לקרוא את הedits מהJNs, והוא עוקב אחריהם באופן רציף כדי לזהות שינויים, עם קבלת השינויים, הStandby NameNode מחיל אותם על הקובץ fsimage והedits שלו.
במקרה של failover, הStandby NameNode יוודא שקרא את כל השינויים מהJN לפני שיעבור ממצב standby למצב active.

התכונות האלו מאפשרים לנו סקלביליות ואת הuptime של המערכת באמצעות זה ש:
1. אנחנו מוודאים שאין לנו single point of failure בכך שיש Standby Nodes
מה שמאפשר לנו גם סקלביליות וגם באותו הזמן משפר את הuptime של המערכת בכך שהיא שרידה לתקלות בNameNodes ולא רק בDataNodes [איפה שיש שכפול מידע].
בנוסף, יש לנו את ניהול הsessions בZooKeeper - כאשר הNameNode המקומי תקין, מחזיק גם znode מיוחד המשמש כ"נעילה".
   
2. **Client Protocol:**  Describe how clients read and write data to HDFS, how they locate NameNodes and DataNodes. Explain the read and write flow in detail: how the client initiates a connection to the cluster, which components it talks to and how ports of communication become known to the client. Explain the protocol alternatives available to the client:
    - What is native API?
    - What is HDFS CLI and what protocol does it utilize?
    - Can you talk to HDFS using REST/HTTP?

    What does a client need to connect to an HDFS cluster using each of the alternatives?
    
    What are the two main types of HDFS operations, and how do they differ in terms of the components they interact with?

Read:
1. הלקוח מבקש לקרוא את הקובץ מהNameNode
2. אוטנטיקציה
3. הNameNode שולח לו מאיזה DataNodeים הוא יכול לקרוא כל block ובאיזה סדר לקרוא.
4. הלקוח קורא את הblock מהDataNode הכי קרוב אליו, או לפי סדר הבלוקים או במקביל*.
Write:
5. הלקוח מבקש מהNameNode ליצור קובץ
6. אוטנטיקציה
7. הNameNode נותן מיקום של DataNode שאפשר ליצור בו את הקובץ
8. הלקוח כותב את הכותב לDataNode בצורת stream, שמפצל את הקובץ לblockים*.
9. הDataNode כותב את אותם blockים ל2 DataNodeים אחרים [הוא כותב לאחד והאחד כותב לאחד נוסף]
10. לאחר סיום כתיבת הקובץ לDataNode הראשון, הוא מחזיר ללקוח שנגמרה הכתיבה
11. הלקוח שולח לNameNode שנגמרת יצירת הקובץ
12. הNameNode מתעדכן מהDataNodes על הmetadata של הקובץ החדש.
-* חשוב לציין כי נעשת בדיקת checksum לולידיות הblock.
Port 50010 פתוח ב-DataNodes וPort 50070 פתוח ב-NameNodes.
הלקוח יוצר חיבור ליציאת TCP במכונת NameNode [פורט configurable].
הוא מתקשר עם הNameNode באמצעות הClientProtocol.
הDataNodes מתקשרים עם הNameNode עם הDataNode protocol.
Abstraction מסוג Remote Procedure Call - RPC, עוטפת את הClientProtocol ואת הDataNode Protocol,חשוב לציין כי NameNode לעולם אינו יוזם קריאות RPC, אלא הוא רק מגיב לבקשות RPC מצד DataNodes או לקוח.
WebHDFS הוא API RESTful של HDFS המבוסס על HTTP.  
HDFSCLI - אינטרפייס CLI לWebHDFS וhttpFS.
אפשר להשתמש בWebHDFS שהוא RESTful.
httpFS - WebHDFS server
הם דברים די שונים - WebHDFS הוא השרת וגם לקוח וhttpFS הוא רק הלקוח

Read וWrite
בRead נתקשר עם יותר מDataNode אחד לעומת בWrite ש[כנראה] נכתוב רק לDataNode אחד ישירות את הקובץ שלנו והוא יטפל בReplication.


1. Object storage VS file storage
   Object storage - large unstructured data
   File storage - hierarchical structured data

2. ping/ack equivalent in HDFS - specifically read and write
   how do we check who's alive as a namenode
   2 אופציות: fsck - בודק health check על node ספציפי וjps - בדיקת המצב של כל הnodes הרצים ב.hdfs
   how do i check if a datanode has finished recieving data - הוא מקבל איזשהו ack

3. What does the NameNode do with the block reports?
   אכלוס ותחזוקה של הmetadata catalog של הNameNode.

4. What is RPC?
   RPC הוא פרוטוקול שתוכנה יכולה להשתמש בו כדי לבקש שירות מתוכנה הנמצאת במחשב אחר.

5. RPC vs REST
   RPC: Action oriented - "קריאה לפונקציות", faster - ניתן לאפטם יותר
   REST: Resource oriented - CRUD, "נשלוף לפי "משאב, discoverable - לא coupled לurl, standardized - משתמש בhttp

6. What is Thrift?
   ששThrift היא Interface description language המשמשת לתקשורת RPC ומאפשרת פיתוח שירותים הפועלים בסביבות שפה שונות.

7. What is JN?
   כדי שהStandby NameNode ישמור על סנכרון, שני הNameNodeים מתקשרים עם קבוצה של daemons הנקראים JournalNodes (או JNs).
   כאשר הActive NameNode מבצע שינוי כלשהו בnamespace, הוא מתעד את השינוי באופן durably ברוב הJNs הללו.
   הStandby NameNode מסוגל לקרוא את הedits מהJNs, והוא עוקב אחריהם באופן רציף כדי לזהות שינויים, עם קבלת השינויים, הStandby NameNode מחיל אותם על הNamespace המקומי שלו.
   במקרה של failover, הStandby NameNode יוודא שקרא את כל השינויים מהJN לפני שיעבור למצב פעיל.


8. What exactly is sent to the JN?
   רשימה של השינויים שקראו על הDataNoeds

9. Where are the JNs saved?
   בNameNode

10. What are snapshots?
   snapshots הם מעקב על השינויים שיעשו לאותו metadata של tree/subtree
   זה לא מעתיק את את המידע

11. What are checkpoints?
   עcheckpoint היא המיזוג של השינויים האחרונים שבוצעו במערכת הקבצים עם הfsimage העדכני ביותר.

12. What are edit logs?
   רשימה של השינויים שהיו בDataNode מסוים

13. Where is the metadata saved?
   בRAM של הNameNode

14. Is the max block size configurable?
   yes: -D dfs.blocksize=XXX

15. What is ZKFC?
   ה-ZKFailoverController הוא רכיב העושה state machine לNameNode.
   כל מכונה המריצה NameNode מריצה גם ZKFC, ורכיב זה אחראי על:
- Health monitoring
- ניהול sessions
- election

16. What does zkfc actually do?
   name node health checks
   holds znode locks for active namenodes
   leader elections

17. What does JN do in failover [quorum]?
    NameNodes write edit logs through a quorum of JournalNode daemons instead of relying on shared storage so when a failover does happen all the changes have been approved by a quorum of jns.

18. What is safe mode?
   Safe mode is a read-only maintenance state that the NameNode enters automatically under certain conditions.
   During safe mode, the NameNode does not accept any write operations from clients - no new files, no deletions, no modifications.
   The cluster is alive but not fully serviceable.

19. What is short-circuit read?
   Reading a file directly over a datanode's disk instead of reaeding it through the datanode

20. What are quotas [1-2 sentences]?
   amount of files and max size of all files in a node/directory

21. What is ACL?
   רשימת הרשאות יותר מפורטת לhdfs, יכול להיות לקובץ ספציפי, לכל הdirectory או לכל הfilesystem

22. What is the name service?
   Nameservices can be either a stand-alone NameNode, a NameNode paired with a Secondary NameNode, or a high-availability pair formed by an active and a stand-by NameNode.

23. What is Google FS?*
   

24. Does simultaneous read return all the blocks at the same time [how does simultaneous read work]?*
   

25. What is reflection
   **רפליקציה זה כשאנחנו לוקחים את המידע ושומרים אותו בכמה מקומות**

26. Where is metadata saved in the namenod
   בRAM

27. what is a block report
   דוח שנשלח עם מידע על Data node registration  
מידע אודות הblockים, הכולל: מזהה הblock, אורך הblock, חותמת הזמן של יצירת הblock, ומצב הreplica של הblock.

28. what is rack awereness
   Rack Awareness היא בחירה של DataNodes הקרובים יותר לNameNode לצורך פעולות קריאה וכתיבה, במטרה למקסם את הביצועים על ידי הפחתת תעבורת הרשת.

29. what is checkpoint
   עcheckpoint היא המיזוג של השינויים האחרונים שבוצעו במערכת הקבצים עם הfsimage העדכני ביותר.
    אומרים לactive namenode להתחיל לרשום את הedits לקובץ חדש [edits.new]
    הstandby namenode לוקח את הקובץ edits והקובץ fsimage ועושה את כל השינויים של edits על הקובץ fsimage.checkpoint [שכפול של fsimage]  
    הקובץ fsimage.chcekpoint מועבר לactive namenoed, ובשני הnamenodes הקובצים הופכים להיות edits וfsimage

30. how is a fallen namenode identified
   הsequential ephemeral znode נפל והwatch שצופה בו יתריע על שינוי

31. How does the standby node know from where to continue
   הZKFC יודע לנהל את זה

32. What happens if the active node was in the middle of writing and it falls
   באסה, מה שנכתב כבר אולי אפשר להציל אבל השאר צריך לעשות append

33. What are leader elections
   אם הNameNode המקומי תקין והZKFC מזהה שאף NameNode אחר אינו מחזיק כרגע בznode של הlock znode, הוא ינסה להשיג את הlock בעצמו.  
אם הצליח בכך, משמעות הדבר היא שהוא ניצח בתהליך הleader elections וכעת הוא אחראי לביצוע תהליך הfailover כדי להפוך את הNameNode המקומי שלו לactive NameNode.

35. How does ack look in a heartbeat


36. what is configurable for max block size [dir, file, node...]
אפשר לעשות גם לdir כללי וגם לfile

37. what is configurable for quotas
directories

38. JN split brain
הJNs לא יאפשרו ליותר מnamespace אחד לכתוב אליהם ובך ימנע מהnamenode האקטיבי האחר לפעול

39. where is fsimage stored at
הNameNode מחזיק **בזיכרון** fsimage וBlockmap אבל מחזיק בfsimage [גם] ובedit logs בדיסק.

40. what is exec perms in hdfs
traversal access - היכולת לגשת לקובץ

41. what is default perms in hdfs
default ACL

42. what is mask perms in hdfs
	הmask היא רשומת ACL מיוחדת המסננת את ההרשאות המוענקות לכל רשומות המשתמשים והקבוצות בעלי השם, מרשומת הקבוצה ללא שם.

43. what is sessions in ZKFC
כאשר הNameNode המקומי תקין, הZKFC מחזיק בSession פתוח בZooKeeper.
אם הNameNode המקומי פעיל, הוא מחזיק גם בznode מיוחד המשמש כlock.
הlock הזה עושה שימוש בתמיכה של ZooKeeper בnodes מסוג ephemeral: אם הSession יפוג, הnode של הlock יימחק באופן אוטומטי.


### 🔄 Alternatives
Assignment: You are required to research and write a comparative analysis between HDFS and an industry alternative.
- Deliverable: A written summary (minimum 1 or 2 sentences).
- Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
- Goal: You must be able to justify why the department uses this tool for our specific environment.

### 🎯 User Story & Scenario
Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.
- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.


## Wrapping Up :trophy:
Review your answers with your mentor and discuss any unclear points. Relate these concepts back to real-world usage scenarios you might encounter.

## Action Items
- Note topics you want to investigate further.
- Prepare questions for the mentor Q&A session.
- Continue the Day 01 challenge by linking these HDFS concepts to other chapters.

## Recommended Resources
- [Official HDFS User Guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html)
- [Hadoop: The Definitive Guide (O'Reilly)](https://piazza-resources.s3.amazonaws.com/ist3pwd6k8p5t/iu5gqbsh8re6mj/OReilly.Hadoop.The.Definitive.Guide.4th.Edition.2015.pdf)
