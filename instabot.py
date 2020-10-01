from keys import base_url,APP_ACCESS_TOKEN
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from termcolor import colored
import requests as request
import urllib
import urllib3
location=[]

def self_info():
  request_url = (base_url + '/users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
  print('Requesting info for:' + request_url)
  my_info = requests.get(request_url).json()
  print('My info is:\n', my_info)
  print('My Followers: %s\n' % (my_info['data']['counts']['followed_by']))
  print('People I Follow: %s\n' % (my_info['data']['counts']['follows']))
  print('No. of posts: %s\n' % (my_info['data']['counts']['media']))

def get_user_id(insta_username):
    request_url = (base_url + '/users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print('Requesting info for:' + request_url)
    search_results = requests.get(request_url).json()
    if search_results['meta']['code'] == 200:
        if len(search_results['data']):
            return search_results['data'][0]['id']
        else:
            print(colored('User does not exist!' ,'red'))
    else:
        print(colored('Status code other than 200 was received!','red'))
        return None


def get_user_info(insta_username):
      user_id = get_user_id(insta_username)
      if user_id == None:
          print(colored('User does not exist!','red'))
          exit()
      request_url = (base_url + '/users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
      print('GET request url : %s' % (request_url))
      user_info = requests.get(request_url).json()

      if user_info['meta']['code'] == 200:
          if len(user_info['data']):
              print('Username: %s' % (user_info['data']['username']))
              print('No. of followers: %s' % (user_info['data']['counts']['followed_by']))
              print('No. of people you are following: %s' % (user_info['data']['counts']['follows']))
              print('No. of posts: %s' % (user_info['data']['counts']['media']))
          else:
              print(colored('There is no data for this user!' ,'red'))
      else:
          print(colored('Status code other than 200 received!','red'))

def get_own_post():
      request_url = (base_url + '/users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
      print('GET request url : %s' % (request_url))
      own_media = requests.get(request_url).json()

      if own_media['meta']['code'] == 200:
          if len(own_media['data']):
              #Fetching the most recent media
              image_name = own_media['data'][0]['id'] + '.jpeg'
              image_url = own_media['data'][0]['images']['standard_resolution']['url']
              urllib.urlretrieve(image_url, image_name)
              print(colored('Your image has been downloaded!' ,'green'))
          else:
              print(colored('Post does not exist!' ,'red'))
      else:
          print(colored( 'Status code other than 200 received!', 'red'))

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print(colored('User does not exist!' ,'red'))
        exit()
    request_url = (base_url + '/users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            # Fetching the most recent media
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print(colored('Your image has been downloaded!' ,'green'))
        else:
            print(colored('Post does not exist!','red'))
    else:
        print(colored( 'Status code other than 200 received!' ,'red'))


def get_user_liked_post():
    request_url= (base_url+'/users/self/media/liked?access_token=%s')%( APP_ACCESS_TOKEN)
    user_liked=requests.get(request_url).json()
    if user_liked['meta']['code']==200:
        if len (user_liked['data']):
            image_name = user_liked['data'][0]['id'] + '.jpeg'
            image_url = user_liked['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print(colored( "Liked media has been downloaded!",'green'))
        else:
            print(colored( "Could not find posts" ,'red'))
    else:
        print(colored('Status code other than 200 received','red'))

def get_post_id(insta_username):
    user_id=get_user_id(insta_username)
    request_url=(base_url +'/users/%s/media/recent/?access_token=%s') % (user_id,APP_ACCESS_TOKEN)
    print('GET request url: %s'%(request_url))
    user_media=requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
          return user_media['data'][0]['id']
        else:
            print(colored('There is no recent post of the user!' ,'red'))
            exit()
    else:
        print(colored( 'Status code other than 200 received!' ,'red'))
        exit()



def like_a_post(insta_username):
    media_id=get_post_id(insta_username)
    if media_id==None:
        print(colored("User does not exist","red"))
        exit()
    request_url=(base_url+'/media/%s/likes')%media_id
    payload={"access_token":APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like=requests.post(request_url,payload).json()
    if post_a_like['meta']['code']==200:
        print(colored( "You have successfully liked the post" ,'green'))
    else:
        print(colored( "Sorry ! the like was unsuccessful" ,'red'))
        exit()

def get_comment_list(insta_username):
    media_id=get_post_id(insta_username)
    request_url=(base_url+'/media/%s/comments?access_token=%s')%(media_id,APP_ACCESS_TOKEN)
    print('GET %s'%request_url)
    comment_list=requests.get(request_url).json()
    if comment_list['meta']['code']==200:
        for x in range(0, len(comment_list['data'])):

            print(colored( comment_list['data'][x]['text'],'blue'))
        print(colored("\n Comments list successfully shown" ,"green"))
    else:
         print(colored ("No comments", 'red'))


def post_a_comment(insta_username):
    media_id=get_post_id(insta_username)
    comment_text=raw_input("Your comment:")
    print(colored(comment_text, 'red'))

    request_url=(base_url+"/media/%s/comments")%(media_id)
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    post_a_comment=requests.post(request_url,payload).json()
    print('POST request url : %s' % (request_url))
    if post_a_comment['meta']['code']==200:
        print(colored( "Thanks! Your comment has been posted successfully" ,'green'))

    else:
        print(colored( "Failed! Comment has not been posted.Please try again" ,'red'))
        exit()


def start_bot():
    while True:
        print("\n")
        print("Hello!Welcome to InstaBot")
        print("What would you like to do?")
        print("a.Get Your own details\n")
        print("b.Get details of another user by username\n")
        print("c.Get your own recent post\n")
        print("d.Get the recent post of a user by username\n")
        print("e.Get liked posts of user\n")
        print("f.Like the recent post of a user\n")
        print("g.Get a list of comments on the recent post of a user\n")
        print("h.Make a comment on the recent post of a user\n")
        print("i.exit")

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_id(insta_username)
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_liked_post()
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "i":
            exit()
        else:
            print(colored( "wrong choice" ,"red"))


start_bot()






















