# IT & Automation Recruitment Task 3
---

## Task Description
You will receive access to several **Ubuntu Server VMs**. On these machines, you are required to:  

1. **Set up a complete Kubernetes cluster**:  
   - Use standard Kubernetes (not simplified variants such as k3s or microk8s).  
   - Configure a master (control plane) node and at least two worker nodes.  
   - Ensure proper communication between nodes.  

2. **Deploy a containerized application**:  
   - Run a simple `hello-world` container on the cluster.  
   - Validate that the deployment works correctly across the cluster.  

3. **Document the entire process**:  
   - Provide a written report describing every step you performed.  
   - Include both the successful steps and the trial-and-error attempts that helped you reach the solution.  
   - Document any resources you consulted (guides, documentation, troubleshooting references).  

4. **Bonus**:
   - Deploy a test pod with ping/traceroute to ensure communication between nodes.
   - Deploy a test pod (like *nicolaka/netshoot*) to testing throughput on different nodes.
---

## Objective
By completing this task, you should demonstrate:  
- Competence in installing and configuring a full Kubernetes cluster from scratch.  
- Understanding of Kubernetes control plane and worker node architecture.  
- Ability to deploy and manage workloads within the cluster.  
- Strong documentation skills, including transparency of troubleshooting and learning process.  

---

## Tools and Resources
- **Virtual Machines**:  
  - Ubuntu Server (VMs provided after contact).  
  - Minimum 3 nodes required (1 control plane, 2 workers).  

- **Kubernetes**:  
  - Installation and setup: [https://kubernetes.io/docs/setup/](https://kubernetes.io/docs/setup/)  
  - Use `kubeadm` for cluster bootstrapping.  

- **Container Runtime**:  
  - Docker or containerd (depending on your setup).  

- **Networking**:  
  - Configure a Container Network Interface (CNI) plugin (e.g., Calico, Flannel, Weave).  

---

## Initial Setup Guidelines
1. **Update the system on each VM**:  
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. Install container runtime (Docker or containerd)
3. Install Kubernetes components (kubeadm, kubelet, kubectl)
    - Disable swap on all machines (sudo swapoff -a)
    - Configure version compatibility
4. Initialize the control plane node
5. Configure kubectl access for your user
6. Join worker nodes to the cluster
7. Install a network plugin (e.g., Calico)
8. Deploy the hello-world container


## Deliverables

- A **working Kubernetes cluster** (full k8s, not simplified distributions).  

- A **hello-world container** successfully deployed and running in the cluster.  

- A **detailed report** including:  
  - Step-by-step setup process.  
  - Resources and references used.  
  - Trial-and-error steps, with explanations of issues encountered and how they were solved.  
  - Verification of the final deployment.  
