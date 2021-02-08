from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#TODO make modular
#TODO convert to csv to allow for programmtic calls to AWS Handler, as of now AWS must be done manually

#The file is currently filled with tweet text, retweets, and favorites. It looks like this right now:
#tweet1 text |-| tweet1 retweets|-| tweet1 favorites|-| BREAKPOINT tweet2 text |-| tweet2 retweets|-| tweet2 favorites|-| BREAKPOINT....
with open('TestSourceFile.txt') as f:

	#"tweets" is a list broken up at each break point "tweets" looks like this after this code:
	#[tweet1 text |-| tweet1 retweets|-| tweet1 favorites|-|, tweet2 text |-| tweet2 retweets|-| tweet2 favorites|-|, .... ]
	tweets = f.read().split('BREAKPOINT')

	#"serializedTweets" will be a list of lists with each sub list being a tweet with 3 values [text, #retweets, #favorites]
	serializedTweets = []

	for tweet in tweets:
		#returns a list for each tweet in "tweets" where the list has 3 values [text, #retweets, #favorites]
		splitTweet = tweet.split('|-|')
		serializedTweets.append(splitTweet)
	
	#The lines below are just to clean up the 2-dimensional list created earlier, splitting so much leads to
	#some pretty jank (but consistent) behavior in a couple places and i'm not sure why. at the end of "serializedTweets" is a list 
	#containing only 1 value [" "] - deletes that and serializedTweets[-1] has [text, #retweets, #favorites, AND " "] - deletes that (" ") as well
	for index in range(0 , len(serializedTweets)):
		del serializedTweets[index][3]

	del serializedTweets[-1]
	del serializedTweets[-1][3]

#this is where extract only the text from each tweet
listOfTweetTexts = []

# "serializedTweets" is now [[tweet 1 text, tweet 1 #retweets, tweet 1 #favorites], [tweet 2 text, tweet 2 #retweets, tweet 2 #favorites]]
for tweet in serializedTweets:
	listOfTweetTexts.append(tweet[0])

# "listOfTweetTexts" is now a list with the text from each tweet 
listOfTweetSentences = []

#The vader nltk wants only 1 sentence to process so this loop breaks up each tweet text body into sentences. So, 
# "listOfTweetSentences" becomes a 2 dimensional list with structure: 
#[[tweet 1 sentence 1, tweet 1 sentence 2, ....],[tweet 2 sentence 1, tweet 2 sentence 2, ....],[tweet 3 sentence 1, tweet 3 sentence 2, ....]]
for tweet in listOfTweetTexts:
	sentences = tweet.split('.')
	listOfTweetSentences.append(sentences)

#set up analyzer
analyzer = SentimentIntensityAnalyzer()

#will hold the average polarity_score from analyzer of all the sentences in each tweet, as of now i'm not sure of a better way to score each tweet
listOfScoresForEachTweet = []

#sum of polarity for all sentences
polaritySum = 0

#runs each sentence of each tweet through the analyzer
for sentences in listOfTweetSentences:
	for sentence in sentences:

		#runs each sentence though the analyzer
		score = analyzer.polarity_scores(sentence)
		polaritySum += score

	#averages out all scores of sentences in tweet
	averagePolarity = polaritySum / len(sentences)
	#saves the final average score of the tweet
	listOfScoresForEachTweet.append(averagePolarity)

sumOfAllTweets = 0

#averages out polarity 
for score in listOfScoresForEachTweet:
	sumOfAllTweets += score

#get average over all tweets analyzed
averagePolarityOfAllTweets = sumOfAllTweets / len(listOfScoresForEachTweet)

print(f"The average polarity score for all tweets was: {averagePolarityOfAllTweets}")