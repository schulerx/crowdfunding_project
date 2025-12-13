# Структура проекта краудфандинга

## Обзор

Проект представляет собой веб-приложение для краудфандинга, построенное на FastAPI с использованием SQLAlchemy для работы с базой данных. Приложение позволяет создавать проекты, собирать пожертвования, управлять пользователями и ролями.

## Архитектура

Проект следует архитектурному паттерну Clean Architecture с разделением на следующие слои:

- **API слой** - маршруты и обработка HTTP-запросов
- **Сервисный слой** - бизнес-логика приложения
- **Репозиторный слой** - работа с базой данных
- **Модельный слой** - ORM-модели
- **Схемы** - Pydantic-схемы для валидации данных

## Модели данных

### UserModel
- `id`: int (первичный ключ)
- `name`: str
- `email`: str (уникальный)
- `hashed_password`: str
- `role_id`: int (внешний ключ на RoleModel)
- `role`: связь с RoleModel

### RoleModel
- `id`: int (первичный ключ)
- `name`: str (уникальный)

### ProjectModel
- `id`: int (первичный ключ)
- `creator_id`: int (внешний ключ на UserModel)
- `title`: str
- `description`: str
- `target_amount`: str
- `collected_amount`: str
- `category_id`: int (внешний ключ на CategoriesModel)
- `is_active`: bool (по умолчанию True)
- `date_start`: int
- `date_end`: int
- `creator`: связь с UserModel
- `category`: связь с CategoriesModel

### CategoriesModel
- `id`: int (первичный ключ)
- `name`: str

### DonationModel
- `id`: int (первичный ключ)
- `project_id`: int (внешний ключ на ProjectModel)
- `user_id`: int (внешний ключ на UserModel)
- `amount`: int
- `project`: связь с ProjectModel
- `user`: связь с UserModel

### RewardModel
- `id`: int (первичный ключ)
- `project_id`: int (внешний ключ на ProjectModel)
- `title`: str
- `description`: str
- `required_quantity`: int
- `project`: связь с ProjectModel

## Схемы данных

### Схемы пользователей (app/schemes/users.py)
- `SUserAddRequest` - схема для регистрации пользователя
- `SUserAdd` - схема для добавления пользователя в базу
- `SUserAuth` - схема для аутентификации
- `SUserGet` - схема для получения пользователя
- `SUserPatch` - схема для обновления пользователя
- `SUserGetWithRels` - схема пользователя с ролью

### Схемы ролей (app/schemes/roles.py)
- `SRoleAdd` - схема для добавления роли
- `SRoleGet` - схема для получения роли
- `SRoleGetWithRels` - схема роли с пользователями

### Схемы проектов (app/schemes/projects.py)
- `SProjectAdd` - схема для добавления проекта
- `SProjectUpdate` - схема для обновления проекта
- `SProjectGet` - схема для получения проекта
- `SProjectsWithRelations` - схема проекта со всеми связями

### Схемы категорий (app/schemes/categories.py)
- `SCategoriesAdd` - схема для добавления категории
- `SCategoriesUpdate` - схема для обновления категории
- `SCategoriesGet` - схема для получения категории
- `SCategoriesWithProjects` - схема категории с проектами

### Схемы пожертвований (app/schemes/donations.py)
- `SDonationAdd` - схема для добавления пожертвования
- `SDonationUpdate` - схема для обновления пожертвования
- `SDonationGet` - схема для получения пожертвования
- `SDonationWithRelations` - схема пожертвования с пользователем и проектом

### Схемы вознаграждений (app/schemes/rewards.py)
- `SRewardAdd` - схема для добавления вознаграждения
- `SRewardUpdate` - схема для обновления вознаграждения
- `SRewardGet` - схема для получения вознаграждения
- `SRewardWithProject` - схема вознаграждения с проектом

## API маршруты

### Авторизация и аутентификация (app/api/auth.py)
- `POST /auth/register` - регистрация нового пользователя
- `POST /auth/login` - аутентификация пользователя
- `GET /auth/me` - получение текущего пользователя
- `POST /auth/logout` - выход пользователя из системы

### Управление ролями (app/api/roles.py)
- `POST /auth/roles` - создание новой роли
- `GET /auth/roles` - получение списка ролей
- `GET /auth/roles/{id}` - получение конкретной роли
- `PUT /auth/roles/{id}` - изменение конкретной роли
- `DELETE /auth/roles/{id}` - удаление конкретной роли

## Система обработки ошибок

Проект реализует иерархическую систему обработки ошибок:

- Базовые классы исключений: `MyAppError` и `MyAppHTTPError`
- Конкретные исключения для различных сценариев (пользователь не найден, недействительный пароль и т.д.)
- HTTP-исключения с соответствующими статус-кодами
- Централизованная обработка исключений в API-слое

## Зависимости

- FastAPI - веб-фреймворк
- SQLAlchemy - ORM для работы с базой данных
- Pydantic - валидация данных
- JWT - аутентификация
- Bcrypt - хеширование паролей
- Alembic - миграции базы данных