# Critique Web Api

Opinions and feedbacks reform most of the services provided by different companies and services providers, while humans are always interested in what and how other people think of them. Ask.fm was made as a platform to ask questions about each other and know more about others opinions. Other platforms was made by different companies to know what their user’s think about their services. While no platform was made before to give feedbacks and opinions to others directly.

Critique API allows clients to write feedback messages to the API and receive such feedback messages through our API on their daily activity, line of work, personal actions and behaviors. Every client has their own inbox on the API, where they can get their private posts, the API gives the client then the option to either accept the post to be publicly visible, delete the post or make a reply on that post. The sender of the post is notified that their feedback has been published or has been replied to, this happens through an update in the API fields. Every client has a river on the API. The river is the news feed of this client, with public posts from the people he/she follows, and his/her own public public posts as well. Whenever the receiver notifies the API that he/she accepts a post to be publicly visible on their river, by either accepting or by replying, the post is publicly visible to all people who follows that person.

The API gives the clients the freedom to add their activity as posts on their own rivers, and it will be publicly visible to others who follow that account, so they can rate them and give them feedbacks. Activities can be multiple things, for example: sleeping hours and cycle, walking distance, sports and healthy meals.

Such idea for a criticism platform have never been implemented before in such design, usually companies and institutions make similar platforms to collect feedback. This is one of the main reasons that we think our platform will be of a great use then.

## Setting up the environment

### You will need

+ Python 3.6.4
+ Flask 0.12.2
+ SQLite3

```bash
virtualenv --python=/path/to/your/python3/binary venv
. venv/bin/activate
pip install flask
```

<!-- ### Starting the server

```bash
python server.py
``` -->