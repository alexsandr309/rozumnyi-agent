# Full prompt for Cursor AI agent
_Exported on 11/12/2025 at 13:59:19 GMT+2 from Cursor (2.0.69)_

---

**User**

Ось повний, кінцевий промт для Cursor AI, який враховує всю нашу фінальну архітектуру, обмеження та вимоги.



🎯 Промт для Cursor AI

Тема: Створення Python-коду для автономного Генеративного AI-Агента для торгівлі, розгорнутого на Render, з контролем ризику та хмарною пам'яттю.

Роль: Ти — елітний AI-розробник, який спеціалізується на Reinforcement Learning (RL), хмарних архітектурах та API бірж.

Мета: Створити повний Python-проєкт для Генеративного AI-Агента, який автономно (24/7) торгує криптовалютою на спотовому ринку, використовуючи безкоштовні хмарні сервіси.

1. ⚙️ Ключова Архітектура (Платформа та Автономність)

Проблема, яку ми вирішуємо: Всі безкоштовні публічні платформи (Colab, Kaggle) блокуються API бірж (Binance, Bybit) через IP-адреси (помилки 403/451).

Наше Рішення (Обов'язкове):

 * Платформа: Ми будемо використовувати Render (Free Tier).

 * Структура Коду: Агент має бути загорнутий у мінімальний веб-сервер Flask з використанням Gunicorn.

 * Автономність 24/7: Код повинен включати "Keep-Alive" ендпоінт (наприклад, @app.route('/')). Цей ендпоінт буде пінгуватися кожні 5-10 хвилин зовнішнім сервісом UptimeRobot (Free Plan), щоб запобігти "засинанню" безкоштовного інстансу Render.

 * Фоновий Процес: Основна логіка AI-Агента (цикл торгівлі та навчання) має працювати у фоновому потоці (threading), незалежно від веб-сервера Flask.

2. 🧠 Архітектура AI-Агента ("Мозок" та "Супервізор")

Вимога: Це має бути Генеративний AI-Агент (не напівавтомат), який використовує Reinforcement Learning (RL) для самостійного знаходження та вдосконалення торгових стратегій.

Джерела Даних (Автономні):

 * Технічний Аналіз (ТА): Агент повинен самостійно аналізувати стандартні індикатори ТА (RSI, MA, Volume, Волатильність) з API біржі.

 * Оцифрований ФА: Агент повинен аналізувати оцифровані фундаментальні дані, доступні через API, які відображають "настрій" ринку. (Наприклад: глибина книги ордерів, аномалії обсягів, співвідношення ордерів на купівлю/продаж). Жодного NLP чи ручного введення новин.

Дворівнева Система Безпеки ("Супервізор"):

 * Рівень 1 (Вибір Користувача): Перед запуском користувач має встановити один із трьох базових режимів:

   * CONSERVATIVE

   * BALANCED

   * AGGRESSIVE

 * Рівень 2 (Контроль AI): AI-Супервізор автоматично коригує ризик, але лише в бік зниження, базуючись на аналізі ринку (ФА+ТА).

   * Логіка:

     * Якщо обрано CONSERVATIVE: AI не може змінювати стиль.

     * Якщо обрано BALANCED: AI може лише знизити ризик до BALANCED_CONSERVATIVE або CONSERVATIVE.

     * Якщо обрано AGGRESSIVE: AI може динамічно знижувати ризик до BALANCED_AGGRESSIVE, BALANCED, CONSERVATIVE і т.д., залежно від "шуму" на ринку.

   * AI ніколи не може підвищити ризик вище базового рівня, встановленого користувачем.

3. 📈 Торгівля та Специфічний Ризик

 * Ринок: Спотова торгівля (Spot Trading). (Жодних ф'ючерсів, жодного кредитного плеча).

 * Біржа: Код має бути налаштований для Binance Testnet (або Bybit Testnet, якщо він підтримує спот).

 * Активи: Агент фокусується лише на BTC/USDT та ETH/USDT. (Надай можливість початкового вибору пари або автоматичного перемикання AI, якщо це ефективно).

 * Правило Агресивного Режиму: Навіть у режимі AGGRESSIVE, Супервізор повинен гарантувати, що агент використовує не більше 30% від загального депозиту для торгівлі, залишаючи 70% у резерві для захисту від "чорних лебедів".

4. 💾 Хмарна Пам'ять (Без Локального Диска)

Вимога: Оскільки файлова система Render є тимчасовою, "мозок" AI-Агента (навчена модель, model.h5 або .pt) повинен зберігатися та завантажуватися з хмари.

 * Рішення: Інтегруй у код функціонал для роботи з Google Drive API.

 * Логіка:

   * Агент повинен мати функцію load_model_from_drive(), яка використовує client_secrets.json (OAuth 2.0) та PyDrive (або аналог) для завантаження файлу моделі з Google Drive при старті.                                               * Агент повинен мати функцію save_model_to_drive(), яка періодично (або після успішного навчання) завантажує оновлений файл моделі назад на Google Drive.

📋 Завдання:

 * Створи requirements.txt: (Включи Flask, gunicorn, ccxt, pandas, tensorflow або pytorch, pydrive або google-api-python-client).

 * Створи app.py: Це має бути повний, готовий до розгортання Flask-додаток, який включає:

   * Налаштування Flask та Gunicorn.

   * Ендпоінт / для UptimeRobot.

   * Запуск фонового потоку (threading) для AI-Агента.

   * Повну архітектуру AI-Агента (Мозок + Супервізор) з логікою трьох режимів ризику та обмеженням 30/70.

   * Інтеграцію з Google Drive API (функції load та save).

   * Приклад підключення до ccxt (Binance Testnet Spot) та цикл торгівлі.

---

**Cursor**

```plaintext
Flask==3.0.3
gunicorn==21.2.0
ccxt==4.3.75
pandas==2.2.2
numpy==1.26.4
scipy==1.11.4
tensorflow==2.15.0
google-api-python-client==2.149.0
google-auth==2.35.0
google-auth-oauthlib==1.2.1
google-auth-httplib2==0.2.0
httplib2==0.22.0
python-dotenv==1.0.1
# Основні залежності
asyncio
aiohttp>=3.8.0
asyncpg>=0.28.0
ccxt>=4.0.0
streamlit>=1.28.0
plotly>=5.15.0
pandas>=2.0.0
numpy>=1.24.0

# Telegram бот (нова версія з асинхронним API)
python-telegram-bot>=20.0
requests>=2.28.0

# AI інтеграція (Google Gemini)
google-genai>=0.2.0

# Оптимізація
optuna>=3.3.0

# Додаткові утиліти
python-dotenv>=1.0.0
pydantic>=2.0.0
loguru>=0.7.0

# Тестування
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-mock>=3.11.0

# Розробка
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
```

```python
import json
import logging
import os
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import ccxt
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, jsonify, request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request as GoogleAuthRequest


# ------------------------------------------------------------------------------
# Configuration & Logging
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(threadName)s %(message)s",
)
logger = logging.getLogger(__name__)

MODEL_FILE_NAME = os.getenv("MODEL_FILE_NAME", "agent_model.keras")
MODEL_DRIVE_FILE_ID = os.getenv("MODEL_DRIVE_FILE_ID")
CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRETS_FILE", "client_secrets.json")
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive.file"]

CCXT_API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
CCXT_SECRET_KEY = os.getenv("BINANCE_TESTNET_SECRET_KEY")

DEFAULT_SYMBOLS = ["BTC/USDT", "ETH/USDT"]
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))
SAVE_MODEL_INTERVAL_STEPS = int(os.getenv("SAVE_MODEL_INTERVAL_STEPS", "30"))
TRAIN_BATCH_SIZE = int(os.getenv("TRAIN_BATCH_SIZE", "32"))
MAX_EPISODE_LENGTH = int(os.getenv("MAX_EPISODE_LENGTH", "96"))  # roughly 96 minutes


# ------------------------------------------------------------------------------
# Risk Management
# ------------------------------------------------------------------------------


class RiskBand(Enum):
    CONSERVATIVE = "CONSERVATIVE"
    BALANCED_CONSERVATIVE = "BALANCED_CONSERVATIVE"
    BALANCED = "BALANCED"
    BALANCED_AGGRESSIVE = "BALANCED_AGGRESSIVE"
    AGGRESSIVE = "AGGRESSIVE"

    @property
    def max_position_fraction(self) -> float:
        mapping = {
            RiskBand.CONSERVATIVE: 0.10,
            RiskBand.BALANCED_CONSERVATIVE: 0.15,
            RiskBand.BALANCED: 0.20,
            RiskBand.BALANCED_AGGRESSIVE: 0.25,
            RiskBand.AGGRESSIVE: 0.30,
        }
        return mapping[self]


RISK_DOWNGRADE_PATHS: Dict[RiskBand, List[RiskBand]] = {
    RiskBand.CONSERVATIVE: [RiskBand.CONSERVATIVE],
    RiskBand.BALANCED: [
        RiskBand.BALANCED,
        RiskBand.BALANCED_CONSERVATIVE,
        RiskBand.CONSERVATIVE,
    ],
    RiskBand.AGGRESSIVE: [
        RiskBand.AGGRESSIVE,
        RiskBand.BALANCED_AGGRESSIVE,
        RiskBand.BALANCED,
        RiskBand.BALANCED_CONSERVATIVE,
        RiskBand.CONSERVATIVE,
    ],
}


class Supervisor:
    """AI supervisor that enforces multi-level risk governance."""

    def __init__(self, user_selected: RiskBand):
        self.user_selected = user_selected
        self.current_band = user_selected

    def evaluate_market_noise(
        self,
        vol_ratio: float,
        book_pressure: float,
        trend_strength: float,
    ) -> RiskBand:
        """
        Decide on a safer risk band depending on market conditions.
        Higher volatility or imbalanced books => lower risk.
        """
        candidates = RISK_DOWNGRADE_PATHS[self.user_selected]
        score = (vol_ratio * 0.5) + (abs(book_pressure) * 0.3) - (abs(trend_strength) * 0.2)
        logger.debug("Supervisor noise score %.4f", score)

        if score > 1.5 and len(candidates) > 1:
            self.current_band = candidates[-1]
        elif score > 1.0 and len(candidates) > 2:
            self.current_band = candidates[-2]
        elif score > 0.7 and len(candidates) > 3:
            self.current_band = candidates[-3]
        else:
            self.current_band = candidates[0]

        logger.info("Supervisor risk band -> %s", self.current_band.value)
        return self.current_band


# ------------------------------------------------------------------------------
# Google Drive Persistence
# ------------------------------------------------------------------------------


class CloudModelManager:
    def __init__(
        self,
        client_secrets_path: str,
        token_path: str,
        drive_file_id: Optional[str],
    ) -> None:
        self.client_secrets_path = client_secrets_path
        self.token_path = token_path
        self.drive_file_id = drive_file_id
        self._service = None

    def _get_credentials(self) -> Credentials:
        if not Path(self.client_secrets_path).exists():
            raise FileNotFoundError(
                f"client_secrets.json не знайдено за шляхом {self.client_secrets_path}"
            )

        creds: Optional[Credentials] = None
        token_file = Path(self.token_path)
        if token_file.exists():
            creds = Credentials.from_authorized_user_file(self.token_path, DRIVE_SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Оновлення Google Drive токена")
                creds.refresh(GoogleAuthRequest())
            else:
                from google_auth_oauthlib.flow import InstalledAppFlow

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_path,
                    DRIVE_SCOPES,
                )
                logger.info("Запуск OAuth-флоу для Google Drive")
                creds = flow.run_console()
            token_file.write_text(creds.to_json(), encoding="utf-8")

        return creds

    def _get_service(self):
        if self._service is None:
            creds = self._get_credentials()
            self._service = build("drive", "v3", credentials=creds, cache_discovery=False)
        return self._service

    def load_model(self, local_path: str) -> bool:
        if not self.drive_file_id:
            logger.warning("MODEL_DRIVE_FILE_ID не заданий; пропускаю завантаження моделі")
            return False

        service = self._get_service()
        try:
            logger.info("Завантаження моделі з Google Drive (%s)", self.drive_file_id)
            request = service.files().get_media(fileId=self.drive_file_id)
            fh = tf.io.gfile.GFile(local_path, "wb")
            downloader = googleapiclient.http.MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.debug("Завантажено %.2f%%", status.progress() * 100)
            fh.close()
            return True
        except HttpError as exc:
            logger.error("Не вдалося завантажити модель: %s", exc)
            return False

    def save_model(self, local_path: str) -> Optional[str]:
        service = self._get_service()
        if not Path(local_path).exists():
            logger.warning("Немає файлу моделі %s для завантаження", local_path)
            return self.drive_file_id

        metadata = {
            "name": MODEL_FILE_NAME,
            "mimeType": "application/octet-stream",
        }
        media = googleapiclient.http.MediaFileUpload(local_path, resumable=True)

        try:
            if self.drive_file_id:
                logger.info("Оновлення моделі на Google Drive (%s)", self.drive_file_id)
                updated = (
                    service.files()
                    .update(fileId=self.drive_file_id, media_body=media, body=metadata)
                    .execute()
                )
            else:
                logger.info("Створення нового файлу моделі на Google Drive")
                updated = service.files().create(media_body=media, body=metadata).execute()

            self.drive_file_id = updated.get("id")
            os.environ["MODEL_DRIVE_FILE_ID"] = self.drive_file_id
            return self.drive_file_id
        except HttpError as exc:
            logger.error("Не вдалося зберегти модель на Google Drive: %s", exc)
            return None


# ------------------------------------------------------------------------------
# Market Data & Execution
# ------------------------------------------------------------------------------


def build_exchange() -> ccxt.Exchange:
    exchange = ccxt.binance(
        {
            "enableRateLimit": True,
            "apiKey": CCXT_API_KEY,
            "secret": CCXT_SECRET_KEY,
            "timeout": 30000,
            "options": {"defaultType": "spot"},
        }
    )
    exchange.set_sandbox_mode(True)
    return exchange


class MarketDataFetcher:
    def __init__(self, exchange: ccxt.Exchange, symbols: List[str]):
        self.exchange = exchange
        self.symbols = symbols

    def get_recent_ohlcv(self, symbol: str, since_ms: Optional[int] = None) -> pd.DataFrame:
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe="1m", since=since_ms, limit=200)
        df = pd.DataFrame(
            ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        return df

    def get_ta_features(self, df: pd.DataFrame) -> Dict[str, float]:
        if df.empty:
            return {"rsi": 50.0, "ma_fast": 0.0, "ma_slow": 0.0, "volatility": 0.0}

        close = df["close"]
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-9)
        rsi = 100 - (100 / (1 + rs.iloc[-1]))

        ma_fast = close.rolling(window=10).mean().iloc[-1]
        ma_slow = close.rolling(window=30).mean().iloc[-1]
        volatility = close.pct_change().rolling(window=30).std().iloc[-1]

        return {
            "rsi": float(np.nan_to_num(rsi, nan=50.0)),
            "ma_fast": float(np.nan_to_num(ma_fast, nan=close.iloc[-1])),
            "ma_slow": float(np.nan_to_num(ma_slow, nan=close.iloc[-1])),
            "volatility": float(np.nan_to_num(volatility, nan=0.0)),
        }

    def get_order_book_metrics(self, symbol: str) -> Dict[str, float]:
        order_book = self.exchange.fetch_order_book(symbol)
        bids = np.array(order_book["bids"][:20])
        asks = np.array(order_book["asks"][:20])
        bid_volume = bids[:, 1].sum() if bids.size else 0.0
        ask_volume = asks[:, 1].sum() if asks.size else 0.0
        imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume + 1e-9)
        return {
            "bid_volume": float(bid_volume),
            "ask_volume": float(ask_volume),
            "imbalance": float(imbalance),
        }


class TradeExecutor:
    def __init__(self, exchange: ccxt.Exchange, supervisor: Supervisor):
        self.exchange = exchange
        self.supervisor = supervisor

    def get_balance(self, asset: str) -> float:
        balance = self.exchange.fetch_balance()
        return float(balance.get(asset, {}).get("free", 0.0))

    def execute(self, symbol: str, side: str, amount: float) -> Optional[Dict[str, Any]]:
        try:
            logger.info("Виконання ордеру %s %s %.6f", symbol, side, amount)
            if amount <= 0:
                return None
            order = self.exchange.create_market_order(symbol, side.lower(), amount)
            return order
        except Exception as exc:  # noqa: BLE001
            logger.error("Помилка виконання ордеру: %s", exc)
            return None

    def max_position_size(self, usdt_balance: float) -> float:
        allowed_fraction = self.supervisor.current_band.max_position_fraction
        return usdt_balance * allowed_fraction


# ------------------------------------------------------------------------------
# Reinforcement Learning Agent
# ------------------------------------------------------------------------------


class TradingEnvironment:
    def __init__(self, data_fetcher: MarketDataFetcher, symbols: List[str]):
        self.data_fetcher = data_fetcher
        self.symbols = symbols
        self.last_prices: Dict[str, float] = {s: 0.0 for s in symbols}

    def get_state(self) -> Tuple[np.ndarray, str]:
        symbol = self._select_symbol()
        df = self.data_fetcher.get_recent_ohlcv(symbol)
        ta = self.data_fetcher.get_ta_features(df)
        book = self.data_fetcher.get_order_book_metrics(symbol)
        latest_price = df["close"].iloc[-1] if not df.empty else self.last_prices[symbol]
        self.last_prices[symbol] = latest_price

        state_vector = np.array(
            [
                ta["rsi"] / 100.0,
                (ta["ma_fast"] - ta["ma_slow"]) / (latest_price + 1e-9),
                ta["volatility"],
                book["imbalance"],
            ],
            dtype=np.float32,
        )
        market_context = {
            "vol_ratio": max(ta["volatility"], 1e-6) * 100,
            "book_pressure": book["imbalance"],
            "trend_strength": ta["ma_fast"] - ta["ma_slow"],
        }
        return state_vector, symbol, market_context

    def _select_symbol(self) -> str:
        weights = []
        for symbol in self.symbols:
            df = self.data_fetcher.get_recent_ohlcv(symbol)
            if df.empty:
                weights.append(1.0)
            else:
                weights.append(df["volume"].iloc[-30:].mean())
        total = sum(weights)
        weights = [w / total if total else 1 / len(self.symbols) for w in weights]
        return np.random.choice(self.symbols, p=weights)


class ActorCriticAgent:
    def __init__(self, state_dim: int, action_dim: int, learning_rate: float = 1e-4):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = 0.99
        self.learning_rate = learning_rate
        self.model = self._build_model()
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)

    def _build_model(self) -> tf.keras.Model:
        inputs = tf.keras.Input(shape=(self.state_dim,))
        dense1 = tf.keras.layers.Dense(64, activation="relu")(inputs)
        dense2 = tf.keras.layers.Dense(64, activation="relu")(dense1)
        policy_logits = tf.keras.layers.Dense(self.action_dim, activation="linear")(dense2)
        value = tf.keras.layers.Dense(1, activation="linear")(dense2)
        model = tf.keras.Model(inputs=inputs, outputs=[policy_logits, value])
        model.compile()
        return model

    def select_action(self, state: np.ndarray) -> Tuple[int, float]:
        state = np.expand_dims(state, axis=0)
        logits, value = self.model(state, training=False)
        logits = logits.numpy()[0]
        probs = tf.nn.softmax(logits).numpy()
        action = np.random.choice(self.action_dim, p=probs)
        return int(action), float(value.numpy()[0][0])

    def train_batch(
        self,
        states: np.ndarray,
        actions: np.ndarray,
        advantages: np.ndarray,
        returns: np.ndarray,
    ) -> float:
        with tf.GradientTape() as tape:
            logits, values = self.model(states, training=True)
            values = tf.squeeze(values, axis=1)
            value_loss = tf.reduce_mean(tf.square(returns - values))
            policy = tf.nn.log_softmax(logits)
            indices = tf.stack([tf.range(tf.shape(actions)[0]), actions], axis=1)
            picked_log_probs = tf.gather_nd(policy, indices)
            policy_loss = -tf.reduce_mean(picked_log_probs * advantages)
            entropy = -tf.reduce_mean(tf.exp(policy) * policy)
            loss = policy_loss + 0.5 * value_loss - 0.01 * entropy

        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        return float(loss.numpy())

    def save(self, path: str) -> None:
        self.model.save(path)

    def load(self, path: str) -> None:
        if Path(path).exists():
            self.model = tf.keras.models.load_model(path)
            logger.info("Модель завантажено з %s", path)
        else:
            logger.warning("Файл моделі %s не знайдено, використовую первісну модель", path)


# ------------------------------------------------------------------------------
# Trading Orchestrator
# ------------------------------------------------------------------------------


class TradingAgentRunner:
    def __init__(
        self,
        supervisor: Supervisor,
        environment: TradingEnvironment,
        executor: TradeExecutor,
        cloud_manager: CloudModelManager,
        symbol_deposit: Dict[str, float],
    ):
        self.supervisor = supervisor
        self.environment = environment
        self.executor = executor
        self.cloud_manager = cloud_manager
        self.symbol_deposit = symbol_deposit
        self.agent = ActorCriticAgent(state_dim=4, action_dim=3)
        self.replay_buffer: List[Tuple[np.ndarray, int, float, float]] = []
        self.step_counter = 0

    def bootstrap(self):
        try:
            if self.cloud_manager.load_model(MODEL_FILE_NAME):
                self.agent.load(MODEL_FILE_NAME)
            else:
                logger.info("Запускаю агента з випадковими параметрами")
        except Exception as exc:  # noqa: BLE001
            logger.error("Не вдалося завантажити модель: %s", exc)

    def _calculate_position(self, symbol: str, risk_band: RiskBand) -> float:
        base, quote = symbol.split("/")
        usdt_balance = self.executor.get_balance(quote)
        max_position = self.executor.max_position_size(usdt_balance)
        price = self.environment.last_prices.get(symbol) or self.executor.exchange.fetch_ticker(
            symbol
        )["last"]
        amount = max_position / price
        logger.debug(
            "Розрахунок позиції %s: баланс=%.2f, ціна=%.2f, кількість=%.6f",
            symbol,
            usdt_balance,
            price,
            amount,
        )
        return max(amount, 0.0)

    def _action_to_order(self, action: int) -> str:
        mapping = {0: "hold", 1: "buy", 2: "sell"}
        return mapping.get(action, "hold")

    def run(self, stop_event: threading.Event):
        self.bootstrap()
        logger.info("Старт торгового циклу")
        episode_rewards: List[float] = []
        while not stop_event.is_set():
            try:
                state, symbol, market_ctx = self.environment.get_state()
                current_band = self.supervisor.evaluate_market_noise(
                    vol_ratio=market_ctx["vol_ratio"],
                    book_pressure=market_ctx["book_pressure"],
                    trend_strength=market_ctx["trend_strength"],
                )
                action, value_estimate = self.agent.select_action(state)
                decision = self._action_to_order(action)

                reward = 0.0
                info: Dict[str, Any] = {"symbol": symbol, "decision": decision}

                if decision in {"buy", "sell"}:
                    amount = self._calculate_position(symbol, current_band)
                    if amount > 0:
                        order = self.executor.execute(symbol, decision, amount)
                        info["order"] = order
                        reward = self._evaluate_trade(symbol, decision, order)
                else:
                    info["note"] = "Пропуск дії"

                self._record_experience(state, action, reward, value_estimate)
                episode_rewards.append(reward)

                logger.info("Крок %s | %s | винагорода %.5f", self.step_counter, info, reward)

                if len(self.replay_buffer) >= TRAIN_BATCH_SIZE:
                    self._train_from_buffer()
                    episode_rewards.clear()

                if self.step_counter % SAVE_MODEL_INTERVAL_STEPS == 0:
                    self._persist_model()

                self.step_counter += 1
                time.sleep(POLL_INTERVAL_SECONDS)
            except Exception as exc:  # noqa: BLE001
                logger.exception("Неочікувана помилка в торговому циклі: %s", exc)
                time.sleep(POLL_INTERVAL_SECONDS)

    def _record_experience(self, state, action, reward, value_estimate):
        self.replay_buffer.append((state, action, reward, value_estimate))
        if len(self.replay_buffer) > 5 * TRAIN_BATCH_SIZE:
            self.replay_buffer.pop(0)

    def _train_from_buffer(self):
        states, actions, rewards, values = zip(*self.replay_buffer)
        states = np.stack(states)
        actions = np.array(actions)
        rewards = np.array(rewards, dtype=np.float32)
        values = np.array(values, dtype=np.float32)

        returns = np.zeros_like(rewards)
        running_return = 0.0
        for t in reversed(range(len(rewards))):
            running_return = rewards[t] + self.agent.gamma * running_return
            returns[t] = running_return

        advantages = returns - values
        loss = self.agent.train_batch(states, actions, advantages, returns)
        logger.info("Оновлено агент (втрата %.5f)", loss)
        self.replay_buffer.clear()

    def _persist_model(self):
        try:
            self.agent.save(MODEL_FILE_NAME)
            drive_id = self.cloud_manager.save_model(MODEL_FILE_NAME)
            logger.info("Модель збережено. DriveID=%s", drive_id)
        except Exception as exc:  # noqa: BLE001
            logger.error("Не вдалося зберегти модель: %s", exc)

    def _evaluate_trade(self, symbol: str, decision: str, order: Optional[Dict[str, Any]]) -> float:
        if not order:
            return -0.001  # невелике покарання
        fills = order.get("trades") or []
        pnl = sum(float(fill.get("fee", {}).get("cost", 0)) for fill in fills)
        pnl -= order.get("fee", {}).get("cost", 0)
        return float(pnl)


# ------------------------------------------------------------------------------
# Flask App & Background Thread
# ------------------------------------------------------------------------------


app = Flask(__name__)
exchange = build_exchange()
user_mode = os.getenv("TRADING_MODE", "BALANCED").upper()
if user_mode not in RiskBand.__members__:
    logger.warning("Некоректний TRADING_MODE=%s, встановлено BALANCED", user_mode)
    user_mode = "BALANCED"

supervisor = Supervisor(RiskBand[user_mode])
data_fetcher = MarketDataFetcher(exchange, DEFAULT_SYMBOLS)
environment = TradingEnvironment(data_fetcher, DEFAULT_SYMBOLS)
executor = TradeExecutor(exchange, supervisor)
cloud_manager = CloudModelManager(CLIENT_SECRETS_FILE, TOKEN_FILE, MODEL_DRIVE_FILE_ID)
symbol_deposit = {symbol: float(os.getenv("DEPOSIT_USDT", "1000")) for symbol in DEFAULT_SYMBOLS}

stop_event = threading.Event()
agent_runner = TradingAgentRunner(supervisor, environment, executor, cloud_manager, symbol_deposit)


def start_background_thread():
    if not hasattr(start_background_thread, "thread") or not start_background_thread.thread.is_alive():  # type: ignore[attr-defined]
        start_background_thread.thread = threading.Thread(  # type: ignore[attr-defined]
            target=agent_runner.run,
            name="TradingAgentThread",
            args=(stop_event,),
            daemon=True,
        )
        start_background_thread.thread.start()  # type: ignore[attr-defined]
        logger.info("Фоновий агент запущено")


@app.route("/", methods=["GET"])
def healthcheck():
    start_background_thread()
    return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()})


@app.route("/supervisor", methods=["GET"])
def get_supervisor():
    return jsonify(
        {
            "user_mode": supervisor.user_selected.value,
            "current_band": supervisor.current_band.value,
            "max_position_fraction": supervisor.current_band.max_position_fraction,
        }
    )


@app.route("/config", methods=["POST"])
def update_config():
    payload = request.get_json(force=True, silent=True) or {}
    symbols = payload.get("symbols")
    if symbols and isinstance(symbols, list):
        environment.symbols = symbols
    poll_interval = payload.get("poll_interval_seconds")
    if poll_interval:
        global POLL_INTERVAL_SECONDS  # noqa: PLW0603
        POLL_INTERVAL_SECONDS = int(poll_interval)
    return jsonify({"updated": True, "symbols": environment.symbols, "poll": POLL_INTERVAL_SECONDS})


@app.route("/shutdown", methods=["POST"])
def shutdown_agent():
    stop_event.set()
    return jsonify({"status": "stopping"})


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------


def create_app() -> Flask:
    return app


if __name__ == "__main__":
    start_background_thread()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
"""
Streamlit веб-інтерфейс для системи арбітражу
"""

import streamlit as st
import asyncio
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

from config import Config
from main import TradingBot


class ArbitrageApp:
    """Головний клас Streamlit додатку"""
    
    def __init__(self):
        self.config = Config()
        self.system = None
        self.setup_page()
    
    def setup_page(self):
        """Налаштування сторінки"""
        st.set_page_config(
            page_title="Система Арбітражу",
            page_icon="💰",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🚀 Система Міжбіржового Арбітражу")
        st.markdown("---")
    
    def run(self):
        """Запуск додатку"""
        # Бокова панель
        self.render_sidebar()
        
        # Основна панель
        self.render_main_panel()
    
    def render_sidebar(self):
        """Рендеринг бокової панелі"""
        with st.sidebar:
            st.header("🎛️ Управління")
            
            # Статус системи
            if self.system:
                status = self.system.get_status()
                if status['is_running']:
                    st.success("🟢 Система активна")
                    st.info(f"Активний модуль: {status['active_module']}")
                else:
                    st.error("🔴 Система зупинена")
            else:
                st.warning("⚠️ Система не ініціалізована")
            
            st.markdown("---")
            
            # Кнопки управління
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("▶️ Запустити", key="start_btn"):
                    self.start_system()
            
            with col2:
                if st.button("⏹️ Зупинити", key="stop_btn"):
                    self.stop_system()
            
            st.markdown("---")
            
            # Налаштування
            st.header("⚙️ Налаштування")
            
            # Управління ризиками
            st.subheader("🛡️ Ризики")
            max_position = st.number_input(
                "Макс. розмір позиції (USD)",
                min_value=100.0,
                max_value=10000.0,
                value=self.config.RISK.max_position_size,
                step=100.0
            )
            
            max_daily_loss = st.number_input(
                "Макс. денний збиток (USD)",
                min_value=10.0,
                max_value=1000.0,
                value=self.config.RISK.max_daily_loss,
                step=10.0
            )
            
            min_profit = st.number_input(
                "Мін. прибуток (%)",
                min_value=0.01,
                max_value=5.0,
                value=self.config.RISK.min_profit_threshold,
                step=0.01
            )
            
            # Копітрейдинг
            st.subheader("📋 Копітрейдинг")
            copy_ratio = st.slider(
                "Коефіцієнт копіювання",
                min_value=0.1,
                max_value=2.0,
                value=self.config.COPY_TRADING.copy_ratio,
                step=0.1
            )
            
            min_copy_profit = st.number_input(
                "Мін. прибуток для копіювання (%)",
                min_value=0.1,
                max_value=10.0,
                value=self.config.COPY_TRADING.min_profit_threshold,
                step=0.1
            )
    
    def render_main_panel(self):
        """Рендеринг основної панелі"""
        # Вкладки
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Дашборд", 
            "💰 Арбітраж", 
            "📋 Копітрейдинг", 
            "🔍 Сканер ринку", 
            "📈 Статистика"
        ])
        
        with tab1:
            self.render_dashboard()
        
        with tab2:
            self.render_arbitrage_tab()
        
        with tab3:
            self.render_copy_trading_tab()
        
        with tab4:
            self.render_market_scanner_tab()
        
        with tab5:
            self.render_statistics_tab()
    
    def render_dashboard(self):
        """Рендеринг дашборду"""
        st.header("📊 Загальний дашборд")
        
        if not self.system:
            st.warning("⚠️ Система не ініціалізована. Натисніть 'Запустити' в боковій панелі.")
            return
        
        status = self.system.get_status()
        
        # Метрики
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Статус системи",
                "🟢 Активна" if status['is_running'] else "🔴 Зупинена",
                delta=None
            )
        
        with col2:
            active_module = status.get('active_module', 'Немає')
            st.metric(
                "Активний модуль",
                active_module,
                delta=None
            )
        
        with col3:
            # Загальна статистика
            total_trades = sum(
                module_stats.get('stats', {}).get('successful_trades', 0) 
                for module_stats in status.get('modules_status', {}).values()
            )
            st.metric(
                "Всього угод",
                total_trades,
                delta=None
            )
        
        with col4:
            # Загальний прибуток
            total_profit = sum(
                module_stats.get('stats', {}).get('total_profit', 0) 
                for module_stats in status.get('modules_status', {}).values()
            )
            st.metric(
                "Загальний прибуток",
                f"${total_profit:.2f}",
                delta=None
            )
        
        st.markdown("---")
        
        # Статус модулів
        st.subheader("🔧 Статус модулів")
        
        modules_data = []
        for module_name, module_status in status.get('modules_status', {}).items():
            modules_data.append({
                'Модуль': module_name,
                'Ініціалізовано': '✅' if module_status.get('is_initialized') else '❌',
                'Працює': '✅' if module_status.get('is_running') else '❌',
                'Угоди': module_status.get('stats', {}).get('successful_trades', 0),
                'Прибуток': f"${module_status.get('stats', {}).get('total_profit', 0):.2f}",
                'Останнє оновлення': module_status.get('last_update', 'Немає')
            })
        
        if modules_data:
            df_modules = pd.DataFrame(modules_data)
            st.dataframe(df_modules, use_container_width=True)
        else:
            st.info("📝 Немає даних про модулі")
    
    def render_arbitrage_tab(self):
        """Рендеринг вкладки арбітражу"""
        st.header("💰 Міжбіржовий арбітраж")
        
        if not self.system:
            st.warning("⚠️ Система не ініціалізована")
            return
        
        # Поточні можливості
        st.subheader("🎯 Поточні арбітражні можливості")
        
        # Mock дані для демонстрації
        opportunities_data = [
            {
                'Пара': 'BTC/USDT',
                'Купівля': 'Binance',
                'Продаж': 'Bybit',
                'Ціна купівлі': 50000.0,
                'Ціна продажу': 50050.0,
                'Спред (%)': 0.1,
                'Чистий прибуток (%)': 0.08,
                'Обсяг': 1000.0
            },
            {
                'Пара': 'ETH/USDT',
                'Купівля': 'KuCoin',
                'Продаж': 'Binance',
                'Ціна купівлі': 3000.0,
                'Ціна продажу': 3005.0,
                'Спред (%)': 0.17,
                'Чистий прибуток (%)': 0.15,
                'Обсяг': 500.0
            }
        ]
        
        df_opportunities = pd.DataFrame(opportunities_data)
        st.dataframe(df_opportunities, use_container_width=True)
        
        # Графік спредів
        st.subheader("📈 Графік спредів")
        
        fig = px.bar(
            df_opportunities, 
            x='Пара', 
            y='Спред (%)',
            title='Арбітражні спреди по парах',
            color='Чистий прибуток (%)',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def render_copy_trading_tab(self):
        """Рендеринг вкладки копітрейдингу"""
        st.header("📋 Копітрейдинг з Traiex")
        
        if not self.system:
            st.warning("⚠️ Система не ініціалізована")
            return
        
        # Статистика бота
        st.subheader("🤖 Статистика бота Traiex")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Всього угод", "150", delta="+5")
        
        with col2:
            st.metric("Прибуткових угод", "95", delta="+3")
        
        with col3:
            st.metric("Win Rate", "63.3%", delta="+2.1%")
        
        with col4:
            st.metric("Загальний прибуток", "$1,250.50", delta="+$45.20")
        
        # Останні скопійовані угоди
        st.subheader("📋 Останні скопійовані угоди")
        
        copied_trades_data = [
            {
                'Час': '2024-01-15 14:30:25',
                'Пара': 'BTC/USDT',
                'Сторона': 'Купівля',
                'Обсяг': 0.1,
                'Ціна': 50000.0,
                'Біржа': 'Binance',
                'Статус': 'Виконано'
            },
            {
                'Час': '2024-01-15 14:25:10',
                'Пара': 'ETH/USDT',
                'Сторона': 'Продаж',
                'Обсяг': 1.0,
                'Ціна': 3000.0,
                'Біржа': 'Bybit',
                'Статус': 'Виконано'
            }
        ]
        
        df_copied = pd.DataFrame(copied_trades_data)
        st.dataframe(df_copied, use_container_width=True)
    
    def render_market_scanner_tab(self):
        """Рендеринг вкладки сканера ринку"""
        st.header("🔍 Сканер ринку")
        
        if not self.system:
            st.warning("⚠️ Система не ініціалізована")
            return
        
        # Топ торгові пари
        st.subheader("🏆 Топ торгові пари")
        
        top_pairs_data = [
            {'Ранг': 1, 'Пара': 'BTC/USDT', 'Рейтинг': 8.5, 'Ліквідність': 9.2, 'Спред (%)': 0.15},
            {'Ранг': 2, 'Пара': 'ETH/USDT', 'Рейтинг': 7.8, 'Ліквідність': 8.5, 'Спред (%)': 0.12},
            {'Ранг': 3, 'Пара': 'BNB/USDT', 'Рейтинг': 7.2, 'Ліквідність': 7.8, 'Спред (%)': 0.18},
            {'Ранг': 4, 'Пара': 'ADA/USDT', 'Рейтинг': 6.9, 'Ліквідність': 6.5, 'Спред (%)': 0.25},
            {'Ранг': 5, 'Пара': 'SOL/USDT', 'Рейтинг': 6.5, 'Ліквідність': 7.1, 'Спред (%)': 0.22}
        ]
        
        df_top_pairs = pd.DataFrame(top_pairs_data)
        st.dataframe(df_top_pairs, use_container_width=True)
        
        # Графік рейтингів
        st.subheader("📊 Графік рейтингів")
        
        fig = px.scatter(
            df_top_pairs,
            x='Ліквідність',
            y='Спред (%)',
            size='Рейтинг',
            color='Рейтинг',
            hover_name='Пара',
            title='Рейтинг торгових пар',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def render_statistics_tab(self):
        """Рендеринг вкладки статистики"""
        st.header("📈 Статистика")
        
        if not self.system:
            st.warning("⚠️ Система не ініціалізована")
            return
        
        # Загальна статистика
        st.subheader("📊 Загальна статистика")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Графік прибутку по днях
            dates = pd.date_range(start='2024-01-01', end='2024-01-15', freq='D')
            profits = [25.50, 45.20, 32.10, 67.80, 23.45, 89.30, 56.70, 34.20, 78.90, 45.60, 67.30, 23.80, 56.40, 89.70, 34.50]
            
            fig_profit = px.line(
                x=dates, 
                y=profits,
                title='Прибуток по днях',
                labels={'x': 'Дата', 'y': 'Прибуток (USD)'}
            )
            st.plotly_chart(fig_profit, use_container_width=True)
        
        with col2:
            # Розподіл угод по модулях
            modules = ['Арбітраж', 'Копітрейдинг', 'Сканер']
            trades_count = [45, 78, 12]
            
            fig_dist = px.pie(
                values=trades_count,
                names=modules,
                title='Розподіл угод по модулях'
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        
        # Детальна статистика
        st.subheader("📋 Детальна статистика")
        
        stats_data = [
            {'Метрика': 'Всього угод', 'Значення': '135', 'Зміна': '+12'},
            {'Метрика': 'Успішних угод', 'Значення': '98', 'Зміна': '+8'},
            {'Метрика': 'Win Rate', 'Значення': '72.6%', 'Зміна': '+3.2%'},
            {'Метрика': 'Загальний прибуток', 'Значення': '$1,234.50', 'Зміна': '+$156.80'},
            {'Метрика': 'Середній прибуток', 'Значення': '$9.14', 'Зміна': '+$1.23'},
            {'Метрика': 'Максимальний прибуток', 'Значення': '$89.30', 'Зміна': 'Новий рекорд'},
            {'Метрика': 'Максимальний збиток', 'Значення': '$12.50', 'Зміна': '-$2.10'}
        ]
        
        df_stats = pd.DataFrame(stats_data)
        st.dataframe(df_stats, use_container_width=True)
    
    def start_system(self):
        """Запуск системи"""
        try:
            if not self.system:
                self.system = TradingBot()
            
            # Запуск в окремому потоці
            asyncio.create_task(self.system.start())
            st.success("✅ Система запущена!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Помилка запуску системи: {e}")
    
    def stop_system(self):
        """Зупинка системи"""
        try:
            if self.system:
                asyncio.create_task(self.system.stop())
                st.success("✅ Система зупинена!")
                st.rerun()
            else:
                st.warning("⚠️ Система не запущена")
                
        except Exception as e:
            st.error(f"❌ Помилка зупинки системи: {e}")


def main():
    """Головна функція"""
    app = ArbitrageApp()
    app.run()


if __name__ == "__main__":
    main()

```

```python
import logging
import os
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import ccxt
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, jsonify, request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request as GoogleAuthRequest
import googleapiclient.http


# ------------------------------------------------------------------------------
# Configuration & Logging
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(threadName)s %(message)s",
)
logger = logging.getLogger(__name__)

MODEL_FILE_NAME = os.getenv("MODEL_FILE_NAME", "agent_model.keras")
MODEL_DRIVE_FILE_ID = os.getenv("MODEL_DRIVE_FILE_ID")
CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRETS_FILE", "client_secrets.json")
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive.file"]

CCXT_API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
CCXT_SECRET_KEY = os.getenv("BINANCE_TESTNET_SECRET_KEY")

DEFAULT_SYMBOLS = ["BTC/USDT", "ETH/USDT"]
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))
SAVE_MODEL_INTERVAL_STEPS = int(os.getenv("SAVE_MODEL_INTERVAL_STEPS", "30"))
TRAIN_BATCH_SIZE = int(os.getenv("TRAIN_BATCH_SIZE", "32"))
MAX_EPISODE_LENGTH = int(os.getenv("MAX_EPISODE_LENGTH", "96"))  # roughly 96 minutes


# ------------------------------------------------------------------------------
# Risk Management
# ------------------------------------------------------------------------------


class RiskBand(Enum):
    CONSERVATIVE = "CONSERVATIVE"
    BALANCED_CONSERVATIVE = "BALANCED_CONSERVATIVE"
    BALANCED = "BALANCED"
    BALANCED_AGGRESSIVE = "BALANCED_AGGRESSIVE"
    AGGRESSIVE = "AGGRESSIVE"

    @property
    def max_position_fraction(self) -> float:
        mapping = {
            RiskBand.CONSERVATIVE: 0.10,
            RiskBand.BALANCED_CONSERVATIVE: 0.15,
            RiskBand.BALANCED: 0.20,
            RiskBand.BALANCED_AGGRESSIVE: 0.25,
            RiskBand.AGGRESSIVE: 0.30,
        }
        return mapping[self]


RISK_DOWNGRADE_PATHS: Dict[RiskBand, List[RiskBand]] = {
    RiskBand.CONSERVATIVE: [RiskBand.CONSERVATIVE],
    RiskBand.BALANCED: [
        RiskBand.BALANCED,
        RiskBand.BALANCED_CONSERVATIVE,
        RiskBand.CONSERVATIVE,
    ],
    RiskBand.AGGRESSIVE: [
        RiskBand.AGGRESSIVE,
        RiskBand.BALANCED_AGGRESSIVE,
        RiskBand.BALANCED,
        RiskBand.BALANCED_CONSERVATIVE,
        RiskBand.CONSERVATIVE,
    ],
}


class Supervisor:
    """AI supervisor that enforces multi-level risk governance."""

    def __init__(self, user_selected: RiskBand):
        self.user_selected = user_selected
        self.current_band = user_selected

    def evaluate_market_noise(
        self,
        vol_ratio: float,
        book_pressure: float,
        trend_strength: float,
    ) -> RiskBand:
        """
        Decide on a safer risk band depending on market conditions.
        Higher volatility or imbalanced books => lower risk.
        """
        candidates = RISK_DOWNGRADE_PATHS[self.user_selected]
        score = (vol_ratio * 0.5) + (abs(book_pressure) * 0.3) - (abs(trend_strength) * 0.2)
        logger.debug("Supervisor noise score %.4f", score)

        if score > 1.5 and len(candidates) > 1:
            self.current_band = candidates[-1]
        elif score > 1.0 and len(candidates) > 2:
            self.current_band = candidates[-2]
        elif score > 0.7 and len(candidates) > 3:
            self.current_band = candidates[-3]
        else:
            self.current_band = candidates[0]

        logger.info("Supervisor risk band -> %s", self.current_band.value)
        return self.current_band


# ------------------------------------------------------------------------------
# Google Drive Persistence
# ------------------------------------------------------------------------------


class CloudModelManager:
    def __init__(
        self,
        client_secrets_path: str,
        token_path: str,
        drive_file_id: Optional[str],
    ) -> None:
        self.client_secrets_path = client_secrets_path
        self.token_path = token_path
        self.drive_file_id = drive_file_id
        self._service = None

    def _get_credentials(self) -> Credentials:
        if not Path(self.client_secrets_path).exists():
            raise FileNotFoundError(
                f"client_secrets.json не знайдено за шляхом {self.client_secrets_path}"
            )

        creds: Optional[Credentials] = None
        token_file = Path(self.token_path)
        if token_file.exists():
            creds = Credentials.from_authorized_user_file(self.token_path, DRIVE_SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Оновлення Google Drive токена")
                creds.refresh(GoogleAuthRequest())
            else:
                from google_auth_oauthlib.flow import InstalledAppFlow

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_path,
                    DRIVE_SCOPES,
                )
                logger.info("Запуск OAuth-флоу для Google Drive")
                creds = flow.run_console()
            token_file.write_text(creds.to_json(), encoding="utf-8")

        return creds

    def _get_service(self):
        if self._service is None:
            creds = self._get_credentials()
            self._service = build("drive", "v3", credentials=creds, cache_discovery=False)
        return self._service

    def load_model(self, local_path: str) -> bool:
        if not self.drive_file_id:
            logger.warning("MODEL_DRIVE_FILE_ID не заданий; пропускаю завантаження моделі")
            return False

        service = self._get_service()
        try:
            logger.info("Завантаження моделі з Google Drive (%s)", self.drive_file_id)
            request = service.files().get_media(fileId=self.drive_file_id)
            fh = tf.io.gfile.GFile(local_path, "wb")
            downloader = googleapiclient.http.MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.debug("Завантажено %.2f%%", status.progress() * 100)
            fh.close()
            return True
        except HttpError as exc:
            logger.error("Не вдалося завантажити модель: %s", exc)
            return False

    def save_model(self, local_path: str) -> Optional[str]:
        service = self._get_service()
        if not Path(local_path).exists():
            logger.warning("Немає файлу моделі %s для завантаження", local_path)
            return self.drive_file_id

        metadata = {
            "name": MODEL_FILE_NAME,
            "mimeType": "application/octet-stream",
        }
        media = googleapiclient.http.MediaFileUpload(local_path, resumable=True)

        try:
            if self.drive_file_id:
                logger.info("Оновлення моделі на Google Drive (%s)", self.drive_file_id)
                updated = (
                    service.files()
                    .update(fileId=self.drive_file_id, media_body=media, body=metadata)
                    .execute()
                )
            else:
                logger.info("Створення нового файлу моделі на Google Drive")
                updated = service.files().create(media_body=media, body=metadata).execute()

            self.drive_file_id = updated.get("id")
            os.environ["MODEL_DRIVE_FILE_ID"] = self.drive_file_id
            return self.drive_file_id
        except HttpError as exc:
            logger.error("Не вдалося зберегти модель на Google Drive: %s", exc)
            return None


# ------------------------------------------------------------------------------
# Market Data & Execution
# ------------------------------------------------------------------------------


def build_exchange() -> ccxt.Exchange:
    exchange = ccxt.binance(
        {
            "enableRateLimit": True,
            "apiKey": CCXT_API_KEY,
            "secret": CCXT_SECRET_KEY,
            "timeout": 30000,
            "options": {"defaultType": "spot"},
        }
    )
    exchange.set_sandbox_mode(True)
    return exchange


class MarketDataFetcher:
    def __init__(self, exchange: ccxt.Exchange, symbols: List[str]):
        self.exchange = exchange
        self.symbols = symbols

    def get_recent_ohlcv(self, symbol: str, since_ms: Optional[int] = None) -> pd.DataFrame:
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe="1m", since=since_ms, limit=200)
        df = pd.DataFrame(
            ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        return df

    def get_ta_features(self, df: pd.DataFrame) -> Dict[str, float]:
        if df.empty:
            return {"rsi": 50.0, "ma_fast": 0.0, "ma_slow": 0.0, "volatility": 0.0}

        close = df["close"]
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-9)
        rsi = 100 - (100 / (1 + rs.iloc[-1]))

        ma_fast = close.rolling(window=10).mean().iloc[-1]
        ma_slow = close.rolling(window=30).mean().iloc[-1]
        volatility = close.pct_change().rolling(window=30).std().iloc[-1]

        return {
            "rsi": float(np.nan_to_num(rsi, nan=50.0)),
            "ma_fast": float(np.nan_to_num(ma_fast, nan=close.iloc[-1])),
            "ma_slow": float(np.nan_to_num(ma_slow, nan=close.iloc[-1])),
            "volatility": float(np.nan_to_num(volatility, nan=0.0)),
        }

    def get_order_book_metrics(self, symbol: str) -> Dict[str, float]:
        order_book = self.exchange.fetch_order_book(symbol)
        bids = np.array(order_book["bids"][:20])
        asks = np.array(order_book["asks"][:20])
        bid_volume = bids[:, 1].sum() if bids.size else 0.0
        ask_volume = asks[:, 1].sum() if asks.size else 0.0
        imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume + 1e-9)
        return {
            "bid_volume": float(bid_volume),
            "ask_volume": float(ask_volume),
            "imbalance": float(imbalance),
        }


class TradeExecutor:
    def __init__(self, exchange: ccxt.Exchange, supervisor: Supervisor):
        self.exchange = exchange
        self.supervisor = supervisor

    def get_balance(self, asset: str) -> float:
        balance = self.exchange.fetch_balance()
        return float(balance.get(asset, {}).get("free", 0.0))

    def execute(self, symbol: str, side: str, amount: float) -> Optional[Dict[str, Any]]:
        try:
            logger.info("Виконання ордеру %s %s %.6f", symbol, side, amount)
            if amount <= 0:
                return None
            order = self.exchange.create_market_order(symbol, side.lower(), amount)
            return order
        except Exception as exc:  # noqa: BLE001
            logger.error("Помилка виконання ордеру: %s", exc)
            return None

    def max_position_size(self, usdt_balance: float) -> float:
        allowed_fraction = self.supervisor.current_band.max_position_fraction
        return usdt_balance * allowed_fraction


# ------------------------------------------------------------------------------
# Reinforcement Learning Agent
# ------------------------------------------------------------------------------


class TradingEnvironment:
    def __init__(self, data_fetcher: MarketDataFetcher, symbols: List[str]):
        self.data_fetcher = data_fetcher
        self.symbols = symbols
        self.last_prices: Dict[str, float] = {s: 0.0 for s in symbols}

    def get_state(self) -> Tuple[np.ndarray, str]:
        symbol = self._select_symbol()
        df = self.data_fetcher.get_recent_ohlcv(symbol)
        ta = self.data_fetcher.get_ta_features(df)
        book = self.data_fetcher.get_order_book_metrics(symbol)
        latest_price = df["close"].iloc[-1] if not df.empty else self.last_prices[symbol]
        self.last_prices[symbol] = latest_price

        state_vector = np.array(
            [
                ta["rsi"] / 100.0,
                (ta["ma_fast"] - ta["ma_slow"]) / (latest_price + 1e-9),
                ta["volatility"],
                book["imbalance"],
            ],
            dtype=np.float32,
        )
        market_context = {
            "vol_ratio": max(ta["volatility"], 1e-6) * 100,
            "book_pressure": book["imbalance"],
            "trend_strength": ta["ma_fast"] - ta["ma_slow"],
        }
        return state_vector, symbol, market_context

    def _select_symbol(self) -> str:
        weights = []
        for symbol in self.symbols:
            df = self.data_fetcher.get_recent_ohlcv(symbol)
            if df.empty:
                weights.append(1.0)
            else:
                weights.append(df["volume"].iloc[-30:].mean())
        total = sum(weights)
        weights = [w / total if total else 1 / len(self.symbols) for w in weights]
        return np.random.choice(self.symbols, p=weights)


class ActorCriticAgent:
    def __init__(self, state_dim: int, action_dim: int, learning_rate: float = 1e-4):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = 0.99
        self.learning_rate = learning_rate
        self.model = self._build_model()
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)

    def _build_model(self) -> tf.keras.Model:
        inputs = tf.keras.Input(shape=(self.state_dim,))
        dense1 = tf.keras.layers.Dense(64, activation="relu")(inputs)
        dense2 = tf.keras.layers.Dense(64, activation="relu")(dense1)
        policy_logits = tf.keras.layers.Dense(self.action_dim, activation="linear")(dense2)
        value = tf.keras.layers.Dense(1, activation="linear")(dense2)
        model = tf.keras.Model(inputs=inputs, outputs=[policy_logits, value])
        model.compile()
        return model

    def select_action(self, state: np.ndarray) -> Tuple[int, float]:
        state = np.expand_dims(state, axis=0)
        logits, value = self.model(state, training=False)
        logits = logits.numpy()[0]
        probs = tf.nn.softmax(logits).numpy()
        action = np.random.choice(self.action_dim, p=probs)
        return int(action), float(value.numpy()[0][0])

    def train_batch(
        self,
        states: np.ndarray,
        actions: np.ndarray,
        advantages: np.ndarray,
        returns: np.ndarray,
    ) -> float:
        with tf.GradientTape() as tape:
            logits, values = self.model(states, training=True)
            values = tf.squeeze(values, axis=1)
            value_loss = tf.reduce_mean(tf.square(returns - values))
            policy = tf.nn.log_softmax(logits)
            indices = tf.stack([tf.range(tf.shape(actions)[0]), actions], axis=1)
            picked_log_probs = tf.gather_nd(policy, indices)
            policy_loss = -tf.reduce_mean(picked_log_probs * advantages)
            entropy = -tf.reduce_mean(tf.exp(policy) * policy)
            loss = policy_loss + 0.5 * value_loss - 0.01 * entropy

        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        return float(loss.numpy())

    def save(self, path: str) -> None:
        self.model.save(path)

    def load(self, path: str) -> None:
        if Path(path).exists():
            self.model = tf.keras.models.load_model(path)
            logger.info("Модель завантажено з %s", path)
        else:
            logger.warning("Файл моделі %s не знайдено, використовую первісну модель", path)


# ------------------------------------------------------------------------------
# Trading Orchestrator
# ------------------------------------------------------------------------------


class TradingAgentRunner:
    def __init__(
        self,
        supervisor: Supervisor,
        environment: TradingEnvironment,
        executor: TradeExecutor,
        cloud_manager: CloudModelManager,
        symbol_deposit: Dict[str, float],
    ):
        self.supervisor = supervisor
        self.environment = environment
        self.executor = executor
        self.cloud_manager = cloud_manager
        self.symbol_deposit = symbol_deposit
        self.agent = ActorCriticAgent(state_dim=4, action_dim=3)
        self.replay_buffer: List[Tuple[np.ndarray, int, float, float]] = []
        self.step_counter = 0

    def bootstrap(self):
        try:
            if self.cloud_manager.load_model(MODEL_FILE_NAME):
                self.agent.load(MODEL_FILE_NAME)
            else:
                logger.info("Запускаю агента з випадковими параметрами")
        except Exception as exc:  # noqa: BLE001
            logger.error("Не вдалося завантажити модель: %s", exc)

    def _calculate_position(self, symbol: str, risk_band: RiskBand) -> float:
        base, quote = symbol.split("/")
        usdt_balance = self.executor.get_balance(quote)
        max_position = self.executor.max_position_size(usdt_balance)
        price = self.environment.last_prices.get(symbol) or self.executor.exchange.fetch_ticker(
            symbol
        )["last"]
        amount = max_position / price
        logger.debug(
            "Розрахунок позиції %s: баланс=%.2f, ціна=%.2f, кількість=%.6f",
            symbol,
            usdt_balance,
            price,
            amount,
        )
        return max(amount, 0.0)

    def _action_to_order(self, action: int) -> str:
        mapping = {0: "hold", 1: "buy", 2: "sell"}
        return mapping.get(action, "hold")

    def run(self, stop_event: threading.Event):
        self.bootstrap()
        logger.info("Старт торгового циклу")
        episode_rewards: List[float] = []
        while not stop_event.is_set():
            try:
                state, symbol, market_ctx = self.environment.get_state()
                current_band = self.supervisor.evaluate_market_noise(
                    vol_ratio=market_ctx["vol_ratio"],
                    book_pressure=market_ctx["book_pressure"],
                    trend_strength=market_ctx["trend_strength"],
                )
                action, value_estimate = self.agent.select_action(state)
                decision = self._action_to_order(action)

                reward = 0.0
                info: Dict[str, Any] = {"symbol": symbol, "decision": decision}

                if decision in {"buy", "sell"}:
                    amount = self._calculate_position(symbol, current_band)
                    if amount > 0:
                        order = self.executor.execute(symbol, decision, amount)
                        info["order"] = order
                        reward = self._evaluate_trade(symbol, decision, order)
                else:
                    info["note"] = "Пропуск дії"

                self._record_experience(state, action, reward, value_estimate)
                episode_rewards.append(reward)

                logger.info("Крок %s | %s | винагорода %.5f", self.step_counter, info, reward)

                if len(self.replay_buffer) >= TRAIN_BATCH_SIZE:
                    self._train_from_buffer()
                    episode_rewards.clear()

                if self.step_counter % SAVE_MODEL_INTERVAL_STEPS == 0:
                    self._persist_model()

                self.step_counter += 1
                time.sleep(POLL_INTERVAL_SECONDS)
            except Exception as exc:  # noqa: BLE001
                logger.exception("Неочікувана помилка в торговому циклі: %s", exc)
                time.sleep(POLL_INTERVAL_SECONDS)

    def _record_experience(self, state, action, reward, value_estimate):
        self.replay_buffer.append((state, action, reward, value_estimate))
        if len(self.replay_buffer) > 5 * TRAIN_BATCH_SIZE:
            self.replay_buffer.pop(0)

    def _train_from_buffer(self):
        states, actions, rewards, values = zip(*self.replay_buffer)
        states = np.stack(states)
        actions = np.array(actions)
        rewards = np.array(rewards, dtype=np.float32)
        values = np.array(values, dtype=np.float32)

        returns = np.zeros_like(rewards)
        running_return = 0.0
        for t in reversed(range(len(rewards))):
            running_return = rewards[t] + self.agent.gamma * running_return
            returns[t] = running_return

        advantages = returns - values
        loss = self.agent.train_batch(states, actions, advantages, returns)
        logger.info("Оновлено агент (втрата %.5f)", loss)
        self.replay_buffer.clear()

    def _persist_model(self):
        try:
            self.agent.save(MODEL_FILE_NAME)
            drive_id = self.cloud_manager.save_model(MODEL_FILE_NAME)
            logger.info("Модель збережено. DriveID=%s", drive_id)
        except Exception as exc:  # noqa: BLE001
            logger.error("Не вдалося зберегти модель: %s", exc)

    def _evaluate_trade(self, symbol: str, decision: str, order: Optional[Dict[str, Any]]) -> float:
        if not order:
            return -0.001  # невелике покарання
        fills = order.get("trades") or []
        pnl = sum(float(fill.get("fee", {}).get("cost", 0)) for fill in fills)
        pnl -= order.get("fee", {}).get("cost", 0)
        return float(pnl)


# ------------------------------------------------------------------------------
# Flask App & Background Thread
# ------------------------------------------------------------------------------


app = Flask(__name__)
exchange = build_exchange()
user_mode = os.getenv("TRADING_MODE", "BALANCED").upper()
if user_mode not in RiskBand.__members__:
    logger.warning("Некоректний TRADING_MODE=%s, встановлено BALANCED", user_mode)
    user_mode = "BALANCED"

supervisor = Supervisor(RiskBand[user_mode])
data_fetcher = MarketDataFetcher(exchange, DEFAULT_SYMBOLS)
environment = TradingEnvironment(data_fetcher, DEFAULT_SYMBOLS)
executor = TradeExecutor(exchange, supervisor)
cloud_manager = CloudModelManager(CLIENT_SECRETS_FILE, TOKEN_FILE, MODEL_DRIVE_FILE_ID)
symbol_deposit = {symbol: float(os.getenv("DEPOSIT_USDT", "1000")) for symbol in DEFAULT_SYMBOLS}

stop_event = threading.Event()
agent_runner = TradingAgentRunner(supervisor, environment, executor, cloud_manager, symbol_deposit)


def start_background_thread():
    if not hasattr(start_background_thread, "thread") or not start_background_thread.thread.is_alive():  # type: ignore[attr-defined]
        start_background_thread.thread = threading.Thread(  # type: ignore[attr-defined]
            target=agent_runner.run,
            name="TradingAgentThread",
            args=(stop_event,),
            daemon=True,
        )
        start_background_thread.thread.start()  # type: ignore[attr-defined]
        logger.info("Фоновий агент запущено")


@app.route("/", methods=["GET"])
def healthcheck():
    start_background_thread()
    return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()})


@app.route("/supervisor", methods=["GET"])
def get_supervisor():
    return jsonify(
        {
            "user_mode": supervisor.user_selected.value,
            "current_band": supervisor.current_band.value,
            "max_position_fraction": supervisor.current_band.max_position_fraction,
        }
    )


@app.route("/config", methods=["POST"])
def update_config():
    payload = request.get_json(force=True, silent=True) or {}
    symbols = payload.get("symbols")
    if symbols and isinstance(symbols, list):
        environment.symbols = symbols
    poll_interval = payload.get("poll_interval_seconds")
    if poll_interval:
        global POLL_INTERVAL_SECONDS  # noqa: PLW0603
        POLL_INTERVAL_SECONDS = int(poll_interval)
    return jsonify({"updated": True, "symbols": environment.symbols, "poll": POLL_INTERVAL_SECONDS})


@app.route("/shutdown", methods=["POST"])
def shutdown_agent():
    stop_event.set()
    return jsonify({"status": "stopping"})


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------


def create_app() -> Flask:
    return app


if __name__ == "__main__":
    start_background_thread()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
"""
Streamlit веб-інтерфейс для системи арбітражу
"""

import streamlit as st
import asyncio
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

from config import Config
from main import TradingBot


class ArbitrageApp:
    """Головний клас Streamlit додатку"""
    
    def __init__(self):
        self.config = Config()
        self.system = None
        self.setup_page()
    
    def setup_page(self):
        """Налаштування сторінки"""
        st.set_page_config(
            page_title="Система Арбітражу",
            page_icon="💰",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🚀 Система Міжбіржового Арбітражу")
        st.markdown("---")
    
    def run(self):
        """Запуск додатку"""
        # Бокова панель
        self.render_sidebar()
        
        # Основна панель
        self.render_main_panel()
    
    def render_sidebar(self):
        """Рендеринг бокової панелі"""
        with st.sidebar:
            st.header("🎛️ Управління")
            
            # Статус системи
            if self.system:
                status = self.system.get_status()
                if status['is_running']:
                    st.success("🟢 Система активна")
                    st.info(f"Активний модуль: {status['active_module']}")
                else:
                    st.error("🔴 Система зупинена")
            else:
                st.warning("⚠️ Система не ініціалізована")
            
            st.markdown("---")
            
            # Кнопки управління
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("▶️ Запустити", key="start_btn"):
                    self.start_system()
            
            with col2:
                if st.button("⏹️ Зупинити", key="stop_btn"):
                    self.stop_system()
            
            st.markdown("---")
            
            # Налаштування
            st.header("⚙️ Налаштування")
            
            # Управління ризиками
            st.subheader("🛡️ Ризики")
            max_position = st.number_input(
                "Макс. розмір позиції (USD)",
                min_value=100.0,
                max_value=10000.0,
                value=self.config.RISK.max_position_size,
                step=100.0
            )
            
            max_daily_loss = st.number_input(
                "Макс. денний збиток (USD)",
                min_value=10.0,
                max_value=1000.0,
                value=self.config.RISK.max_daily_loss,
                step=10.0
            )
            
            min_profit = st.number_input(
                "Мін. прибуток (%)",
                min_value=0.01,
                max_value=5.0,
                value=self.config.RISK.min_profit_threshold,
                step=0.01
            )
            
            # Копітрейдинг
            st.subheader("📋 Копітрейдинг")
            copy_ratio = st.slider(
                "Коефіцієнт копіювання",
                min_value=0.1,
                max_value=2.0,
                value=self.config.COPY_TRADING.copy_ratio,
                step=0.1
            )
            
            min_copy_profit = st.number_input(
                "Мін. прибуток для копіювання (%)",
                min_value=0.1,
                max_value=10.0,
                value=self.config.COPY_TRADING.min_profit_threshold,
                step=0.1
            )
    
    def render_main_panel(self):
        """Рендеринг основної панелі"""
        # Вкладки
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Дашборд", 
            "💰 Арбітраж", 
            "📋 Копітрейдинг", 
            "🔍 Сканер ринку", 
            "📈 Статистика"
        ])
        
        with tab1:
            self.render_dashboard()
        
        with tab2:
            self.render_arbitrage_tab()
        
        with tab3:
            self.render_copy_trading_tab()
        
        with tab4:
            self.render_market_scanner_tab()
        
        with tab5:
            self.render_statistics_tab()
    
    def render_dashboard(self):
        """Рендеринг дашборду"""
        st.header("📊 Загальний дашборд")
        
        if not self.system:
            st.warning("⚠️ Система не ініціалізована. Натисніть 'Запустити' в боковій панелі.")
            return
        
        status = self.system.get_status()
        
        # Метрики
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Статус системи",
                "🟢 Активна" if status['is_running'] else "🔴 Зупинена",
                delta=None
            )
        
        with col2:
            active_module = status.get('active_module', 'Немає')
            st.metric(
                "Активний модуль",
                active_module,
                delta=None
            )
        
        with col3:
            # Загальна статистика
            total_trades = sum(
                module_stats.get('stats', {}).get('successful_trades', 0) 
                for module_stats in status.get('modules_status', {}).values()
            )
            st.metric(
                "Всього угод",
                total_trades,
                delta=None
            )
        
        with col4:
            # Загальний прибуток
            total_profit = sum(
                module_stats.get('stats', {}).get('total_profit', 0) 
                for module_stats in status.get('modules_status', {}).values()
            )
            st.metric(
                "Загальний прибуток",
                f"${total_profit:.2f}",
                delta=None
            )
        
        st.markdown("---")
        
        # Статус модулів
        st.subheader("🔧 Статус модулів")
        
        modules_data = []
        for module_name, module_status in status.get('modules_status', {}).items():
            modules_data.append({
                'Модуль': module_name,
                'Ініціалізовано': '✅' if module_status.get('is_initialized') else '❌',
                'Працює': '✅' if module_status.get('is_running') else '❌',
                'Угоди': module_status.get('stats', {}).get('successful_trades', 0),
                'Прибуток': f"${module_status.get('stats', {}).get('total_profit', 0):.2f}",
                'Останнє оновлення': module_status.get('last_update', 'Немає')
            })
        
        if modules_data:
            df_modules = pd.DataFrame(modules_data)
            st.dataframe(df_modules, use_container_width=True)
        else:
            st.info("📝 Немає даних про модулі")
    
    def render_arbitrage_tab(self):
        """Рендеринг вкладки арбітражу"""
        st.header("💰 Міжбіржовий арбітраж")
        
        if not self.system:
            st.warning("⚠️ Система не ініціалізована")
            return
        
        # Поточні можливості
        st.subheader("🎯 Поточні арбітражні можливості")
        
        # Mock дані для демонстрації
        opportunities_data = [
            {
                'Пара': 'BTC/USDT',
                'Купівля': 'Binance',
                'Продаж': 'Bybit',
                'Ціна купівлі': 50000.0,
                'Ціна продажу': 50050.0,
                'Спред (%)': 0.1,
                'Чистий прибуток (%)': 0.08,
                'Обсяг': 1000.0
            },
            {
                'Пара': 'ETH/USDT',
                'Купівля': 'KuCoin',
                'Продаж': 'Binance',
                'Ціна купівлі': 3000.0,
                'Ціна продажу': 3005.0,
                'Спред (%)': 0.17,
                'Чистий прибуток (%)': 0.15,
                'Обсяг': 500.0
            }
        ]
        
        df_opportunities = pd.DataFrame(opportunities_data)
        st.dataframe(df_opportunities, use_container_width=True)
        
        # Графік спредів
        st.subheader("📈 Графік спредів")
        
        fig = px.bar(
            df_opportunities, 
            x='Пара', 
            y='Спред (%)',
            title='Арбітражні спреди по парах',
            color='Чистий прибуток (%)',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def render_copy_trading_tab(self):
        """Рендеринг вкладки копітрейдингу"""
        st.header("📋 Копітрейдинг з Traiex")
        
        if not self.system:
            st.warning("⚠️ Система не ініціалізована")
            return
        
        # Статистика бота
        st.subheader("🤖 Статистика бота Traiex")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Всього угод", "150", delta="+5")
        
        with col2:
            st.metric("Прибуткових угод", "95", delta="+3")
        
        with col3:
            st.metric("Win Rate", "63.3%", delta="+2.1%")
        
        with col4:
            st.metric("Загальний прибуток", "$1,250.50", delta="+$45.20")
        
        # Останні скопійовані угоди
        st.subheader("📋 Останні скопійовані угоди")
        
        copied_trades_data = [
            {
                'Час': '2024-01-15 14:30:25',
                'Пара': 'BTC/USDT',
                'Сторона': 'Купівля',
                'Обсяг': 0.1,
                'Ціна': 50000.0,
                'Біржа': 'Binance',
                'Статус': 'Виконано'
            },
            {
                'Час': '2024-01-15 14:25:10',
                'Пара': 'ETH/USDT',
                'Сторона': 'Продаж',
                'Обсяг': 1.0,
                'Ціна': 3000.0,
                'Біржа': 'Bybit',
                'Статус': 'Виконано'
            }
        ]
        
        df_copied = pd.DataFrame(copied_trades_data)
        st.dataframe(df_copied, use_container_width=True)
    
    def render_market_scanner_tab(self):
        """Рендеринг вкладки сканера ринку"""
        st.header("🔍 Сканер ринку")
        
        if not self.system:
            st.warning("⚠️ Система не ініціалізована")
            return
        
        # Топ торгові пари
        st.subheader("🏆 Топ торгові пари")
        
        top_pairs_data = [
            {'Ранг': 1, 'Пара': 'BTC/USDT', 'Рейтинг': 8.5, 'Ліквідність': 9.2, 'Спред (%)': 0.15},
            {'Ранг': 2, 'Пара': 'ETH/USDT', 'Рейтинг': 7.8, 'Ліквідність': 8.5, 'Спред (%)': 0.12},
            {'Ранг': 3, 'Пара': 'BNB/USDT', 'Рейтинг': 7.2, 'Ліквідність': 7.8, 'Спред (%)': 0.18},
            {'Ранг': 4, 'Пара': 'ADA/USDT', 'Рейтинг': 6.9, 'Ліквідність': 6.5, 'Спред (%)': 0.25},
            {'Ранг': 5, 'Пара': 'SOL/USDT', 'Рейтинг': 6.5, 'Ліквідність': 7.1, 'Спред (%)': 0.22}
        ]
        
        df_top_pairs = pd.DataFrame(top_pairs_data)
        st.dataframe(df_top_pairs, use_container_width=True)
        
        # Графік рейтингів
        st.subheader("📊 Графік рейтингів")
        
        fig = px.scatter(
            df_top_pairs,
            x='Ліквідність',
            y='Спред (%)',
            size='Рейтинг',
            color='Рейтинг',
            hover_name='Пара',
            title='Рейтинг торгових пар',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def render_statistics_tab(self):
        """Рендеринг вкладки статистики"""
        st.header("📈 Статистика")
        
        if not self.system:
            st.warning("⚠️ Система не ініціалізована")
            return
        
        # Загальна статистика
        st.subheader("📊 Загальна статистика")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Графік прибутку по днях
            dates = pd.date_range(start='2024-01-01', end='2024-01-15', freq='D')
            profits = [25.50, 45.20, 32.10, 67.80, 23.45, 89.30, 56.70, 34.20, 78.90, 45.60, 67.30, 23.80, 56.40, 89.70, 34.50]
            
            fig_profit = px.line(
                x=dates, 
                y=profits,
                title='Прибуток по днях',
                labels={'x': 'Дата', 'y': 'Прибуток (USD)'}
            )
            st.plotly_chart(fig_profit, use_container_width=True)
        
        with col2:
            # Розподіл угод по модулях
            modules = ['Арбітраж', 'Копітрейдинг', 'Сканер']
            trades_count = [45, 78, 12]
            
            fig_dist = px.pie(
                values=trades_count,
                names=modules,
                title='Розподіл угод по модулях'
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        
        # Детальна статистика
        st.subheader("📋 Детальна статистика")
        
        stats_data = [
            {'Метрика': 'Всього угод', 'Значення': '135', 'Зміна': '+12'},
            {'Метрика': 'Успішних угод', 'Значення': '98', 'Зміна': '+8'},
            {'Метрика': 'Win Rate', 'Значення': '72.6%', 'Зміна': '+3.2%'},
            {'Метрика': 'Загальний прибуток', 'Значення': '$1,234.50', 'Зміна': '+$156.80'},
            {'Метрика': 'Середній прибуток', 'Значення': '$9.14', 'Зміна': '+$1.23'},
            {'Метрика': 'Максимальний прибуток', 'Значення': '$89.30', 'Зміна': 'Новий рекорд'},
            {'Метрика': 'Максимальний збиток', 'Значення': '$12.50', 'Зміна': '-$2.10'}
        ]
        
        df_stats = pd.DataFrame(stats_data)
        st.dataframe(df_stats, use_container_width=True)
    
    def start_system(self):
        """Запуск системи"""
        try:
            if not self.system:
                self.system = TradingBot()
            
            # Запуск в окремому потоці
            asyncio.create_task(self.system.start())
            st.success("✅ Система запущена!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Помилка запуску системи: {e}")
    
    def stop_system(self):
        """Зупинка системи"""
        try:
            if self.system:
                asyncio.create_task(self.system.stop())
                st.success("✅ Система зупинена!")
                st.rerun()
            else:
                st.warning("⚠️ Система не запущена")
                
        except Exception as e:
            st.error(f"❌ Помилка зупинки системи: {e}")


def main():
    """Головна функція"""
    app = ArbitrageApp()
    app.run()


if __name__ == "__main__":
    main()

```

---

**User**

Будь ласка увесь проект та усі файли роби в окремій папці. Яку створи самостійно та надай їй назву "розумний агент "

---

**Cursor**

Файли перенесені до нової папки `розумний агент`. Тепер увесь проєкт лежить у `розумний агент/app.py` та `розумний агент/requirements.txt`.

