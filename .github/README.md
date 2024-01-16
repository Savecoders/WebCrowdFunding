# Init Project

<img
 align="center"
 src="assets/PagePreview.png"
 alt="Page Preview"
/>

## Specification

In Powersheel execute the command:

```sh
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser ​
```

please execute next commands in powersheel

## Install Dependencies

* [Download Python](https://www.python.org/downloads/windows/)
* [Download OracleDB 21c xe](https://www.oracle.com/database/technologies/xe-downloads.html)
* [Download Git](https://git-scm.com/download/win)
* [Download VSCode](https://code.visualstudio.com/download)

## Developer Folder

```sh
cd C:\Users\nameUser\Documents\ 
mkdir Developer 
cd Developer
```

## clone repository

```sh
git clone https://github.com/Savecoders/WebCrowdFunding.git
cd WebCrowdFunding
```

## Config git user

```sh
git config --global user.name "username"
git config --global user.email "email@gmail.com"
```

please using your username and email from github

> [!NOTE]
> It's the most important step from execute this project

## Create Virtual Environment

```sh
py -m venv venv.
```

## Activate Virtual Environment

```sh
.\venv\Scripts\activate
```

## update pip

```sh
python.exe -m pip install --upgrade pip

```

## Dependencies Environment

```sh
pip install -r requirements.txt
```

## Environment Variables

> [!IMPORTANT]
> You necesary replace the .env.template -> .env

```sh
SECRET_KEY='secret'
DATABASE_HOST='localhost'
DATABASE_PASSWORD='password'
DATABASE_USER='user'
DATABASE_PORT=1521
```

## Run Project in normal mode

```sh
py app.py
```

or

```sh
python app.py
```

or

```sh
set FLASK_APP=app.py 
set FLASK_ENV=development 
flask run
python3 -m flask run
```

## Open Browser

```sh
http://localhost:5000/
```

## Push and pull changes

```sh
git pull --set-upstream origin main
git push --set-upstream origin main
```
