"""
Генеративний AI-Агент для автономної торгівлі криптовалютою
Розгортається на Render з хмарною пам'яттю через Google Drive
"""

# КРИТИЧНО: Встановити CUDA_VISIBLE_DEVICES ДО будь-яких імпортів TensorFlow
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Вимкнути GPU, використовувати тільки CPU
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Приховати warnings

import logging
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

# Оптимізація TensorFlow для обмежених ресурсів (Render Free Tier, Railway)
# CUDA_VISIBLE_DEVICES вже встановлено на початку файлу
import tensorflow as tf

# Вимкнути GPU та використовувати тільки CPU
try:
    # Спроба вимкнути GPU (якщо доступні)
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:
            pass
    # Вимкнути всі GPU пристрої
    tf.config.set_visible_devices([], 'GPU')
except Exception:
    pass  # Ігноруємо помилки - CPU буде використано автоматично

# Обмежити використання пам'яті та потоків TensorFlow
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)

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
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "service_account.json")
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive.file"]

CCXT_API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
CCXT_SECRET_KEY = os.getenv("BINANCE_TESTNET_SECRET_KEY")

DEFAULT_SYMBOLS = ["BTC/USDT", "ETH/USDT"]
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))
SAVE_MODEL_INTERVAL_STEPS = int(os.getenv("SAVE_MODEL_INTERVAL_STEPS", "100"))  # Оптимізовано: було 30
TRAIN_BATCH_SIZE = int(os.getenv("TRAIN_BATCH_SIZE", "64"))  # Оптимізовано: було 32
MAX_EPISODE_LENGTH = int(os.getenv("MAX_EPISODE_LENGTH", "96"))

# ------------------------------------------------------------------------------
# Risk Management - Дворівнева Система Безпеки
# ------------------------------------------------------------------------------


class RiskBand(Enum):
    """Режими ризику з обмеженнями на розмір позиції"""
    CONSERVATIVE = "CONSERVATIVE"
    BALANCED_CONSERVATIVE = "BALANCED_CONSERVATIVE"
    BALANCED = "BALANCED"
    BALANCED_AGGRESSIVE = "BALANCED_AGGRESSIVE"
    AGGRESSIVE = "AGGRESSIVE"

    @property
    def max_position_fraction(self) -> float:
        """Максимальна частка депозиту для торгівлі"""
        mapping = {
            RiskBand.CONSERVATIVE: 0.10,  # 10%
            RiskBand.BALANCED_CONSERVATIVE: 0.15,  # 15%
            RiskBand.BALANCED: 0.20,  # 20%
            RiskBand.BALANCED_AGGRESSIVE: 0.25,  # 25%
            RiskBand.AGGRESSIVE: 0.30,  # 30% максимум (70% залишається в резерві)
        }
        return mapping[self]


# Шляхи зниження ризику (AI може тільки знижувати, ніколи не підвищувати)
RISK_DOWNGRADE_PATHS: Dict[RiskBand, List[RiskBand]] = {
    RiskBand.CONSERVATIVE: [RiskBand.CONSERVATIVE],  # Не може змінювати
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
    """AI Супервізор - автоматично коригує ризик тільки в бік зниження"""

    def __init__(self, user_selected: RiskBand):
        self.user_selected = user_selected
        self.current_band = user_selected
        logger.info("Супервізор ініціалізовано з режимом: %s", user_selected.value)

    def evaluate_market_noise(
        self,
        vol_ratio: float,
        book_pressure: float,
        trend_strength: float,
    ) -> RiskBand:
        """
        Оцінює ринковий "шум" та автоматично знижує ризик при небезпечних умовах.
        Ніколи не підвищує ризик вище базового рівня користувача.
        """
        candidates = RISK_DOWNGRADE_PATHS[self.user_selected]
        
        # Розрахунок "шумового" індексу
        # Вища волатильність + дисбаланс книги = більший шум = менший ризик
        score = (vol_ratio * 0.5) + (abs(book_pressure) * 0.3) - (abs(trend_strength) * 0.2)
        logger.debug("Супервізор: шумовий індекс = %.4f", score)

        # Автоматичне зниження ризику залежно від шуму
        if score > 1.5 and len(candidates) > 1:
            self.current_band = candidates[-1]  # Найнижчий ризик
        elif score > 1.0 and len(candidates) > 2:
            self.current_band = candidates[-2]
        elif score > 0.7 and len(candidates) > 3:
            self.current_band = candidates[-3]
        else:
            self.current_band = candidates[0]  # Базовий рівень

        if self.current_band != self.user_selected:
            logger.warning(
                "Супервізор знизив ризик: %s -> %s (шум = %.4f)",
                self.user_selected.value,
                self.current_band.value,
                score,
            )
        else:
            logger.debug("Супервізор залишив ризик на рівні: %s", self.current_band.value)

        return self.current_band


# ------------------------------------------------------------------------------
# Google Drive Persistence - Хмарна Пам'ять
# ------------------------------------------------------------------------------


class CloudModelManager:
    """Управління моделлю AI через Google Drive API"""

    def __init__(
        self,
        client_secrets_path: str,
        token_path: str,
        drive_file_id: Optional[str],
        service_account_path: Optional[str] = None,
    ) -> None:
        self.client_secrets_path = client_secrets_path
        self.token_path = token_path
        self.drive_file_id = drive_file_id
        self.service_account_path = service_account_path or SERVICE_ACCOUNT_FILE
        self._service = None

    def _get_credentials(self) -> Credentials:
        """Отримання credentials: спочатку Service Account, потім OAuth"""
        # Створити service_account.json зі змінної середовища, якщо файл не існує
        service_account_file = Path(self.service_account_path)
        if not service_account_file.exists():
            service_account_json = os.getenv("SERVICE_ACCOUNT_JSON")
            if service_account_json:
                try:
                    service_account_file.parent.mkdir(parents=True, exist_ok=True)
                    service_account_file.write_text(service_account_json, encoding='utf-8')
                    logger.info("Створено service_account.json зі змінної середовища")
                except Exception as exc:
                    logger.warning("Не вдалося створити service_account.json: %s", exc)
        
        # Спробувати Service Account (для автоматичної роботи)
        if Path(self.service_account_path).exists():
            try:
                from google.oauth2 import service_account
                logger.info("Використання Service Account для Google Drive")
                creds = service_account.Credentials.from_service_account_file(
                    self.service_account_path,
                    scopes=DRIVE_SCOPES,
                )
                return creds
            except Exception as exc:
                logger.warning("Не вдалося використати Service Account: %s", exc)
        
        # Fallback до OAuth (для ручного налаштування)
        if not Path(self.client_secrets_path).exists():
            raise FileNotFoundError(
                f"Не знайдено ні service_account.json, ні client_secrets.json"
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
        """Отримання сервісу Google Drive"""
        if self._service is None:
            creds = self._get_credentials()
            self._service = build("drive", "v3", credentials=creds, cache_discovery=False)
        return self._service

    def load_model(self, local_path: str) -> bool:
        """Завантаження моделі з Google Drive"""
        if not self.drive_file_id:
            logger.warning("MODEL_DRIVE_FILE_ID не заданий; пропускаю завантаження моделі")
            return False

        service = self._get_service()
        try:
            logger.info("Завантаження моделі з Google Drive (ID: %s)", self.drive_file_id)
            request = service.files().get_media(fileId=self.drive_file_id)
            fh = tf.io.gfile.GFile(local_path, "wb")
            downloader = googleapiclient.http.MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.debug("Завантажено %.2f%%", status.progress() * 100)
            fh.close()
            logger.info("Модель успішно завантажена з Google Drive")
            return True
        except HttpError as exc:
            logger.error("Не вдалося завантажити модель: %s", exc)
            return False
        except Exception as exc:
            logger.error("Неочікувана помилка при завантаженні: %s", exc)
            return False

    def save_model(self, local_path: str) -> Optional[str]:
        """Збереження моделі на Google Drive"""
        if not Path(local_path).exists():
            logger.warning("Немає файлу моделі %s для завантаження", local_path)
            return self.drive_file_id

        service = self._get_service()
        metadata = {
            "name": MODEL_FILE_NAME,
            "mimeType": "application/octet-stream",
        }
        media = googleapiclient.http.MediaFileUpload(local_path, resumable=True)

        try:
            if self.drive_file_id:
                logger.info("Оновлення моделі на Google Drive (ID: %s)", self.drive_file_id)
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
            logger.info("Модель успішно збережена на Google Drive (ID: %s)", self.drive_file_id)
            return self.drive_file_id
        except HttpError as exc:
            logger.error("Не вдалося зберегти модель на Google Drive: %s", exc)
            return None
        except Exception as exc:
            logger.error("Неочікувана помилка при збереженні: %s", exc)
            return None


# ------------------------------------------------------------------------------
# Market Data & Execution - Технічний та Фундаментальний Аналіз
# ------------------------------------------------------------------------------


def build_exchange() -> ccxt.Exchange:
    """Створення підключення до Binance Testnet"""
    exchange = ccxt.binance(
        {
            "enableRateLimit": True,
            "apiKey": CCXT_API_KEY,
            "secret": CCXT_SECRET_KEY,
            "timeout": 30000,
            "options": {"defaultType": "spot"},  # Тільки спотова торгівля
        }
    )
    exchange.set_sandbox_mode(True)  # Testnet режим
    logger.info("Підключення до Binance Testnet налаштовано")
    return exchange


class MarketDataFetcher:
    """Отримання та обробка ринкових даних"""

    def __init__(self, exchange: ccxt.Exchange, symbols: List[str]):
        self.exchange = exchange
        self.symbols = symbols

    def get_recent_ohlcv(self, symbol: str, since_ms: Optional[int] = None) -> pd.DataFrame:
        """Отримання OHLCV даних (200 останніх хвилин)"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe="1m", since=since_ms, limit=200)
            df = pd.DataFrame(
                ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
            return df
        except Exception as exc:
            logger.error("Помилка отримання OHLCV для %s: %s", symbol, exc)
            return pd.DataFrame()

    def get_ta_features(self, df: pd.DataFrame) -> Dict[str, float]:
        """Технічний аналіз: RSI, MA, Волатильність"""
        if df.empty:
            return {"rsi": 50.0, "ma_fast": 0.0, "ma_slow": 0.0, "volatility": 0.0}

        close = df["close"]
        
        # RSI (Relative Strength Index)
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-9)
        rsi = 100 - (100 / (1 + rs.iloc[-1]))

        # Moving Averages
        ma_fast = close.rolling(window=10).mean().iloc[-1]
        ma_slow = close.rolling(window=30).mean().iloc[-1]
        
        # Волатильність (стандартне відхилення процентних змін)
        volatility = close.pct_change().rolling(window=30).std().iloc[-1]

        return {
            "rsi": float(np.nan_to_num(rsi, nan=50.0)),
            "ma_fast": float(np.nan_to_num(ma_fast, nan=close.iloc[-1])),
            "ma_slow": float(np.nan_to_num(ma_slow, nan=close.iloc[-1])),
            "volatility": float(np.nan_to_num(volatility, nan=0.0)),
        }

    def get_order_book_metrics(self, symbol: str) -> Dict[str, float]:
        """Фундаментальний аналіз: глибина книги ордерів, дисбаланс"""
        try:
            order_book = self.exchange.fetch_order_book(symbol, limit=20)
            bids = np.array(order_book["bids"][:20]) if order_book["bids"] else np.array([])
            asks = np.array(order_book["asks"][:20]) if order_book["asks"] else np.array([])
            
            bid_volume = bids[:, 1].sum() if bids.size > 0 else 0.0
            ask_volume = asks[:, 1].sum() if asks.size > 0 else 0.0
            
            # Дисбаланс книги (показує тиск купівлі/продажу)
            total_volume = bid_volume + ask_volume
            imbalance = (bid_volume - ask_volume) / (total_volume + 1e-9)
            
            return {
                "bid_volume": float(bid_volume),
                "ask_volume": float(ask_volume),
                "imbalance": float(imbalance),  # -1 до +1: негативне = продаж, позитивне = купівля
            }
        except Exception as exc:
            logger.error("Помилка отримання книги ордерів для %s: %s", symbol, exc)
            return {"bid_volume": 0.0, "ask_volume": 0.0, "imbalance": 0.0}


class TradeExecutor:
    """Виконання торгових операцій з контролем ризику"""

    def __init__(self, exchange: ccxt.Exchange, supervisor: Supervisor):
        self.exchange = exchange
        self.supervisor = supervisor

    def get_balance(self, asset: str) -> float:
        """Отримання доступного балансу"""
        try:
            balance = self.exchange.fetch_balance()
            return float(balance.get(asset, {}).get("free", 0.0))
        except Exception as exc:
            logger.error("Помилка отримання балансу для %s: %s", asset, exc)
            return 0.0

    def execute(self, symbol: str, side: str, amount: float) -> Optional[Dict[str, Any]]:
        """Виконання торгового ордеру"""
        try:
            if amount <= 0:
                logger.warning("Спроба виконати ордер з нульовою кількістю")
                return None
            
            logger.info("Виконання ордеру: %s %s %.6f %s", symbol, side, amount, symbol.split("/")[0])
            order = self.exchange.create_market_order(symbol, side.lower(), amount)
            logger.info("Ордер виконано: %s", order.get("id", "N/A"))
            return order
        except Exception as exc:
            logger.error("Помилка виконання ордеру: %s", exc)
            return None

    def max_position_size(self, usdt_balance: float) -> float:
        """Розрахунок максимального розміру позиції згідно з поточним режимом ризику"""
        allowed_fraction = self.supervisor.current_band.max_position_fraction
        max_size = usdt_balance * allowed_fraction
        logger.debug(
            "Максимальний розмір позиції: %.2f USDT (%.1f%% від балансу %.2f)",
            max_size,
            allowed_fraction * 100,
            usdt_balance,
        )
        return max_size


# ------------------------------------------------------------------------------
# Reinforcement Learning Agent - "Мозок" Агента
# ------------------------------------------------------------------------------


class TradingEnvironment:
    """Середовище для RL агента"""

    def __init__(self, data_fetcher: MarketDataFetcher, symbols: List[str]):
        self.data_fetcher = data_fetcher
        self.symbols = symbols
        self.last_prices: Dict[str, float] = {s: 0.0 for s in symbols}

    def get_state(self) -> Tuple[np.ndarray, str, Dict[str, float]]:
        """
        Отримання поточного стану ринку для RL агента.
        Повертає: (вектор стану, символ, контекст ринку для супервізора)
        """
        symbol = self._select_symbol()
        df = self.data_fetcher.get_recent_ohlcv(symbol)
        ta = self.data_fetcher.get_ta_features(df)
        book = self.data_fetcher.get_order_book_metrics(symbol)
        
        latest_price = df["close"].iloc[-1] if not df.empty else self.last_prices.get(symbol, 0.0)
        if latest_price > 0:
            self.last_prices[symbol] = latest_price

        # Нормалізований вектор стану для RL агента
        state_vector = np.array(
            [
                ta["rsi"] / 100.0,  # RSI нормалізований [0, 1]
                (ta["ma_fast"] - ta["ma_slow"]) / (latest_price + 1e-9),  # Відносна різниця MA
                ta["volatility"] * 100,  # Волатильність (масштабована)
                book["imbalance"],  # Дисбаланс книги [-1, 1]
            ],
            dtype=np.float32,
        )

        # Контекст ринку для супервізора
        market_context = {
            "vol_ratio": max(ta["volatility"], 1e-6) * 100,  # Волатильність для оцінки шуму
            "book_pressure": book["imbalance"],  # Тиск з книги ордерів
            "trend_strength": (ta["ma_fast"] - ta["ma_slow"]) / (latest_price + 1e-9),  # Сила тренду
        }

        return state_vector, symbol, market_context

    def _select_symbol(self) -> str:
        """Вибір символу на основі обсягу торгівлі"""
        weights = []
        for symbol in self.symbols:
            df = self.data_fetcher.get_recent_ohlcv(symbol)
            if df.empty:
                weights.append(1.0)
            else:
                # Більший обсяг = більша ймовірність вибору
                weights.append(df["volume"].iloc[-30:].mean())
        
        total = sum(weights)
        if total > 0:
            weights = [w / total for w in weights]
        else:
            weights = [1.0 / len(self.symbols)] * len(self.symbols)
        
        return np.random.choice(self.symbols, p=weights)


class ActorCriticAgent:
    """RL агент на основі Actor-Critic архітектури"""

    def __init__(self, state_dim: int, action_dim: int, learning_rate: float = 1e-4):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = 0.99  # Коефіцієнт дисконтування
        self.learning_rate = learning_rate
        self.model = self._build_model()
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)

    def _build_model(self) -> tf.keras.Model:
        """Побудова нейронної мережі (Actor-Critic) - оптимізовано для Render Free Tier"""
        inputs = tf.keras.Input(shape=(self.state_dim,))
        dense1 = tf.keras.layers.Dense(32, activation="relu")(inputs)  # Оптимізовано: було 64
        dense2 = tf.keras.layers.Dense(32, activation="relu")(dense1)  # Оптимізовано: було 64
        
        # Actor: політика (ймовірності дій)
        policy_logits = tf.keras.layers.Dense(self.action_dim, activation="linear")(dense2)
        
        # Critic: оцінка стану (value)
        value = tf.keras.layers.Dense(1, activation="linear")(dense2)
        
        model = tf.keras.Model(inputs=inputs, outputs=[policy_logits, value])
        model.compile()
        return model

    def select_action(self, state: np.ndarray) -> Tuple[int, float]:
        """Вибір дії на основі поточного стану"""
        state = np.expand_dims(state, axis=0)
        logits, value = self.model(state, training=False)
        logits = logits.numpy()[0]
        
        # Softmax для отримання ймовірностей
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
        """Навчання агента на батчі досвіду"""
        with tf.GradientTape() as tape:
            logits, values = self.model(states, training=True)
            values = tf.squeeze(values, axis=1)
            
            # Value loss (MSE)
            value_loss = tf.reduce_mean(tf.square(returns - values))
            
            # Policy loss (з advantage)
            policy = tf.nn.log_softmax(logits)
            indices = tf.stack([tf.range(tf.shape(actions)[0]), actions], axis=1)
            picked_log_probs = tf.gather_nd(policy, indices)
            policy_loss = -tf.reduce_mean(picked_log_probs * advantages)
            
            # Entropy bonus (для дослідження)
            entropy = -tf.reduce_mean(tf.exp(policy) * policy)
            
            # Загальна втрата
            loss = policy_loss + 0.5 * value_loss - 0.01 * entropy

        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        return float(loss.numpy())

    def save(self, path: str) -> None:
        """Збереження моделі локально"""
        self.model.save(path)
        logger.info("Модель збережено локально: %s", path)

    def load(self, path: str) -> None:
        """Завантаження моделі з локального файлу"""
        if Path(path).exists():
            self.model = tf.keras.models.load_model(path)
            logger.info("Модель завантажено з %s", path)
        else:
            logger.warning("Файл моделі %s не знайдено, використовую первісну модель", path)


# ------------------------------------------------------------------------------
# Trading Orchestrator - Головний Цикл Торгівлі
# ------------------------------------------------------------------------------


class TradingAgentRunner:
    """Оркестратор торгового агента"""

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
        
        # RL агент (3 дії: hold, buy, sell)
        self.agent = ActorCriticAgent(state_dim=4, action_dim=3)
        self.replay_buffer: List[Tuple[np.ndarray, int, float, float]] = []
        self.step_counter = 0

    def bootstrap(self):
        """Ініціалізація: завантаження моделі з Google Drive"""
        try:
            if self.cloud_manager.load_model(MODEL_FILE_NAME):
                self.agent.load(MODEL_FILE_NAME)
                logger.info("Агент ініціалізовано з навченою моделлю")
            else:
                logger.info("Запускаю агента з випадковими параметрами (перший запуск)")
        except Exception as exc:
            logger.error("Не вдалося завантажити модель: %s", exc)
            logger.info("Продовжую з випадковими параметрами")

    def _calculate_position(self, symbol: str, risk_band: RiskBand) -> float:
        """Розрахунок розміру позиції згідно з режимом ризику"""
        base, quote = symbol.split("/")
        usdt_balance = self.executor.get_balance(quote)
        max_position = self.executor.max_position_size(usdt_balance)
        
        price = self.environment.last_prices.get(symbol)
        if not price or price <= 0:
            ticker = self.executor.exchange.fetch_ticker(symbol)
            price = ticker["last"]
        
        amount = max_position / price if price > 0 else 0.0
        
        logger.debug(
            "Розрахунок позиції %s: баланс=%.2f %s, ціна=%.2f, кількість=%.6f %s",
            symbol,
            usdt_balance,
            quote,
            price,
            amount,
            base,
        )
        return max(amount, 0.0)

    def _action_to_order(self, action: int) -> str:
        """Перетворення дії агента в торгову операцію"""
        mapping = {0: "hold", 1: "buy", 2: "sell"}
        return mapping.get(action, "hold")

    def run(self, stop_event: threading.Event):
        """Головний цикл торгівлі (працює у фоновому потоці)"""
        self.bootstrap()
        logger.info("=== Старт торгового циклу ===")
        
        episode_rewards: List[float] = []
        
        while not stop_event.is_set():
            try:
                # 1. Отримання стану ринку
                state, symbol, market_ctx = self.environment.get_state()
                
                # 2. Супервізор оцінює ринковий шум та коригує ризик
                current_band = self.supervisor.evaluate_market_noise(
                    vol_ratio=market_ctx["vol_ratio"],
                    book_pressure=market_ctx["book_pressure"],
                    trend_strength=market_ctx["trend_strength"],
                )
                
                # 3. Агент вибирає дію
                action, value_estimate = self.agent.select_action(state)
                decision = self._action_to_order(action)
                
                # 4. Виконання дії та отримання винагороди
                reward = 0.0
                info: Dict[str, Any] = {"symbol": symbol, "decision": decision}
                
                if decision in {"buy", "sell"}:
                    amount = self._calculate_position(symbol, current_band)
                    if amount > 0:
                        order = self.executor.execute(symbol, decision, amount)
                        info["order"] = order.get("id", "N/A") if order else None
                        reward = self._evaluate_trade(symbol, decision, order)
                    else:
                        info["note"] = "Недостатньо балансу"
                        reward = -0.001
                else:
                    info["note"] = "Утримання позиції"
                    reward = 0.0
                
                # 5. Збереження досвіду для навчання
                self._record_experience(state, action, reward, value_estimate)
                episode_rewards.append(reward)
                
                logger.info(
                    "Крок %d | %s | %s | винагорода=%.5f | ризик=%s",
                    self.step_counter,
                    symbol,
                    decision,
                    reward,
                    current_band.value,
                )
                
                # 6. Навчання агента
                if len(self.replay_buffer) >= TRAIN_BATCH_SIZE:
                    self._train_from_buffer()
                    episode_rewards.clear()
                
                # 7. Періодичне збереження моделі
                if self.step_counter > 0 and self.step_counter % SAVE_MODEL_INTERVAL_STEPS == 0:
                    self._persist_model()
                
                self.step_counter += 1
                time.sleep(POLL_INTERVAL_SECONDS)
                
            except Exception as exc:
                logger.exception("Неочікувана помилка в торговому циклі: %s", exc)
                time.sleep(POLL_INTERVAL_SECONDS)

    def _record_experience(self, state, action, reward, value_estimate):
        """Збереження досвіду в буфер"""
        self.replay_buffer.append((state, action, reward, value_estimate))
        # Обмеження розміру буфера (оптимізовано для Render Free Tier)
        if len(self.replay_buffer) > 3 * TRAIN_BATCH_SIZE:  # Оптимізовано: було 5
            self.replay_buffer.pop(0)

    def _train_from_buffer(self):
        """Навчання агента на накопиченому досвіді"""
        if len(self.replay_buffer) < TRAIN_BATCH_SIZE:
            return
        
        states, actions, rewards, values = zip(*self.replay_buffer)
        states = np.stack(states)
        actions = np.array(actions)
        rewards = np.array(rewards, dtype=np.float32)
        values = np.array(values, dtype=np.float32)
        
        # Розрахунок returns (дисконтовані винагороди)
        returns = np.zeros_like(rewards)
        running_return = 0.0
        for t in reversed(range(len(rewards))):
            running_return = rewards[t] + self.agent.gamma * running_return
            returns[t] = running_return
        
        # Advantages (returns - baseline)
        advantages = returns - values
        
        # Нормалізація advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        loss = self.agent.train_batch(states, actions, advantages, returns)
        logger.info("Агент навчено (втрата=%.5f, батч=%d)", loss, len(self.replay_buffer))
        self.replay_buffer.clear()

    def _persist_model(self):
        """Збереження моделі локально та на Google Drive"""
        try:
            self.agent.save(MODEL_FILE_NAME)
            drive_id = self.cloud_manager.save_model(MODEL_FILE_NAME)
            if drive_id:
                logger.info("Модель збережено на Google Drive (ID: %s)", drive_id)
            else:
                logger.warning("Не вдалося зберегти модель на Google Drive")
        except Exception as exc:
            logger.error("Не вдалося зберегти модель: %s", exc)

    def _evaluate_trade(self, symbol: str, decision: str, order: Optional[Dict[str, Any]]) -> float:
        """Оцінка виконаної угоди (винагорода для RL)"""
        if not order:
            return -0.001  # Невелике покарання за невдалу угоду
        
        # Спрощена оцінка: враховуємо комісії та можливий PnL
        try:
            cost = float(order.get("cost", 0))
            fee = float(order.get("fee", {}).get("cost", 0)) if isinstance(order.get("fee"), dict) else 0.0
            
            # Базова винагорода: негативна комісія (агент навчиться мінімізувати комісії)
            reward = -fee / (cost + 1e-9) if cost > 0 else -0.001
            
            # TODO: Додати оцінку PnL після закриття позиції
            return float(reward)
        except Exception as exc:
            logger.error("Помилка оцінки угоди: %s", exc)
            return 0.0


# ------------------------------------------------------------------------------
# Flask App & Background Thread
# ------------------------------------------------------------------------------


app = Flask(__name__)

# Ініціалізація компонентів
exchange = build_exchange()

# Вибір режиму ризику (CONSERVATIVE, BALANCED, AGGRESSIVE)
user_mode = os.getenv("TRADING_MODE", "BALANCED").upper()
if user_mode not in RiskBand.__members__:
    logger.warning("Некоректний TRADING_MODE=%s, встановлено BALANCED", user_mode)
    user_mode = "BALANCED"

supervisor = Supervisor(RiskBand[user_mode])
data_fetcher = MarketDataFetcher(exchange, DEFAULT_SYMBOLS)
environment = TradingEnvironment(data_fetcher, DEFAULT_SYMBOLS)
executor = TradeExecutor(exchange, supervisor)
cloud_manager = CloudModelManager(
    CLIENT_SECRETS_FILE, 
    TOKEN_FILE, 
    MODEL_DRIVE_FILE_ID,
    service_account_path=SERVICE_ACCOUNT_FILE
)
symbol_deposit = {symbol: float(os.getenv("DEPOSIT_USDT", "1000")) for symbol in DEFAULT_SYMBOLS}

stop_event = threading.Event()
agent_runner = TradingAgentRunner(supervisor, environment, executor, cloud_manager, symbol_deposit)


def start_background_thread():
    """Запуск фонового потоку для AI-агента"""
    if not hasattr(start_background_thread, "thread") or not start_background_thread.thread.is_alive():
        start_background_thread.thread = threading.Thread(
            target=agent_runner.run,
            name="TradingAgentThread",
            args=(stop_event,),
            daemon=True,
        )
        start_background_thread.thread.start()
        logger.info("Фоновий агент запущено")


@app.route("/", methods=["GET"])
def healthcheck():
    """
    Keep-Alive ендпоінт для UptimeRobot.
    Цей ендпоінт буде пінгуватися кожні 5-10 хвилин.
    """
    start_background_thread()
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent_running": start_background_thread.thread.is_alive() if hasattr(start_background_thread, "thread") else False,
        "step_counter": agent_runner.step_counter,
    })


@app.route("/supervisor", methods=["GET"])
def get_supervisor():
    """Отримання інформації про супервізора"""
    return jsonify({
        "user_mode": supervisor.user_selected.value,
        "current_band": supervisor.current_band.value,
        "max_position_fraction": supervisor.current_band.max_position_fraction,
        "max_position_percent": f"{supervisor.current_band.max_position_fraction * 100:.1f}%",
    })


@app.route("/config", methods=["POST"])
def update_config():
    """Оновлення конфігурації"""
    payload = request.get_json(force=True, silent=True) or {}
    symbols = payload.get("symbols")
    if symbols and isinstance(symbols, list):
        environment.symbols = symbols
        data_fetcher.symbols = symbols
    
    poll_interval = payload.get("poll_interval_seconds")
    if poll_interval:
        global POLL_INTERVAL_SECONDS
        POLL_INTERVAL_SECONDS = int(poll_interval)
    
    return jsonify({
        "updated": True,
        "symbols": environment.symbols,
        "poll_interval_seconds": POLL_INTERVAL_SECONDS,
    })


@app.route("/shutdown", methods=["POST"])
def shutdown_agent():
    """Зупинка агента"""
    stop_event.set()
    return jsonify({"status": "stopping"})


@app.route("/status", methods=["GET"])
def get_status():
    """Детальний статус системи"""
    return jsonify({
        "agent_running": start_background_thread.thread.is_alive() if hasattr(start_background_thread, "thread") else False,
        "step_counter": agent_runner.step_counter,
        "replay_buffer_size": len(agent_runner.replay_buffer),
        "supervisor": {
            "user_mode": supervisor.user_selected.value,
            "current_band": supervisor.current_band.value,
        },
        "symbols": environment.symbols,
    })


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------


def create_app() -> Flask:
    """Фабрика додатку для Gunicorn"""
    return app


if __name__ == "__main__":
    # Локальний запуск (для тестування)
    start_background_thread()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=False)
