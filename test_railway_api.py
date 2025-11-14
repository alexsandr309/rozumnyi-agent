"""Тестовий скрипт для перевірки Railway GraphQL API"""
import json
import requests

# Читаємо конфіг
with open("auto_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

api_key = config["railway"]["api_key"]
# Спробуємо обидва endpoint'и
urls = [
    "https://backboard.railway.com/graphql/v2",
    "https://backboard.railway.app/graphql/v2"
]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Тест 1: Простий запит me (замість viewer)
print("=== Тест 1: Отримання me ===")
query1 = """
query {
    me {
        id
        email
        name
    }
}
"""
working_url = None
for url in urls:
    print(f"\nСпроба з {url}:")
    response1 = requests.post(url, headers=headers, json={"query": query1})
    print(f"Status: {response1.status_code}")
    print(f"Response: {response1.text}")
    if response1.status_code == 200:
        working_url = url
        break

# Тест 2: Отримання проектів через me
print("\n=== Тест 2: Отримання проектів ===")
query2 = """
query {
    me {
        projects {
            edges {
                node {
                    id
                    name
                }
            }
        }
    }
}
"""
if not working_url:
    working_url = urls[0]
for url in urls:
    print(f"\nСпроба з {url}:")
    response2 = requests.post(url, headers=headers, json={"query": query2})
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.text}")
    if response2.status_code == 200:
        working_url = url
        break

# Тест 3: Створення проекту (якщо тести 1-2 успішні)
if response1.status_code == 200 and response2.status_code == 200:
    print("=== Тест 3: Створення проекту ===")
    mutation = """
    mutation($name: String!) {
        projectCreate(input: { name: $name }) {
            id
            name
        }
    }
    """
    variables = {"name": "test-project"}
    response3 = requests.post(working_url, headers=headers, json={"query": mutation, "variables": variables})
    print(f"Status: {response3.status_code}")
    print(f"Response: {response3.text}\n")

