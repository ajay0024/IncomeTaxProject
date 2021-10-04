import pickle
import random



class DataHandler:
    def load_data(self):
        try:
            with open("bin.dat","rb") as f:
                objects = pickle.load(f)
        except:
            print("Couln't open bin.dat")
            objects = []
        return objects

    def save_data(self, data):
        with open("bin.dat", "wb") as f:
            pickle.dump(data, f)
    def save_data_db(self, data ):
        for d in data:
            print(d.section_title)
