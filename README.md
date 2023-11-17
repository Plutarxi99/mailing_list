# mailing_list
Проект создан в рамках изучения модуля Django.
Проект создан для создания рассылок и их настройки. Также запускается скрипт, каждые 2 (или любое другое время) минуты на проверку времени.

<details>

<summary>Данный проект содержит в себе 3 приложения:</summary>

* **mailing**
   - позволяет работать с продуктами
       - содержит модели MailingMessage, MailingLog, Client, MailingSetting
* **journal**
    - позоваляет работать с журналами
        - содержит модели Journal
* **users**
   - служит для аунтификации пользователя 
       - содержит модели User 
</details>

<details>

<summary>Что делает приложение?</summary>
Функционал:

* Приложение работает с со всеми моделями и superuser имеет доступ ко всем контроллерам.
* Можно добавлять, изменять, смотреть и удалять продукты. Это реализовано CRUD на CBV.
* Добавлена группа "Manager" и у нее ограничен функционал с работой контролерами.
* Реализована работа и подключении папки <media> для загрузки изображений.
* С помощью задания настроек рассылок и сопотствуюших параметров отсылает заданным клиентам сообщения и записывания логов
* и тд...
</details>

> [!IMPORTANT]
> Добавлен файл https://github.com/Plutarxi99/mailing_list/blob/main/.env.sample (для использования надо привести к ввиду **<.env>**) с помощью, которого можно настроить работу проекта. В нем лежат настройки (далее идут примеры заполнения полей):
<details>
<summary>Настройки, которые надо установить для работы приложения</summary>

| Значение | Содержание | Примечание |
|-----|-----------|-----:|
|     **CACHE_ENABLED**| 1 |     Если записывать в кэш, иначе ставится 0|
|     **CACHE_LOCATION**| <pre><code>redis://127.0.0.1:6379</code></pre>    |     база данных для записи кэша|
|     **DATABASE_LOGIN**| <pre><code>'{"ENGINE": "django.db.backends.postgresql","NAME": "django_proj_educ","USER": "postgres",}'</code></pre> |     словарь для подключения к базе данных. P.S. не забудь создать ее|
|     **EMAIL_HOST_USER**|your.email@yandex.ru       |     Email с какого отправлять письмо|
|     **EMAIL_HOST_PASSWORD**| rgergergersgsdrg       |     пароль приложения, получить можно тут https://id.yandex.ru/security/app-passwords|
|     **EMAIL_BACKEND**| <pre><code>django.core.mail.backends.smtp.EmailBackend</code></pre>       |     объязательные настройки для отправки письма|
|     **EMAIL_HOST**| <pre><code>smtp.yandex.ru</code></pre>       |     объязательные настройки для отправки письма|
|     **EMAIL_PORT**| <pre><code>465</code></pre>       |     объязательные настройки для отправки письма|
|     **EMAIL_USE_SSL**| <pre><code>True</code></pre>       |     объязательные настройки для отправки письма|
|     **SECRET_KEY**| django-insecure-hu213gr51uh234gbrtf34oqufg35835g3q5g       |     код генерируется автоматически при создании приложения|
|     **CRONTIME**| <pre><code>'*/2 * * * *'</code></pre>       |     установка запуска скрипта(на данный момент каждые 2 минуты) P.S. документация crontab: https://github.com/kraiz/django-crontab |
|     **EXCLUDE_WORD**| "[]"       |     список запрещенных слов|
|     **SUPERUSER_EMAIL**| email_superuser       |     установить почту суперюзера|
|     **SUPERUSER_PASSWORD**| password_superuser       |     установить пароль суперюзера|
</details>

<details>

<summary>Как использовать?</summary>

* После установки нужных настроук в файле **<.env>**. Надо выполнить команду для установки пакетов:
  <pre><code>pip install -r requirements.txt </code></pre>

* Создать суперюзера:
  <pre><code>python3 manage.py ccsu</code></pre>

* Можно задать разное время для срабатывания скрипта и проверку временем писем в файле **<.env>** в настройке CRONTIME

* Для запуска сайта выполни команду:
  <pre><code>python3 manage.py runserver</code></pre>
  
* Для запуска скрипта проверки рассылок, необходимо:
   - Добавить задачу на выполненение скрипта и получение номера:
     <pre><code>python3 manage.py crontab add</code></pre>
   - Пример полученной строки: adding cronjob: (82f37ffd86b31eb271f72c56dc4a2613) -> ('*/2 * * * *', 'mailing.cron.my_scheduled_job')
   - Далее запускаем скрипт, следующей строкой:
     <pre><code>python3 manage.py crontab run 82f37ffd86b31eb271f72c56dc4a2613</code></pre>
   - Чтобю отключить, испольщуем следующий код:
     <pre><code>python3 manage.py crontab remove 82f37ffd86b31eb271f72c56dc4a2613</code></pre>
  
* Можно использовать отладочные данные, чтоббы заполнили уже данными базы данных:
  <pre><code>python3 manage.py loaddata data.json</code></pre>

</details>
