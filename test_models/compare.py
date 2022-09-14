"""
Runs comparisons between people between cameras, and calculates a distance score
In this file, the models can be loaded at the load_network function
"""

import json
import sys
sys.path.append('..\models')
import numpy as np
import random
import torch
import torch.nn.functional as F
from triplet import Tripletb0
from quadruplet import Quadrupletb0
from quintuplet import quintupletb0
from itertools import product
from pairwise import Pairwise
from PIL import Image
from utils import load_json
from torchvision import transforms
from torch.utils.data import DataLoader

## Global parameters
IMG_COMPARISONS_PER_PAIR = 1
GPU = False
TESTSET_FOLDER = "../market1501/testset/"
TRANSFORMATION = transforms.Compose(
        [
        transforms.Resize( (224, 224) ),
        transforms.ToTensor(),
        transforms.Normalize(
            mean = [0.486, 0.459, 0.408],
            std = [0.229, 0.224, 0.225]
            ),
        ]
    )
COMPARE_IMAGES_PATH = "temp_save/compare_images.json"
TEST_IMAGES_PATH = "temp_save/test_images.json"

def load_network(gpu):
    """
    Loads the re-id model to either the GPU or the CPU
    returns the loaded model with the trained weights
    """

    #change to Quadrupletb0().cuda() for quadruplet and the approriate weights
    if gpu:
        net = Tripletb0().cuda()
        checkpoint = torch.load('../weights/triplet1501V2validb1schedule')
    else:
        net = Tripletb0()
        checkpoint = torch.load('../weights/triplet1501V2validb1schedule', map_location=torch.device('cpu'))

    # loads the trained weights to the model, stored in the weights folder
    net.load_state_dict(checkpoint['model_state_dict'])

    # set model to evaluation mode
    net.eval()
    return net

def compare_two_people(
    person1,
    person2,
    net,
    gpu,
    max_image_comparisons,
    transformation,
    testset_folder
    ):
    """
    Takes in two tracks for comparison ad the amount of images to be compared of the test set and applies the image transormation to this data
    Returns the distance of the compared images
    """

    print(f"Comparing Person {person1[0][:4]},",
        f"camera {person1[0][5:7]}",
        f"with Person {person2[0][:4]},",
        f"camera {person2[0][5:7]}")

    permutations = list(product(person1, person2))
    random.shuffle(permutations)

    # Compares multiple images
    distances = []
    for img_comparison, (person1_img, person2_img) in enumerate(permutations):

        image1 = Image.open(f'{testset_folder}{person1[0][:4]}/{person1_img}')
        image2 = Image.open(f'{testset_folder}{person2[0][:4]}/{person2_img}')

        pairwise = Pairwise(
            image1,
            image2,
            transform = transformation)

        pair = DataLoader(
                pairwise,
                num_workers = 0,
                batch_size = 1,
                shuffle = False
                )

        dataiter = iter(pair)
        image11, image22 = next(dataiter)
        
        #for quadruplet the quadruplet, add another ,_ to both and two underscores for quintuplet model.
        if gpu:
            (vector1, vector2, _) = net(image11.cuda(), image22.cuda())
        else:
            (vector1, vector2, _) = net(image11, image22)

        distance = F.pairwise_distance(vector1, vector2)

        ## Keeps the distances to create an average over the total amount of images that are compared
        distances.append(distance.item())

        if max_image_comparisons == (img_comparison + 1):
            return np.average(distances)

        print(f"Image comparison {img_comparison + 1} done.")
    return np.average(distances)

def calculate_distances(
    testset_folder,
    compare_images,
    test_images,
    transformation,
    gpu,
    max_image_comparisons
    ):
    """
    returns the set distance between probe and gallery set 
    """
    
    

    net = load_network(gpu)

    distances = {}
    for database_person_cam in compare_images.keys():
        for test_person_cam in test_images.keys():
            average_distance = compare_two_people(
                person1 = compare_images[database_person_cam],
                person2 = test_images[test_person_cam],
                net = net,
                gpu = gpu,
                max_image_comparisons = max_image_comparisons,
                transformation = transformation,
                testset_folder = testset_folder
            )
            distances[f'{database_person_cam}_and_{test_person_cam}'] = average_distance

    ## Sort the distances for easier reading
    distances = dict(sorted(distances.items(), key=lambda item: item[0]))

    return distances

def make_scoreboard(distances):
    """
    creates a scoreboard of the distances of people that are a match and peolpe that aren't
    """
    scoreboard = {
    "Same" : [],
    "Different": []
    }

    for k in distances.keys():
        if k[:4] == k[12:16]:
            scoreboard['Same'].append(distances[k])
        else:
            scoreboard['Different'].append(distances[k])

    scoreboard['Same'] = sorted(scoreboard['Same'])
    scoreboard['Different'] = sorted(scoreboard['Different'])

    return scoreboard

if __name__ == "__main__":
    ## To run separately from main.py

    compare_images = load_json(COMPARE_IMAGES_PATH)
    test_images = load_json(TEST_IMAGES_PATH)

    print("Making comparisons..")
    distances = calculate_distances(
        TESTSET_FOLDER,
        compare_images,
        test_images,
        TRANSFORMATION,
        GPU,
        IMG_COMPARISONS_PER_PAIR,
        )

    print("Comparisons done. Making scoreboard.")
    scoreboard = make_scoreboard(distances)

    print("Saving & done.")
    with open("temp_save/scoreboard.json", 'w') as json_file:
        json.dump(scoreboard, json_file)
    with open("temp_save/distances.json", 'w') as json_file:
        json.dump(distances, json_file)
