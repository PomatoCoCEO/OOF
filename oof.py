import datetime
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

__author__ = "Paulo Cortesão"
__email__ = "paulocortesao@student.dei.uc.pt"
__date__ = "18/7/2023"
__version__ = "1.0"
__license__ = "MIT"

class OOF:
    def __init__(self, analyse: bool = False, output_folder: str = None) -> None:
        '''starts the OOF instance. If analyse is True, then the output folder is the one specified by the user. Otherwise, it is automatically generated.'''
        if not analyse:
            curr_time = datetime.datetime.now()
            self.day = curr_time.day
            self.month = curr_time.month
            self.year = curr_time.year
            self.hour = curr_time.hour
            self.minute = curr_time.minute
            self.output_folder = (
                f"out/{self.year}/{self.month}/{self.day}/{self.hour}-{self.minute}"
            )
            no_folder = self.__discover_number__()
            self.output_folder += f"/{no_folder}"
            self.config = {}
            self.__create_folders__()
        else:
            # only for analysis of a folder
            self.output_folder = output_folder

    def __discover_number__(self) -> int:
        '''discovers the number of the folder to be created'''
        i = 1
        while os.path.isdir(self.output_folder + f"/{i}"):
            i += 1
        return i

    def __create_folders__(self) -> None:
        '''creates the folders for the output'''
        os.makedirs(self.output_folder)
        folder_names = ["txt", "npy", "npz", "img"]
        for folder_name in folder_names:
            os.makedirs(self.output_folder + f"/{folder_name}")

    def plot(self, *args, **kwargs) -> None:
        '''plots the data and saves it in the img folder. If a name is specified, it is used as the name of the file. Otherwise, a number is assigned to the file.'''
        plot_name = None
        if "name" in kwargs:
            plot_name = str(kwargs["name"])
            del kwargs["name"]
        
        plt.plot(*args, **kwargs)
        if plot_name:
            plt.savefig(self.output_folder + f"/img/{plot_name}.png")
        else:
            plot_no = len(os.listdir(self.output_folder + "/img")) + 1
            plt.savefig(self.output_folder + f"/img/plot_{plot_no}.png")
        plt.show(block=False)

    def plot_3d(self, *args, **kwargs) -> None:
        '''plots the data in 3d and saves it in the img folder. If a name is specified, it is used as the name of the file. Otherwise, a number is assigned to the file.'''
        plot_name = None
        if "name" in kwargs:
            plot_name = str(kwargs["name"])
            del kwargs["name"]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot(*args, **kwargs)
        if plot_name:
            plt.savefig(self.output_folder + f"/img/{plot_name}.png")
        else:
            plot_no = len(os.listdir(self.output_folder + "/img")) + 1
            plt.savefig(self.output_folder + f"/img/plot_{plot_no}.png")
        plt.show(block=False)

    def log(self, *args, **kwargs) -> None:
        '''prints in log file and in the console simultaneously'''
        with open(self.output_folder + "/txt/log.txt", "a") as f:
            print(*args, **kwargs, file=f)
        print(*args, **kwargs)

    def save_array(
        self, array: np.ndarray, name: str, compressed: bool = False
    ) -> None:
        '''saves a numpy array in the output folder. If compressed is True, the array is saved in compressed format.'''
        if compressed:
            np.savez_compressed(self.output_folder + f"/npz/{name}.npz", array)
        else:
            np.save(self.output_folder + f"/npy/{name}.npy", array)

    def load_array(self, name: str, compressed: bool = False):
        '''loads a numpy array from the output folder. If compressed is True, the array is loaded from compressed format.'''
        if compressed:
            data = np.load(self.output_folder + f"/npz/{name}.npz")
            ks = data.files
            print("ks", ks)
            if len(ks) == 1:
                return data[ks[0]]
            else:
                # in this case, a dictionary is returned
                return data

        else:
            return np.load(self.output_folder + f"/npy/{name}.npy")

    # saves data in a user-defined format
    def save_data(self, data, name: str, lambda_save, format: str) -> None:
        '''saves data in a user-defined format'''
        # takes the data, the name of the file, the format and the function to use for formatting
        if not os.isdir(self.output_folder + f"/{format}"):
            os.makedirs(self.output_folder + f"/{format}")
        lambda_save(data, self.output_folder + f"/format/{name}.{format}")

    # loads data in a user-defined format
    def load_data(self, name: str, lambda_load, format: str) -> None:
        '''loads data in a user-defined format'''
        # takes the name of the file, the format and the function to use for formatting
        return lambda_load(self.output_folder + f"/format/{name}.{format}")

    def report(self) -> None:
        '''prints the report of the file structure in the console'''
        # prints the report of the file structure in the console
        print("OFoI Report")
        print("-----------")
        print(f"Output Folder: {self.output_folder}")
        print(f"Config: {self.config}")
        print(f"Number of Plots: {len(os.listdir(self.output_folder + '/img'))}")
        print(f"Number of Numpy Arrays: {len(os.listdir(self.output_folder + '/npy'))}")
        print(
            f"Number of Compressed Numpy Arrays: {len(os.listdir(self.output_folder + '/npz'))}"
        )
        print(f"Number of Text Files: {len(os.listdir(self.output_folder + '/txt'))}")
        for f in os.listdir(self.output_folder):
            if f not in ["img", "npy", "npz", "txt"]:
                print(
                    f"Number of {f} Files: {len(os.listdir(self.output_folder + '/' + f))}"
                )
        print("End of Report")
