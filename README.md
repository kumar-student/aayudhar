# aayudhar

Auther is a blood bank app for tracking blood donations and processing request from users
which helps in smoothening blood donation and receiving process.

### Setting up virtual environment

Makesure you are inside your project directory

Creating virtual environment
```shell
# on linux
$ python3 -m venv venv

# on widows
$ python -m venv venv
```

Activating virtual environment
```shell
# on linux
$ source venv/bin/activate

# on widonws
$ source venv/Scripts/activate
```

### Configure environment variables

Exporting environment variables
```shell
(venv) $ export FLASK_APP=blood_bank.py
(venv) $ export SECRET_KEY=<your secret key>
```

### Database

Intializing database
```shell
(venv) $ flask db init
```

Migrating database
```shell
(venv) $ flask db migrate -m "<Your message>"
```

Applying migratios
```shell
(venv) $ flask db upgrade
```

### Running server
```shell
(venv) $ python blood_bank.py
```