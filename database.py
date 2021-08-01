import mysql.connector
import datetime
import pandas as pd

def is_empty(df):
    if df.empty:
        print('Empty table')

db_user = input('Enter database user : ')
db_password = input('Enter database password : ')

connection = mysql.connector.connect(host='localhost', user = db_user, password = db_password, db='twitter')
cursor = connection.cursor()
print("")
print("Welcome to my Twitter application")
print("In each page there will be guidlines")
print("Please choose the desired option and enter data")
print(',' * 50)

while True:
    print("1-Log in")
    print("2-Sign up")
    option = int(input())

    if option == 1:
        arguments = []
        print('Enter userName')
        userName = input()
        arguments.append(userName)
        print('Enter password')
        password = input()
        arguments.append(password)
        cursor.callproc('login', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]

        if 'invalid'not in result:
            print(result)
            connection.commit()
            break
        else:
            print(result)
            input()
            connection.rollback()

    elif option == 2:
        arguments = []
        print('Enter userName(20 character long):')
        userName = input()
        arguments.append(userName)
        print('Enter first name(20 character long):')
        firstname = input()
        arguments.append(firstname)
        print('Enter last name(20 character long):')
        lastname = input()
        arguments.append(lastname)

        flag = False
        print('Enter date of birth(YYYY-MM-DD):')
        while not flag:
            try:
                birthdate = input()
                birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
                flag = True
            except:
                print('Please enter date of birth in valid format:')

        arguments.append(birthdate)
        print('Enter bio(if you dont want to have bio, enter \"none\"):')
        bio = input()
        if bio == 'none':
            bio = None
        arguments.append(bio)
        print('Enter password(128 character long ):')
        password = input()
        arguments.append(password)
        cursor.callproc('create_account', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        if result != 'Sorry, this username is already taken.':
            print(result)
            connection.commit()
            break
        else:

            print(result)
            connection.rollback()
            input()
    else:
        print('INVALID INPUT!')
        
    print('')

print('Welcome to your twitter page')

while True:
    print('0-Quit')
    print('1-Send a new tweet')
    print('2-Get personal tweets')
    print('3-Get personal tweets and replies')
    print('4-Follow')
    print('5-Unfollow')
    print('6-Block')
    print('7-Unblock')
    print('8-Get following activities')
    print('9-Get a specific user activities')
    print('10-Add a new comment')
    print('11-Get comments of specific tweet')
    print('12-Gets tweets consist of specific hashtag')
    print('13-Like')
    print('14-Get like numbers of specific tweet')
    print('15-List of liking of specific tweet')
    print('16-Popular tweets')
    print('17-Send a text message in direct')
    print('18-Send a tweet in direct')
    print('19-Receive a list of messages received from the specific user')
    print('20-Get a list of message senders')
    print('21-get login records')

    option = int(input())

    if option == 0:
        break

    elif option == 1:
        arguments = []
        print('Enter your tweet content(Maximum 256 character long):')
        tweet_content = input()
        arguments.append(tweet_content)
        cursor.callproc('send_tweet', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        print(result)
        connection.commit()
        input()

    elif option == 2:
        cursor.callproc('get_own_tweets')
        result = ''
        for i in cursor.stored_results():
            result = i.fetchall()
            df = pd.DataFrame(result)
            is_empty(df)
            print(df.to_markdown())
        input()

    elif option == 3:
        cursor.callproc('get_own_tweets_and_replies')
        result = ''
        for i in cursor.stored_results():
            result = i.fetchall()
            df = pd.DataFrame(result)
            is_empty(df)
            print(df.to_markdown())
        input()

    elif option == 4:
        arguments = []
        print('Enter the username of the person you want to follow:')
        username = input()
        arguments.append(username)
        cursor.callproc('follow', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        print(result)
        connection.commit()
        input()

    elif option == 5:
        arguments = []
        print('Enter the username of the person you want to unfollow:')
        username = input()
        arguments.append(username)
        cursor.callproc('stop_follow', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        print(result)
        connection.commit()
        input()

    elif option == 6:
        arguments = []
        print('Enter the username of the person you want to block:')
        username = input()
        arguments.append(username)
        cursor.callproc('block', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        print(result)
        connection.commit()
        input()

    elif option == 7:
        arguments = []
        print('Enter the username of the person you want to unblock:')
        username = input()
        arguments.append(username)
        cursor.callproc('stop_block', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        print(result)
        connection.commit()
        input()

    elif option == 8:
        cursor.callproc('get_following_activity')
        result = ''
        for i in cursor.stored_results():
            result = i.fetchall()
            df = pd.DataFrame(result)
            is_empty(df)
            print(df.to_markdown())
        input()

    elif option == 9:
        arguments = []
        print('Enter the username of the person whose activities you want to see:')
        username = input()
        arguments.append(username)
        cursor.callproc('get_user_activity', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchall()
            df = pd.DataFrame(result)
            is_empty(df)
            print(df.to_markdown())
        input()

    elif option == 10:
        arguments = []
        print('Enter the tweet ID you want to comment on:')
        tweet_id = int(input())
        arguments.append(tweet_id)
        print('Enter your comment content:')
        comment_content = input()
        arguments.append(comment_content)

        cursor.callproc('comment', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        print(result)
        connection.commit()
        input()

    elif option == 11:
        arguments = []
        print('Enter the tweet ID you want to see it\'s comments:')
        tweet_id = int(input())
        arguments.append(tweet_id)
        cursor.callproc('get_comments_of_tweet', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchall()
            df = pd.DataFrame(result)
            is_empty(df)
            print(df.to_markdown())
        input()

    elif option == 12:
        arguments = []
        print('Enter the hashtag you want to see its tweets')
        hashtag = input()
        arguments.append(hashtag)
        cursor.callproc('hashtag_tweets', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchall()
            df = pd.DataFrame(result)
            is_empty(df)
            print(df.to_markdown())
        input()

    elif option == 13:
        arguments = []
        print('Enter the tweet ID you want to like it:')
        tweet_id = int(input())
        arguments.append(tweet_id)
        cursor.callproc('liking', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        print(result)
        connection.commit()
        input()

    elif option == 14:
        arguments = []
        print('Enter the tweet ID you want to see it\'s number of likes:')
        tweet_id = int(input())
        arguments.append(tweet_id)
        cursor.callproc('number_of_likes', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchall()
            df = pd.DataFrame(result)
            is_empty(df)
            print(df.to_markdown())
        input()

    elif option == 15:
        arguments = []
        print('Enter the tweet ID you want to see it\'s List of likings :')
        tweet_id = int(input())
        arguments.append(tweet_id)
        cursor.callproc('list_of_liking', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchall()
            df = pd.DataFrame(result)
            is_empty(df)
            print(df.to_markdown())
        input()

    elif option == 16:
        cursor.callproc('get_popular_tweets')
        result = ''
        for i in cursor.stored_results():
            result = i.fetchall()
            df = pd.DataFrame(result)
            is_empty(df)
            print(df.to_markdown())
        input()

    elif option == 17:
        arguments = []
        print('Enter the username to which you want to send a text message:')
        username = input()
        arguments.append(username)
        print('Enter your text message:')
        message = input()
        arguments.append(message)

        cursor.callproc('direct_text_message', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        print(result)
        connection.commit()
        input()

    elif option == 18:
        arguments = []
        print('Enter the username to which you want to send a tweet:')
        username = input()
        arguments.append(username)
        print('Enter the tweet ID you want to send it:')
        tweet_id = int(input())
        arguments.append(tweet_id)

        cursor.callproc('direct_tweet_message', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        print(result)
        connection.commit()
        input()

    elif option == 19:
        arguments = []
        print('Enter the username whose messages you want to view:')
        username = input()
        arguments.append(username)
        cursor.callproc('get_a_user_messages', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchall()
            df = pd.DataFrame(result)
            is_empty(df)
            print(df.to_markdown())
        input()

    elif option == 20:
        cursor.callproc('list_of_message_sender')
        result = ''
        for i in cursor.stored_results():
            result = i.fetchall()
            df = pd.DataFrame(result)
            is_empty(df)
            print(df.to_markdown())
        input()

    elif option == 21:
        cursor.callproc('user_logins')
        result = ''
        for i in cursor.stored_results():
            result = i.fetchall()
            df = pd.DataFrame(result)
            is_empty(df)
            print(df.to_markdown())
        input()

    else:
        print('INVALID INPUT!')

cursor.close()
connection.close()