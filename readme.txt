1. Create a new directory and initialize for version control by running
   'git init' command while inside the directory. 

2. Make sure your Vagrant box is congigured to listen on needed port (8000)
   Check file VagrantFile for network configuration of your Vagrant box.

3. Create your database in psql: run 'CREATE DATABASE dbname;' command 
   You do not need to create tables yet.

4. Create the database_setup.py file and run it, which will create all 
   tables defined in the file. You may check those in psql.

5. Create the webserver.py file where you define function main() to be
   run when the file is opened by python interpreter.