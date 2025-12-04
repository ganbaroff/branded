# Video Creation Agent Example

Пример агента для автоматизации создания видео с использованием различных API сервисов.

## Описание

Этот пример демонстрирует, как создать агента, который автоматизирует весь процесс создания видео:

1. **Выбор фотографий** из базы данных на основе промпта
2. **Генерация голоса** через ElevenLabs API
3. **Создание видео** с аватаром через HeyGen API
4. **Добавление анимации** и эффектов
5. **Доставка** готового файла (S3, email, webhook и т.д.)

## Архитектура

```
Промпт → Агент → [База данных] → Фото
              ↓
         [ElevenLabs API] → Аудио
              ↓
         [HeyGen API] → Базовое видео
              ↓
         [Обработка] → Эффекты/Анимация
              ↓
         [Доставка] → Готовое видео
```

## Установка

```bash
# Установите зависимости
pip install -e .

# Дополнительные библиотеки для продакшена
pip install requests boto3 psycopg2-binary moviepy
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
