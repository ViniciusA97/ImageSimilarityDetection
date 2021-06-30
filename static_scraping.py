import requests
import pandas as pd
from bs4 import BeautifulSoup
import selenium_teste
import converter
import get_image_feature_vectors
import cluster_image_feature_vectors

search_term = 'joao pessoa'

selenium_teste.search_and_download(
    search_term=search_term,
    driver_path=selenium_teste.DRIVER_PATH,
    number_images= 10)

converter.createJsonData(search_term)

get_image_feature_vectors.get_image_feature_vectors(search_term)
cluster_image_feature_vectors.cluster(search_term)


