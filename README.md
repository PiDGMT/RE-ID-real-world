<!-- ABOUT THE PROJECT -->
## About The Project

This is a project done for a thesis on open-world re-identification. In this repo, the files for training a triplet model, a quadruplet model and a quintuplet model on the EfficientNet-b0 are pusblished, as well as the trained weights for on the Market-1501 dataset. 

In addtion, an evaluation method is built for these models, where the models can simply be loaded and tested on an open-world re-id setting.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Instructions:

Instructions: 
The training of the models can be found in the .ypinb files in the training folder. These files explain the training procedure and how they can be run using a GPU. 

The evaluation function is found in the test_models folder.

This is a evaluation procedure that fits a real-world re-id scenario to test re-id models .


By default, 3 random camera tracks for 10 random peolpe in the testset will be selected as probe tracks. These tracks will be compared to the gallery tracks, that are also split up based on their camera ID. The gallery conists out of the remaining 90 people, sepererated by camera ID, and the remaining 3 camera tracks of the 10 selected people.

The goal of the model is to correctly assign the right tracks as 'same' while assigning the wron identities as different.

Out of the scoreboard, the False Target Rate (FTR) and the True Target Rate (TTR) will be calculated based on the best cutoff score.
The final score will be the TTR minus FTR.

To run the test, simply run main.py

<p align="right">(<a href="#readme-top">back to top</a>)</p>
