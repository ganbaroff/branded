# Enhanced Video Creation Agent

Улучшенный агент для автоматизации создания видео с полной валидацией и поддержкой нескольких персонажей.

## 🎯 Новые возможности

### ✅ Валидация данных
- **Проверка фотографий**: проверка что это настоящее фото, не поврежденное
- **Детекция людей**: проверка наличия человека на фото
- **Распознавание лиц**: проверка качества лица на фото
- **Валидация качества**: проверка разрешения и четкости

### ✅ База данных знаменитостей
- Фотографии знаменитостей с привязанными голосами
- Автоматический выбор голоса для знаменитостей
- Кастомные фотографии с выбором голоса

### ✅ Мульти-персонажи
- **Основной персонаж** (обязательно)
- **Второй персонаж** (опционально) - знаменитость или пользователь
- Поддержка разных голосов для каждого персонажа

### ✅ Локация фона
- Загрузка фотографии локации
- Проверка качества локации
- Интеграция в видео

### ✅ Валидация и улучшение сценария
- **Проверка цензуры**: автоматическая модерация контента
- **Проверка логики**: AI анализирует связность сценария
- **Улучшение текста**: AI улучшает грамматику и стиль
- **Оптимизация для озвучки**: адаптация текста для TTS

## Архитектура

```
Пользователь → Веб-сайт
                   ↓
          [Выбор персонажа 1] → База данных знаменитостей
          [Выбор персонажа 2] → Загрузка своего фото (опционально)
          [Выбор локации] → Загрузка фото локации
          [Написание сценария] → AI проверка + улучшение
                   ↓
              Отправка → VideoCreationAgent
                   ↓
          ┌────────┴────────┐
          │  ВАЛИДАЦИЯ      │
          │ ✓ Фото 1        │ → Проверка: настоящее фото? есть человек? есть лицо?
          │ ✓ Фото 2        │ → Проверка (если есть второй персонаж)
          │ ✓ Локация       │ → Проверка качества
          │ ✓ Сценарий      │ → Цензура, логика, качество
          └────────┬────────┘
                   ↓
          ┌────────┴────────┐
          │  ОБРАБОТКА      │
          │                 │
          │ 1. Улучшение    │ → AI улучшает сценарий
          │    сценария     │
          │                 │
          │ 2. Выбор голосов│ → Знаменитость: привязанный голос
          │                 │ → Кастом: дефолтный/выбранный
          │                 │
          │ 3. Генерация    │ → ElevenLabs API
          │    аудио        │
          │                 │
          │ 4. Создание     │ → HeyGen API
          │    видео        │ → Персонажи + локация + аудио
          │                 │
          │ 5. Анимация     │ → Эффекты, переходы
          │                 │
          └────────┬────────┘
                   ↓
          [Готовое видео] → Доставка пользователю
```

## Установка

```bash
# Установите зависимости
pip install -e .

# Дополнительные библиотеки для продакшена
pip install requests boto3 psycopg2-binary moviepy pillow

# Для валидации изображений (выберите один):
pip install openai  # OpenAI Vision API
# или
pip install google-cloud-vision  # Google Vision API
# или
pip install boto3  # AWS Rekognition
```

## Использование

### Базовый пример с валидацией

```python
from branded import Config
from examples.video_creation_agent import (
    VideoCreationAgent,
    VideoRequest,
    Character
)

# Создайте конфигурацию
config = Config("config/video_agent_config.yaml")
agent = VideoCreationAgent(config=config)

# Создайте запрос на видео
request = VideoRequest(
    # Основной персонаж (знаменитость)
    primary_character=Character(
        photo_path="/db/celebrities/celebrity_001.jpg",
        name="Имя знаменитости",
        voice_id="voice_id_celebrity",
        is_celebrity=True
    ),
    
    # Второй персонаж (опционально - пользователь)
    secondary_character=Character(
        photo_path="/uploads/user_photo.jpg",
        name="Имя пользователя",
        is_celebrity=False  # Будет использован дефолтный голос
    ),
    
    # Локация
    location_photo="/uploads/location_beach.jpg",
    
    # Сценарий и текст
    script="Сценарий видео с описанием действий",
    text_to_speak="Текст который будет озвучен в видео",
    user_prompt="Создать видео на пляже с двумя персонажами"
)

# Создайте видео (с автоматической валидацией)
result = agent.create_video(request)

if result["success"]:
    print(f"✓ Видео создано: {result['video_file']}")
    print(f"  Валидация: {result['validation']}")
    print(f"  Персонажи: {result['characters_used']}")
    print(f"  URL: {result['delivery']['url']}")
else:
    print(f"✗ Ошибка: {result['error']}")
    if "validation_errors" in result:
        print(f"  Ошибки валидации: {result['validation_errors']}")
```

## Система валидации

### 1. Валидация фотографий

Агент автоматически проверяет все фотографии:

```python
# Встроенная валидация через _validate_photo()
validation_result = agent._validate_photo(
    photo_path="/path/to/photo.jpg",
    require_person=True  # True для персонажей, False для локации
)

if validation_result.is_valid:
    print(f"✓ Фото валидно (уверенность: {validation_result.confidence})")
    print(f"  Детали: {validation_result.details}")
else:
    print(f"✗ Ошибка: {validation_result.message}")
```

**Проверки:**
- Файл существует и читается
- Формат изображения валиден (JPEG, PNG и т.д.)
- Изображение не повреждено
- Для персонажей: есть человек на фото
- Для персонажей: детектировано лицо
- Качество изображения достаточно высокое
- Контент подходящий (через модерацию)

**Интеграция с Vision API:**

```python
# С OpenAI Vision API
import openai
from PIL import Image
import base64

class VisionValidator:
    def __init__(self, api_key):
        openai.api_key = api_key
    
    def validate_photo(self, photo_path, require_person=True):
        # Загрузите изображение
        with open(photo_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()
        
        # Анализ через OpenAI Vision
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this image: Is it a valid photo? Is there a person? Is there a face visible? Rate quality 0-1."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                    }
                ]
            }],
            max_tokens=300
        )
        
        # Парсите ответ
        analysis = response.choices[0].message.content
        # Извлеките данные из ответа...
        
        return {
            "has_person": True/False,
            "has_face": True/False,
            "quality_score": 0.92,
            "is_appropriate": True
        }

# Используйте в агенте
agent.vision_api = VisionValidator(api_key="your-openai-key")
```

### 2. Валидация сценария

```python
# Встроенная валидация через _validate_script()
script_validation = agent._validate_script(
    script="Ваш сценарий",
    text_to_speak="Текст для озвучки"
)

if script_validation.is_valid:
    print("✓ Сценарий прошел все проверки")
    print(f"  Цензура: {script_validation.details['censorship_passed']}")
    print(f"  Логика: {script_validation.details['logic_score']}")
else:
    print(f"✗ Ошибка: {script_validation.message}")
```

**Проверки:**
- Минимальная длина текста
- Проверка на неприемлемый контент (цензура)
- Проверка логической связности
- Качество языка

**Интеграция модерации:**

```python
import openai

class ContentModerator:
    def __init__(self, api_key):
        openai.api_key = api_key
    
    def check(self, text):
        response = openai.Moderation.create(input=text)
        result = response.results[0]
        
        return {
            "flagged": result.flagged,
            "categories": result.categories,
            "confidence": result.category_scores
        }

# Используйте в агенте
agent.content_moderator = ContentModerator(api_key="your-openai-key")
```

### 3. Улучшение сценария с AI

```python
# Встроенное улучшение через _enhance_script()
enhanced = agent._enhance_script(request)

print(f"Оригинал: {enhanced['original_script']}")
print(f"Улучшенный: {enhanced['enhanced_script']}")
print(f"Улучшения: {enhanced['improvements']}")
```

**Интеграция GPT для улучшения:**

```python
import openai

class ScriptEnhancer:
    def __init__(self, api_key):
        openai.api_key = api_key
    
    def enhance(self, script, context):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional video script writer. Improve the script while keeping the main message."
                },
                {
                    "role": "user",
                    "content": f"Improve this script for a video with {context['characters']} characters:\n\n{script}"
                }
            ]
        )
        
        improved_script = response.choices[0].message.content
        
        return {
            "original_script": script,
            "enhanced_script": improved_script,
            "improvements": ["Grammar improved", "Flow enhanced", "Clarity increased"]
        }

# Используйте в агенте
agent.script_enhancer = ScriptEnhancer(api_key="your-openai-key")
```

## База данных знаменитостей

### Схема базы данных

```sql
-- Таблица знаменитостей
CREATE TABLE celebrities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    photo_url TEXT NOT NULL,
    voice_id VARCHAR(255) NOT NULL,  -- ID голоса в ElevenLabs
    category VARCHAR(100),  -- Актер, певец, спортсмен и т.д.
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица локаций
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    photo_url TEXT NOT NULL,
    category VARCHAR(100),  -- Пляж, офис, природа и т.д.
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица пользовательских фото
CREATE TABLE user_photos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    photo_url TEXT NOT NULL,
    validated BOOLEAN DEFAULT FALSE,
    validation_details JSONB,  -- Результаты валидации
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Таблица запросов на создание видео
CREATE TABLE video_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    primary_character_type VARCHAR(50),  -- 'celebrity' или 'custom'
    primary_character_id INTEGER,
    secondary_character_type VARCHAR(50),
    secondary_character_id INTEGER,
    location_id INTEGER,
    script TEXT,
    text_to_speak TEXT,
    status VARCHAR(50),  -- 'pending', 'processing', 'completed', 'failed'
    video_url TEXT,
    validation_results JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Интеграция с базой данных

```python
import psycopg2
from typing import Optional, List

class CelebrityDatabase:
    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)
    
    def get_celebrity(self, celebrity_id: int) -> Optional[dict]:
        """Получить знаменитость по ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM celebrities WHERE id = %s AND is_active = TRUE",
            (celebrity_id,)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "photo_url": row[2],
                "voice_id": row[3],
                "category": row[4]
            }
        return None
    
    def get_location(self, location_id: int) -> Optional[dict]:
        """Получить локацию по ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM locations WHERE id = %s",
            (location_id,)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "photo_url": row[2],
                "category": row[3]
            }
        return None
    
    def save_user_photo(self, user_id: int, photo_url: str, validation: dict) -> int:
        """Сохранить пользовательское фото с результатами валидации."""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO user_photos (user_id, photo_url, validated, validation_details)
               VALUES (%s, %s, %s, %s) RETURNING id""",
            (user_id, photo_url, validation["is_valid"], json.dumps(validation))
        )
        photo_id = cursor.fetchone()[0]
        self.conn.commit()
        return photo_id
    
    def create_video_request(self, request_data: dict) -> int:
        """Создать запрос на создание видео."""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO video_requests 
               (user_id, primary_character_type, primary_character_id, 
                secondary_character_type, secondary_character_id, location_id,
                script, text_to_speak, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending')
               RETURNING id""",
            (
                request_data["user_id"],
                request_data["primary_type"],
                request_data["primary_id"],
                request_data.get("secondary_type"),
                request_data.get("secondary_id"),
                request_data.get("location_id"),
                request_data["script"],
                request_data["text_to_speak"]
            )
        )
        request_id = cursor.fetchone()[0]
        self.conn.commit()
        return request_id

# Используйте в агенте
agent.database = CelebrityDatabase("postgresql://localhost/video_db")
```

## Полный рабочий процесс

### На стороне веб-сайта

```python
from flask import Flask, request, jsonify
from video_creation_agent import VideoCreationAgent, VideoRequest, Character

app = Flask(__name__)
agent = VideoCreationAgent(config=Config("config.yaml"))

@app.route("/api/create-video", methods=["POST"])
def create_video_endpoint():
    data = request.json
    
    # 1. Получите данные от пользователя
    user_id = data["user_id"]
    primary_type = data["primary_character_type"]  # 'celebrity' или 'custom'
    primary_id = data["primary_character_id"]
    
    # 2. Загрузите данные из базы
    if primary_type == "celebrity":
        celeb = agent.database.get_celebrity(primary_id)
        primary_char = Character(
            photo_path=celeb["photo_url"],
            name=celeb["name"],
            voice_id=celeb["voice_id"],
            is_celebrity=True
        )
    else:
        # Пользовательское фото - сначала валидируйте
        photo = agent.database.get_user_photo(primary_id)
        if not photo["validated"]:
            return jsonify({"error": "Photo not validated"}), 400
        
        primary_char = Character(
            photo_path=photo["photo_url"],
            name=data["primary_character_name"],
            is_celebrity=False
        )
    
    # 3. Обработайте второго персонажа (если есть)
    secondary_char = None
    if "secondary_character_id" in data:
        # Аналогично...
        pass
    
    # 4. Загрузите локацию
    location_photo = None
    if "location_id" in data:
        location = agent.database.get_location(data["location_id"])
        location_photo = location["photo_url"]
    
    # 5. Создайте запрос
    video_request = VideoRequest(
        primary_character=primary_char,
        secondary_character=secondary_char,
        location_photo=location_photo,
        script=data["script"],
        text_to_speak=data["text_to_speak"],
        user_prompt=data["user_prompt"]
    )
    
    # 6. Создайте видео (асинхронно в продакшене)
    result = agent.create_video(video_request)
    
    # 7. Сохраните результат
    if result["success"]:
        agent.database.update_video_request(
            request_id=data["request_id"],
            status="completed",
            video_url=result["delivery"]["url"],
            validation=result["validation"]
        )
        
        return jsonify({
            "success": True,
            "video_url": result["delivery"]["url"],
            "validation": result["validation"]
        })
    else:
        return jsonify({
            "success": False,
            "error": result["error"],
            "validation_errors": result.get("validation_errors", [])
        }), 400

if __name__ == "__main__":
    app.run(debug=True)
```

## Конфигурация

Создайте файл `config/video_agent_config.yaml` с вашими API ключами:

```yaml
heygen:
  api_key: "ваш-ключ-heygen"
  avatar_id: "id-аватара"

elevenlabs:
  api_key: "ваш-ключ-elevenlabs"
  voice_id: "id-голоса"

database:
  url: "postgresql://localhost/photos_db"

storage:
  provider: "s3"
  bucket: "мой-бакет"
```

## Использование

### Базовый пример

```python
from branded import Agent, Config
from examples.video_creation_agent import VideoCreationAgent

# Загрузите конфигурацию
config = Config("config/video_agent_config.yaml")

# Создайте агента
agent = VideoCreationAgent(config=config)

# Создайте видео
result = agent.create_video(
    prompt="Создать видео о новом продукте в современном стиле",
    script="""
    Приветствую! Сегодня я расскажу о нашем новом продукте.
    Это инновационное решение для бизнеса.
    Давайте посмотрим, как это работает.
    """
)

print(f"Видео готово: {result['video_file']}")
print(f"URL: {result['delivery']['url']}")
```

### Интеграция с API

#### 1. HeyGen API

```python
import requests

class HeyGenAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.heygen.com/v1"
    
    def create_video(self, avatar_id, script, audio=None):
        response = requests.post(
            f"{self.base_url}/video/generate",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "avatar_id": avatar_id,
                "script": script,
                "voice": {"audio_url": audio}
            }
        )
        return response.json()
```

#### 2. ElevenLabs API

```python
import requests

class ElevenLabsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
    
    def text_to_speech(self, text, voice_id):
        response = requests.post(
            f"{self.base_url}/text-to-speech/{voice_id}",
            headers={"xi-api-key": self.api_key},
            json={"text": text, "model_id": "eleven_multilingual_v2"}
        )
        return response.content  # Audio bytes
```

#### 3. База данных для фотографий

```python
import psycopg2

class PhotoDatabase:
    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)
    
    def search_photos(self, keywords, limit=10):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT url FROM photos WHERE tags @> %s LIMIT %s",
            (keywords, limit)
        )
        return [row[0] for row in cursor.fetchall()]
```

## Продакшен

### Обработка ошибок и повторные попытки

Агент автоматически обрабатывает ошибки:

```python
from branded import Agent

class RobustVideoAgent(VideoCreationAgent):
    def create_video(self, prompt, script, max_retries=3):
        for attempt in range(max_retries):
            try:
                return super().create_video(prompt, script)
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
```

### Асинхронная обработка

Для обработки нескольких видео параллельно:

```python
import asyncio

class AsyncVideoAgent(VideoCreationAgent):
    async def create_video_async(self, prompt, script):
        # Используйте aiohttp для асинхронных API вызовов
        photos_task = asyncio.create_task(self._select_photos_async(prompt))
        audio_task = asyncio.create_task(self._generate_voice_async(script))
        
        photos, audio = await asyncio.gather(photos_task, audio_task)
        # ... дальнейшая обработка
```

### Очередь задач

Для масштабируемости используйте очередь:

```python
# С использованием Celery
from celery import Celery

app = Celery('video_tasks', broker='redis://localhost:6379')

@app.task
def create_video_task(prompt, script):
    agent = VideoCreationAgent()
    return agent.create_video(prompt, script)

# Использование
result = create_video_task.delay(prompt, script)
```

## Альтернативы

Вместо создания собственного агента, можно использовать:

### Преимущества собственного решения (Branded Agent):
✅ Полный контроль над процессом
✅ Интеграция с вашей инфраструктурой
✅ Кастомная логика и бизнес-правила
✅ Нет зависимости от сторонних платформ
✅ Можно комбинировать разные сервисы
✅ Гибкая обработка ошибок и повторных попыток

### Альтернативные сервисы:
- **Zapier** - простая автоматизация, но ограниченная гибкость
- **Make.com (Integromat)** - визуальная автоматизация
- **n8n** - self-hosted автоматизация
- **Готовые видео платформы** - Synthesia, Descript и др.

### Когда использовать сторонние сервисы:
- Нужно быстрое прототипирование
- Малый объем видео (<100 в месяц)
- Нет специфических требований

### Когда использовать Branded Agent:
- Большой объем видео (>100 в месяц)
- Нужна интеграция с внутренними системами
- Специфическая бизнес-логика
- Требуется полный контроль и кастомизация

## Пример полного рабочего процесса

```python
from branded import Config
from video_creation_agent import VideoCreationAgent

# 1. Настройка
config = Config("config/video_agent_config.yaml")
agent = VideoCreationAgent(config=config)

# 2. Получение задания (из API, очереди, базы данных)
job = {
    "id": "job_123",
    "prompt": "Создать рекламное видео продукта",
    "script": "Ваш скрипт здесь...",
    "customer_email": "customer@example.com"
}

# 3. Создание видео
try:
    result = agent.create_video(job["prompt"], job["script"])
    
    # 4. Отправка результата
    send_email(
        to=job["customer_email"],
        subject="Ваше видео готово!",
        video_url=result["delivery"]["url"]
    )
    
    # 5. Обновление статуса
    update_job_status(job["id"], "completed", result)
    
except Exception as e:
    # 6. Обработка ошибок
    log_error(job["id"], str(e))
    notify_admin(f"Ошибка при создании видео: {e}")
```

## Мониторинг и логи

Агент автоматически логирует все шаги:

```
2025-12-04 19:36:16 - VideoCreator - INFO - Step 1: Selecting photos
2025-12-04 19:36:16 - VideoCreator - INFO - Selected 3 photos
2025-12-04 19:36:17 - VideoCreator - INFO - Step 2: Generating voice
2025-12-04 19:36:18 - VideoCreator - INFO - Step 3: Creating video
2025-12-04 19:36:19 - VideoCreator - INFO - ✓ Video creation completed
```

## Стоимость

Примерная стоимость на 1 видео (2-3 минуты):
- HeyGen API: ~$0.50-2.00
- ElevenLabs API: ~$0.10-0.30
- AWS S3 storage: ~$0.01
- Compute: ~$0.05
**Итого: ~$0.66-2.36 за видео**

## Дополнительные ресурсы

- [HeyGen API Documentation](https://docs.heygen.com)
- [ElevenLabs API Documentation](https://elevenlabs.io/docs)
- [Branded Framework Documentation](../docs/getting_started.md)

## Поддержка

Для вопросов и поддержки создайте issue в GitHub репозитории.
