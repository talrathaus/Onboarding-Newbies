# Container Orchestration Foundations: Kubernetes & Helm

Before deploying production-grade services, it is important to understand how container orchestration works.

This module introduces Kubernetes and Helm as the standard tools for managing containerized applications at scale.

The goal is to understand *how systems are deployed, configured, and managed*, and to gain hands-on experience using real-world labs.

---

### ⏳ Timeline  
Estimated Duration: 2 Days  

**Day 0.5 – Theory & Concepts**  
- Kubernetes core architecture    
- Helm fundamentals and packaging
- Introduction to GitOps

**Day 1.5 – Hands-On Labs**  
- Kubernetes practical labs  
- Helm chart deployment  
- Debugging and inspection
- K8s & Openshift Concepts  

---

### 📚 Resources  
Use the resources below as your primary reference:

- [Kubernetes Documentation](https://kubernetes.io/docs/)  
- [Helm Documentation](https://helm.sh/docs/)  
- [OpenShift Documentation](https://docs.openshift.com/)
- [K8s & Openshift Concepts.md](https://github.com/netagolani/Onboarding-Newbies/blob/refactor/openshift/Chapter%204%20-%20Devops%20%26%20Devlopment/assets/K8s%20%26%20Openshift%20Concepts.md) - Must Knows

---

# Day 1 – Kubernetes & Helm Concepts

### ❓ Guide Questions

1. What is Kubernetes, and what problems does it solve compared to running containers manually on vm?  

Kubernetes is a container orchestration platform that automates the deployment, management, and scaling of containerized applications.
It eliminates the manual steps required to configure and run applications or allocate resources.

Kubernetes is focused on container orchestration - compared to running containers manually on VMs, K8S operates at the infrastructure level, managing how containers are deployed, scaled, and maintained across clusters of machines.
It also schedules containers based on available resources, monitors application health, restarts failed containers, and handles networking so distributed applications continue running smoothly.

2. Describe the main Kubernetes components and architecture.  
   Include: cluster, nodes, control plane, kubelet, API server, etcd, controllers.

The 2 main components of a Kubernetes cluster are the control plane, which coordinates the nodes, and the worker nodes [which run container pods], which function in a master-slave architecture.

The control plane is built from:
- An API server - the front end for the Kubernetes control plane.
The main implementation of a Kubernetes API server is kube-apiserver, which can scale horizontally.
- etcd - Consistent and highly available key-value store used as Kubernetes' backing store for all cluster data.
- A Scheduler - watches for newly created Pods with no assigned node, and selects a node for them to run on.
- A Controller Manager - runs controller processes.
Each controller is a separate process, but they are all compiled into a single binary and run in a single process for simplicity; these include:
   - Node controller - notices and responds when nodes go down.
   - Job controller - watches for Job objects that represent one-off tasks, then creates Pods to run those tasks to completion.
   - ServiceAccount controller - creates default ServiceAccounts for new namespaces.
   - Node controller - checks the provider to determine if a node has been deleted in the cloud after it stops responding.
   - Service controller - For creating, updating, and deleting provider load balancers.

The node is built from:
- kubelet - runs on each node in the cluster.
It makes sure that containers are running “healthily” in a Pod.
The kubelet only manages Kubernetes-created containers.
- kube-proxy  - a network proxy that maintains network rules on nodes.
It uses the operating system packet filtering layer if there is one and it's available; otherwise, it forwards the traffic itself.
- Container runtime - responsible for managing the execution and lifecycle of containers within the Kubernetes environment.

3. You deploy a deployment specifying replicas: 3 to your cluster, but a node crash reduces the running pods to 2. How does the Kubernetes Controller Manager detect and resolve this discrepancy between the manifest and the cluster? (include `declarative manifest`, `reconciliation` and `controller managers` in your answer)

The Kubernetes controller continuously monitors node heartbeats.
If a node stops sending heartbeats, the controller identifies it as unresponsive and initiates the necessary recovery and resource-cleanup procedures.

It also operates through a reconciliation loop, continuously comparing the desired state defined in the declarative manifest with the cluster's actual state.
For example, if the manifest specifies 3 replicas but only 2 are currently running, the controller detects the discrepancy and creates an additional Pod to restore the desired replica count.

The kube-controller-manager is a critical component of the Kubernetes control plane.
It runs the various controllers responsible for continuously monitoring and maintaining the cluster's desired state.

4. What is Helm, and why is it used?  
   Explain charts, values.yaml, templating, and how Helm simplifies deployments.

Helm is a package manager for Kubernetes that makes it easy to deploy multipliable applications on a Kubernetes cluster.
It’s used because doing it just through Kubernetes is both hard to understand and hard to configure.

Helm charts are a collection of files that describe a Kubernetes cluster’s resources and package them together as an application.
They comprise three basic components: 
- The chart - `Chart.yaml` defines the application metadata like name, version, dependencies, etc.
- Values - `values.yaml` sets values, which is how you will set variable substitutions for reusing your chart
- The templates directory - `templates/` houses your templates and combines them with the values set in your values.yaml file to create manifests
- The charts directory - `charts/` stores any chart dependencies you define in Chart.yaml and reconstructs with helm dependency build or helm dependency update.

5. What is GitOps? Compare GitOps to DevOps. What is ArgoCD? Describe the basics operations in ArgoCD. Describe what is Iac and why do we need to use it? 

GitOps is a set of practices for managing infrastructure and application configurations to expand upon existing processes and improve the application lifecycle.
It uses Git repositories as a single source of truth.

GitOps gives you tools and a framework to take DevOps practices, like collaboration, CI/CD, and version control, and apply them to infrastructure automation and application deployment, as well as to platform engineering practices like internal developer platforms.

Argo CD: A declarative continuous delivery tool for Kubernetes. It allows development teams to deploy and manage applications without needing full knowledge of Kubernetes and full access to the Kubernetes system. By monitoring running applications, ArgoCD ensures that your applications do not fall out of sync with your desired state. 

Infrastructure as Code (IaC) is an automated approach to managing and provisioning IT infrastructure.

With IaC, you define your infrastructure specifications in configuration files.
This makes it easier to edit and distribute configurations at scale, while making sure you provision the same environment every time.
By codifying and documenting your configuration specifications, IaC aids configuration management and helps you avoid undocumented, ad hoc configuration changes.
IaC paves the way tforfaster scaling and flexibility.
You can release applications to production faster and spin up, scale, and take down infrastructure frequently.
IaC makes all of this possible while improving consistency and reducing errors that can happen with manual configuration.

---

# Day 2 – Hands-On Labs (Kubernetes & Helm)

### ⚠️ Important

There are **two versions of this exercise**:

- Internal lab (provided by the team)  
- External lab (public platforms)  

👉 **You must ask your mentor which version you are required to complete before starting.**

---

## 🧪 Lab Tasks (External Option)

### Kubernetes Core Practice

👉 Start here:  
- [KillerCoda Kubernetes Labs](https://killercoda.com/kubernetes)

**You must complete the following scenarios:**

- Kubernetes Basics  
- Kubernetes Pods  
- Kubernetes Deployments  

---

### 🎯 Required Skills (Must Demonstrate)

During the labs, you must perform:

- Deploy an application (nginx or similar)  
- Expose it using a Service  
- **Scale the deployment (replicas up/down)**  
- **Perform a Rolling Update (change image/version)**  
- Inspect logs and running pods  

---

### Helm Hands-On Lab

👉 Helm practice:  
- [KillerCoda Helm Labs](https://killercoda.com/helm)

Tasks:

- Install a Helm chart  
- Modify values.yaml  
- Perform upgrade  
- Uninstall release  

---

## 🔄 Alternatives

Assignment: Compare two Kubernetes deployment approaches:

- Helm Charts vs Raw Kubernetes YAML manifests

Deliverable:
- 1–2 sentences comparison  
- Include a real-world use case for each  

Goal:
Understand the trade-offs between templated/package-based deployments and manual resource definitions.

---

## 🎯 User Story & Scenario

Assignment: Describe a real-world Kubernetes deployment using Helm.

Deliverable (2 paragraphs):

- Describe a service (e.g., API) deployed to Kubernetes  
- Explain how deployment is managed using Helm (chart, values.yaml, releases)  
- Describe how Helm helps manage environments (dev/staging/prod) and simplifies updates (e.g., rolling upgrades)  

---

## 🎯 Deliverable

By the end of this module, you should have:

- Completed the assigned labs (internal or external, per mentor decision)  
- Successfully deployed and exposed an application in Kubernetes  
- Demonstrated scaling and rolling updates  
- Used Helm to install and manage an application  
- Demonstrated ability to inspect and debug workloads 
