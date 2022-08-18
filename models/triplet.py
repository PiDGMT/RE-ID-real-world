from torchvision import models
import torch

class Tripletb0(torch.nn.Module):

    def __init__(self):
        super(Tripletb0, self).__init__()
        self.net = models.efficientnet_b1()

    def forward(self, input1, input2, input3=None):

        output1 = self.net(input1)
        output2 = self.net(input2)
        if input3:
          output3 = self.net(input3)
        else: output3 = None

        return output1, output2, output3

if __name__ == "__main__":
  net = Tripletb0().cuda()
  #hieronder zijn de weights
  checkpoint = torch.load('../weights/triplet1501V2validb1schedule')
  net.load_state_dict(checkpoint['model_state_dict'])
  #dit is om hem in evaluation modus te zetten
  net.eval()
