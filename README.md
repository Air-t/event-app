# event-app

App to handle CRUD operations for events with payment methods available.
Allows 'owner' to manage events. Clients have its own interface to browse and
book tickets available in system.

## Installation

Setup virtual environment [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

Use at least Python 3.6.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all necessary libraries.

```bash
pip install -r requirements.txt
```
For the simplicity SQLite database is used. Feel free to setup Postgres/MSQL or any other database instead.
Crate necessary initial django database setup:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py superuser <username> <email> <password>
python3 manage.py create_owner <username> <email> <password>
```


If you would like to have application filed with random data, populate it wit command:
```bash
python3 manage.py loaddata .fixtures/data.json
```

## Notes
Payment procedure and methods not available yet.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author

Air-t

