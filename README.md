# Pet project
Project deploy - https://24kovalishin.ru
# API
## Authtorization
### POST _/api/token/_ 
Get Bearer Token
```
curl --location 'http://127.0.0.1:8000/api/token/' --form 'username="admin"' --form 'password="Qwerty7890!"'
```
### POST _/api/token/refresh/_
Refresh Bearer Token
```
curl --location 'http://127.0.0.1:8000/api/token/refresh/' --form 'refresh="access token"'
```
### GET _/api/me/_
Get my info
```
curl --location 'http://127.0.0.1:8000/api/me/' --header 'Authorization: Bearer access token'
```
### GET _/api/permissions/_
Get my permissions
```
curl --location 'http://127.0.0.1:8000/api/permissions/' --header 'Authorization: Bearer access token'
```
## ChatGPT
### GET _/api/chatgpt/_
Get ChatGPT history
```
curl --location 'http://127.0.0.1:8000/api/chatgpt/' --header 'Authorization: Bearer access token'
```
### POST _/api/chatgpt/gpt/_
Ask a question to gpt-3.5-turbo
```
curl --location 'http://127.0.0.1:8000/api/chatgpt/gpt/' --form 'chatquestion="Your question"' --header 'Authorization: Bearer access token'
```
### POST _/api/chatgpt/dalle/_
Сreating a picture based on the description by dall-e-2
```
curl --location 'http://127.0.0.1:8000/api/chatgpt/dalle/' --form 'chatquestion="Your question"' --header 'Authorization: Bearer access token'
```
### POST _/api/chatgpt/tts/_
Text to speech conversion by tts-1(voice alloy)
```
curl --location 'http://127.0.0.1:8000/api/chatgpt/tts/' --form 'chatquestion="Your question"' --header 'Authorization: Bearer access token'
```
