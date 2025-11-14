"""
Автоматичне налаштування проєкту "Розумний Агент"
Виконує всі необхідні кроки для розгортання на Railway, Render або Replit
"""

import json
import os
import sys
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import requests
except ImportError:
    print("Встановлюю requests...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# Кольори для виводу
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(step: str, message: str):
    """Виведення кроку з кольором"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}[{step}]{Colors.END} {message}")

def print_success(message: str):
    """Виведення успішного повідомлення"""
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_error(message: str):
    """Виведення помилки"""
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_warning(message: str):
    """Виведення попередження"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def print_info(message: str):
    """Виведення інформаційного повідомлення"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

def load_config() -> Dict[str, Any]:
    """Завантаження конфігурації"""
    config_path = Path("auto_config.json")
    
    if not config_path.exists():
        print_error("Файл auto_config.json не знайдено!")
        print("Створіть файл auto_config.json з credentials (див. AUTO_SETUP.md)")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_service_account() -> bool:
    """Перевірка наявності service_account.json"""
    sa_path = Path("service_account.json")
    if not sa_path.exists():
        print_error("Файл service_account.json не знайдено!")
        print("Створіть Service Account та завантажте JSON ключ (див. AUTO_SETUP.md)")
        return False
    print_success("Service Account знайдено")
    return True

def create_github_repo(config: Dict[str, Any]) -> Optional[str]:
    """Отримання URL існуючого GitHub репозиторію"""
    print_step("1", "Перевірка GitHub репозиторію...")
    
    github_config = config.get("github", {})
    username = github_config.get("username")
    token = github_config.get("token")
    repo_name = github_config.get("repo_name", "rozumnyi-agent")
    
    if not username:
        print_error("GitHub username не знайдено в auto_config.json")
        return None
    
    # Формуємо URL існуючого репозиторію
    repo_url = f"https://github.com/{username}/{repo_name}"
    
    # Перевірка, чи репозиторій існує (опціонально, якщо є валідний токен)
    if token:
        try:
            url = f"https://api.github.com/repos/{username}/{repo_name}"
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print_success(f"Репозиторій знайдено: {repo_url}")
                return repo_url
            elif response.status_code == 401:
                print_warning("GitHub token недійсний, але репозиторій вже існує")
                print_success(f"Використовую існуючий репозиторій: {repo_url}")
                return repo_url
            elif response.status_code == 404:
                print_warning("Репозиторій не знайдено через API, але спробую використати URL")
                return repo_url
            else:
                print_warning(f"Помилка перевірки репозиторію: {response.status_code}")
                print_success(f"Використовую існуючий репозиторій: {repo_url}")
                return repo_url
        except Exception as e:
            print_warning(f"Помилка перевірки через API: {e}")
            print_success(f"Використовую існуючий репозиторій: {repo_url}")
            return repo_url
    else:
        print_success(f"Використовую існуючий репозиторій: {repo_url}")
        return repo_url

def setup_git_repo(repo_url: str) -> bool:
    """Налаштування Git та завантаження коду"""
    print_step("2", "Налаштування Git репозиторію...")
    
    try:
        # Перевірка, чи вже є git репозиторій
        if Path(".git").exists():
            print_success("Git репозиторій вже існує")
        else:
            subprocess.run(["git", "init"], check=True, capture_output=True)
            print_success("Git репозиторій ініціалізовано")
        
        # Додавання/оновлення remote
        subprocess.run(
            ["git", "remote", "remove", "origin"],
            capture_output=True
        )
        subprocess.run(
            ["git", "remote", "add", "origin", f"{repo_url}.git"],
            check=True,
            capture_output=True
        )
        print_success("Remote налаштовано")
        
        # Перейменування поточної гілки на main (якщо потрібно)
        try:
            subprocess.run(
                ["git", "branch", "-M", "main"],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError:
            pass  # Гілка вже main
        
        # Перевірка, чи є незбережені зміни
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        has_changes = bool(result.stdout.strip())
        
        if has_changes:
            # Додавання файлів
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            
            # Коміт
            subprocess.run(
                ["git", "commit", "-m", "Auto-update: prepare for deployment"],
                check=True,
                capture_output=True
            )
            print_success("Зміни закомічено")
            
            # Push
            try:
                subprocess.run(
                    ["git", "push", "-u", "origin", "main"],
                    check=True,
                    capture_output=True
                )
                print_success("Код оновлено на GitHub")
            except subprocess.CalledProcessError as push_err:
                print_warning("Не вдалося виконати git push (можливо, недійсний токен або немає доступу)")
                print_warning(str(push_err))
                print_warning("Пропускаю push — переконайтесь вручну, що репозиторій синхронізовано")
        else:
            print_success("Немає нових змін, репозиторій вже синхронізовано")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Помилка Git: {e}")
        return False
    except Exception as e:
        print_error(f"Неочікувана помилка: {e}")
        return False

def create_render_service(config: Dict[str, Any], repo_url: str) -> Optional[str]:
    """Створення Render Web Service"""
    print_step("3", "Створення Render Web Service...")
    
    render_config = config.get("render", {})
    api_key = render_config.get("api_key")
    
    if not api_key:
        print_error("Render API key не знайдено в auto_config.json")
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Отримання ownerId (потрібно для створення сервісу)
    owner_id = render_config.get("owner_id")  # Можна вказати вручну в auto_config.json
    
    if not owner_id:
        # Спробувати отримати автоматично
        print_warning("ownerId не вказано в конфігурації, спробую отримати автоматично...")
        try:
            # Спробувати різні endpoints
            endpoints = [
                "https://api.render.com/v1/owners",
                "https://api.render.com/v1/user",
                "https://api.render.com/v1/me"
            ]
            
            for endpoint in endpoints:
                try:
                    resp = requests.get(endpoint, headers=headers, timeout=10)
                    if resp.status_code == 200:
                        data = resp.json()
                        # Різні можливі структури відповіді
                        if isinstance(data, list) and data:
                            owner_id = data[0].get("id") or data[0].get("ownerId")
                        elif isinstance(data, dict):
                            owner_id = data.get("id") or data.get("ownerId") or data.get("user", {}).get("id")
                        if owner_id:
                            print_success(f"ownerId отримано: {owner_id}")
                            break
                except:
                    continue
            
            if not owner_id:
                print_error("Не вдалося автоматично отримати ownerId")
                print_warning("Додайте 'owner_id' в секцію 'render' в auto_config.json")
                print_warning("Або створіть сервіс вручну через Render Dashboard")
                print_info("Щоб знайти ownerId:")
                print_info("1. Відкрийте Render Dashboard")
                print_info("2. Перейдіть в Settings -> API")
                print_info("3. Або подивіться URL вашого профілю")
                return None
        except Exception as e:
            print_error(f"Помилка отримання ownerId: {e}")
            print_warning("Додайте 'owner_id' вручну в auto_config.json")
            return None
    else:
        print_success(f"Використовую ownerId з конфігурації: {owner_id}")
    
    # Витягування owner та repo з URL
    # https://github.com/username/repo -> username/repo
    repo_path = repo_url.replace("https://github.com/", "")
    
    url = "https://api.render.com/v1/services"
    
    service_name = render_config.get("service_name", "розумний-агент")
    branch = render_config.get("branch", "main")
    root_dir = render_config.get("root_dir", "розумний агент")
    build_command = render_config.get("build_command", "pip install -r requirements.txt")
    start_command = render_config.get("start_command", "gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120")
    plan = render_config.get("plan", "free")
    region = render_config.get("region", "oregon")
    python_version = render_config.get("python_version", "3.11")
    
    data = {
        "type": "web_service",
        "name": service_name,
        "ownerId": owner_id,
        "repo": repo_path,
        "branch": branch,
        "rootDir": root_dir,
        "buildCommand": build_command,
        "startCommand": start_command,
        "serviceDetails": {
            "plan": plan,
            "region": region,
            "env": "python",
            "envSpecificDetails": {
                "pythonVersion": python_version
            }
        },
        "envVars": []
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            service_id = response.json()["service"]["id"]
            service_url = response.json()["service"]["serviceDetails"]["url"]
            print_success(f"Render сервіс створено: {service_url}")
            return service_id
        else:
            print_error(f"Помилка створення сервісу: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print_error(f"Помилка: {e}")
        return None

def setup_render_env_vars(service_id: str, config: Dict[str, Any]) -> bool:
    """Налаштування Environment Variables на Render"""
    print_step("4", "Налаштування Environment Variables...")
    
    render_config = config.get("render", {})
    api_key = render_config.get("api_key")
    binance_config = config.get("binance", {})
    trading_config = config.get("trading", {})
    
    env_vars = [
        {"key": "BINANCE_TESTNET_API_KEY", "value": binance_config.get("testnet_api_key", "")},
        {"key": "BINANCE_TESTNET_SECRET_KEY", "value": binance_config.get("testnet_secret_key", "")},
        {"key": "TRADING_MODE", "value": trading_config.get("mode", "BALANCED")},
        {"key": "DEPOSIT_USDT", "value": str(trading_config.get("deposit_usdt", 1000))},
        {"key": "MODEL_FILE_NAME", "value": "agent_model.keras"},
        {"key": "CLIENT_SECRETS_FILE", "value": "service_account.json"},
        {"key": "GOOGLE_TOKEN_FILE", "value": "token.json"},
        {"key": "POLL_INTERVAL_SECONDS", "value": "60"},
        {"key": "SAVE_MODEL_INTERVAL_STEPS", "value": "30"},
        {"key": "TRAIN_BATCH_SIZE", "value": "32"},
        {"key": "LOG_LEVEL", "value": "INFO"},
    ]
    
    url = f"https://api.render.com/v1/services/{service_id}/env-vars"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        for env_var in env_vars:
            response = requests.post(url, headers=headers, json=env_var)
            if response.status_code in [200, 201]:
                print_success(f"Додано: {env_var['key']}")
            else:
                print_warning(f"Не вдалося додати {env_var['key']}: {response.status_code}")
        
        return True
    except Exception as e:
        print_error(f"Помилка: {e}")
        return False

def upload_render_secret_file(service_id: str, config: Dict[str, Any]) -> bool:
    """Завантаження Secret Files на Render"""
    print_step("5", "Завантаження Secret Files...")
    
    render_config = config.get("render", {})
    api_key = render_config.get("api_key")
    
    sa_path = Path("service_account.json")
    if not sa_path.exists():
        print_error("service_account.json не знайдено!")
        return False
    
    # Читаємо вміст файлу
    with open(sa_path, 'r', encoding='utf-8') as f:
        sa_content = f.read()
    
    url = f"https://api.render.com/v1/services/{service_id}/secret-files"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    data = {
        "name": "service_account.json",
        "contents": sa_content
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            print_success("service_account.json завантажено")
            return True
        else:
            print_warning(f"Не вдалося завантажити файл: {response.status_code}")
            print("Можливо, потрібно завантажити вручну через Render Dashboard")
            return False
    except Exception as e:
        print_error(f"Помилка: {e}")
        return False

def create_replit_repl(config: Dict[str, Any], repo_url: str) -> Optional[str]:
    """Створення Repl на Replit"""
    print_step("3a", "Створення Repl на Replit...")
    
    replit_config = config.get("replit", {})
    api_token = replit_config.get("api_token")
    username = replit_config.get("username")
    repl_name = replit_config.get("repl_name", "розумний-агент")
    
    if not api_token:
        print_warning("Replit API token не знайдено, пропускаю створення Repl")
        return None
    
    # Replit API endpoint для створення Repl
    url = "https://api.replit.com/v1/repls"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": repl_name,
        "description": "Генеративний AI-Агент для торгівлі криптовалютою",
        "language": "python3",
        "isPrivate": False,
        "template": "python3"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            repl_data = response.json()
            repl_id = repl_data.get("id")
            repl_url = f"https://replit.com/@{username}/{repl_name}" if username else repl_data.get("url", "")
            print_success(f"Repl створено: {repl_url}")
            return repl_id
        else:
            print_warning(f"Не вдалося створити Repl: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print_error(f"Помилка створення Repl: {e}")
        return None

def setup_replit_secrets(repl_id: str, config: Dict[str, Any]) -> bool:
    """Налаштування Secrets на Replit"""
    print_step("4a", "Налаштування Secrets на Replit...")
    
    replit_config = config.get("replit", {})
    api_token = replit_config.get("api_token")
    binance_config = config.get("binance", {})
    trading_config = config.get("trading", {})
    
    if not api_token:
        print_warning("Replit API token не знайдено, пропускаю")
        return False
    
    # Secrets для Replit
    secrets = {
        "BINANCE_TESTNET_API_KEY": binance_config.get("testnet_api_key", ""),
        "BINANCE_TESTNET_SECRET_KEY": binance_config.get("testnet_secret_key", ""),
        "TRADING_MODE": trading_config.get("mode", "BALANCED"),
        "DEPOSIT_USDT": str(trading_config.get("deposit_usdt", 1000)),
        "MODEL_FILE_NAME": "agent_model.keras",
        "SERVICE_ACCOUNT_FILE": "service_account.json",
        "POLL_INTERVAL_SECONDS": "60",
        "SAVE_MODEL_INTERVAL_STEPS": "30",
        "TRAIN_BATCH_SIZE": "32",
        "LOG_LEVEL": "INFO",
    }
    
    url = f"https://api.replit.com/v1/repls/{repl_id}/secrets"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    try:
        for key, value in secrets.items():
            data = {"key": key, "value": value}
            response = requests.post(url, headers=headers, json=data)
            if response.status_code in [200, 201]:
                print_success(f"Додано secret: {key}")
            else:
                print_warning(f"Не вдалося додати {key}: {response.status_code}")
        
        return True
    except Exception as e:
        print_error(f"Помилка: {e}")
        return False

def upload_replit_file(repl_id: str, file_path: str, content: str, api_token: str) -> bool:
    """Завантаження файлу на Replit"""
    url = f"https://api.replit.com/v1/repls/{repl_id}/files/{file_path}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    data = {"content": content}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.status_code in [200, 201]
    except Exception as e:
        print_error(f"Помилка завантаження файлу {file_path}: {e}")
        return False

def setup_replit_files(repl_id: str, config: Dict[str, Any]) -> bool:
    """Завантаження файлів на Replit"""
    print_step("5a", "Завантаження файлів на Replit...")
    
    replit_config = config.get("replit", {})
    api_token = replit_config.get("api_token")
    
    if not api_token:
        print_warning("Replit API token не знайдено, пропускаю")
        return False
    
    # Завантаження service_account.json
    sa_path = Path("service_account.json")
    if sa_path.exists():
        with open(sa_path, 'r', encoding='utf-8') as f:
            sa_content = f.read()
        if upload_replit_file(repl_id, "service_account.json", sa_content, api_token):
            print_success("service_account.json завантажено")
        else:
            print_warning("Не вдалося завантажити service_account.json")
    
    # Завантаження app.py
    app_path = Path("app.py")
    if app_path.exists():
        with open(app_path, 'r', encoding='utf-8') as f:
            app_content = f.read()
        if upload_replit_file(repl_id, "app.py", app_content, api_token):
            print_success("app.py завантажено")
    
    # Завантаження requirements.txt
    req_path = Path("requirements.txt")
    if req_path.exists():
        with open(req_path, 'r', encoding='utf-8') as f:
            req_content = f.read()
        if upload_replit_file(repl_id, "requirements.txt", req_content, api_token):
            print_success("requirements.txt завантажено")
    
    return True

def execute_railway_graphql(query: str, variables: Optional[Dict] = None, api_key: str = "") -> Optional[Dict]:
    """Виконання GraphQL запиту до Railway API"""
    # Спробуємо обидва endpoint'и
    urls = [
        "https://backboard.railway.com/graphql/v2",
        "https://backboard.railway.app/graphql/v2"
    ]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    # Спробуємо обидва endpoint'и
    last_error = None
    for url in urls:
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
        
            # Спробуємо отримати JSON навіть якщо статус не 200
            try:
                result = response.json()
            except:
                result = None
            
            # Якщо успішно, повертаємо результат
            if response.status_code == 200:
                # Перевіряємо наявність помилок у відповіді
                if result and "errors" in result:
                    # Не виводимо помилку для "Not Authorized" - це нормально для деяких запитів
                    errors = result.get("errors", [])
                    if not any("Not Authorized" in str(e) for e in errors):
                        print_error(f"GraphQL помилки: {errors}")
                    return result  # Повертаємо для обробки помилок
                return result
            
            # Якщо помилка, зберігаємо для останньої спроби
            error_msg = f"{response.status_code} {response.reason}"
            if result and "errors" in result:
                error_msg += f": {result['errors']}"
            elif result:
                error_msg += f": {result}"
            last_error = error_msg
            
            # Якщо це останній URL, виводимо помилку
            if url == urls[-1]:
                print_error(f"Помилка GraphQL запиту: {last_error}")
                if result:
                    return result  # Повертаємо результат навіть з помилками для аналізу
                return None
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            if url == urls[-1]:
                print_error(f"Помилка мережевого запиту: {last_error}")
                return None
        except Exception as e:
            last_error = str(e)
            if url == urls[-1]:
                print_error(f"Неочікувана помилка: {last_error}")
                return None
    
    return None

def create_railway_project(config: Dict[str, Any]) -> Optional[str]:
    """Створення Railway проекту"""
    print_step("3", "Створення Railway проекту...")
    
    railway_config = config.get("railway", {})
    api_key = railway_config.get("api_key")
    
    if not api_key:
        print_error("Railway API key не знайдено в auto_config.json")
        return None
    
    project_name = railway_config.get("project_name", "розумний-агент")
    
    # Спочатку отримуємо список існуючих проектів через me
    query = """
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
    
    result = execute_railway_graphql(query, None, api_key)
    if result and "errors" not in result:
        # Перевіряємо, чи вже є проект з такою назвою
        data = result.get("data")
        if data:
            me_data = data.get("me")
            if me_data:
                projects = me_data.get("projects", {}).get("edges", [])
                
                for edge in projects:
                    if edge.get("node", {}).get("name") == project_name:
                        project_id = edge["node"]["id"]
                        print_success(f"Використовую існуючий проект: {project_name} ({project_id})")
                        return project_id
    elif result and "errors" in result:
        # Якщо є помилка авторизації для me, просто продовжуємо створення
        errors = result.get("errors", [])
        if any("Not Authorized" in str(e) for e in errors):
            print_info("Не вдалося перевірити існуючі проекти (Not Authorized), створюємо новий...")
    
    # Створюємо новий проект
    # Railway може потребувати workspace ID, спробуємо без нього спочатку
    mutation = """
    mutation($name: String!) {
        projectCreate(input: { name: $name }) {
            id
            name
        }
    }
    """
    
    variables = {
        "name": project_name
    }
    
    result = execute_railway_graphql(mutation, variables, api_key)
    if not result:
        print_error("Не вдалося виконати запит до Railway API")
        return None
    
    if "errors" in result:
        error_msg = result.get("errors", [])
        print_error(f"Помилка створення проекту: {error_msg}")
        # Виводимо детальну інформацію для дебагу
        if isinstance(error_msg, list) and len(error_msg) > 0:
            print_info(f"Деталі помилки: {error_msg[0]}")
        return None
    
    project_data = result.get("data", {}).get("projectCreate")
    if project_data:
        project_id = project_data.get("id")
        print_success(f"Railway проект створено: {project_name} ({project_id})")
        return project_id
    
    print_error("Неочікувана відповідь від Railway API")
    if result:
        print_info(f"Відповідь API: {result}")
    return None

def create_railway_service(config: Dict[str, Any], project_id: str, repo_url: str) -> Optional[str]:
    """Створення Railway сервісу з GitHub репозиторію"""
    print_step("4", "Створення Railway сервісу...")
    
    railway_config = config.get("railway", {})
    api_key = railway_config.get("api_key")
    
    # Витягуємо owner/repo з URL: https://github.com/username/repo -> username/repo
    repo_path = repo_url.replace("https://github.com/", "").replace(".git", "")
    
    mutation = """
    mutation($input: ServiceCreateInput!) {
        serviceCreate(input: $input) {
            service {
                id
                name
            }
        }
    }
    """
    
    variables = {
        "input": {
            "projectId": project_id,
            "source": {
                "repo": repo_path,
                "branch": railway_config.get("branch", "main"),
                "rootDirectory": railway_config.get("root_dir", "розумний агент")
            }
        }
    }
    
    result = execute_railway_graphql(mutation, variables, api_key)
    if not result or "errors" in result:
        if result and "errors" in result:
            print_error(f"Помилка створення сервісу: {result['errors']}")
        return None
    
    service_data = result.get("data", {}).get("serviceCreate", {}).get("service")
    if service_data:
        service_id = service_data.get("id")
        service_name = service_data.get("name", "розумний-агент")
        print_success(f"Railway сервіс створено: {service_name} ({service_id})")
        return service_id
    
    return None

def setup_railway_env_vars(service_id: str, config: Dict[str, Any]) -> bool:
    """Налаштування Environment Variables на Railway"""
    print_step("5", "Налаштування Environment Variables...")
    
    railway_config = config.get("railway", {})
    api_key = railway_config.get("api_key")
    binance_config = config.get("binance", {})
    trading_config = config.get("trading", {})
    
    env_vars = {
        "BINANCE_TESTNET_API_KEY": binance_config.get("testnet_api_key", ""),
        "BINANCE_TESTNET_SECRET_KEY": binance_config.get("testnet_secret_key", ""),
        "TRADING_MODE": trading_config.get("mode", "BALANCED"),
        "DEPOSIT_USDT": str(trading_config.get("deposit_usdt", 1000)),
        "MODEL_FILE_NAME": "agent_model.keras",
        "CLIENT_SECRETS_FILE": "service_account.json",
        "GOOGLE_TOKEN_FILE": "token.json",
        "POLL_INTERVAL_SECONDS": "60",
        "SAVE_MODEL_INTERVAL_STEPS": "100",
        "TRAIN_BATCH_SIZE": "64",
        "LOG_LEVEL": "INFO",
    }
    
    # Railway використовує variableCollectionUpsert для встановлення env vars
    mutation = """
    mutation($input: VariableCollectionUpsertInput!) {
        variableCollectionUpsert(input: $input) {
            variableCollection {
                id
            }
        }
    }
    """
    
    variables = {
        "input": {
            "serviceId": service_id,
            "variables": [{"key": k, "value": v} for k, v in env_vars.items()]
        }
    }
    
    result = execute_railway_graphql(mutation, variables, api_key)
    if result and "errors" not in result:
        print_success("Environment Variables встановлено")
        return True
    else:
        if result and "errors" in result:
            print_warning(f"Помилка встановлення env vars: {result['errors']}")
        # Спробуємо встановити по одній
        for key, value in env_vars.items():
            single_mutation = """
            mutation($input: VariableUpsertInput!) {
                variableUpsert(input: $input) {
                    variable {
                        id
                    }
                }
            }
            """
            single_vars = {
                "input": {
                    "serviceId": service_id,
                    "key": key,
                    "value": value
                }
            }
            single_result = execute_railway_graphql(single_mutation, single_vars, api_key)
            if single_result and "errors" not in single_result:
                print_success(f"Додано: {key}")
            else:
                print_warning(f"Не вдалося додати {key}")
        return True

def upload_railway_secret_file(service_id: str, config: Dict[str, Any]) -> bool:
    """Завантаження service_account.json як секрету на Railway"""
    print_step("6", "Завантаження Secret Files...")
    
    railway_config = config.get("railway", {})
    api_key = railway_config.get("api_key")
    
    sa_path = Path("service_account.json")
    if not sa_path.exists():
        print_error("service_account.json не знайдено!")
        return False
    
    # Читаємо вміст файлу
    with open(sa_path, 'r', encoding='utf-8') as f:
        sa_content = f.read()
    
    # Railway використовує variableUpsert для секретів
    mutation = """
    mutation($input: VariableUpsertInput!) {
        variableUpsert(input: $input) {
            variable {
                id
            }
        }
    }
    """
    
    variables = {
        "input": {
            "serviceId": service_id,
            "key": "SERVICE_ACCOUNT_JSON",
            "value": sa_content
        }
    }
    
    result = execute_railway_graphql(mutation, variables, api_key)
    if result and "errors" not in result:
        print_success("service_account.json завантажено як секрет")
        return True
    else:
        print_warning("Не вдалося завантажити service_account.json через API")
        print_info("Завантажте файл вручну через Railway Dashboard -> Variables -> Add Secret File")
        return False

def create_uptimerobot_monitor(config: Dict[str, Any], service_url: str) -> bool:
    """Створення UptimeRobot монітора"""
    print_step("6", "Створення UptimeRobot монітора...")
    
    uptime_config = config.get("uptimerobot", {})
    api_key = uptime_config.get("api_key")
    
    if not api_key:
        print_warning("UptimeRobot API key не знайдено, пропускаю")
        return False
    
    url = "https://api.uptimerobot.com/v2/newMonitor"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "api_key": api_key,
        "format": "json",
        "type": "1",  # HTTP(s)
        "url": service_url,
        "friendly_name": "Розумний Агент",
        "interval": "300",  # 5 хвилин
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        
        if result.get("stat") == "ok":
            print_success("UptimeRobot монітор створено")
            return True
        else:
            print_warning(f"Не вдалося створити монітор: {result.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Помилка: {e}")
        return False

def main():
    """Головна функція"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  Автоматичне налаштування 'Розумний Агент'{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    # Перевірка наявності необхідних файлів
    if not Path("auto_config.json").exists():
        print_error("Файл auto_config.json не знайдено!")
        print("\nСтворіть файл auto_config.json з credentials (див. AUTO_SETUP.md)")
        sys.exit(1)
    
    if not check_service_account():
        sys.exit(1)
    
    # Завантаження конфігурації
    config = load_config()
    
    # Крок 1: GitHub репозиторій
    repo_url = create_github_repo(config)
    if not repo_url:
        print_error("Не вдалося створити GitHub репозиторій")
        sys.exit(1)
    
    # Крок 2: Git налаштування
    if not setup_git_repo(repo_url):
        print_error("Не вдалося налаштувати Git")
        sys.exit(1)
    
    # Вибір платформи: Railway, Render або Replit
    platform = config.get("platform", "railway").lower()
    
    if platform == "replit":
        # Крок 3a: Replit Repl
        repl_id = create_replit_repl(config, repo_url)
        if not repl_id:
            print_warning("Не вдалося створити Repl на Replit")
            print("Можливо, потрібно створити вручну через Replit Dashboard")
        else:
            # Крок 4a: Secrets на Replit
            setup_replit_secrets(repl_id, config)
            
            # Крок 5a: Файли на Replit
            setup_replit_files(repl_id, config)
            
            print_success("Replit налаштування завершено!")
            print(f"Перевірте ваш Repl: https://replit.com/@{config.get('replit', {}).get('username', '')}/розумний-агент")
    elif platform == "railway":
        # Крок 3: Railway проект
        project_id = create_railway_project(config)
        if not project_id:
            print_error("Не вдалося створити Railway проект")
            print("Можливо, потрібно створити вручну через Railway Dashboard")
            sys.exit(1)
        
        # Крок 4: Railway сервіс
        service_id = create_railway_service(config, project_id, repo_url)
        if not service_id:
            print_error("Не вдалося створити Railway сервіс")
            print("Можливо, потрібно створити вручну через Railway Dashboard")
            sys.exit(1)
        
        # Очікування створення сервісу
        print_warning("Очікую створення сервісу на Railway (10 секунд)...")
        time.sleep(10)
        
        # Крок 5: Environment Variables
        if not setup_railway_env_vars(service_id, config):
            print_warning("Не всі Environment Variables встановлено")
        
        # Крок 6: Secret Files
        if not upload_railway_secret_file(service_id, config):
            print_warning("Не вдалося завантажити Secret Files")
            print("Завантажте service_account.json вручну через Railway Dashboard -> Variables")
        
        print_success("Railway налаштування завершено!")
        print(f"Перевірте ваш проект: https://railway.app/project/{project_id}")
    else:
        # Крок 3: Render сервіс
        service_id = create_render_service(config, repo_url)
        if not service_id:
            print_error("Не вдалося створити Render сервіс")
            print("Можливо, потрібно створити вручну через Render Dashboard")
            sys.exit(1)
    
        # Очікування створення сервісу
        print_warning("Очікую створення сервісу на Render (30 секунд)...")
        time.sleep(30)
        
        # Крок 4: Environment Variables
        if not setup_render_env_vars(service_id, config):
            print_warning("Не всі Environment Variables встановлено")
        
        # Крок 5: Secret Files
        if not upload_render_secret_file(service_id, config):
            print_warning("Не вдалося завантажити Secret Files")
            print("Завантажте service_account.json вручну через Render Dashboard")
        
        # Отримання URL сервісу (потрібно зробити запит)
        render_config = config.get("render", {})
        api_key = render_config.get("api_key")
        url = f"https://api.render.com/v1/services/{service_id}"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                service_url = response.json()["service"]["serviceDetails"]["url"]
                
                # Крок 6: UptimeRobot
                create_uptimerobot_monitor(config, service_url)
            else:
                print_warning("Не вдалося отримати URL сервісу")
        except Exception as e:
            print_warning(f"Не вдалося отримати URL: {e}")
    
    # Підсумок
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}  Налаштування завершено!{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.END}\n")
    
    print("Наступні кроки:")
    if platform == "railway":
        print("1. Перевірте Railway Dashboard для перевірки деплою")
        print("2. Перевірте логи на Railway")
        print("3. Перевірте Keep-Alive ендпоінт: curl https://your-app.railway.app/")
        print("4. (Опціонально) Налаштуйте UptimeRobot монітор для Keep-Alive")
    elif platform == "replit":
        print("1. Перевірте Replit Dashboard для перевірки деплою")
        print("2. Перевірте логи на Replit")
    else:
        print("1. Перевірте Render Dashboard для перевірки деплою")
        print("2. Перевірте логи на Render")
        print("3. Перевірте Keep-Alive ендпоінт: curl https://your-app.onrender.com/")
        print("4. (Опціонально) Налаштуйте UptimeRobot монітор для Keep-Alive")
    print("\n⚠️  ВАЖЛИВО: Видаліть auto_config.json після налаштування!")

if __name__ == "__main__":
    main()

