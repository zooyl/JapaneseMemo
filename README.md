# JapaneseMemo
Simple Japanese memory game to learn alphabet.
Registration and login system with leaderboards.
Rest API included for future usage.
Using PostgreSQL

### Installing

These instructions will get you a copy of the project up and running.
Create virtual environment on your machine, then install requirements using:

```
pip install -r requirements.txt
```
### Important
In ```JapaneseMemo``` folder, update ```local_settings.py.txt```  to your settings and delete ```.txt``` from the end
of a file.

Open terminal in ```manage.py``` directory and type ```python manage.py migrate```.
After that, fill database using ```python manage.py loaddata HiraganaData``` 
and start server by ```python manage.py runserver``` command.

### Preview
## Landing Page:

![Landing](https://github.com/zooyl/JapaneseMemo/blob/master/Preview/Landing.png?raw=true)

## Home Page:

![Home](https://github.com/zooyl/JapaneseMemo/blob/master/Preview/Home.png?raw=true)

## Exercise:

![Exercise](https://github.com/zooyl/JapaneseMemo/blob/master/Preview/Level.png)

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Django REST](https://www.django-rest-framework.org/)
* [Bootstrap](https://getbootstrap.com/) - Front-end done using Bootstrap
