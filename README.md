# cs-emenu

This is a API for managing Electronic Menu Cards:

## How to run this project:
* make sure You have installed Docker on your machine
* clone repository
* navigate to the root directory
* run build_n_run.sh script
### This is going to
   * build and run docker-compose image
   * seed database with mock data (menu cards and dishes)
   * create some example users + 1 superadmin
When It is all done:
## API endpoints
* PORT: 8070
* /v1/dishes/ - returns all dishses in database **this endpoint is protected, requires token to get access**
  * ALLOWED METHODS: GET. POST, PATCH, PUT, DELETE
* /v1/dishes/{dish_id}/photo - endpoint to add photo to given dish
  * ALLOWED METHODS: POST
* /v1/menu/ - returns all menu cards in database **this endpoint is protected, requires token to get access**
  * ALLOWED METHODS: GET. POST, PATCH, PUT, DELETE
* /admin/ - django admin (by default there is superuser created with follwing credentials: { admin : adminadmin }

## How to get API Token
* Make sure that application is up, running and database is seeded
* Go to http://localhost:8070/admin
* Log in with default superadmin account (username : admin, password : adminadmin)
* In the Tokens table there should visible be token for admin
* This is the token which You could use to communicate with API

## EXAMPLE:
curl --location --request GET 'localhost:8070/v1/dishes' --header 'Authorization: Token dc8d8e8cc74b4fff5670e173ef868812bd55eda2'

## DJANGO Commands:
 If someone would like to run commands by himself then here is the list:
 - seed_db (seed db with mocked dishes and menus)
 - create_users (seed db with users)
 - send_emails (send emails to users with created / modified dishes and menus from yesterday)

## Emails:
Under the hood there is a Celery job working and **send_emails** command is scheduled to run every 24 hours at 10 am.
This can be changed in the settings file:
``` CELERY_BEAT_SCHEDULE = {
    "send_emails_task": {
        "task": "mail.tasks.send_emails",
        "schedule": crontab(minute=0, hour="10"), << make changes here !
    }
}
```

## TESTS
There are bunch of test cases inside this project. They can be found in /tests/ directories in each module
# How to run tests:
* run this script:
``` ./tests.sh```
