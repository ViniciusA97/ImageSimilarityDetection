
#################################################
# This script reads image feature vectors from a folder
# and saves the image similarity scores in json file
# by Erdem Isbilen - December/2019
#################################################

#################################################
# Imports and function definitions
#################################################

# Numpy for loading image feature vectors from file
import numpy as np

# Time for measuring the process time
import time

# Glob for reading file names in a folder
import glob
import os.path

# json for storing data in json file
import json

# Annoy and Scipy for similarity calculation
from annoy import AnnoyIndex
from scipy import spatial
import os
#################################################

#################################################
# This function reads from 'image_data.json' file
# Looks for a specific 'filename' value
# Returns the product id when product image names are matched 
# So it is used to find product id based on the product image name
#################################################
def match_id(filename):
  with open('./output_images.json') as json_file:
    
    for file in json_file:
        seen = json.loads(file)

        for line in seen:
          
          if filename==line['imageName']:
            return line['uuid']
            break
#################################################

#################################################
# This function; 
# Reads all image feature vectores stored in /feature-vectors/*.npz
# Adds them all in Annoy Index
# Builds ANNOY index
# Calculates the nearest neighbors and image similarity metrics
# Stores image similarity scores with productID in a json file
#################################################
def cluster(termo:str):

  termo = termo.replace(" ", "_")
  start_time = time.time()
  
  print("---------------------------------")
  print ("Step.1 - ANNOY index generation - Started at %s" %time.ctime())
  print("---------------------------------")

  # Defining data structures as empty dict
  file_index_to_file_name = {}
  file_index_to_file_vector = {}
  file_index_to_uuid_id = {}

  # Configuring annoy parameters
  dims = 1792
  n_nearest_neighbors = 20
  trees = 10000

  # Reads all file names which stores feature vectors 
  allfiles = glob.glob('./result/'+termo+'/*.npz')

  t = AnnoyIndex(dims, metric='angular')

  for file_index, i in enumerate(allfiles):
    
    # Reads feature vectors and assigns them into the file_vector 
    file_vector = np.loadtxt(i)

    # Assigns file_name, feature_vectors and corresponding product_id
    file_name = os.path.basename(i).split('.')[0]
    print("File name: ", file_name)
    file_index_to_file_name[file_index] = file_name
    file_index_to_file_vector[file_index] = file_vector
    file_index_to_uuid_id[file_index] = match_id(file_name)

    # Adds image feature vectors into annoy index   
    t.add_item(file_index, file_vector)

    print("---------------------------------")
    print("Annoy index     : %s" %file_index)
    print("Image file name : %s" %file_name)
    print("Product id      : %s" %file_index_to_uuid_id[file_index])
    print("--- %.2f minutes passed ---------" % ((time.time() - start_time)/60))


  # Builds annoy index
  t.build(trees)

  print ("Step.1 - ANNOY index generation - Finished")
  print ("Step.2 - Similarity score calculation - Started ") 
  
  named_nearest_neighbors = []

  first_image_name = file_index_to_file_name[0]
  first_image_to_file_vector = file_index_to_file_vector[0]
  first_imag_to_uuid_id = match_id(file_name)

  named_nearest_neighbors.append({
    "masterImageName": first_image_name,
    "masterImageUuid": first_imag_to_uuid_id,
    "masterImageSimilarity":[]
  })

  # Calculates the nearest neighbors of the master item
  nearest_neighbors = t.get_nns_by_item(0, n_nearest_neighbors)

  # Loops through the nearest neighbors of the master item
  for j in nearest_neighbors:

    print(j)

    # Assigns file_name, image feature vectors and product id values of the similar item
    neighbor_file_name = file_index_to_file_name[j]
    neighbor_file_vector = file_index_to_file_vector[j]
    neighbor_uuid_id = file_index_to_uuid_id[j]

    # Calculates the similarity score of the similar item
    similarity = 1 - spatial.distance.cosine(first_image_to_file_vector, neighbor_file_vector)
    rounded_similarity = int((similarity * 10000)) / 10000.0

      # Appends master product id with the similarity score 
      # and the product id of the similar items
    named_nearest_neighbors[0]["masterImageSimilarity"].append({
      'similarity': rounded_similarity,
      'uuid': neighbor_uuid_id,
      'imageName': neighbor_file_name})

    print("---------------------------------") 
    print("Similarity index       : %s" %j)
    print("Master Image file name : %s" %file_index_to_file_name[j]) 
    print("Nearest Neighbors.     : %s" %nearest_neighbors) 
    print("--- %.2f minutes passed ---------" % ((time.time() - start_time)/60))

  
  print ("Step.2 - Similarity score calculation - Finished ") 

  # Writes the 'named_nearest_neighbors' to a json file
  with open('nearest_neighbors.json', 'w') as out:
    json.dump(named_nearest_neighbors, out)

  print ("Step.3 - Data stored in 'nearest_neighbors.json' file ") 
  print("--- Prosess completed in %.2f minutes ---------" % ((time.time() - start_time)/60))
