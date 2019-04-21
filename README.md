# JapaneseMemo
Simple Japanese memory game to learn alphabet.
Registration and login system with leaderboards.
Rest API included for future usage.
Using PostgreSQL

# It's Live!
You can check it by yourself at https://japanese-memo.herokuapp.com/


### Automatic installation

Open terminal in repository directory.  
Run: ```chmod +x ./install.sh```  
After that you can install script by ```./install.sh``` command in terminal (make sure you are in the same directory)  

### Important
In ```JapaneseMemo``` folder, update ```local_settings.py.txt```  to your settings and delete ```.txt``` from the end
of a file.

### Manual installation

These instructions will get you a copy of the project up and running.
Create virtual environment on your machine, then install requirements using:

```
pip install -r requirements.txt
```

Open terminal in ```manage.py``` directory and type ```python manage.py migrate```.
After that, fill database using ```python manage.py loaddata HiraganaData``` .
Run tests ```python manage.py test``` and finally start server by ```python manage.py runserver``` command.

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Django REST](https://www.django-rest-framework.org/)
* [Bootstrap](https://getbootstrap.com/) - Front-end done using Bootstrap
