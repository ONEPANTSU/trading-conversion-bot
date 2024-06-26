# Телеграм Бот для Регистрации на Биржах

Данный проект представляет собой Telegram бота, который помогает пользователям зарегистрироваться на криптовалютных биржах, предоставляет инструкции по регистрации и отправляет ссылки для регистрации. Бот также проверяет, зарегистрировался ли пользователь по предоставленной ссылке, и предоставляет доступ к "приватным" сигналам после успешной регистрации.

## Примеры подобных ботов

- [Headliners Traders Bot](https://t.me/headliners_traders_bot)
- [Trading Face Bot](https://t.me/trading_face_bot)
- [SmokeFX Chatbot](https://t.me/SmokeFXchatbot)

## Мультиязычность

Бот поддерживает следующие языки:
- Русский
- Английский

## Основной функционал

1. Отправка разогревающих сообщений или кружков для привлечения внимания пользователя.
2. Отправка инструкции по регистрации на криптовалютных биржах.
3. Отправка пользователю ссылок для регистрации на биржах.
4. Проверка, зарегистрировался ли пользователь по предоставленной ссылке.
5. Предоставление доступа к "приватным" сигналам после успешной регистрации.


## Использование

1. Создайте нового бота через [BotFather](https://t.me/BotFather) в Telegram и получите его токен.
2. Получите API ключи бирж
3. Заполните файл `.env` согласно примеру: `.env.sample`
4. Запустите бота с помощью команды `make up`
5. Необходимо добавить первого администратора:
```bash
make bash-db
psql -U postgres -d trading_conversion_bot
INSERT INTO public."user" (id, username, role_id, language_code, privacy) 
VALUES 
(ADMIN_TELEGRAM_ID, 'ADMIN_TELEGRAM_USERNAME', 2, 'ru', true);
\p
exit
```

## Разработчику

Для автоматической развёртки с помощью GitHub Actions необходимо создать Repository secrets:
- ENV
- DOCKER_USERNAME
- DOCKER_PASSWORD
- SERVER_HOST
- SERVER_PORT
- SERVER_USERNAME
- SSH_KEY
- SSH_KNOWN_HOSTS
- SSH_PASSPHRASE

## Авторы

- [**ONEPANTSU**](https://github.com/ONEPANTSU).