import json
import os
import shutil


def separateImages(search_term:str, images_path='./images', target_path='./similarityResult'):
    jsonfile = open('nearest_neighbors.json')
    data = json.load(jsonfile)
    
    imageSimilarityArray = data[0]['masterImageSimilarity']

    for image in imageSimilarityArray:
        similarityDegree = '{:.2f}'.format(image['similarity'])
        if(similarityDegree == '1.00'):
            similarityDegree = "same_image"

        target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))
        target_folder = os.path.join(target_folder, similarityDegree)
        # Cria a pasta com a similaridade de duas casas caso a mesma não exista
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        origin_folder = os.path.join(images_path,'_'.join(search_term.lower().split(' ')))
        origin_file = origin_folder + '/' + image['imageName'] + '.jpg'
        shutil.copyfile(origin_file, target_folder + '/' + image['imageName'] + '.jpg')

    jsonfile.close()



