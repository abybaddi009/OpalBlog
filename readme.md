# Simple Django Blog project
[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

Github URL: https://github.com/abybaddi009/OpalBlog

## Description

This is a simple django blog project with the following feature::

1. Fully functional Monolith with:

    a. Login and Registration pages

    b. Blog create / edit / detail and list pages

    c. Post create / edit / detail pages

2. Rest API with JWT authentication:

    a. Login and Registration end-points

    b. Viewsets to list, create, update and delete blogs

    c. Viewsets to list, create, update and delete posts

3. Anonymous users can view published posts via frontend or API
4. Only users who have created the posts can take actions on the posts
5. Blogs can be added / edited by all

## Steps for setting up the project on your local

1. Create virtual environment

2. Install Dependencies 
```
pip install -r requirements.txt
```

3. Setup database
```
python manage.py makemigrations
python manage.py migrate
```

4. Create SuperUser 
```
python manage.py createsuperuser
```

4. Run development server
```
python manage.py runserver
```

## Author
- [Abhishek Baddi](https://github.com/abybaddi009)


This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg