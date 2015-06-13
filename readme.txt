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
HOW TO RUN THE APPLICATION
==========================================================================

-- Dowload application files from GitHub:
   https://github.com/adilbekm/personal_budget.git

-- Make sure your Vagrant box is congigured to listen on needed port (8000)
   Check file VagrantFile for network configuration of your Vagrant box.

-- run Vagrant and open console with commands:
   vagrant up
   vagrant ssh

-- Create the psql database used by the application by running commands:
   psql
   CREATE DATABASE personalbudget;
   \q

-- start the webserver by running command:
   python webserver.py

==========================================================================
HOW TO USE THE APPLICATION
==========================================================================

-- Open browser and navigate to:
   http://localhost:8000

-- To login with Google Plus, click on "Login" and click the "g+ Sign in"

-- To login with a local application account, first register by clicking
   "Register", and on all subsequent sign-ins click "Login" and then click
   "Local Sign in".

-- From this point, follow instructions provided by the application

==========================================================================
AUTHOR INFORMATION
==========================================================================

Name: Adilbek Madaminov
Email: adilbekm@yahoo.com
