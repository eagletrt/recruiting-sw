# IT & Automation Recruitment Task 2
---

## Task Description
You will be given access to an **empty Ubuntu Server VM**. On this VM, you are required to:  

1. **Set up a GitHub self-hosted runner**:  
   - Connect the runner to your personal GitHub repository.  
   - Ensure it is correctly registered and can execute jobs from your repo.  

2. **Set up a local Docker Registry** on the VM:  
   - This registry will serve as a private storage for Docker images built by your pipelines.  

3. **Prepare a sample project**:  
   - Push a simple application (choice is up to you: e.g., a small Python/Node.js/Go web service, or any lightweight program) into your repository.  

4. **Create a GitHub Action workflow**:  
   - The action must run on your **self-hosted runner** (not GitHub’s hosted runners).  
   - It should build a Docker image of your application from the repository’s code.  
   - After building, the workflow must push the image to the **local Docker Registry** running on your VM.  

---

## Objective
By completing this task, you will demonstrate the following:  
- Ability to configure and register GitHub self-hosted runners.  
- Familiarity with Docker and container registries.  
- Understanding of CI/CD workflows in GitHub Actions.  
- Knowledge of image publishing to a private registry.  
- Ability to document a reproducible setup and automation pipeline.  

---

## Tools and Resources
- **Virtual Machine**:  
  - OS: Ubuntu Server (pre-installed).  
  - VM will be created and credentials provided by us.  

- **GitHub**:  
  - A personal repository under your account (you will create or use an existing one).  
  - GitHub Actions workflows defined in `.github/workflows/`.  
  - Documentation: [https://docs.github.com/actions](https://docs.github.com/actions).  

- **Self-Hosted Runner**:  
  - Runner setup guide: [https://docs.github.com/actions/hosting-your-own-runners/about-self-hosted-runners](https://docs.github.com/actions/hosting-your-own-runners/about-self-hosted-runners).  

- **Docker**:  
  - Local registry setup guide: [https://docs.docker.com/registry/](https://docs.docker.com/registry/).  
  - Useful ports: default registry runs on `5000` (e.g., `http://<vm-ip>:5000`).  

---

## Initial Setup Guidelines
1. **Update the VM**:  
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. Install Docker and Docker Compose
3. Set up the Docker Registry
4. Install GitHub Runner
    - Download the latest runner from GitHub on your VM.
    - Configure it to connect to your personal repository.
    - Ensure the service is running and available for workflows.
5. Verify installation
    - Run a test job on the runner (e.g., a simple workflow that echoes text, or some more articulated examples).
    - Test pushing/pulling an image to/from the registry (docker push / docker pull).


## Deliverables

- A configured **self-hosted GitHub runner** connected to your personal repository.  

- A **Docker registry** running on your VM.  

- A **sample project** in your repository with a functional **Dockerfile**.  

- A **GitHub Action workflow** that:  
  - Builds the Docker image of your project.  
  - Runs on the self-hosted runner.  
  - Pushes the image into the local Docker registry.  

- A **README file** containing:  
  - Step-by-step setup and configuration instructions.  
  - Address and port of your local registry.  
  - Example of pulling the pushed image from the registry.  
  - Notes on how to reproduce the pipeline in a fresh environment.  

