# CS50-Final-Project
## Need for Text
#### Video Demo: https://youtu.be/N8tUaDy9-bs
#### Description: **_Need for Text_** is a **social network** designed for its users to **search or recommend texts** in their communities.

### Requirements
The project runs with **Python Flask**. In the _requirements.txt_ file you find the python packages you need to install. Also you have to configure the the **SQLite database** and also the **application**-settings and **Flask-Mail**-Serversettings in the _init.py_-file. If everything is set, you just have to run `python run.py` from the main directory to run the project.

### Functionality
First, you need to **sign up** (_/register_) for an account and confirm your registration via email. If you already have an account, you can **login directly** (_/login_).

The main page **displays all the posts** of you and the users you follow (_/_). Also there is a sidebar on each page that shows all the users you follow. In a post users can **either search or recommend texts**, and in addition to that there are also **info** posts that let you know who started following you or one of your friends. By clicking on a post you can see **more information** about the searched or recommended text. If a post is yours, you can **update** or **delete** it. If not, you can **contact** the author of the post via an email form (_/contact/<post_id>_). The email address will remain unknown to you until the user decides to reply to your message.

Every user has his own **public page** that displays his profile picture and information (_/user/<username>_). On your own page you can **update** your information or profile picture. Apart from that you have four options of what you want to have displayed: 1. All the posts from the user and his friends, 2. only his own posts, 3. every user he follows, or 4. every user he is followed by.
  
Of course you can **create your own posts** (_/post/new_). You just have to choose whether you want to search or recommend a text, and then write the title and some additional information in the boxes.
  
You also have the possibility to **search a certain user** (_/search_) using the search bar. You just need to write his name and click enter. You can then click on his profile and choose to **follow** or **unfollow** him.
  
When you are done with your session you can logout (_/logout_). If you forget your password the next time you want to login, you can get a confirmation mail to reset your password (_/reset_request_).
