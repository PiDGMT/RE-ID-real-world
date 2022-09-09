"""
Selects a database of people to recognise, and subtracts them from
the rest of the testset. Also orders by camera.
"""

import os
import random
import json

## Parameters to tweak
CAMERA_IDS = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6']
NUMBER_TEST_PEOPLE = 10
NUMBER_CAMERAS_PER_PERSON = 5

def get_random_people(
    input,
    camera_ids,
    number_test_people,
    number_cameras_per_person
    ):
    """
    Takes the different camera IDs of the dataset, the number of peole that are to be tested and the amount of images
    returns the randomly chosen test images and camera ID split
    """

    imagefile = sorted(os.listdir(input))

    testpeople = random.sample(imagefile, number_test_people)
    testcameras = random.sample(camera_ids, number_cameras_per_person)

    ## Collect a database of 'known' people
    compare_images = {}
    for tm_map in testpeople:
        for s in os.listdir(f'{input}{tm_map}/'):
            cam = ""
            for i in testcameras:
                if i in s:
                    cam = i
            if f'{tm_map}_{cam}' in compare_images.keys():
                compare_images[f'{tm_map}_{cam}'].append(s)
            elif cam in testcameras:
                compare_images[f'{tm_map}_{cam}'] = [s]

    ## Collect the entire testset
    all_testimages = {}
    for path, _, files in os.walk(input):
        for file in files:
            if f"{path[-4:]}{file[4:7]}" in all_testimages:
                all_testimages[f"{path[-4:]}{file[4:7]}"].append(file)
            else:
                all_testimages[f"{path[-4:]}{file[4:7]}"] = [file]

    ## Subtract the known people from the entire testset
    test_images = {}
    for key in all_testimages.keys():
        if key in compare_images:
            test_images[key] = list(
                set(all_testimages[key]) - set(compare_images[key]))
            if test_images[key] == []:
                del test_images[key]
        else:
            test_images[key] = all_testimages[key]

    return testcameras, testpeople, compare_images, test_images

if __name__ == "__main__":
    ## To run separately from main.py

    testcameras, testpeople, compare_images, test_images = get_random_people(
        '../market1501/testset/',
        CAMERA_IDS,
        NUMBER_TEST_PEOPLE,
        NUMBER_CAMERAS_PER_PERSON
        )

    with open("temp_save/compare_images.json", 'w') as json_file:
        json.dump(compare_images, json_file)
    print("Total database (person + camera): ", len(compare_images))

    with open("temp_save/test_images.json", 'w') as json_file:
        json.dump(test_images, json_file)

    print("Total test (person + camera): ", len(test_images))

    print("People in the database: ", testpeople, "Length: ", len(testpeople))
    print("People in test: ", testcameras, "Length: ", len(testcameras))
