## **How to Work Together**

This guide explains how to set up the repository and work together efficiently on our project.


### **Step 1: Setting Up Git**

If you don't have Git installed, follow these steps:

1. **Download Git**  
   - Go to the [Git website](https://git-scm.com/) and download the installer for your operating system.

2. **Install Git**  
   - Run the installer and follow the setup instructions.

3. **Check Git Installation**  
   - Open your terminal (Command Prompt, PowerShell, or a terminal on macOS/Linux).
   - Run the following command to verify Git is installed:
     ```bash
     git --version
     ```
     You should see a version number (e.g., `git version 2.x.x`).

4. **Configure Git**  
   Set your name and email for commits:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "youremail@example.com"
   ```

---


### **Repository Setup**

Follow these steps to set up the project repository on your local machine:

1. **Navigate to Your Desired Folder**  
    Before cloning the repository, navigate to the folder where you want the project to be stored. For example:
    ```bash
   cd /path/to/your/desired/folder
   ```

2. **Clone the Repository**  
   Open your terminal and run:
   ```bash
   git clone https://github.com/ymb287/HSG_BA_and_DS_Applications.git
   ```

3. **Navigate to the Repository**  
   Move into the project folder:
   ```bash
   cd HSG_BA_and_DS_Applications
   ```

4. **Start Working**  
   You're ready to contribute! Follow the workflow below.

---

### **How to Work on the Repository**

Each person (Jakob, Yannik, Sonya, Jules) works in their designated folder to keep things organized and avoid conflicts.

1. **Work in Your Folder**  
   Add all your work (notebooks, scripts, results, etc.) to your folder:
   - Jakob: `person_jakob/`
   - Yannik: `person_yannik/`
   - Sonya: `person_sonya/`
   - Jules: `person_jules/`

2. **Pull the Latest Changes**  
   Before starting any work, make sure you have the latest updates:
   ```bash
   git pull origin main
   ```

3. **Add and Commit Changes**  
   After making changes, save them to the local repository:
   ```bash
   git add .
   git commit -m "Descriptive message about your changes"
   ```

4. **Push Your Changes**  
   Upload your changes to GitHub:
   ```bash
   git push origin main
   ```

---


### **Best Practices**

1. **Stay Organized**  
   - Only work in your designated folder unless it's a shared file (in `shared/`).

2. **Use Shared Functions**  
   - Use standardized code from `shared/` for consistency.

3. **Pull First, Push Later**  
   - Always pull the latest changes before starting and push your updates once done.
