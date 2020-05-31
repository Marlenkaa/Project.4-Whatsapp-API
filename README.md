# Whatsapp API

<p align="left">
    <img src="https://raw.githubusercontent.com/Shurlena/Project.4-Whatsapp-API/master/images/Whatsapplogo.png" width="100">
</p>

The goal of this project is to create an API that analyzes the conversations of a chat. For this purpose, a real WhatsApp chat group has been used.

The first step is create a database with chat's information. If you also want to analyze a Whatsapp conversation, all you need to do is download the .txt file from a chosen chat. You can do this pressing the three dots on the top-right corner, select `More` and `Export chat` option.

The API is prepared to clean Whatsapp files and create automatically the database from it. It should be saved in INPUT folder with `whatsapp.txt` name. Otherwise, you need to introduce data manually.

##### REQUESTS [POST]

Here you can find the requests you can use to introduce data:

- File cleaning and database creation: `/createdatabase`
- Create an user: `/insert/user/<name>`
- Create a chat: `/insert/chat/<name>`
- Insert message: `/insert/message/<chat>/<name>/<datetime>/<message>`
- Insert user into a chat: `/insert/user/to/chat/<chat>/<name>`

##### REQUESTS [GET]

On the other hand, these are the requests to obtain some information about the chat:

- List of users: `/get/info/users`
- List of chats: `/get/info/chats`
- List of messages from a chat: `/get/info/<chat>`
- Messages wrote by specified user: `/get/messages/<name>`
- Analysis of sentiments from a chat: `/get/sentiments/from/<chat>`
- Analysis of sentiments from a chat (spanish version): `/get/sentiments/from/spanish/<chat>`
- Recommendation of similar users: `/recommend/user/<name>`

### INPUT

Contains the Whatsapp file we want to analyze through the API.

### OUTPUT

Once the `/createdatabase` request is made, it will automatically generate four .csv files, one with the original Whatsapp cleaned file, and another three divided in users list, chats and conversations extracted.

### src

* *api.py* -> main file where all requests are configured.
* *dataCleaning.py* -> cleaning and adaptation of the downloaded Whatsapp file.
* *users.py* -> functions to create users manually, insert them into a chat or into a collection.
* *chats.py* -> functions to create chats manually or insert them into a collection.
* *conversation.py* -> functions to create messages manually or insert them into a collection.
* *sentiments.py* -> analyzes the sentiments of specified chat.
* *recommendation.py* -> analyzes the users similarity and lists an ordered recommendation.

### api-tests.ipynb

All requests are tested in this file in order to see the final results.