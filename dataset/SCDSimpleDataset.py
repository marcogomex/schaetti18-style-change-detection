# -*- coding: utf-8 -*-
#

# Imports
from torch.utils.data.dataset import Dataset
import urllib
import os
import zipfile
import json
import codecs


# Style change detection dataset
class SCDSimpleDataset(Dataset):
    """
    Style change detection dataset
    """

    # Constructor
    def __init__(self, root='./data', download=False, transform=None, train=True):
        """
        Constructor
        :param root:
        :param download:
        :param transform:
        :param train:
        """
        # Properties
        self.root = root
        self.transform = transform
        self.train = train
        self.samples = list()
        self.changes_char = dict()

        # Create directory if needed
        if not os.path.exists(self.root):
            self._create_root()
        # end if

        # Download the data set
        if download and not os.path.exists(os.path.join(self.root, "training")):
            self._download()
        # end if

        # Generate data set
        self._load()
    # end __init__

    ##########################################
    # PUBLIC
    ##########################################

    # Set train
    def set_train(self, mode):
        """
        Set train (or validation)
        :param mode:
        :return:
        """
        self.train = mode

        # Load data
        self._load()
    # end set_train

    ##########################################
    # OVERRIDE
    ##########################################

    # Length
    def __len__(self):
        """
        Length
        :return:
        """
        return len(self.samples)
    # end __len__

    # Get item
    def __getitem__(self, idx):
        """
        Get item
        :param idx:
        :return:
        """
        # Get sample
        text_file, truth_file = self.samples[idx]

        # Read text
        sample_text = codecs.open(text_file, 'r', encoding='utf-8').read()

        # Read truth
        sample_truth = json.load(codecs.open(truth_file, 'r', encoding='utf-8'))

        # Changes
        changes = sample_truth['changes']

        # Transform
        transformed = self.transform(sample_text)

        # Class
        c = 1 if changes else 0

        return transformed, c, sample_truth['positions']
    # end __getitem__

    ##########################################
    # PRIVATE
    ##########################################

    # Create the root directory
    def _create_root(self):
        """
        Create the root directory
        :return:
        """
        os.mkdir(self.root)
    # end _create_root

    # Download the dataset
    def _download(self):
        """
        Download the dataset
        :return:
        """
        # Path to zip file
        path_to_zip = os.path.join(self.root, "pan18-style-change-detection.zip")

        # Download
        urllib.urlretrieve("http://www.nilsschaetti.com/datasets/pan18-style-change-detection.zip", path_to_zip)

        # Unzip
        zip_ref = zipfile.ZipFile(path_to_zip, 'r')
        zip_ref.extractall(self.root)
        zip_ref.close()

        # Delete zip
        os.remove(path_to_zip)
    # end _download

    # Load dataset
    def _load(self):
        """
        Load the dataset
        :return:
        """
        # Sub directory
        if self.train:
            subdir = "training"
        else:
            subdir = "validation"
        # end if

        # For each file
        for file_name in os.listdir(os.path.join(self.root, subdir)):
            # Text file
            if file_name[-4:] == ".txt":
                # Truth file
                truth_file = file_name[:-4] + ".truth"
                truth_file = os.path.join(self.root, subdir, truth_file)

                # Add to samples
                self.samples.append((os.path.join(self.root, subdir, file_name), truth_file))
            # end if
        # end for
    # end _load

# end SCDSimpleDataset
