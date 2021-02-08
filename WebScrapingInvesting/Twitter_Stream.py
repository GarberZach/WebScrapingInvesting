import tweepy
import json


consumer_key = 
consumer_secret = 
access_token = 
access_token_secret = 



#This class authenticates and connnects to twitter api
class Authenticator():

	def authenticate(self):
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		return auth

#This class creates a stream that will pull tweets containing a keyword
class Stream (tweepy.StreamListener):

	def __init__(self, auth, listener):
		self.stream = tweepy.Stream(auth = auth, listener = listener)

	def start(self):
		#enter keywords to find here, could be company, product, etc...
		self.stream.filter(track=['python'])

    def on_status(self, status):
        print(status.text)

    
#This listener waits for data then processes it or disconnects from 
# API because twitter will ban us if we keep trying to request data after we get the error code '420'

class Listener(tweepy.StreamListener):

    #Gets called for every new tweet that gets passed from the stream
	def on_data(self, raw_data):
    	self.process_data(self, raw_data)

    #This is where the tweet gets processed. The tweet is a json object so it will need to be parsed.
    #I chose to write the tweet to a file, there is probably a much cleaner way to save each tweet 
    #but I think it would be helpful in the future to have a file to read from opposed to connecting 
    # with this script. For now I chose to save only the text of the tweet, amount of retweets, and amount of favorites.
    #For my purposes now, I only need the text of the tweet but having more information on the tweet will be
    #useful in the future when deciding how much importance to give each tweet
    #This method is called for every tweet
    def process_data(self, raw_data):

        #This flag indicates if a tweet has been correctly loaded into a workable format
        tweetLoaded = False


        try:
            #load tweet to parse it
            tweet = json.loads(raw_data)
            #indicate it has been correctly loaded
            tweetLoaded = True

        except BaseException as error:  
            print("Error in on_data: %s" % str(error))

        #TODO create a more durable file system
    	if tweetLoaded:
            #this is where each tweet will be written to once parsed
    		with open('TestSourceFile.txt', 'a') as f:

                #TODO move json parsing into seperate method
                #extracts only wanted info from each tweet
                tweetText = tweet['text']
                tweetRetweets = tweet['retweet_count']
                tweetFavorites = tweet['favorite_count']

                # "|-|" is used as a point to seperate each piece of info for each tweet once it being read from file
    			f.write(tweetText + "|-|")
                f.write(tweetRetweets + "|-|")
                f.write(tweetFavorites + "|-|")
    			#"BREAKPOINT" signifies end of one tweet, used to seperate tweets when being read from file
    			f.write("BREAKPOINT")
    			f.close

    	return True

    #stop stream if this error or twitter will hit us with the ban hammer
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

if __name__ == "__main__":

	authenticator = Authenticator()
	auth = authenticator.authenticate()

	listener = Listener()
	stream = Stream(auth, listener)
    #starts stream of tweets
	stream.start()