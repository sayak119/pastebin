
【c1】YONEXOP12【c1】


# A simple Pastebin app using Flask

It is a simple web application made using Flask web micro-framework to implement a Pastebin-like site. 

Please take in considerations than this web application is still under active development and we cannot guarantee that nothing will break between versions. Most of the core features are already there, so we expect to release a beta version soon.

## Features
* Syntax highlighting
* Paste expiration
* Guest and member privileges
* Edit and  delete your pastes.
* View all your pastes (for members only)
* Download codes
* you can now use it on Android without root  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Prerequisites

Things you need to install the software and instructions to install them:

* You should have python3 and pip3 installed:

First check if python3 is intstalled by using the command:

```
python3 -V
```

```
Output:
Python 3.5.2
```

If not installed then type the following:

```
sudo apt-get update

```

* Instructions for installing pip

```
sudo apt-get install python3-pip
```

* Instructions for installing few more packages and development tools for the programming environment

```
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
```

### Installing

Getting our web app up and running is simple. 
To run it you have to do what you do with most flask apps.

* Setting up virtual environment:

```
virtualenv -p /usr/bin/python3 name_of_your_environment
source name_of_your_environment/bin/activate
pip install -r requirements.txt
```

* Creating the initial database:

```
python db_create.py
python db_migrate.py # In case you need to migrate the database
```

* Please check if the port 8000 is free or not.

### Emacs file configurations

* Create a .emcs file (if not already present).
* Append the following to it.
* [.emacs](https://pastebin.com/5HHudUKL)
* Open Emacs and perform 
```
M-x package-list-packages [RET]
M-x package-install [RET] htmlize [RET]
```

## Deployment

To Deploy python apps, we use nginx as a reverse proxy server. We use uWSGI with nginx to deploy python apps like flask. Insight about WSGI - Web Server Gateway Interface (WSGI) is a specification for simple and universal interface between web servers and web applications. 

## Built With

* [FLask](http://flask.pocoo.org/) - The web microframework used
* [highlight.js](https://highlightjs.org/) - For syntax highlighting

## Versioning

We use git(https://git-scm.com/) for versioning. 

## Authors

* **Samyak Agarwal (20161180)**
* **Aniruddha P. Deshpande (20161058)** 
* **Kanav Gupta (20161151)**
* **Sayak Kundu (20161035)** 

## License

This project is licensed under the MIT License - [LICENSE.md](LICENSE.md)

## Acknowledgments

* Special thanks of gratitude to **D.R. Venkatesh Choppella** for providing us with this excellent oppurtunity to design a web application.
* To our mentor **Ayush Naik** without whose help it would have been difficult to complete this project.
