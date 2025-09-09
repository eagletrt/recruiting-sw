# IT & Automation Recruitment Task 1
---

## Task Description
You will be given access to an **empty virtual machine (VM)** running **Ubuntu Server**. 
Your goal is to set up and configure a **NocoDB environment using Docker**. 
Once NocoDB is up and running, you will need to:

1. Import data into NocoDB using a **Python script**.  
   - Download the **JSON files** in this folder containing example data.  
   - Your Python script should parse the JSON and create the corresponding rows in NocoDB via the **REST API**.  
   - Make sure to correctly handle relationships between tables (e.g., one-to-one, one-to-many).  
   - As a **bonus**, you can implement support for **many-to-many relationships**.

2. Implement a **Telegram bot** that interacts with the NocoDB API.  
   - The bot should expose simple commands to demonstrate interaction, for example:  
     - Retrieving an **ODG (Ordine del Giorno)** (You can create a table with sample data for it).  
     - Adding a new user directly into the database.  
   - As a **bonus**, you may implement a command to update roles and permissions dynamically 

---

## Objective
By completing this task, you should demonstrate the following:
- Ability to set up and configure Dockerized services on a Linux VM.  
- Proficiency in interacting with REST APIs using Python.  
- Correct handling of database relationships (one-to-one, one-to-many, and optionally many-to-many).  
- Integration of third-party APIs (Telegram Bot API) with backend services.  
- Writing clean, maintainable, and well-documented code.  

---

## Tools and Resources
- **Virtual Machine**:  
  - OS: Ubuntu Server (pre-installed)  
  - Password: you will receive credentials separately.

- **NocoDB**:  
  - Run using **Docker** (docker-compose recommended).  
  - Documentation: [https://docs.nocodb.com](https://docs.nocodb.com)  
  - Default API Endpoint: `http://<vm-ip>:8080` (update based on your configuration).  

- **Python**:  
  - Libraries you may need:  
    - `requests` (to interact with NocoDB REST API)  
    - `python-telegram-bot` (to build the Telegram bot)  

- **Telegram Bot**:  
  - Use [BotFather](https://core.telegram.org/bots#botfather) to create a new bot and obtain an API token.  
  - Ensure you keep this token private.  

---

## Initial Setup Guidelines
Before starting the task, ensure the following steps are completed:  

1. Update the system
2. Install Docker and Docker Compose
3. Verify Python installation
4. Prepare your environment:

- Create a working directory for your project.

- Store your JSON data file in a structured location within the VM.

- Document any environment variables or secrets used (e.g., Telegram token, NocoDB credentials).


## Deliverables
- A *Docker setup* (docker-compose file or equivalent) that runs NocoDB successfully.
- A *Python script* capable of importing data from the provided JSON into NocoDB.
- A *Telegram bot* that integrates with NocoDB’s API and provides at least one working command.
- A *README file* that includes:
    - Step-by-step instructions to reproduce your setup.
    - Endpoint URL of the deployed NocoDB instance.
    - Link to NocoDB documentation.
    - Example usage of your Python script and Telegram bot.
    - Optional: description of any bonus functionality you implemented.
