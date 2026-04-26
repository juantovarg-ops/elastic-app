from IPython.utils.sysinfo import platform
from elasticsearch import Elasticsearch
import streamlit as st

ELASTIC_CLOUD_ID = st.secrets["ELASTIC_CLOUD_ID"]

ELASTIC_API_KEY = st.secrets["ELASTIC_API_KEY"]

client = Elasticsearch(
    cloud_id=ELASTIC_CLOUD_ID,
    api_key=ELASTIC_API_KEY,
)

def pretty_response(response):
    if len(response["hits"]["hits"]) == 0:
        st.warning("Your search returned no results.")
    else:
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            st.markdown(source.get("title", ""))
            st.markdown(source.get("summary", "No summary available"))
            st.markdown(source.get("publisher", "NA"))
            st.markdown(f"**Score:** {hit['_score']}")
            st.markdown("---")

st.title("Search Engine")

query = st.text_input("Enter your search query:", placeholder="Python, Javascript, etc.")

filter_pub = st.text_input("Filter by publisher (optional):", placeholder="oreilly, etc")
#{"term": {"publisher.keyword": "oreilly"}}

if st.button("Search") and query:
  base_query = {
      "bool":{
          "must": [
              {"match": {"title": query}}
          ],
          "filter":[]
      }
  }
  if filter_pub:
    base_query["bool"]["filter"].append({"term": {"publisher.keyword": filter_pub.lower()}})
   
  response = client.search(
      index="book_index_v1",
      body={
          "query": base_query,
          "size": 5
      }
  )

  pretty_response(response)
