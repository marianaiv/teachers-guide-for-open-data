# Introduction to coding in Python

Being able to code is an essential skill for a Particle Physicist (or any scientist, for that matter). 
Our datasets are simply too large to process without the assistance of computers!  An ATLAS Physicist 
typically uses some combination of the C++ and Python programming languages to accomplish everything 
from simulating proton-proton collisions to searching for Higgs bosons.

As being code-literate is a prerequisite to analysing ATLAS data, we will in this notebook review some 
of the basics of coding in Python.  We will do this by presenting a diluted and interactive version of 
the tutorial of the [official Python documentation](https://docs.python.org/3/tutorial/index.html).  For more information on any topic, let 
the official Python documentation be your first port of call.  We will link to specific parts of the tutorial 
as we go along.

Python is extensively used by beginners and software engineers alike, for both business and pleasure.  
It can be fun!  It is named after the BBC series "Monty Python's Flying Circus" and refers to its founder as 
a Benevolent Dictator For Life ([BDFL](https://docs.python.org/3/glossary.html)).

---
## Hello, world
                
The ["Hello, World!" programme](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) is a time-honoured tradition 
in Computer Science which will be respected here.  The idea of Hello World is to illustrate the basics of a language and 
to verify that the coding environment has been properly installed and set up.  So to test Python in this notebook, have a 
go at running the code of the next cell (`Shift + Enter`)...if it does what you expect, then you are good to go!

```python
print("Hello, World!")
```

---

## Numbers, Strings, and Compound Data Types

[Following [An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html)]  
                
### Python as a calculator

Python is good at maths! Run the examples of the following code cells to see what the operators `+`, `-`, `*` and `/` do, to 
find that they have the effect of addition, subtraction, multiplication, and division.

```python
print(2+2)
```

```python
print((50 - 5*6) / 4)
```

Python additionally povides a convenient power operator `**`.

```python
print(2**7) # Power
```

```python
print(4**(1/2)) # Use fractional powers to calculate roots
```

Notice the `#`'s above? This notation tells Python that everything after the hashtag in that same line should not be executed 
as a command, but it is just a comment.
                
Why do some of the numbers produced by these operations have decimal points, while others do not?  It is because we have here two _types_ 
of numbers: `int` types and `float` types.  The `float` type represents a [floating point number](https://en.wikipedia.org/wiki/Floating-point_arithmetic) 
and is a computer's formulaic binary representation of a decimal number.  The `int` type represents integer values.
> If you are lucky, you will never have to worry about 'floating point precision', but it can be a significant consideration, with errors here having in the 
past caused [rockets to explode](http://www-users.math.umn.edu/~arnold/disasters/ariane.html)!

It is possible to assign a value to a variable using the `=` operator.          

```python
x = 4
print(x**2)
```


We have also the handy in-place operators `+=`, `-=`, `*=` and `/=`. These perform an operation on the variable they are being applied to, 
then reassigning that variable to the result of the operation.

```python
y = 10
y += 2
print(y)
```
    
### Strings

The Python `string` is a string of characters enclosed in quotation marks (`'...'` or `"..."`).  Strings may be operated upon by the above 
mathematical operations and are indexed as if they were lists of characters!

```python
prefix = 'Py'
print(prefix + 'thon')
```

```python
print(3 * 'un' + 'ium')
```
    
```python
word = 'Python'
# Access the first character of the string which is indexed by 0                    
print(word[0])
# Access the last character of the string which is indexed by -1
print(word[-1])
# Slice the string from index 1 (inclusive) to 5 (not inclusive)
print(word[1:5])
```

### Compound Data Types

A Python list is a mutable (i.e. you can change it), compound (the list itself holds values of a certain type) data type 
for grouping together a sequence of values, and have them ordered in a certain way so that we can find each entry in the array 
by its "house number" or index.


```python
# Here is an example list
nums = [1, 2, 3]
# Lists are mutable
nums[0] = 4 #Like strings, the numbering of the elements starts at 0, not 1
print(nums)
```

```python
# Lists can contain different data types
nums = [1, 2, 3]
nums += ['a']
print(nums)
```

```python
# Lists can be 'sliced'
nums = [1, 2, 3, 4, 5]
print(nums[1:3])
```

The [built-in](https://docs.python.org/3/library/functions.html) function [`len(s)`](https://docs.python.org/3/library/functions.html#len) returns the length of, or number of items in, a sequence or collection `s`.  One excellent example use case is to find which of the words ['Llanfairpwllgwyngyllgogerychwyrndrobwllsantysiliogogogoch'](https://en.wikipedia.org/wiki/Llanfairpwllgwyngyll) and 'supercalifragilisticexpialidocious' is longer.

```python
len_llanfair = len('Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch')
len_supercali = len('supercalifragilisticexpialidocious')

print(len_llanfair)
print(len_llanfair / len_supercali)
```

As compound data types, [_tuples_](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences) and [_dictionaries_](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) are also frequently used.  Can you figure out what they do from the linked pages?  Feel free to make new code cells here to explore.

## Control Flow <a name="3."></a>

In the preceding example code snippets (the mathematical and string operations, and list manipulations), we programmed our commands to be executed line-by-line.  It would be fair to say that these top-to-bottom programmes are quite dull.  A programme may be made to exhibit a more complex [control flow](https://en.wikipedia.org/wiki/Control_flow>) by use of [_control flow statements_](https://docs.python.org/3/tutorial/controlflow.html).  


Python has two types of control flow statements - conditional statements and loop constructs.  Conditional statements (`if`, `elif`, `else`) are used to execute blocks of code only when certain conditions are met - Python only does the thing mentioned after the "if" statement if the "if" statement is correct, otherwise it doesn't do it.  Loop constructs are used to execute blocks of code some number of times (`for`) or while certain conditions are met (`while`).

### `if` Statements

```python
x = # Write an integer here
# Example conditional 'if' block
if x < 0: #Python checks if this is a true statement
    print('You entered a negative number!')
elif x == 0: #Short for 'else if', this condition is checked if the 'if' statement is false
    print('You entered zero')
else: #All other cases
    print('You entered a positive number')
```
Notice the whitespace (specifically, 4 spaces) in front of the code blocks after `if`, `elif` and `else`? We call this _indentation_, and it tells Python which lines of code should only be executed if the control flow statement is true. This has the advantage that the code becomes easily readable for humans. So, remember, indent = 4 times space bar.|

### `for` Statements

`for` statements in Python allow you to iterate over the items of any sequence (like a list or string) in order.

Notice again the _indentation_!

```python
# Measure some strings in a `for` loop
words = ['cat', 'window', 'defenestrate', 'quark']
for w in words:
    print(w, len(w))
```
In conjunction with `for` statements, the built-in [`range()`](https://docs.python.org/3/library/stdtypes.html#range) function is often useful.  It returns a range object, constructed by calling `range(stop)` or `range(start, stop[, step])`, that represents a sequence of numbers that goes from `start` (0 by default) to `stop` in steps of `step` (1 by default).

```python
# Example 'for' loop over a range that pushes items onto a list
items = []
for i in range(10):
    items.append(i) #.append() is another useful way to add something to the end of a python list
print(items)
```
