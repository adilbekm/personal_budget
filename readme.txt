-- Create a new directory and initialize for version control by running
   'git init' command while inside the directory. 

-- Make sure your Vagrant box is congigured to listen on needed port (8000)
   Check file VagrantFile for network configuration of your Vagrant box.

-- Install a flask extension called 'flask-login' if it is not yet installed.
   To check whether installed, run 'pip freeze'. To install, run 
   'pip install flask-login' (many need to put 'sudo' in front of command).

-- Create your database in psql: run 'CREATE DATABASE dbname;' command 
   You do not need to create tables yet.

-- Create the database_setup.py file and run it, which will create all 
   tables defined in the file. You may check those in psql.

-- Create the webserver.py file where you define function main() to be
   run when the file is opened by python interpreter.