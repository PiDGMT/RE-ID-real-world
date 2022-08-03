import os
import shutil

markettrain = os.listdir("C:/Users/piete/documents/siamese/multi-query")

counter = 0
for i in sorted(markettrain):
  counter += 1
  if counter % 15 == 0:
    shutil.move("C:/Users/piete/documents/siamese/multi-query/"+i, "C:/Users/piete/documents/siamese/testset")