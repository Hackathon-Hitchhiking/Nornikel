## C4
![C4.jpg](.assets/C4.jpg)

## inference pipeline
![inferense.jpg](.assets/inferense.jpg)

## Indexing
![index.jpg](.assets/index.jpg)

## Как запустить
### 1. Клонирование репозитория

Для начала клонируйте репозиторий на вашу локальную машину:

```bash
git clone https://github.com/Hackathon-Hitchhiking/Nornikel.git
cd Nornikel
```

### 2. Создание и настройка файла окружения для Docker

Скопируйте пример файла окружения `.docker/.env.example` в `.docker/.env` и заполните необходимые переменные:

```bash
cp .docker/.env.example .docker/.env
nano .docker/.env
```

### 3. Создание и настройка файла конфигурации

Аналогично, скопируйте пример файла конфигурации `configs/.env.example` в `configs/.env` и укажите соответствующие переменные:

```bash
cp configs/.env.example configs/.env
nano configs/.env
```


### 4. Запуск Docker Compose

После настройки всех конфигурационных файлов запустите Docker Compose для сборки и запуска контейнеров:

```bash
docker compose up --build
```

Убедитесь, что все переменные окружения и конфигурационные файлы корректно настроены перед запуском команд. 
