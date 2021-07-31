Blue Library Manager

By:
Bridgette Bryant
Roland Chaumont
Paul Percifield
Nicholas Vitale

CS 4347.0W1



CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Requirements
 * Installation of MySQL
 * Installation of Python / Django
 * Import Required Files
 * Troubleshooting



INTRODUCTION
------------

Blue Library Manager (BLM) is a database host application that implements a Library
Management System using a backend SQL database. BLM is intended for librarians whom 
can then interface with the GUI to access various features. These features include:
 
 * A search interface to find a book using any combination of ISBN, author, and title.
 * Indication of availability of books, otherwise tracking when a book was checked out,
   generate a return date, and log check-in date.
 * Ability to check-out and check-in books using an ID system based on phone numbers.
 * A management system to create new users with unique IDs and library cards, using
   the new users' personal information.
 * Issue relevant fines to users with overdue books automatically, along with mechanisms
   to enter payment for fines and record payment of fines.



REQUIREMENTS
------------

 * Windows OS ver(8.1 or later)  OR  Mac OSX ver(10.9 or later)
 * Python ver(3.9.6 or later)
   download: https://www.python.org/
 * Django ver(3.2.5 or later), can be installed through Python.
   download: https://www.djangoproject.com/download/
 * MySQL database application. Download depends on OS system. 
   (see: Installation of MySQL)
 * GitHub account, will allow for easy implementation of the software.
   https://github.com/BridgetteBXP13/programming_project.git



INSTALLATION OF MYSQL
---------------------

Follow the guide for the OS present on the machine to install BLM on:

	##### Windows OS installation guide #####

 * Download MySQL database application for Windows: 
       https://dev.mysql.com/downloads/mysql/
   (Make sure to download for the correct processor on machine, 32-bit or 64-bit)

 * Extract the ZIP file to a location on disk (recommended C:\Program Files\), renaming
   the folder to something simple like "mysql" will simplify subsequent steps. This folder
   will be referred to as "mysql" from here on for installation purposes.

 * Add mysql\bin to the PATH environment variable in Windows.
	1. Right click on My Computer and select Properties. Then click Advanced system
	   settings in the newly opened window, which should open another new window 
           called System Properties.

	2. On the Advanced tab click the Environment Variables button. In the System
	   Variables section scroll down to the variable that says Path. Select it and
           click on the Edit button.

	3. In the Variable value text field, go all the way to the end of the line type
	   the full MySQL installation bin directory path as C:\mysql\bin\, or 
	   C:\Program Files\mysql\bin\, or another as chosen, and click OK. Click OK 
           on the Environment Variables window; click OK on the System Properties window.
           Then finally, close the Control Panel window.

 * Install MySQL as a Windows service. As the administrator of the machine:
	1. Open the Windows Command Processor (cmd).

	2. Type: mysqld --install

	3. Press <Enter>, you should see the message "Service successfully installed".

	4. You can start the database service by typing: mysqld --console

	   ## ERROR [MY-011011] may occur, check Troubleshooting.

 * Access the MySQL query window. As the administrator of the machine:
	1. Open a new command prompt, then type: mysql -u root -p
	   (This step assumes you started up the database using: mysqld --console)

	2. This should prompt a password, for which nothing should be set, so continue
	   by pressing <Enter>. You are now in the MySQL query window where you type
	   in SQL queries for the database.

	   ## IN EVENT OF ACCESS DENIAL, check Troubleshooting.
	   
	3. Change to the database by typing: use mysql;

	   ## IF INITIALIZED, ITS RECOMMENDED TO CREATE A BRAND NEW DATABASE INSTEAD,
 	      AND USE THE NEW DATABASE.

	4. To change the root user's password, type the following command shown below:

		ALTER USER 'root'@'localhost' IDENTIFIED BY 'YOUR_PASSWORD';

	   The following message will appear if successful:
		Query OK, 3 rows affected (0.08 sec)
		Rows matched: 3 Changed: 3 Warnings: 0

	   Type: flush privileges;
	   Type: quit
	
	5. The MySQL service will be stopped once the command prompt used to start it
	   is closed. Stopping the service prevents any queries to be executed.

	#########################################



	###### Mac OSX installation guide ######

 * For OSX 10.10  OR  OSX 10.11
	1. Copy and paste this into Terminal: 
		bash <(curl -Ls http://git.io/eUx7rg)
	
	2. Enter in your system password when prompted.

	3. The script will install MySQL, generate a root password and display it along
	   with writing a file to the desktop including the password.

	4. Click to install the MySQL preference pane when prompted.

	5. Close your terminal and open a new terminal to access MySQL via command line.

	6. (IN EVENT OF ACCESS DENIAL, OR LOSS OF PASSWORD) Run the following in Terminal:
		bash <(curl -Ls http://git.io/9xqEnQ)
	   This script will restart MySQL, reset the password, and then restart it again.
	
	Complete Documentation found at:
	https://github.com/MacMiniVault/Mac-Scripts/blob/master/mmvMySQL/
	mmvmysql-README.md

 * For OSX 10.9
	1. Copy and paste this into Terminal: 
		bash <(curl -Ls http://git.io/eUx7rg)

	2. Accept prompt to install Preference Pane

	3. The script will install MySQL, generate a root password and display it along
	   with writing a file to the desktop including the password.

	4. Decline prompt for Sequel Pro

	########################################


SQL Tutorial: https://www.w3schools.com/sql/



INSTALLATION OF PYTHON / DJANGO
-------------------------------
 
Install Python on whichever preferred IDE or Code Editor; For the purposes of this guide,
VIsual Studio Code (VS Code) will be used. Some Editors or IDEs will have a method of 
installing Python but if a download is needed, see [Requirements].

Step 1  -  Install Python
   (All operating systems) Download from python.org; typically use the Download Python
   3.9.X button that appears first on the page (or whatever is the latest version).

(Linux) The built-in Python 3 installation works well, but to install other Python 
   packages you must run " sudo apt install python3-pip " in the terminal.

(Mac OS) An installation through Homebrew on macOS using brew install python3 (the system 
   install of Python on macOS is not supported).


Step 2  -  Install the extension for Python on VS Code: 
   Install the extension for Python on VS Code: 
   https://marketplace.visualstudio.com/items?itemName=ms-python.python


Step 3  -  Start the VS Code Terminal
   Create a folder anywhere of your choosing on the system.

	### OPTIONAL ###
   You can create a virtual environment for the database if the system will be used for 
   other programs that rely on Python. This can be used to avoid conflicts. Then run the 
   following command dependent on your Operating System:

   (Windows)
   python -m venv env

   (Linux)
   sudo apt-get install python3-venv    # If needed
   python3 -m venv env

   (Mac OS)
   python3 -m venv env
	################

   Open the project folder in VS Code by running: code . 
   or by running VS Code and using the File > Open Folder command.

   In VS Code, open the Command Palette (View > Command Palette or (Ctrl+Shift+P)). Then
   select the Python: Select Interpreter command.

   Run Terminal: Create New Integrated Terminal (Ctrl+Shift+`) from Command Palette.


Step 4  -  Pull required files from GitHub.
   Now that the environment is set up, download all the files needed from GitHub. 
   https://github.com/BridgetteBXP13/programming_project.git
   Within VS Code, go to File > Open Folder, then select the programming_project-main
   folder. The Explorer in VS Code should now display the project and all its files.
   

Step 5  -  Install the dependencies.
   There is a provided requirements.txt file. Run the following command:
   pip install -r requirements.txt 
   The command above will download/install everything that is needed for the program.



IMPORT COMMA SEPERATED VALUE FILES (.csv)
-----------------------------------------

These next steps assume that you have the MySQL Server running on a console window, and
that the database switched to is EMPTY (verify in cmd with command: SHOW TABLES;).
Two csv files are included within the project. Import them with the following commands:

python manage.py runscript import_borrowers_csv
python manage.py runscript import_books_csv  (Massive file; Will take several minutes)

Afterwards, migrate the changes to the server.

python manage.py makemigrations
python manage.py migrate

On the MySQL console, you can see the new tables added with the command: SHOW TABLES;
You may now use SQL commands to search for books.



TROUBLESHOOTING
---------------

 * ERROR [MY-011011] occurs when launching "mysqld --console" for the first time:
   First go into C:\mysql and verify that the 'data' directory exists. If not, simply
   create it manually. Then try initializing the server with the following command:
   mysqld --initialize
   Doing this may generate a random password for root user. The password should appear in 
   the terminal. Otherwise it can be found in: mysql\data\YOUR_DEVICE_NAME.err

 * Root user's password not blank upon MySQL installation.
   On first time setup, password may be generated. Check mysql\data\YOUR_DEVICE_NAME.err
   Worst case scenario, refer to this guide for Windows OS: 
   https://www.strongdm.com/blog/how-to-change-the-mysql-root-password
   
   Or run this script in Mac OSX Terminal:
   bash <(curl -Ls http://git.io/9xqEnQ)

 * Unwanted tables exist in SQL database. (Assumes default database name is "mysql")
   Ensure that the database is started in seperate cmd after command: mysqld --console
   Switch to the database by typing into the MySQL query window: use mysql
   Type: DROP DATABASE mysql;

   A proper implementation of the SQL database should only display the following tables:

	+----------------------------+
	| Tables_in_library          |
	+----------------------------+
	| auth_group                 |
	| auth_group_permissions     |
	| auth_permission            |
	| auth_user                  |
	| auth_user_groups           |
	| auth_user_user_permissions |
	| authors                    |
	| book                       |
	| book_authors               |
	| book_loans                 |
	| borrower                   |
	| django_admin_log           |
	| django_content_type        |
	| django_migrations          |
	| django_session             |
	| fines                      |
	+----------------------------+

   MySQL may not allow you to drop databases. In that event, it is easier to simply create
   a new database in the MySQL console with command: CREATE DATABASE databasename; 
   Then configure the DATABASES module under settings.py within VS Code to match the 
   databasename. While you are here, double check the login credentials.

