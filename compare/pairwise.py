from torch.utils.data import Dataset

class Pairwise(Dataset):
    """
    Transforms the input images to be suitable for the re-id model
    """
    def __init__(self, img1, img2, transform):
        self.img1 = img1
        self.img2 = img2
        self.transform = transform

    def __getitem__(self, index):
        img1 = self.transform(self.img1)
        img2 = self.transform(self.img2)
        return img1, img2

    def __len__(self):
        return 2
