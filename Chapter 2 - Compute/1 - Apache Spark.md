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


The 3 main components are the Spark Driver, the Spark Executor, and the Cluster Manager.

The Driver is the master, while the Executor is the slave in the master-slave relationship.

The application communicates with the Driver via a session; once the Driver understands and optimizes the query, it splits it into tasks and assigns them to Executors.

The Driver partitions the total data for each task before assigning it; if a task fails, the Driver must reassign it to another Executor.

The Driver plans a job and makes sure that it’s executed; however, it will rarely touch the data itself.

The Executor can process multiple tasks in parallel - as many tasks as the CPU cores the Executor has.

A data shuffle happens when multiple Executors shuffle the data between them to make their tasks more efficient; it also happens once all tasks finish running in parallel, and if there’s a result [ie an output is expected], it’s sent back to the Driver.

Gathering all data received from all Executors into 1 Executor is also a task, and taking any action on that data is a task.

The spark-submit script is used to launch applications on a cluster.

The cluster manager is an application that provides the resources for an execution, and it will usually happen under the hood.

The cluster manager is usually either K8S, YARN, standalone, or Mesos.

The Driver and the Executor can run in 3 deployment modes:

1. Local deployment mode - Driver and Executor on my computer
    
2. Client deployment mode - Driver on my computer and Executors in datacenter/cloud
    
3. Cluster deployment mode - Driver and Executor on datacenter/cloud
    

Transformations are business logic we want to apply to our data; they are lazy, meaning they don’t happen unless Spark has to do them [by using an action].  
The two types of transformations are: Narrow Transformations - Filter, Select, Create new col, Cast, and Wide Transformations - Group By, Sort, Join.

Actions are demands for results; these are operations that kick off the computation itself.

Examples include Collect, Count, Save, Take, Show.

The difference being the forcing nature of Actions vs the lazy nature of Transformations.

Lazy evaluation is a feature in Spark, which holds off on executing transformations until an action is executed.

Once an action is run, Spark will run a couple of optimizations on our query, like moving transformations like filter to the earliest point possible, implementing Catalyst Optimizer’s optimizations, and applying Tungsten’s CPU and memory optimizations.

Once the RDD is finalized, the Driver partitions the total data given to tasks before assigning said tasks to Executors where they will run.

The 3 concrete steps are:

1. Resolving your logical plan  
    The catalyst optimizer makes sure all your references make sense - It’s a series of verifications.
    
2. Optimizing your logical plan  
    The catalyst optimizer figures out several efficient logical plans, i.e., when to filter your data, and applies other optimizations such as constant folding and predicate pushdown.
    
3. Translating to a physical plan  
    There are now several optimized logical plans - some are more optimal than others depending on your resources.  
    Spark looks at your cluster, figures out how much resource and execution time different plans require, then selects the most cost-efficient one given your available resources.
    

A Directed acyclic graph is a Spark job that has 1 or more stages, and each stage is split into 1 or more tasks.  
DAGs are the actual “big picture” job that Spark has to execute.

A Job can be parallel or sequential; stages are sequential, and Tasks can run in parallel.  
Data shuffle is a boundary between stages.

We use DAGs for fault tolerance because if any operation is going on and all of a sudden any RDD crashes, with the help of the cluster manager, we will identify the partition in our DAG where the loss occurs.

It’s also used for scheduling due to it being a directed and non-circular [acyclic] “plan”.

[Before Spark 2.0] SparkContext is the entry point for Spark applications.  
It represents the connection to a Spark cluster and is responsible for coordinating and managing the resources required for executing tasks.  
SparkContext helps in setting up the environment and is a gateway to interact with Spark's low-level API. 

[After Spark 2.0] SparkSession is a unified entry point for reading data, creating DataFrames, working with Spark SQL, and using the Dataset API.  
SparkSession combines the functionality of SparkContext, SQLContext, and HiveContext into a single object, providing a more consistent and efficient interface for working with Spark.

The 2 main differences between the two are the amount of API support SparkSession gives compared to SparkContext and the simplification of the interface in SparkSession.


2. **Spark Planning & Optimization:** Logical vs. Physical Planning — walk through the transition from Logical Plan to Physical Plan. What is the fundamental difference between Rule-Based (RBO) and Cost-Based (CBO) optimization, and what are the common kinds of optimizations used? What is AQE? Why is running `ANALYZE TABLE` recommended for performant CBO? And what is whole-stage code generation?

The transition from logical to physical planning is this:

1. Resolving your logical plan  
    The Catalyst optimizer makes sure all your references make sense - It’s a series of verifications.
    
2. Optimizing your logical plan  
    The Catalyst optimizer figures out several efficient logical plans, i.e., when to filter your data, and applies other optimizations such as constant folding [replacing constants saved as 2*3 into just 6] and predicate pushdown [making the filters earlier].
    
3. Translating to a physical plan  
    There are now several optimized logical plans - some are more optimal than others depending on your resources.  
    Spark looks at your cluster, figures out how much resource and execution time different plans require, then selects the most cost-efficient one given your available resources.
    

Rule-Based Optimization applies a set of predefined rules to optimize the query plan.  
These rules identify certain patterns in the query & replace them with optimized alternatives.  
Ex.: Predicate pushdown, constant folding, etc.

Cost-Based Optimization assesses the cost of different query plans based on stats, distribution & available resources.  
It will then choose the plan with the lowest cost.  
Ex.: Join reordering, Index selection, etc.  
To enable this, we need to set spark.sql.cbo.enabled to true.  
Also, individual settings like spark.sql.cbo.joinReorder.enabled

  

Common optimizations that Spark does are:

- Spark distributes data processing across multiple Executors.  
    Partitioning is how Spark distributes data, making it perhaps the most fundamental optimization technique.
    
- Caching and Persistence - Stop Recomputing the Same Thing
    
- Broadcast Joins: Eliminating Expensive Shuffles
    
- Joins create performance bottlenecks in Spark applications due to data shuffling.
    
- Serialization: Optimizing Data Transfer
    
- Columnar Formats: Optimizing Storage and Retrieval
    
- Vectorized UDFs: Speeding Up Custom Functions
    
- Using the DataFrame API, which provides better optimization opportunities than RDDs.
    
- Speculative Execution - speculative execution launches backup tasks for slow-running tasks, taking results from whichever finishes first.
    

Adaptive Query Execution recalculates certain optimizations [reoptimizations] from the Catalyst Optimizer upon large changes during query execution.

The ANALYZE TABLE statement collects statistics about one specific table or all the tables in one specified database that are to be used by the query optimizer to find a better query execution plan; said statistics are stored in the catalog.

Whole-Stage Java Code Generation is a physical query optimization in Spark SQL which improves the execution performance of a query by collapsing a query tree into a single optimized function.


3. **Spark Shuffle & Joins:** Compare the different kinds of joins — when will Spark use each, and how can we tell Spark to prefer one over another? What is join reordering? Why is "broadcasting" considered a high-risk, high-reward optimization? What is a *Narrow* transformation and a *Wide* transformation? Why do some operations require a shuffle? What exactly is written in a shuffle?

Inner Join - The inner join is the default join in Spark SQL. It selects rows that have matching values in both relations.

Left Join - A left join returns all values from the left relation and the matched values from the right relation, or appends NULL if there is no match. It is also referred to as a left outer join.

Right Join - A right join returns all values from the right relation and the matched values from the left relation, or appends NULL if there is no match. It is also referred to as a right outer join.

Full Join - A full join returns all values from both relations, appending NULL values on the side that does not have a match. It is also referred to as a full outer join.

Cross Join - A cross join returns the Cartesian product of two relations.

Semi Join - A semi join returns values from the left side of the relation that have a match with the right. It is also referred to as a left semi join.

Anti Join - An anti join returns values from the left relation that have no match in the right. It is also referred to as a left anti join.

Syntax: relation [ Join Type/blank for inner ] JOIN…

Join reordering is reordering the joins so we are always joining the smaller element into the larger element to save compute, and if there are multiple joins, then we will order them with the same thought in mind.

  

A broadcast join is a join where a small dataset is broadcast to all Executors, allowing it to be efficiently joined with a larger dataset without shuffling data across the network.

It’s high risk because it only works well [without OOM errors] when all Executors can fit into their memory, but it is high reward because it will work much, much faster.

  

Narrow Transformations - the data required to compute the records in a single partition of the parent RDD is available in only one partition; no shuffling involved.

Wide Transformations - the data needed to compute the records in a single partition may reside in multiple parent partitions.  
In a data shuffle, 2 files are written per task:

shuffle_0_X.data    ← All partitions from map task X, concatenated

shuffle_0_X.index ← Byte offsets for quick lookup


4. **Tungsten, Abstractions & Memory:** What is an RDD? Why did Spark move away from RDDs in favor of DataFrames/Datasets? Explain how Tungsten uses off-heap memory to avoid Garbage-Collection pauses. Why is it a bad idea to give one executor a lot of resources (the "Fat Executor" problem)? What is the difference between Execution/Storage memory and overhead memory, and what happens when a task exceeds its allotted execution memory? In PySpark specifically, where does the Python worker's memory live relative to the JVM heap — and why can heavy Python UDFs cause memory trouble the JVM heap won't show? On Kubernetes, how does all of this relate to `memoryOverhead` and to a pod being `OOMKilled`?

RDD - Resilient Distributed Dataset, meaning it’s immutable, and this helps make Spark fault-tolerant; it can only be communicated with the data via the RDD API.

It was moved away from because it’s not optimized by default and “a pain in asshole to write”.

DataFrames - SQL-like API alternative to RDD, optimized by Catalyst Optimizer.

DataSet - further optimized, only for Scala, also optimized by the Catalyst Optimizer.

Tungsten is an optimizer that generates optimized code with the goal of improving Spark jobs’ CPU and memory efficiency.

Because of Tungsten’s optimizations, there is less GarbageCollector pressure as it uses Off-heap management, which reduces constant object allocation.

  

A Fat Executor is an Executor that has large/maximum resources; the basic idea of having this Executor is to provide maximum resource allocation for each task.

Whilst it is good for CPU/memory-intensive workloads, it’s dogshit at parallelism, and increases the risk of GC issues if too big.

  

Overhead memory is used for Spark’s internal operations such as serialization/deserialization of data, network buffers for shuffle operations, and other JVM-level necessities.

  

Execution Memory:

Used for active computations: running tasks, shuffles (sorting, hashing, aggregating data), joins, and any calculations defined in your Spark jobs. Buffers for reading data and for shuffle operations reside here.

Storage Memory:

Used for caching data: when you call .cache() or .persist() on a DataFrame or RDD, the data partitions are stored here (in RAM by default). This also holds broadcast variables. Caching helps speed up iterative algorithms and frequently accessed datasets by avoiding recomputation.

If execution memory is insufficient even after borrowing from storage, Spark will spill data to the node’s local disk, leading to slower performance due to I/O overhead.

  

The Python worker’s memory is from the Memory Overhead region, and when the memory cap is reached, the worker starts writing to disk.

The JVM heap itself might be fine, but off-heap allocations, Python workers, or native libraries pushed the container past its limit.

In K8S, the spark.kubernetes.memoryOverheadFactor will set how much memory will be allocated to non-JVM memory [Python worker, which is off-heap]; therefore, if it’s too low, it might cause some Python worker pods to receive an OOM error.


5. **Spark Skew, Partitioning & Caching:** What is data skew, and how can it be solved? What is the difference between `repartition(n)` and `coalesce(n)`? What are the Spark `StorageLevel`s? What is the difference between `cache` and `persist`? Why are UDFs (especially in Python) bad, and how does Spark address the serde bottleneck with UDFs?

Data skew is when processing a dataset in Spark, you group the data by a key, each partition should be roughly equal in size, however, if one instance of the key appears far more frequently, the data associated with said key could end up in a single partition, leading to an imbalance.

It causes 3 issues:

1. Creates Stragglers - Tasks that process larger partitions will be slower.
    
2. Resource Imbalance - Some nodes in the cluster might be underutilized while others are overwhelmed.
    
3. Out of Memory Errors - Skewed partitions may require more memory than is available.
    

The solutions:

Salting - adding a random component to the skewed keys, creating multiple unique keys to distribute the data more evenly across partitions.  
  

Splitting Skewed Data - identifying the skewed keys and processing them separately. This technique allows you to handle the skewed data without affecting the rest of the dataset.  
  

Increasing the Number of Partitions - by increasing the number of partitions, you can distribute the data more evenly across the cluster, reducing the load on any single partition.

  

The repartition(N) transformation is used to either increase or decrease the number of partitions in a DataFrame to N.

Pros:

- Even Data Distribution: Because it shuffles all the data, repartition() tends to create new partitions that are roughly equal in size.
    

Cons:

- Expensive: The full shuffle makes it a resource-intensive and time-consuming operation.
    

  

The coalesce(N) transformation is primarily used to reduce the number of partitions in a DataFrame to N.

Pros:

- Faster for Reducing Partitions: Significantly faster than repartition() when the goal is just to decrease the partition count.
    

Cons:

- Can Lead to Uneven Partitions: Since it merges existing partitions without a full reshuffle, if the original partitions were uneven in size, the coalesced partitions might also be uneven. This can impact subsequent operations if they are sensitive to data skew.
    
- Primarily for Decreasing: Its main optimization shines when shuffle=False (the default) and you're reducing partitions.
    

StorageLevel is a flag that accompanies every RDD; it records whether to use memory, whether to drop the RDD to disk if it falls out of memory, whether to keep the data in memory in a Java-specific serialized format, and whether to replicate the RDD partitions on multiple nodes.

  

The Cache() method is used to cache the intermediate results of the transformation so that other transformations run on top of the cached DataFrame. 

Persist is a superset of Cache; it also takes an argument.  
If no argument is given, it will act like the cache method since, with default configuration, it saves the DataFrame to MEMORY_AND_DISK storage level.  
By explicitly passing the storage level, we can change this location where the data is saved.

  

User-Defined Functions are user-programmable routines that act on one row.

They are bad in Python because Spark’s built-in functions

- run inside the JVM
    
- vectorized
    
- optimized by Catalyst
    
- benefit from codegen
    
- support predicate pushdown
    
- prune unneeded columns
    

Python UDFs

- break all of the above
    
- force Spark to serialize every row
    
- send it to a Python worker
    
- wait for Python to finish
    
- serialize the output again
    
- send it back
    
- repeat this millions of times
    

So they are BAD 😔

Solution: Write the UDF in native Spark functions.


6. **Configuration & Tuning:** What configs would you expect to set for a typical job, and how do they shape its parallelism and memory? What is dynamic allocation, and what does it rely on (keeping in mind there is no external shuffle service on Kubernetes)? When the same setting is defined in more than one place — in the SparkSession, injected by Airflow, and in `spark-defaults` — how does Spark decide which one wins, and which settings can't be changed once the application has started? If a tenant sets a config and it seems to have no effect, how would you investigate — and how do you check what configuration a running application actually has?

Important configurations:

- spark. Executor.memory: Sets the memory for each Executor process. spark. Driver.memory: Specifies the amount of memory for the Driver process.
    
- spark.Executor.cores: Sets the number of cores for each Executor process.
    
- spark.Driver.cores: Sets the number of cores for the Driver process.
    
- spark.default.parallelism: Specifies the default parallelism.
    
- spark.Executor.instances: Specifies the number of Executor instances.
    
- spark.yarn.am.cores: Specifies the number of cores for the YARN Application Master.
    
- spark.yarn.Executor. memoryOverhead: Specifies the memory overhead for each Executor in YARN.
    
- spark.yarn.Executor.cores: Sets the number of cores for each Executor in YARN.
    
- spark. yarn.maxAppAttempts: Specifies the maximum number of attempts for an application in YARN.
    
- spark.yarn.queue: Specifies the queue for the application in YARN.
    
- spark.dynamicAllocation.enabled: Enables/disables dynamic resource allocation.
    
- spark.dynamicAllocation.minExecutors: Sets the minimum number of Executors for dynamic allocation.
    
- spark.dynamicAllocation.maxExecutors: Sets the maximum number of Executors for dynamic allocation.
    
- spark.sql.shuffle.partitions: Specifies the number of partitions for shuffles in SQL.
    
- spark.shuffle.spill: Enables/disables spilling of data to disk during shuffles.
    
- spark.shuffle.spill.compress: Enables/disables compression for spilled data during shuffles.
    
- spark. Driver.maxResultSize: Sets the maximum size of results that the Driver can accumulate before releasing them.
    
- spark.Executor.heartbeatInterval: Specifies the interval for heartbeats between the Executor and Driver.
    
- spark.network.timeout: Sets the network timeout for communication between nodes.
    

  

Spark provides a mechanism to dynamically adjust the resources your application occupies based on the workload. This means that your application may give resources back to the cluster if they are no longer used and request them again later when there is demand. This feature is particularly useful if multiple applications share resources in your Spark cluster.

This feature is disabled by default and available on all coarse-grained cluster managers, i.e., standalone mode, YARN mode, Mesos coarse-grained mode, and K8s mode.

  

Standalone – a simple cluster manager included with Spark that makes it easy to set up a cluster.

Apache Mesos – a general cluster manager that can also run Hadoop MapReduce and service applications. (Deprecated)

Hadoop YARN – the resource manager in Hadoop 3.

K8S – an open-source system for automating deployment, scaling, and management of containerized applications.

  

Airflow takes priority, SparkSession is next, and then it’s spark-default - the more specific the configuration is set, the greater its override.

SparkSession can’t be changed mid-application running.

  

If a configuration is set, first check with the tenant that it has been saved, then it should be checked if it was overridden in one of those 3 options.

שאלות סקילה 1 יא אוטיסט:

השוואה בין pandas, polaris וspark - מה הuse case, יתרונות [spark-standalone], חסרונות, משהו מעניין על כל אחד.

|                                |                                    |                            |               |
| ------------------------------ | ---------------------------------- | -------------------------- | ------------- |
| Polars                         | Pandas                             | Spark                      |               |
| No complex infra but very fast | No complex infra, the simplest one | A lot of data very quickly | Use Case      |
| Optimization phase             | Runs immediately                   | Optimization phase         | Advantages    |
| Not scalable                   | No optimization phase              | Complicated                | Disadvantages |


מה קורה clientside אחרי SPARK SUBMIT

מודפסים הרבה לוגים של הspark instance עולה ולאחר מכן צריך להיכנס לsparkshell [באמצעות spark-shell] או להיכנס לshell אחר של spark, לדוגמא - pysparkshell [באמצעות pyspark].

  

איזה פרמטרים Spark submit מקבל

- --class: The entry point for your application
    
- --master: The master URL for the cluster
    
- --deploy-mode: Whether to use cluster or client deployment mode (default: client)
    
- --conf: Arbitrary Spark configuration property in key=value format. application-jar: Path to a bundled jar including your application and all dependencies.
    
- application-arguments: Arguments passed to the main method of your main class, if any.
    

  

לחקור קצת על Scala

Scala is an OOP and a highly scalable FUN language, and in it everything is a value.

  

איפה קוד Scala רץ

רץ על הJVM

  

לקרוא על quirckים של כתיבה בPySpark

PySpark has integrations with other Python libraries [pandas, numpy]

Spark operations compile straight to bytecode, whereas custom Python code [Which is essentially UDFs] requires serialization across the Python-JVM boundary, adding some overhead.

  

מה זה Apache Arrow*

  

הבדלים בין DataSet וDataFrame

RDD - the most basic data frame; it’s [effectively] simply a partitionable array of data.

DataSet - it is a structured RDD, very similar to a spreadsheet, SQL table, or a dict.

DataFrames - very similar to a dataset but are structured columnarily and further optimized.

  

תכלס מה ההבדל בין repartitioning וcoalesce

Coalesce לא יעביר מידע כל עוד הוא יכול בין exexcutorים לעומת repartitioning שיעשה partitioning לכל המידע מחדש

  

יתרונות של spark על mapreduce

לאחר כל שלב של Map ו-Reduce, היה צורך לכתוב את הנתונים לדיסק, דבר שגרם לעיכובים, מה שאין בspark.

Complex Pipelines

שרשור של מספר משימות MapReduce לצורך ביצוע מטלות מורכבות מסורבל לעומת בSpark שהוא פשוט באמצעות DAG.

  

מה זה checkpoint

Checkpointing היא פעולה של שמירת הDataFrame בדיסק, כך שפניות עתידיות לDataFrame זה יצביעו על הpartitions המאוחסנות בדיסק, במקום לחשב מחדש את הDataFrame ממקורו המקורי.

  

מה זה persist וcache

Cache() משמש לcaching של תוצאות הביניים של הטרנספורמציה, כך שטרנספורמציות אחרות יוכלו לפעול על גבי הDataFrame השמור בcache.

Persist() הוא הרחבה של Cache(); הוא יכול לקבל ארגומנט נוסף.

אם לא מסופק ארגומנט, הוא יפעל בדיוק כמו Cache(), כי בקונפיגורציה, הdefault הוא שמירת הDataFrame בMEMORY_AND_DISK.

באמצעות ציון מפורש של StorageLevel, ניתן לשנות את המיקום שבו הנתונים נשמרים.





שאלות סקילה 2 אבל אני יודע לבשל 😝😝😝

  

מה יש בין py\java לscala - להסביר תקשורת

PySpark משתמש ב-Py4J כדי לתקשר עם ממשקי ה-API של JVM של Spark. הוא אינו מתרגם את Python ל-Scala; הוא קורא למימושים קיימים של Java/Scala. Spark מבצע עבודה מבוזרת על פקודות JVM, תוך שימוש ב-Workers נפרדים של Python כאשר נדרשים UDF של Python. 

  

מה זה persist ולמה הוא יותר טוב

אתה יכול לבחור איפה בדיסק לשמור את התוצאות של הtransformation

  

מה זה אומר שmapreduce הוא I/O Bound

שלוקח יותר זמן לקרוא\לכתוב לדיסק מאשר הפעולה עצמה.

  

לאן checkpoint שומר את השינויים ואיזה שיוניים נשמרים

Checkpointing היא פעולה של שמירת הDataFrame בדיסק, כך שפניות עתידיות לDataFrame זה יצביעו על הpartitions המאוחסנות בדיסק, במקום לחשב מחדש את הDataFrame ממקורו המקורי.

  

למה אי אפשר לשלוח שאילתות SQL פשוטות לSpark

Spark SQL בנוי לOLAP, לעומת SQL רגיל שבו עדיף OLTP, בנוסף, SparkSQL יודע להתמודד עם עם Data Formats כמו Parquet/JSON.

  

מתי TypeErrors בSpark

כאשר הנתונים אינם type-safe, שום דבר לא מונע מהcompilers לאמת את הData Types - מצב העלול להוביל לType Error.

  

איך Predicate pushdown מומש - ספציפית Hive-HDFS

אופטימיזציית Catalyst של Spark דוחפת את המסננים קרוב יותר למקור הנתונים. עם טבלאות Hive ב-HDFS, גיזום מחיצות מדלג על מחיצות שלמות, בעוד שקוראי Parquet/ORC יכולים לדלג על גושי נתונים לא רלוונטיים. HDFS עצמו אינו מעריך פרדיקטים.


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
