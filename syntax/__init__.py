from  dataclasses import dataclass

@dataclass
class Rectangle:
    width : int
    height : int

    def area(self) -> int:
        return self.width * self.height

rect = Rectangle(3,4)
print(rect.area())

if __name__ =='__Rectangle__':
    Main()
