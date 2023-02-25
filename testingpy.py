
class Vehicle:
    def __init__(self):
        pass

    def make_of_vehicle(self):
        return "No Make"
    
class BMW(Vehicle):
    def __init__(self):
        pass

    def make_of_vehicle(self):
        return "BMW"

def printMake(v: Vehicle):
    print(v.make_of_vehicle())

print("hello")
v = Vehicle()
c = BMW()
print(v.make_of_vehicle())
print(c.make_of_vehicle())
printMake(v)
printMake(c)