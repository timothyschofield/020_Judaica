
##### OOPs formats #####
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"I'm {self.name}, and I'm {self.age} years old."

    def __repr__(self):
        return f"{type(self).__name__}(name='{self.name}', age={self.age})"
    
jane = Person("Jane Doe", 25)

print("This calls __str__ ")
print(f"{jane!s}")

print("This calls __repr__ ")
print(f"{jane!r}")



