from A.person_pb2 import Person
from addressbook_pb2 import AddressBook
from google.protobuf.json_format import MessageToJson
import json

# create a instance
person = Person()
person.name = "Alice"
person.age = 18
person.emails.append("aaa@xxx.com")
person.emails.append("bbb@xxx.com")
person.scores["a"] = 5
person.scores["b"] = 4
person.test_age = 4

# serialize
with open("person.bin", "wb") as f:
    f.write(person.SerializeToString())

# deserialize
person = Person()
with open("person.bin", "rb") as f:
    person.ParseFromString(f.read())
    
print('write into file person.json')
with open("person.json", "w") as f:
    json_str = MessageToJson(person, preserving_proto_field_name=True, indent=2)
    f.write(json_str)

print(f'person: {type(person)}\n{json.loads(MessageToJson(person, preserving_proto_field_name=True))}')

# create a recursive instance
book = AddressBook()
book.holder = "Bob"
book.persons.append(person)
print(f'book: {type(book)}\n{json.loads(MessageToJson(book, preserving_proto_field_name=True))}')
