import json
from compare import calculate_distances, make_scoreboard
from get_random_people import get_random_people
from theta_search import theta_split
from torchvision import transforms
import numpy as np

"""
Runs everything and returns accuracy
"""
## list that keep track of scores for each run
list_best_scores = []
list_best_thetas = []
list_TTR = []
list_FTR = []

seed = 0

Amount_Of_Runs = 10


for i in range(Amount_Of_Runs):
    seed+=1
    random.seed(seed)
  
    ### These should be separable:
    ## 1. Selection
    ## 2. Comparison
    ## 3. Theta calculation
    #TODO: allow running just the comparison part

    ## Paramters that decide the database
    CAMERA_IDS = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6']
    NUMBER_TEST_PEOPLE = 10
    NUMBER_CAMERAS_PER_PERSON = 3

    ## Comparison parameters
    IMG_COMPARISONS_PER_PAIR = 5
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

    ## Parameters to find the best theta (cutoff) value
    SCOREBOARD_PATH = "temp_save/scoreboard.json"
    CUTOFF_VALUE = 0.1
    SCORING_TYPE = "minus"

    ## 1. ------- Selection
    print("---- 1. Selecting people for the database.. ----")
    testcameras, \
    testpeople, \
    compare_images, \
    test_images = get_random_people(
        TESTSET_FOLDER,
        CAMERA_IDS,
        NUMBER_TEST_PEOPLE,
        NUMBER_CAMERAS_PER_PERSON
        )

    print("Total test (person + camera): ", len(test_images))

    print("People in the database: ", testpeople, "Length: ", len(testpeople))
    print("People in test: ", testcameras, "Length: ", len(testcameras))

    with open("temp_save/compare_images.json", 'w') as json_file:
        json.dump(compare_images, json_file)
    with open("temp_save/test_images.json", 'w') as json_file:
        json.dump(test_images, json_file)

    ## 2. ------- Comparisons

    print("---- 2. Running all comparisons.. ----")

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

    ## 3.  ------- Theta calculations

    print("---- 3. Calculating best theta and score.. -----")
    best_theta, best_score, ttr, ftr = theta_split(SCOREBOARD_PATH, SCORING_TYPE, CUTOFF_VALUE)
    print("Best theta: ", best_theta)
    print("Best score: ", best_score)
    print("TTR: ", ttr)
    print("FTR: ", ftr)
    
    list_best_scores.append(best_score)
    list_best_thetas.append(best_theta)
    list_TTR.append(ttr)
    list_FTR.append(ftr)     

print('list best scores = ', list_best_scores)  
print('list best thetas = ', list_best_thetas)    
print('list TTRs = ', list_TTR)
print('list FTRs = ', list_FTR)

print('average score = ', np.mean(list_best_scores))  
print('average theta = ', np.mean(list_best_thetas))   
print('average TTR = ', np.mean(list_TTR))
print('average FTR = ', np.mean(list_FTR))
