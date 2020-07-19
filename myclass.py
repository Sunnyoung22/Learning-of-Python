# This Python source file includes some classes I need
# 2020.07.14    Sunnyoung

# Import some modules needed
import copy
import os
import csv
import abc

import zipfile

class Person(object):
    # Attention, is __; not _!
    def __init__(self, name, sex, age): # This is a magic function
        self.name = name              
        self.sex = sex
        self.age = age
    # Set some raleted parameter
    def set_name(self, name):
        self.name = name
    def set_sex(self, sex):
        self.sex = sex
    def set_age(self, age):
        self.age = age
    
    # Return infomation
    def get_name(self):
        return self.name
    def get_sex(self):
        return self.sex
    def get_age(self):
        return self.age
    def __str__(self):  #magic func
        #return self.__name + self.__sex + self.__age + '\n'
        return "{} {} {}".format(self.name, self.sex, self.age)

    # Print infomation about this people
    def show_info(self):
        print("Name:{}\tSex:{}\tAge:{}".format(self.name, self.sex, self.age))

    
# Class josephus 
class JosephusCircle(object):

    def __init__(self, group, step=1, start_pos=1):

        if step <= 0 or start_pos <= 0:
            raise Exception("The input parameter needs to be greater than 0.")
        self._people = copy.deepcopy(group)
        self._people_bak = copy.deepcopy(group)
        self.step = step
        self.start_pos = start_pos
        
    # Set some raleted parameter
    def set_step(self, step):
        if step <= 0:
            raise Exception("The input parameter needs to be greater than 0.")
        self.step = step
    def set_pos(self, start_pos):
        if start_pos <= 0:
            raise Exception("The input parameter needs to be greater than 0.")
        self.start_pos = start_pos

    @property
    def total(self): # Number of members
        return len(self._people)

    # Add a new preson to JosephusCircle
    def append(self, person):
        self._people.append(person)
    
    # Pop a person with the rule of JosephusCircle
    def pop(self):

        if self.total == 0:
            raise Exception("There is no one here.")
        out_index = (self.start_pos - 1 + self.step - 1) %self.total
        return self._people.pop(out_index)

    """Use the __iter__() method to generate iterative objects, 
    and then use the __next__() method to access
    """
    # Make this Class Iterable
    def __iter__(self): # Magic func
        return self
    # Make it an iterator
    def __next__(self):
        if self.total > 0:
            return self.pop()
        else:
            self._people = copy.deepcopy(self._people_bak)  #Restore list for next traversal
            raise StopIteration()

# Class MyReader class can read personnel information in txt, csv and zip files
class MyReader(object):
    def __init__(self, file_name):# File_name must include file path
        if os.path.isfile(os.path.realpath(file_name)):
            self.file_name = file_name
        else:
            raise Exception("The file does not exist")
    # Returns the file extension 
    def get_file_type(self):
        return os.path.splitext(self.file_name)[1]
    
    def get_all_info(self):
        file_type = self.get_file_type()

        ret_info = []
        if file_type == ".txt" :
            with open(self.file_name, 'r') as target_file:
                for line in target_file: # Read it by line
                    ret_info.append(line.strip('\n')) # remove \n
            return ret_info
        
        elif file_type == ".csv":
            with open(self.file_name, 'r') as target_file:
                for line in csv.reader(target_file):
                    ret_info.append(' '.join(line)) # Use blank to join list to str and then store it to ret_info
            return ret_info
        
        elif file_type == ".zip":
            with zipfile.ZipFile(self.file_name, "r") as zfile:
                zfile.extractall(".\\The extracted file") # Extract all files to the specified directory
            for extracted_file in os.listdir(".\\The extracted file"):
                if os.path.splitext(extracted_file)[1] == ".txt" or ".csv":
                    self.file_name = ".\\The extracted file.\\{}".format(extracted_file)
                    ret_info.extend(self.get_all_info()) # Recursively call functions to handle txt and csv
                    os.remove(self.file_name)
            return ret_info
        else:
            raise Exception("Unsupported file type")

# An abstract class whitch named Reader
class Reader(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def get_file_type(self):
        pass

    @abc.abstractmethod
    def get_all_info(self):
        pass

    @abc.abstractmethod
    def __iter__(self):
        pass
    

class TxtReader(Reader):
    # Just 4 txt type
    def __init__(self, file_name):# File_name must include file path
        if os.path.isfile(os.path.realpath(file_name)):
            if os.path.splitext(file_name)[1] == ".txt":
                self.file_name = file_name
            else:
                raise Exception("File is not in txt format")
        else:
            raise Exception("The file does not exist")

    def get_file_type(self):
        return "txt"
    
    # Rewrite
    def get_all_info(self):
        ret_info = []
        with open(self.file_name, 'r') as target_file:
            for line in target_file: # Read it by line
                ret_info.append(line.strip('\n')) # remove \n
        return ret_info

    def __iter__(self):
        with open(self.file_name, 'r') as target_file:
            for line in target_file: # Read it by line
                yield line.strip('\n') # remove \n
    

class CsvReader(Reader):
    
    def __init__(self, file_name):# File_name must include file path
        if os.path.isfile(os.path.realpath(file_name)):
            if os.path.splitext(file_name)[1] == ".csv":
                self.file_name = file_name
            else:
                raise Exception("File is not in csv format")
        else:
            raise Exception("The file does not exist")
    
    def get_file_type(self):
        return "csv"

    # Rewrite
    def get_all_info(self):
        ret_info = []
        with open(self.file_name, 'r') as target_file:
            for line in csv.reader(target_file):
                ret_info.append(' '.join(line)) # Use blank to join list to str and then store it to ret_info
        return ret_info

    def __iter__(self):
        with open(self.file_name, 'r') as target_file:
            for line in csv.reader(target_file): # Read it by line
                yield ' '.join(line)


class ZipReader(Reader):

    def __init__(self, file_name):# File_name must include file path
        if os.path.isfile(os.path.realpath(file_name)):
            if os.path.splitext(file_name)[1] == ".zip":
                self.file_name = file_name
            else:
                raise Exception("File is not in zip format")
        else:
            raise Exception("The file does not exist")
    
    def get_file_type(self):
        return "zip"

    # Rewrite
    def get_all_info(self):
        ret_info = []
        with zipfile.ZipFile(self.file_name, "r") as zfile:
            zfile.extractall(".\\The extracted file") # Extract all files to the specified directory
        for extracted_file in os.listdir(".\\The extracted file"):
            if os.path.splitext(extracted_file)[1] == ".txt":
                self.file_name = ".\\The extracted file.\\{}".format(extracted_file)
                txt_reader = TxtReader(self.file_name) # Create an object temporarily to get info
                ret_info.extend(txt_reader.get_all_info())
                os.remove(self.file_name)
            if os.path.splitext(extracted_file)[1] == ".csv":
                self.file_name = ".\\The extracted file.\\{}".format(extracted_file)
                csv_reader = CsvReader(self.file_name)
                ret_info.extend(csv_reader.get_all_info())
                os.remove(self.file_name)
        return ret_info

    def __iter__(self):
        return self.get_all_info().__iter__()

if __name__ == '__main__':
    file_name = ".\\Personal Information.txt"
    txt_reader = TxtReader(file_name)
    for i in txt_reader:
        print(i)