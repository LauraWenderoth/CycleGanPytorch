from data.base_dataset import BaseDataset, get_transform
from data.image_folder import make_dataset
from PIL import Image
from data.patch_extraction import pad_image_to_size

class SingleDataset(BaseDataset):
    """This dataset class can load a set of images specified by the path --dataroot /path/to/data.
    It can be used for generating CycleGAN results only for one side with the model option '-model test'.
    """

    def __init__(self, opt):
        """Initialize this dataset class.
        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """

        BaseDataset.__init__(self, opt)
        self.A_paths = sorted(make_dataset(opt.dataroot, opt.max_dataset_size))
        self.A_size = len(self.A_paths)  # get the size of dataset A
        input_nc = self.opt.output_nc if self.opt.direction == 'BtoA' else self.opt.input_nc
        self.transform = get_transform(opt, grayscale=(input_nc == 1))

    def __getitem__(self, index):
        """Return a data point and its metadata information.
        Parameters:
            index - - a random integer for data indexing
        Returns a dictionary that contains A and A_paths
            A(tensor) - - an image in one domain
            A_paths(str) - - the path of the image
        """

        path_index = index // 64
        A_path = self.A_paths[path_index % self.A_size]  # make sure index is within then range

        A_img = Image.open(A_path).convert('RGB')


        # slice part
        img_pad_A = pad_image_to_size(A_img, 2048)

        patch_index = index % 64
        x = patch_index // 8
        y = patch_index % 8
        A = img_pad_A[x * 256:x * 256 + 256, y * 256:y * 256 + 256]

        # convert to PIL
        A = Image.fromarray(A)
        # apply image transformation

        return {'A': A, 'A_paths': A_path}

    def __len__(self):
        """Return the total number of images in the dataset."""
        return len(self.A_paths)