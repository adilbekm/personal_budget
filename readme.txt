==========================================================================
OVERVIEW
==========================================================================

This is Project 3 of Udacity's Full Stack Nanodegree Program - an item
catalog web application. The application is called Personal Budget and
it allows to track your personal budget and expenses. 

It works as follows: you create a budget period, let's say "June 2015",
and then you add categories inside it like "Rent" or "Car payment"
along with the budgeted dollar amounts. As you go through June and spend
money, you log in to the application and enter your expenses in the
appropriate budget categories. The application calculates and shows the
balance for each category as well as for the entire period. At any given
time, you can see how well (or how bad) you are doing for the period and
for each of the categories.

==========================================================================
OVERVIEW
==========================================================================



-- Create a new directory and initialize for version control by running
   'git init' command while inside the directory. 

-- Make sure your Vagrant box is congigured to listen on needed port (8000)
   Check file VagrantFile for network configuration of your Vagrant box.

-- (Not needed) Install a flask extension called 'flask-login' if it is not
   yet installed. To check whether installed, run 'pip freeze'. To install,
   run 'pip install flask-login' (many need to put 'sudo' in front of command).

-- Create your database in psql: run 'CREATE DATABASE dbname;' command 
   You do not need to create tables yet.

-- Create the database_setup.py file and run it, which will create all 
   tables defined in the file. You may check those in psql.

-- Create the webserver.py file where you define function main() to be
   run when the file is opened by python interpreter.