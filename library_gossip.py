#!/usr/bin/python
from twitter import *
import os.path

## I'm using this library: https://github.com/sixohsix/twitter

#As soon as the app has the credentials on an account it creates this file
MY_TWITTER_CREDS = os.path.expanduser('~/.library_credentials')

#Personal API keys
CONSUMER_KEY='wvVkXNQ5DbclWozoaFmMg'
CONSUMER_SECRET='CjeNjHDklYdsG2upkeTwKjJ0BmF4yOuv90MsKgUji18'

#Ask for credentials
if not os.path.exists(MY_TWITTER_CREDS):
	    oauth_dance('Library talk', CONSUMER_KEY, CONSUMER_SECRET,
	                    MY_TWITTER_CREDS)

oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))



## Get followers and add as friends (Autofollow)
fo = twitter.followers.ids()
followers =  fo['ids']

##Get friends
fr = twitter.friends.ids()
friends = fr['ids']

## Pending friend requests
og = twitter.friendships.outgoing()
pending = og['ids']

for i in followers:
	
	#If I haven't added them yet
	if (i not in pending and i not in friends):
		twitter.friendships.create(user_id=i)
##Get my tweets
mt = twitter.statuses.user_timeline(screen_name = 'library_gossip',count = 50)
mytweets =[]

##Get text only
mt_len = len(mt)
for i in range(mt_len):
	mytweets.append(mt[i]['text'])

## Read direct messages
dm = twitter.direct_messages()
dm_len = len(dm)

for i in range(dm_len):
	text = dm[i]['text']
	OP = dm[i]['sender_id']
	ID = dm[i]['id']

	## Check length of the message
	if len(text) > 118:
		
		##Send a message back
		twitter.direct_messages.new(user_id=OP, text='Message too long, it must not exceed 118 characters.')
	else:
		##Post gossip
		msg = 'A birdie told me that ' + text

		#Check for duplicates
		if (msg not in mytweets):
			print msg
			twitter.statuses.update(status = msg)
		else:
			##Send a message back
			twitter.direct_messages.new(user_id=OP, text='Message duplicated.')
			print 'Message duplicated'

	##Delete direct msg
	twitter.direct_messages.destroy( _id=ID )
