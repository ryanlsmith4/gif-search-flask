from flask import Flask, render_template, request
import requests
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

@app.route('/')
def index():
    """Return homepage."""
    api_key = os.getenv("API_KEY")
    #  Extract the query term from url using request.args.get()
    name = request.args.get('gif')
    if name:
        #  Make 'params' dictionary containing:
        # a) the query term, 'q'
        # b) your API key, 'key'
        # c) how many GIFs to return, 'limit'
        params = {
          'q' : name,
          'key' : api_key,
          'limit' : 10, 
        }
        #  Make an API call to Tenor using the 'requests' library. For 
        # reference on how to use Tenor, see: 
        # https://tenor.com/gifapi/documentation
        r = requests.get(
        "https://api.tenor.com/v1/search?", params = params )
        # Use the '.json()' function to get the JSON of the returned response
        # object
        if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
          result = json.loads(r.content)
        # Using dictionary notation, get the 'results' field of the JSON,
        # which contains the GIFs as a list
          result_dict = result['results']
          result_list = []
          for gif in result_dict:
            result_list.append(gif['media'][0]['tinygif']['url'])
          return render_template("index.html", gifs_list = result_list)
        else:
          top_ten_list = "Failed Response"
        # Render the 'index.html' template, passing the list of gifs as a
        # named parameter called 'gifs'
          return render_template("index.html", gifs_list = top_ten_list)
    else:
        params = {
          'locale' : 'en_US',
          'key' : api_key,
          'limit' : 10,
       }
        r = requests.get("https://api.tenor.com/v1/search?", params = params )
        if r.status_code == 200:
          featured_list = []
          popular_gifs = json.loads(r.content)
          popular_gifs_list = popular_gifs['results']
          for gif in popular_gifs_list:
            featured_list.append(gif['media'][0]['tinygif']['url'])
          return render_template("index.html", gifs_list = featured_list)


if __name__ == '__main__':
    app.run(debug=True)
