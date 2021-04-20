# Recetario!
#### Video Demo:  https://youtu.be/64Xenl2Oz4g

## Introduction

Hello, this is Recetario!

For this project I tought I could create a simple web app to store you're favourite recipies. Since I am from Argentina, all of the app is in spanish.
I took a lot of ideas form the "finance" problem from problem set 8, creating a web-based application using JavaScript, Python, Flask and SQL.
I made the complete app in the CS50 IDE.


## How the webpage works?

- The users can register with a username and password.
- They can create, edit and delete their recipies.
- From "Recetas" they can see all of their recipes.

## app.py
App.py is the main application file. Its from where everything is controlled. Here are the different routes the user can access to. I created a sqlite3 database, for storing the recipes and the users info.
It uses jinja for passing information to/from the html files.
One of the biggest challenges I had to face was to make the Register/Log In system.

## recetas.db
This is the database. Where the user's information and recipes are stored. Is made with sqlite3. It has two tables: users and recipes.

## helpersRecetas.py
This is a module where I put the login_requiered function used in app.py. It controls that the user is logged in.

## layout.html
The layout is where the navegation bar is made. I imported bootstrap for this project. Also is where the flashes are displayed when needed. Using jinja, the layout will be displayed in all of the other routes.

## index.html
This is just an introduction to the web app.

## login.html
Here the users can log in if they already have a username and password. App.py will first check that everything is correct, and will flash an error mesagge if else.
The flashing messages also were a challenge. I made different categories, acording to the type of message. In this case, the messages are in red.

## register.html
Here the users can register themselves. They must enter a username, password and password confirmation. Also there will be a ckecking system as in log in. It checks the database for a non used username. An upgrade might be to add password requirements.

## Crear.html
This is where the users, once they are logged in, can create their recipes. They can do it by inputing a name, the ingredients and the how-to. The information is saved into the database, with an id and connected with the user id.

## recetas.html
This file reads form database and shows all of the recipes in a table. Is checks all of the recipes with the user id in session. It also has an edit and delete button for each one.

## editar.html
By clicking the "Editar" button from "Recetas" the users can edit an existing recipe. The users will be redirected to editar.html which is similar to create.html but the database will change an existing recipe instead of creating one. Also, the users will see the inputs already filled with the existing recipe info.

## static
Here I saved the background image.
