# Planner Outdoor

Planner Outdoor is an application that lets you plan outdoor activities according to the weather.

## Description

This application offers a solution for organizing your outdoor activities (cycling, hiking, etc.) from a predefined list, taking weather conditions into account.

## Technologies used

- **Backend** : Django with Django Rest Framework and simpleJWT
- **Frontend** : Vue.js with Axios and TailwindCSS
- **Database** : MySQL with docker volume for persistent data
- **Containerization** : Docker (four containers and one volume)
- **2in1 SMTP** : Papercut (simulate real email reception)

## Installation

**1. Make sure you have Docker Desktop installed on your machine.**
&nbsp;
    If not, go to: `https://docs.docker.com/desktop/`.
&nbsp;
**2. Create your free OpenWeatherMap account :**
&nbsp;
   `https://home.openweathermap.org/users/sign_up`
&nbsp;
   choose the "Free Access" for everyone and obtain your api key.
&nbsp;
**3. Clone the repository:**

```bash
git clone https://github.com/MgCodeFactory/planner_outdoor.git
```

**4. Create the `.env` file.**
    &nbsp;
    Create this file at the root of the project, based on the `.env_example` template supplied. Fill in the sensitive values.
&nbsp;
**5. Build Docker images and start containers.**
&nbsp;
    Go to the same directory as the `docker-compose.yml` file.
    Build containers :

```bash
docker-compose build
```

**6. Init MySQL database.**
&nbsp;
    Modify `init_db.sql` repalcing "replace_by_your_admin_password" with your password.
&nbsp;
    Copy `init_db.sql` to the container:

```bash
docker cp init_db.sql po_mysql:/init_db.sql
```

go to mysql container shell and init db:

```bash
docker-compose exec mysql mysql -u root -p
mysql> source /init_db.sql;
```

exit mysql container.
&nbsp;
**7. Apply Django migrations.**

```bash
docker-compose exec django django manage.py migrate
```

**8. Populate Activities table (optionnal).**
&nbsp;
    Copy `insert_activities.sql` to the container:

```bash
docker cp insert_activities.sql po_mysql:/insert_activities.sql
```

go to mysql container:

```bash
docker-compose exec mysql mysql -u root -p
mysql> source /insert_activities.sql;
```

or do it manually using backend browsable API if you want.
&nbsp;
**9. Restart application.**

```bash
docker-compose up --build -d
```

This will rebuild all containers, and erase *.sql copied files before.

## Use the application

- Use the application in your browser: `http://localhost:8080`
- Papercut emails are accessible at: `http://localhost:8090`
- To use backend API: `http://localhost:8020/schema/swagger/`

## Notes

- Make sure that ports 8020, 8080, 8090, 3306 are available on your machine.
- All password in application have these requirements:
  `At least 8 characters, one uppercase, one lowercase, one number, one special character, and all different.`
- To stop the application, run `docker-compose down`.

## Administration users (optionnal)

If you need a django superuser to access admin console, the default `createsuperuser` will fail.
The application use a custom user model, with an extra JSON required field.

Go into django container shell:

```bash
docker-compose exec django django manage.py shell
```

In running shell, copy/paste, replacing with your own values:

```python
from django.contrib.auth import get_user_model

User = get_user_model()

po_superuser = User.objects.create_superuser(
    username="po_superuser",
    email="replace_by_email_address",
    password="replace_by_strong_valid_password",
    location={
        "name":"poapp",
        "lat":0.1245,
        "lon":0.6789,
        "country":"DB"
    }
)
```

Then quit the python shell:

```python
>>> quit()
```

With superuser you can access the django admin console at:
`http://localhost:8020/admin/`

If you need a staff user, you can add it before closing the shell (replacing with your values):

```python
po_staffuser = User.objects.create_user(
    username="po_staffuser",
    email="replace_by_email_address",
    password="replace_by_strong_valid_password",
    is_staff=True,
    location={
        "name":"poapp",
        "lat":0.1245,
        "lon":0.6789,
        "country":"DB"
    }
)
```

## Author

MgCodeFactory

## Licence

[MIT](LICENSE)
