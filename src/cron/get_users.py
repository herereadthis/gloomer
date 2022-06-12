import os
import json
import requests
import pandas as pd
from datetime import datetime


def fetch(url: str) -> list:
    res = requests.get(url)
    return json.loads(res.content)


def process(users: list) -> pd.DataFrame:
    processed = []
    for user in users:
        processed.append({
            'ID': user['id'],
            'Name': user['name'],
            'Username': user['username'],
            'Email': user['email'],
            'Phone': user['phone'],
            'Company': user['company']['name']
        })
    return pd.DataFrame(processed)


def save(users: pd.DataFrame, path: str) -> None:
    users.to_csv(path, index=False)


if __name__ == '__main__':
    users = fetch(url='https://jsonplaceholder.typicode.com/users')
    users = process(users=users)
    curr_timestamp = int(datetime.timestamp(datetime.now()))
    path = os.path.normpath(f'~/Sites/gloomer/tmp/users_{curr_timestamp}.csv')
    save(users=users, path=path)