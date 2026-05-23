import os 
from ddgs import DDGS
from langchain_community.utilities import GoogleSerperAPIWrapper
from openai import OpenAI
from promts import systemPromt, userPromt
import json
import requests

google_api_key = os.getenv("SERPER_KEY")
googlemapsKey = os.getenv("MAPS_KEY")
grok_llm_key = os.getenv("GROK_KEY")
googlesearch = GoogleSerperAPIWrapper(serper_api_key=google_api_key)

keys = ["name","address","sources","phone","geocode"]
poi = {key:[] for key in keys}

#get the google poi details from google
def googleSearch(query):
  results = googlesearch.results(f"{query} phone number and address").get("organic",[])
  if results is not None:
    return results
  else:
    return None

#get the poi details from duckduck
def duckduck(query):
    with DDGS() as ddgs:
        ddgs_gen = list(ddgs.text(f"{query} phone number and address"))
        if ddgs_gen is not None:
            return ddgs_gen
        else:
          return None     

# Initializing the llm model here used grok 
llm = OpenAI(
    api_key=grok_llm_key,
    base_url="https://api.x.ai/v1"
)


#Now calling llm to segrarate the poi details
def llmcall(query):
   googleresult = googleSearch(query)
   duckresult = duckduck(query)

   response = llm.chat.completions.create(
       model = "grok-3",
       messages=[
      {
      "role":"system",
      "content":systemPromt() 
   },
   {
      "role":"user",
      "content":userPromt(query,googleresult,duckresult)
   }],temperature=0
   )
   content = response.choices[0].message.content 
   return json.loads(content)

def geocode(address):


    url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "key": googlemapsKey
    }

    response = requests.get(url, params=params)

    data = response.json()

    results = data.get("results", [])

    if results:
        location = results[0]["geometry"]["location"]

        return {
            "lat": location["lat"],
            "lng": location["lng"]
        }

    return None

def poidetails(query):

    # get extracted structured data
    poi = llmcall(query)

    # safely get address
    address = poi.get("address")

    # default geocode
    geocode_data = None

    # only geocode if address exists
    if address:
        geocode_data = geocode(address)

    # attach coordinates
    poi["geocode"] = geocode_data

    return poi
