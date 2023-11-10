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

## Create Virtual Environment

```sh
py -m venv venv.
```

## Activate Virtual Environment

```sh
.\venv\Scripts\activate
```

## Dependencies Environment

```sh
pip install -r requirements.txt
```

## Environment Variables

```sh
SECRET_KEY='secret'
DATABASE_HOST='localhost'
DATABASE_PASSWORD='password'
DATABASE_USER='user'
DATABASE_PORT=1521
```

## Run

```sh
py app.py
```

or

```sh
python app.py
```

## Open Browser

```sh
http://localhost:5000/
```
