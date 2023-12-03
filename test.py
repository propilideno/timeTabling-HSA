import random
import time

class Person:
    def __init__(self, uniqueString, name, age):
        self.uniqueString = uniqueString
        self.name = name
        self.age = age

    def __str__(self):
        return self.uniqueString

if __name__ == '__main__':
    persons_dict = {}
    start = time.time()

    for i in range(3000000):
        # Generate a random string to be name
        # Random int to be age (0-100)
        p = Person(f"Person{i}", str(random.random()), random.randint(0, 100))
        persons_dict[p.uniqueString] = p
        # persons_dict.update({p.uniqueString: p})
    print('Created')

    # Exemplo de busca por uniqueString
    search_key = "Person12323"
    if search_key in persons_dict:
        found_person = persons_dict[search_key]
        print(f"Person found: {found_person.name}, Age: {found_person.age}")
    else:
        print(f"Person with uniqueString '{search_key}' not found.")

    print('Time:', time.time() - start)
