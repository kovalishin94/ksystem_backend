# Pet project
Project deployment - https://kovalishin.ru
# API
## Authtorization
### POST _/api/token/_ 
Get Token
```
curl --location 'http://127.0.0.1:8000/api/token/' --form 'username="admin"' --form 'password="Qwerty7890!"'
```
### POST _/api/token/refresh/_
Refresh Token
```
curl --location 'http://127.0.0.1:8000/api/token/refresh/' --form 'refresh="token"'
```
### GET _/api/me/_
Get my info
```
curl --location 'http://127.0.0.1:8000/api/me/' --header 'Authorization: Bearer token'
```
### GET _/api/permissions/_
Get my permissions
```
curl --location 'http://127.0.0.1:8000/api/permissions/' --header 'Authorization: Bearer token'
```
## ChatGPT
### GET _/api/chatgpt/_
Get ChatGPT history
```
curl --location 'http://127.0.0.1:8000/api/chatgpt/' --header 'Authorization: Bearer token'
```
### POST _/api/chatgpt/gpt/_
Ask a question to gpt-3.5-turbo
```
curl --location 'http://127.0.0.1:8000/api/chatgpt/gpt/' --form 'chatquestion="Your question"' --header 'Authorization: Bearer token'
```
### POST _/api/chatgpt/dalle/_
Сreating a picture based on the description by dall-e-2
```
curl --location 'http://127.0.0.1:8000/api/chatgpt/dalle/' --form 'chatquestion="Your question"' --header 'Authorization: Bearer token'
```
### POST _/api/chatgpt/tts/_
Text to speech conversion by tts-1(voice alloy)
```
curl --location 'http://127.0.0.1:8000/api/chatgpt/tts/' --form 'chatquestion="Your question"' --header 'Authorization: Bearer token'
```
## Profiles
### GET _/api/profiles/create/_
Create profile
```
curl --location 'http://127.0.0.1:8000/api/profiles/create/' --header 'Authorization: Bearer token' --form 'username="user"' --form 'password1="Qwerty7890!"' --form 'password2="Qwerty7890!"'
```
### GET _/api/profiles/_
Get all profiles
```
curl --location 'http://127.0.0.1:8000/api/profiles/' --header 'Authorization: Bearer token'
```
### GET _/api/profiles/<<uuid:profile_id>>/_
Get profile by id
```
curl --location 'http://127.0.0.1:8000/api/profiles/894c0d48-ca95-4041-b9c6-d00ea90d5b06/' --header 'Authorization: Bearer token'
```
### POST/PATCH/DELETE _/api/profiles/<<uuid:profile_id>>/
Update/Delete profile
## Chat
### GET _/api/chat/create/_
Create chat
```
curl --location 'http://127.0.0.1:8000/api/chat/' --form 'id="<int:user_id>"' --header 'Authorization: Bearer token'
```
### GET _/api/chat/_
Get list of your chats
```
curl --location '/chat/' --header 'Authorization: Bearer token'
```
### GET _/api/chat/<<uuid:chat_id>>/_
Get list of messages in chat by id
```
curl --location 'http://127.0.0.1:8000/api/chat/6aa51cb9-9d21-4066-84fc-d178f216d405/' --header 'Authorization: Bearer token'
```
### GET _/api/chat/<<uuid:chat_id>>/delete/_
Delete chat
```
curl --location DELETE 'http://127.0.0.1:8000/api/chat/6aa51cb9-9d21-4066-84fc-d178f216d405/' --header 'Authorization: Bearer token'
```
### WebSocket _/ws/chat/<<uuid:chat_id>/?token=token>_
Send
```
{"body": "Your message"}
```
in ws connection to create new message and your companion get it in real time
## Tests
### POST/GET/PATCH/DELETE _/api/test/_
CRUD operations with tests
```
curl --location --request PATCH 'http://127.0.0.1:8000/api/test/0431cdb5-ecbf-4188-9da5-6cc0c520ab75/' --header 'Authorization: Bearer token' --form 'name="Testname"' --form 'possible_attempts="3"'
```
### POST/GET/PATCH/DELETE _/api/test/questions/_
CRUD operations with questions
```
curl --location --request PATCH 'http://127.0.0.1:8000/api/test/questions/bc58fca5-3781-4c4c-a91e-03ee1015b6db/' --header 'Authorization: Bearer token' --form 'image=@"/C:/picture.png"'
```
### GET _/api/test/questions/?id=<<uuid:test_id>>_
Get all questions and options(with answers) by test id
```
curl --location 'http://127.0.0.1:8000/api/test/questions/?id=75bd85e5-e66a-453a-b746-ac95d3df721b' --header 'Authorization: Bearer token'
```
### GET _/api/test/questions/solve_list/?id=<<uuid:test_id>>_
Get all questions and options(without answers) by test id
```
curl --location 'http://127.0.0.1:8000/api/test/questions/solve_list/?id=75bd85e5-e66a-453a-b746-ac95d3df721b' --header 'Authorization: Bearer token'
```
### POST/PATCH/DELETE _/api/test/options/_
Create/Update/Delete options
```
curl --location 'http://127.0.0.1:8000/api/test/options/' --header 'Authorization: Bearer token' \
--form 'body="optionname"' \
--form 'question="8784dc17-6c92-4e61-baba-646bb889ef98"' \
--form 'is_true="false"'
```
### POST/GET/DELETE _/api/test/answers/_
Create/Get/Delete answers
```
curl --location 'http://127.0.0.1:8000/api/test/answers/' --header 'Authorization: Bearer token' \
--form 'option="8784dc17-6c92-4e61-baba-646bb889ef98"' \
--form 'question="bc58fca5-3781-4c4c-a91e-03ee1015b6db"' \
```
### POST/GET _/api/test/results/_
Finish the test solution by:
```
curl --location 'http://127.0.0.1:8000/api/test/results/' --header 'Authorization: Bearer token' --form 'test="8784dc17-6c92-4e61-baba-646bb889ef98"' 
```
or get list of all test results:
```
curl --location 'http://127.0.0.1:8000/api/test/results/' --header 'Authorization: Bearer token' 
```
### GET _/api/test/results/my_results/?id=<<uuid:test_id>>_
Get only your results in test by id
