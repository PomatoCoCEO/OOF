import shutil
import os
import numpy as np
import pandas as pd
from oof import OOF


def test_folder_creation():
    oof = OOF()
    assert os.path.isdir(oof.output_folder)
    for format in ["txt", "npy", "npz", "img"]:
        assert os.path.isdir(oof.output_folder + f"/{format}")
    shutil.rmtree(oof.output_folder)


def test_plot():
    oof = OOF()
    oof.plot([1, 2, 3], [1, 2, 3])
    assert os.path.isfile(oof.output_folder + "/img/plot_1.png")
    shutil.rmtree(oof.output_folder)


def test_plot_3d():
    oof = OOF()
    oof.plot_3d([1, 2, 3], [1, 2, 3], [1, 2, 3])
    assert os.path.isfile(oof.output_folder + "/img/plot_1.png")
    shutil.rmtree(oof.output_folder)


def test_log():
    oof = OOF()
    oof.log("test")
    assert os.path.isfile(oof.output_folder + "/txt/log.txt")
    shutil.rmtree(oof.output_folder)


def test_save_array():
    oof = OOF()
    oof.save_array([1, 2, 3], "test")
    assert os.path.isfile(oof.output_folder + "/npy/test.npy")
    shutil.rmtree(oof.output_folder)


def test_load_array():
    oof = OOF()
    oof.save_array([1, 2, 3], "test")
    assert oof.load_array("test").all() == np.array([1, 2, 3]).all()
    shutil.rmtree(oof.output_folder)


def test_save_array_compressed():
    oof = OOF()
    oof.save_array([1, 2, 3], "test", compressed=True)
    assert os.path.isfile(oof.output_folder + "/npz/test.npz")
    shutil.rmtree(oof.output_folder)


def test_load_array_compressed():
    oof = OOF()
    oof.save_array([1, 2, 3], "test", compressed=True)
    assert oof.load_array("test", compressed=True).all() == np.array([1, 2, 3]).all()
    shutil.rmtree(oof.output_folder)

def test_save_data():
    oof = OOF()
    def save_pandas(frame: pd.DataFrame, name: str):
        frame.to_csv(name, index=False)
    frame = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    oof.save_data(frame, "test", save_pandas, 'csv')
    assert os.path.isfile(oof.output_folder + "/csv/test.csv")

def test_load_data():
    oof = OOF()
    def save_pandas(frame: pd.DataFrame, name: str):
        # index=False so that the first column is not Unnamed: 0
        frame.to_csv(name, index=False)
    frame = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    oof.save_data(frame, "test", save_pandas, 'csv')
    def load_pandas(name:str):
        return pd.read_csv(name)
    fr2 = oof.load_data("test", load_pandas, 'csv')
    print(fr2.head())
    print(frame.head())
    assert fr2.equals(frame)


def test_report():
    oof = OOF()
    oof.log("test")
    assert os.path.isfile(oof.output_folder + "/txt/log.txt")
    oof.report()
    shutil.rmtree(oof.output_folder)


if __name__ == "__main__":
    test_folder_creation()
    test_plot()
    test_plot_3d()
    test_log()
    test_save_array()
    test_load_array()
    test_save_array_compressed()
    test_load_array_compressed()
    test_save_data()
    test_load_data()
    test_report()
    # shutil.rmtree("out")
    print("All tests passed!")
