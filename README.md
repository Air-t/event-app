# event-app

App to handle CRUD operations for events with payment methods available

## Installation

Setup virtual envirnoment [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

Use at least Python 3.6.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all necessary libraries.

```bash
pip install -r requirements.txt
```
For the simplicity SQLite database is used. Feel free to setup Postgres/MSQL or any other database instead.
Crate necessary initial django database setup:

```bash
python3 manage.py loaddata makemigrations
python3 manage.py loaddata migrate
```


Add some dummy data to ses how's it works:
```bash
python3 manage.py loaddata .fixtures/data.json
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author

Air-t
