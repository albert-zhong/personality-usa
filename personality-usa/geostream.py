from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import words
import codes


class GeoListener(StreamListener):

    def __init__(self, city_object, api=None):
        super().__init__(api=None)
        self.city_object = city_object
        self.counter = 0
        self.dictionary = {}  # Dictionary of words; keys are words, values are frequency

    def on_connect(self):
        print("Connected to Twitter stream!")

    def on_status(self, status):
        text = status.text
        word_list = words.parse_text_to_list(text)

        for word in word_list:
            self.dictionary[word] = self.dictionary.setdefault(word, 0) + 1

        if len(self.dictionary) > 5:
            words.create_csv_from_dictionary(self.dictionary, self.city_object)

    def on_error(self, status_code):
        print("Encountered error with status code: " + status_code)
        if status_code == 420:  # Too many failed connections in a window of time
            return False  # Kill stream
        return True  # By default don't kill the stream

    def on_timeout(self):
        print("Timeout...")
        return True  # Don't kill the stream


def create_stream(city):

    # Create Twitter stream
    auth = OAuthHandler(codes.consumer_key, codes.consumer_secret)
    auth.set_access_token(codes.access_token, codes.access_secret)

    # Create StreamListener
    my_listener = GeoListener(city)
    my_stream = Stream(auth, my_listener)

    my_stream.filter(languages=["en"], locations=city.geo_box)
    print("Hello World")

