<!-- ABOUT THE PROJECT -->
## About The Project

This is a project done for a thesis on open-world re-identification. In this repo, the files for training a triplet model, a quadruplet model and a quintuplet model on the EfficientNet-b0 are pusblished, as well as the trained weights for on the Market-1501 dataset. 

In addtion, an evaluation method is built for these models, where the models can simply be loaded and tested on an open-world re-id setting.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Instructions:

Instructions: This is a test procedure for re-id models that simulates a real-world re-id scenario.

3 random camera tracks for 10 random peolpe in the testset will be selected as probe tracks that will be compared against the gallery tracks. The gallery conists out of the remaining 90 people, sepererated by camera ID, and the remaining camera tracks of the 10 selected people.

The goal of the model is to correctly assign the right tracks as 'same' while assigning the wron identities as different.

Out of the scoreboard, the False Target Rate (FTR) and the True Target Rate (TTR) will be calculated based on the best cutoff score.
The final score will be the TTR minus FTR.

To run the test, simply run main.py

<p align="right">(<a href="#readme-top">back to top</a>)</p>
