import tweet_scraper
import language_finder
import tweet_cleaner
import keyword_tokenizer
import sent_transformer
import out_tagger
import tsi_builder

def main():
	"""
	ETL routine:
	Scrape tweets from twitter.
	Detect tweet languages.
	Clean tweets.
	Build tweet keywords.
	Transform tweet text to sentiment.
	Tag the outlier tweets.
	Build the TSI indicator.
	Loads the indicator as csv.
	Inputs none.
	Returns none.
	"""

	#edit old file as needed
	old_indicator_file = 'tsi002.csv'

	print('Tweet Scraper Stage.')
	df_raw = tweet_scraper.scrapeTweets()

	print('Language Finder Stage.')
	df_lang = language_finder.detectLang(df_raw)

	print('Tweet Cleaner Stage.')
	df_clean = tweet_cleaner.cleanTweets(df_lang)

	print('Keyword Tokenizer Stage.')
	df_tok = keyword_tokenizer.tokenKey(df_clean)

	print('Sentiment Transformer Stage.')
	df_sent = sent_transformer.tweetSent(df_tok)

	print('Outlier Tagging Stage.')
	df_tag = out_tagger.tagOkay(df_sent)

	print('Indicator Build Stage.')
	df_tsi = tsi_builder.loadInd(df_tag, old_indicator_file)

	print('ETL Process Complete.')


if __name__ == '__main__':
	main()
