## The Great Pieter Meulenbelt Re-ID system

Instructions:

Instructions: This is a test procedure for re-id models that simulates a real-world re-id scenario.

3 random camera tracks for 10 random peolpe in the testset will be selected as probe tracks that will be compared against the gallery tracks. The gallery conists out of the remaining 90 people, sepererated by camera ID, and the remaining camera tracks of the 10 selected people.

The goal of the model is to correctly assign the right tracks as 'same' while assigning the wron identities as different.

Out of the scoreboard, the False Target Rate (FTR) and the True Target Rate (TTR) will be calculated, and the score will be the TTR-FTR.

To run the test, simply run main.py