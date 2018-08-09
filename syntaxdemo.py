# Syntax examples
import sys
import mysql.connector

#if

#for
a = ['Mary', 'had', 'a', 'little', 'lamb']
for word in a:
  print(word)
print("-"*40)
for i in range(len(a)):
  print(i, a[i])

knights = {'gallahad': 'the pure', 'robin': 'the brave', 'donald':'the duck'}
for k, v in knights.items():
  print(k, v)

#while


#function
def cheeseshop(kind, *arguments, **keywords): # one star argument is: tuple, two stars argumen is dictionary
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])

cheeseshop("Limburger", "It's very runny, sir.", "It's really very, VERY runny, sir.",
           shopkeeper="Michael Palin",
           client="John Cleese",
           sketch="Cheese Shop Sketch")

#class

class Animal:
  def __init__(self, **kwargs):
    if 'type' in kwargs: self._type = kwargs['type']
    self._name = kwargs['name']
    self._age = kwargs['age']
  
  def type(self):
    return self._type

  def name(self, t = None): #default value: None, is like js undefined
    if t: self._type = t #this makes it both a getter AND a setter (if t is provided it will replace the value of self._type)
    return self._name

  def age(self):
    return self._age
  
  def __str__(self):
    return str(self.__dict__)

  def __eq__(self, other): #equals method compares all attributes of the class.
    return self.__dict__ == other.__dict__
  
  # def __str__(self): # The python way to make a toString() method
  # return f'{self.name()} er et {self.type()} med alderen: {self.age()} år'


otto = Animal(type='næsehorn',name='otto',age=2)
print(otto)

#Inheritance
class Duck(Animal): #Duck inherits from Animal
  def __init__(self, **kwargs):
    self._type = 'Duck'
    if 'type' in kwargs: del kwargs['type']
    super().__init__(**kwargs)

donald = Duck(name='Donald', age='3')
donald2 = Duck(name='Donald', age='3')
daisy = Duck(name='Daisy', age='3')
print(donald, daisy)
print(donald == donald2)
print(donald == daisy)

#collections
##lists and tuples (immutable lists)
a = (3, 5, 7)
x = [12,13] #list
y=list(range(5)) # mutable list made from immutable tuple
z = {'horse', 'cow', 'donkey'} # set (contains no dublicates)
æ = range(20, 40, 3) # immutable tuble with range(startvalue, stopvalue, step)
for listvalue in x: 
  print(listvalue)
for listvalue in y:
  print(listvalue)
for listvalue in z:
  print(listvalue)
for listvalue in æ:
  print(listvalue)

print(type(a))
print(type(z))

##dictionary
b = {"one":1, "two":2, "three":3}
print(type(b))
print(b["two"])

## exceptions
def demoExceptions():
  try:
    x = int("foo") # comment this line out to test second exception 
    y = 30/0
  except ValueError: #except is like 'catch()' in java
    print(f'I caught a value error{sys.exc_info()}')
  except ZeroDivisionError as e:
    print('You tried to divide by zero')
    print(f'error message is: {e}')
  else: 
    print('You did it without hitting any exceptoins')

demoExceptions()

# I/O
print('-'*40)
def main():
  print('Read and write text files')
  infile = open('text.txt') # the file object returned is an iterator open('text.txt','r') is readmode and 'w' is in write mode. 'a' is append
  outfile = open('outputfile.txt','wt') # wt: writemode and text (rather than binary) - the file will be created if it does not exist.
  for line in infile:
    #print(line.rstrip()) # simple print to console
    print(line.rstrip(), file=outfile)
    print('.', end='', flush=True)
  outfile.close()
  print('\ndone.')
  
  print('Read and write binary files')
  inbinary = open('moon.jpg','rb')
  outbinary = open('outputbinary.jpg','wb')
  while True:
    buf = inbinary.read(10240) # 10k buffer size is small for laptop but, might be resonable memory allocation on a mobile device.
    if buf:
      outbinary.write(buf)
      print('.',end='', flush=True)
    else: break
  outbinary.close()
  print('\ndone.')


if __name__ == '__main__': main()

# database: See the dbconnection.py file

# deserializing json
import json 
print('-------------------------------------------------------------')
json_input = '{"persons": [{"name": "Brian", "city": "Seattle"}, {"name": "David", "city": "Amsterdam"} ] }'
 
try:
    decoded = json.loads(json_input)
 
    # Access data
    for x in decoded['persons']:
        print(x['name'])
 
except (ValueError, KeyError, TypeError):
    print("JSON format error")

# reading from rest api
## Make a get request to get the latest position of the international space station from the opennotify api.
import requests, datetime
response = requests.get("http://api.open-notify.org/iss-now.json")

# Print the status code of the response.
print(response.status_code)
print(response.content)
jsontxt = response.json()
print(jsontxt)
print(jsontxt["timestamp"])
ts = jsontxt["timestamp"]
time = datetime.datetime.fromtimestamp(ts/1000.0)
print(time)