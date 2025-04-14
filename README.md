# Практикум по курсу «Облачные вычисления и виртуализация»

Сервис предоставляет метод для извлечения атрибутов новостной страницы по URL. Атрибуты: заголовок, подзаголовок, дата публикации, текст, автор, теги, категории и источник.
Извлечение осуществляется с помощью библиотеки [trafilatura](https://github.com/adbar/trafilatura).

В сервисе происходит проверка существования в базе извлечённой новости по поданному URL. Если есть, возвращаем результат. Если нет, скачиваем HTML, извлекаем атрибуты, записываем в базу результат и возвращаем его пользователю.

## Стек

* Веб-сервис:  Python с библиотекой FastAPI
* Взаимодействие с базой данных: библиотека SQLModel от разработчиков FastAPI
* Менеджер зависимостей Python: Poetry
* База данных: MySQL

## Развёртывание через docker compose

```
docker compose up --build
```

## Развёртывание через Minikube

```
minikube start

eval $(minikube docker-env)
docker build -t news-reader:latest ./app

kubectl apply -f k8s/mysql.yaml
kubectl apply -f k8s/app.yaml
```

Проверить статус подов сервиса и базы:
```
kubectl get pods
```

Получить URL сервиса:
```
minikube service app-service --url
```

## Пример работы

Request:
```
curl -X POST "http://<IP>:<PORT>/extract/?url=https://news.sky.com/story/woman-dies-and-two-others-left-injured-after-car-hits-pedestrians-near-crawley-leisure-centre-13348075"
```

Response:
```
{
    "title": "Woman dies and two others left injured after car hits pedestrians near Crawley Leisure Park",
    "text": "Woman dies and two others left ..."",
    "categories": "",
    "subtitle": "The incident involving a grey BMW 3 Series took place outside Crawley Leisure Park in West Sussex at about 8.36pm on Saturday, Sussex Police say.",
    "id": 3,
    "publication_date": "2025-04-13 00:00:00",
    "url": "https://news.sky.com/story/woman-dies-and-two-others-left-injured-after-car-hits-pedestrians-near-crawley-leisure-centre-13348075",
    "author": null,
    "tags": "",
    "source": "Sky News"
}
```