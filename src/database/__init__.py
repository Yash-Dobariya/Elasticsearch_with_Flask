from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

es = Elasticsearch(os.getenv("ELASTICSEARCH_HOSTS"))
