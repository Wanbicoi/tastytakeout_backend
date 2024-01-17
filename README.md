# Implement Backend for TaskyTakout

## Installation

Please note that we use Python3.

1. Create virtual environment

```bash
python3 -m venv venv

# linux only
source venv/bin/activate

# windows (powershell)
Scripts\Activate
```

2. Install requirements

```bash
pip install -r requirements.txt
```

3. Start server

```bash
python3 manage.py runserver
```

4. Navigate to this link: [http://localhost:8000/swagger/](http://localhost:8000/swagger/).

## TODOs

[List UI Usecases](https://docs.google.com/spreadsheets/d/1yH2P1UtLlyWZNL87CDAHikUZFfhJuQUGOxtdd9LmiZE/edit#gid=816855299)

## Keys

Sample accounts:

- For seller:

```json
{
  "username": "0782592035",
  "password": "12345678"
}
```

- For buyer:

```json
{
  "username": "0305021142",
  "password": "1234"
}
```

## Socket Chat

1. Buyer or Seller connect to this url `ws://localhost:8000/ws/chat/<room_name>/?token=<token>`(`room_name` is: <buyer*id> + "*" + <store_id>, `token` is access_token)
   Ex: `ws://localhost:8000/ws/chat/10_2/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxODg1NzkzNzA1LCJpYXQiOjE3MDQzNTM3MDUsImp0aSI6ImJkZDVjMDZhMTE5YjQ1NjU4ZDdhZjkwODE5MGMzMzg0IiwidXNlcl9pZCI6MTEsInJvbGUiOiJTRUxMRVIiLCJzdG9yZV9pZCI6Mn0.t4tx1KWFUnVnLRzTNKZ7tH6TlLvHWqriO5xFfB9CJxY`

2. Get all list of chat at: `/chat`
