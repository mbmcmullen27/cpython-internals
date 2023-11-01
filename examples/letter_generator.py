def letters():
  i = 97 # letter 'a' in ascii
  end = 97 + 26
  while i < end:
    yield chr(i)
    i +=1

# >>> from letter_generator import letters
# >>> for letter in letters():
# ...   print(letter)
# ... 
# a
# b
# c
# d
# e
# f
# ...