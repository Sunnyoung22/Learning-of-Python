#%%
# Try to solve joseph problem using object-oriented programming
# 2020.7.14 Sunnyoung
def get_person_from_file(file_name):
    """Get information about people from "file_name"
    Return information about people in the form of a list
    """
    # import Class 
    from myclass import MyReader
    from myclass import Person

    myreader = MyReader(file_name)
    personal_info = myreader.get_information()

    group = [] # Initialize a group of people
    # Use blank to split the information and use them to create new object of Person Class
    for i in range(len(personal_info)):
            group.append(Person(personal_info[i].split(" ")[0], personal_info[i].split(" ")[1], personal_info[i].split(" ")[2]))
    return group
  

# Determine if the input is a positive integer
def is_inputlegal(input_):
    if not input_.isdigit():
        return False
    elif int(input_) < 0:
        return False
    else:
        return True

# import Class which named JosephusCircle from myclass.py 
from myclass import JosephusCircle
file_name = ".\\Personal Information.zip"

STEP = input("请输入数到几排除成员:")
if is_inputlegal(STEP):
    START_POS = input("请输入开始序号:")
    if is_inputlegal(START_POS):
        group = get_person_from_file(file_name) # Get people from files 
        try:
            josephus = JosephusCircle(group, int(STEP), int(START_POS))   # Create an object of type JosephusCircle
            print("The first one to be out:")
            print(josephus.pop())
            print("\nThe order of outs:")
            [x.show_info() for x in josephus]   # Output the result through traversal
        except Exception as ex:
            print(ex)
    else:
        print("请输入正整数")
else:
    print("输入参数有误，请输入正整数")


#%%
# Testing
group = get_person_from_file(file_name)

josephus_one = JosephusCircle(group)
josephus_two = JosephusCircle(group, 2, 1)
josephus_three = JosephusCircle(group, 1, 3)
josephus_four = JosephusCircle(group, 3, 2)

assert(id(josephus_one._people) != id(group))
assert(josephus_one.pop().get_name() == "Dani")
assert(josephus_two.pop().get_name() == "John")
assert(josephus_three.pop().get_sex() == "male")
assert(josephus_four.pop().get_age() == "20")
# assert(JosephusCircle(group, -1, 0), "The input parameter needs to be greater than 0.")
