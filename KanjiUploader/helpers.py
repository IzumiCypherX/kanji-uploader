import requests, json, pymongo.errors

from KanjiUploader import KANJI_API, API_KEY, collection


class KanjiToday:
    """Base Class for Kanji Uploading.\n
    """
    def make_kanji_file(self):
        """Call the `KANJI_API` endpoint and creates a database entry that stores all the characters
        The characters are used one by one and are removed from the file.\n
        The method parses the response into a python list."""        
        try:
            grade = collection.find_one({"_id": "curr_grade"})['grade']
        except TypeError:
            collection.insert_one({"_id": "curr_grade", "grade": 1})
            grade = 1
        
        querystring = {"grade":grade}
        headers = {
	        "X-RapidAPI-Key": API_KEY,
	        "X-RapidAPI-Host": "kanjialive-api.p.rapidapi.com"
        }

        response = requests.get(KANJI_API+f'/search/advanced/', headers=headers, params=querystring)
        response = json.loads(response.text)

        l = [ i['kanji']['character'] for i in response ]

        collection.insert_one({"_id": "kanjichars", "characters": l, "now_at": 0})

        if(grade <= 6):
            collection.update_one({"_id": "curr_grade"}, {"$set": {"grade": grade+1}})

  
    def get_todays_kanji(self):
        """Assigns the next kanji to be posted.\n
        Reads the file `kanji.txt` created by `make_kanji_file` and assigns the first character to be posted.\n
        After the first character is assigned, it is removed from the file."""

        all_chars = []
        now_at = 0
        try:
            self.make_kanji_file()
        except pymongo.errors.DuplicateKeyError:
            resp = collection.find_one({"_id": "kanjichars"})
            all_chars = resp['characters']
            now_at = resp['now_at']
            try:
                self.character = all_chars[now_at]
                collection.update_one({"_id": "kanjichars"}, {"$set": {"now_at": now_at + 1}})
                self.get_kanji_details(self.character)
            except IndexError:
                collection.delete_one({"_id": "kanjichars"})
                pass


    def get_kanji_details(self, kanji):
        """calls the REST API from the `KANJI_API` endpoint and assigns the details to respective data members.\n
        `kanji` (`str`): The kanji whose details are to be retreievd. The first character of the file `kanji.txt`"""
        headers = {
	        "X-RapidAPI-Key": API_KEY,
	        "X-RapidAPI-Host": "kanjialive-api.p.rapidapi.com"
        }
        response = requests.get(url=KANJI_API+'/kanji/'+str(kanji), headers=headers)
        response = json.loads(response.text)
        print(kanji)
        print(response)
        self.character = kanji
        self.meanings = response['meaning']
        self.stroke_count = response['kstroke']
        self.kun_readings = response['kunyomi_search'].pop()
        self.on_readings = response['onyomi_search'].pop()
        self.strokevideo = response['kanji']['video']['mp4']

