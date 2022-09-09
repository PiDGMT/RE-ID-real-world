from torchvision import models
import torch

class Quadrupletb0(torch.nn.Module):

    def __init__(self):
        """
        Loads the model architecture from Pytorch and the pretrained ImageNet weights
        """
        super(Quadrupletb0, self).__init__()
        self.net = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights)

    def forward(self, input1, input2, input3=None, input4=None):
        """
        Forwards the inputs of the model trough the model
        The 3rd and 4th inputs as set to None, as for image comparison suring tested, these are not used
        returns the outputs
        """

        output1 = self.net(input1)
        output2 = self.net(input2)
        if input3:
          output3 = self.net(input3)
        else: output3 = None
        if input4:
          output4 = self.net(input4)
        else: output4 = None


        return output1, output2, output3, output4

if __name__ == "__main__":
  net = Quadrupletb0().cuda()
  #hieronder zijn de weights
  checkpoint = torch.load('../weights/quadruplet1501V2validschedule')
  net.load_state_dict(checkpoint['model_state_dict'])
  #dit is om hem in evaluation modus te zetten
  net.eval()
