# PRO_Act

<img src="https://github.com/sruti2024/PRO_Act/blob/main/media/cover.png" height="400px" width="1000px">

[![Issues](https://img.shields.io/github/issues/sruti2024/PRO_Act)](https://github.com/sruti2024/PRO_Act/issues)
<img src="https://img.shields.io/badge/Front%20End-CSS%20JS-orange">
<img src="https://img.shields.io/badge/Back%20End-DJango%20MySQLite-lightgrey">
<img src="https://img.shields.io/badge/Open%20Source-Connect%20Contribute-blueviolet">
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

Pro_Act provides you with an efficient way of managing your tasks. It works on the principals of divide and conquer, allows the user to enter tasks and then divide them into further sub-tasks and handle them efficiently!
Best when working with team to be updated about the tasks that are completed and those that are yet to be done.

Color scheme : https://colorhunt.co/palette/269111

---
## Getting Started 

* First `fork` this repository to your account
* Clone it in your local machine using command `git clone url`
* After a copy of the project is made in your machine , follow the `Explore` section to run the project in your local server.
* All pages are present in the `templates` folder , project files in the `pro_act` folder.
* Make the required changes and run it in the server to see the working.
* `git add .` to add all the changes and `git add filename.txt` to add changes to a perticular file.
* `git commit -m "message"` it is recommended to commit with a message to tell what are the things you have changed.
* `git push` to push all changes to main branch from local branch.



## Explore
Try it out by installing Django. (It is required to have Python installed , if not then download it from : [here](https://www.python.org/downloads/))

    python -m pip install Django
    
    
After installation of Django, open this file in any text editor and in the teminal type the following commandes to migrate the file . 
Migrate the files:

    python manage.py makemigrations
    python manage.py migrate

And then start the server (default: http://localhost:8000)

    python manage.py runserver


## Work Flow

* First the user needs to login to the page , if on is logged in they will be redirected to the dashboard else to the log in page.
* If one has not signed up they may do it using the sign up page and then log in .
* Now the dashboard contains a navbar and a welcome message in it's body.
* In the project tab, there is option to add and view projects.
* The add project consists of a form to enter the details of project.
* The view page consists of cards containing project details.
* This page will also have an option of adding sub tasks to the projects.

For a better idea on how to contribute , click here!
[link](./guidelines.md)
---
