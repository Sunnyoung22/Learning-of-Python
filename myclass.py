# This Python source file includes some classes I need
# 2020.07.14    Sunnyoung

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

        self._people = group
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
            raise StopIteration()
