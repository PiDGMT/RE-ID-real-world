from torchvision import models
import torch

class quintuplet(torch.nn.Module):

    def __init__(self):
        super(quintuplet, self).__init__()
        self.net = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights)


    def forward(self, input1, input2, input3=None, input4=None, input5=None):

        output1 = self.net(input1)
        output2 = self.net(input2)
        if input3:
          output3 = self.net(input3)
        else: output3 = None
        if input4:
          output4 = self.net(input4)
        else: output4 = None
        if input5:
            output5 = self.net(input5)
        else: output5= None
            
if __name__ == "__main__":
  net = quintuplet().cuda()
  #hieronder zijn de weights
  checkpoint = torch.load('C:/Users/piete/Documents/siamese/weights/quadruplet1501V2valid')
  net.load_state_dict(checkpoint['model_state_dict'])
  #dit is om hem in evaluation modus te zetten
  net.eval()