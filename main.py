from math import gcd, log2

def reduction(x):
  h = gcd(x[0],x[1])
  p = x[0]//h
  q = x[1]//h
  return (p,q)

number = ["0","1","2","3","4","5","6","7","8","9"]
#number = ["0","1"]
base = len(number)
operator = ["+","-","*","/"]
letter = number + operator
letter_last_index = len(letter) -1

all_expression = []
normal_expression = []
all_answer = []
normal_answer = []

size = 8
#isPrint = True
isPrint = False

ReadFromFile = True
#ReadFromFile = False

if not ReadFromFile:
  total_case = 0
  for length in range(1, size-1):
    if isPrint: print("length:", length)

    #find all possible expression
    all_expression.append([])
    normal_expression.append([])
    all_answer.append([])
    normal_answer.append([])

    expression = []
    expression_index = []
    for i in range(0, length):
      expression_index.append(0)

    isEnd = False
    count = 0
    expression_last_index = len(expression_index) -1
    while True:
      count += 1
      if count%100000 == 0:
        print(count)

      #print(expression_index)
      total_case += 1

      #create the expression and reject some cases
      index = 0
      expression.clear()
      reject = False
      error_message = ""
      isNormal = True
      isAnswer = True
      while index <= expression_last_index:
        new_letter = letter[expression_index[index]]
        if len(expression) == 0:
          #reject the expression that start with "*" or "/"
          if new_letter == "*" or new_letter == "/":
            reject = True
            error_message = "(Start with operator " + new_letter + ")"
            break

        else:
          if expression[-1] == "+":
            #reject the expression that contain "+*" or "+/"
            if new_letter == "*" or new_letter == "/":
              reject = True
              error_message = "(Contain +" + new_letter + ")"
              break

            #convert "++" to "+"
            elif new_letter == "+":
              index += 1
              isNormal = False
              if error_message == "": error_message = "(Not normal: contain ++)"
              continue

            #convert "+-" to "-"
            elif new_letter == "-":
              expression[-1] = "-"
              index += 1
              isNormal = False
              if error_message == "": error_message = "(Not normal: contain +-)"
              continue

          elif expression[-1] == "-":
            #reject the expression that contain "-*" or "-/"
            if new_letter == "*" or new_letter == "/":
              reject = True
              error_message = "Contain -" + new_letter + ")"
              break

            #convert "-+" to "-"
            elif new_letter == "+":
              expression[-1] = "-"
              index += 1
              isNormal = False
              if error_message == "": error_message = "(Not normal: contain -+)"
              continue

            #convert "--" to "+"
            elif new_letter == "-":
              expression[-1] = "+"
              index += 1
              isNormal = False
              if error_message == "": error_message = "(Not normal: contain --)"
              continue

          elif expression[-1] == "*" or expression[-1] == "/":
            #reject the expression that contain "**" or "*/" or "/*" or "//"
            if new_letter == "*" or new_letter == "/":
              reject = True
              error_message = "(Contain " + expression[-1] + new_letter + ")"
              break

        expression.append(new_letter)
        index += 1

      if not reject:
        #reject the expression that end with "+" or "-" or "*" or "/"
        if expression[-1] == "+" or expression[-1] == "-" or expression[-1] == "*" or expression[-1] == "/":
          reject = True
          error_message = "(End with operator " + expression[-1] + ")"

      #calculate the expression
      if not reject:
        if isPrint: print(expression)

        #Convert number string to rational number
        reading_number = False
        i = 0
        while True:
          if expression[i] in number:
            if reading_number == False:
              expression[i] = (int(expression[i]), 1)
              reading_number = True

              #check whether 00000111
              if i <= len(expression)-2 and expression[i][0] == 0 and expression[i+1] in number:
                isNormal = False
                if error_message == "": error_message = "(Not normal: the leftmost digit is 0.)"

              i += 1
            else:
              expression[i-1] = (expression[i-1][0]*base + int(expression[i]), 1)
              del expression[i]
          else:
            reading_number = False
            i += 1

          if i == len(expression): break
        if isPrint: print("->", expression)

        #absorb the unary operator "+" and "-" into the rational number
        i = 0
        while True:
          if expression[i] == "+" or expression[i] == "-":
            if not (i >= 1 and expression[i-1] != "*" and expression[i-1] != "/"):
              if expression[i] == "+":
                isNormal = False
                if error_message == "": error_message = "(Not normal: non-negative integer has + sign.)"
              elif expression[i] == "-":
                expression[i+1] = (- expression[i+1][0], 1)
                if expression[i+1][0] == 0:
                  isNormal = False
                  if error_message == "": error_message = "(Not normal: -0)"
              del expression[i]

            else: i += 1

          else: i += 1

          if i == len(expression): break
        if isPrint: print("->", expression)

        #calculate "*" and "/"
        i = 0
        while True:
          if expression[i] == "*":
              expression[i-1] = (expression[i-1][0] * expression[i+1][0], expression[i-1][1] * expression[i+1][1])
              expression[i-1] = reduction(expression[i-1])
              del expression[i+1]
              del expression[i]

              isAnswer = False

          elif expression[i] == "/":
              if expression[i+1][0] == 0:
                reject = True
                error_message = "(Divided by zero.)"
                if isPrint: print(error_message)
                break

              expression[i-1] = (expression[i-1][0] * expression[i+1][1], expression[i-1][1] * expression[i+1][0])
              expression[i-1] = reduction(expression[i-1])
              del expression[i+1]
              del expression[i]

              isAnswer = False

          else: i += 1

          if i == len(expression): break

      #calculate the expression
      if not reject:
        if isPrint: print("->", expression)

        #calculate "+" and "-"
        i = 0
        while True:
          if expression[i] == "+":
              expression[i-1] = (expression[i-1][0] * expression[i+1][1] + expression[i+1][0] * expression[i-1][1], expression[i-1][1] * expression[i+1][1])
              expression[i-1] = reduction(expression[i-1])
              del expression[i+1]
              del expression[i]

              isAnswer = False

          elif expression[i] == "-":
              expression[i-1] = (expression[i-1][0] * expression[i+1][1] - expression[i+1][0] * expression[i-1][1], expression[i-1][1] * expression[i+1][1])
              expression[i-1] = reduction(expression[i-1])
              del expression[i+1]
              del expression[i]

              isAnswer = False

          else: i += 1

          if i == len(expression): break
        if isPrint: print("->", expression)

        if len(expression) != 1:
          Print("Error: the calculation cannot be done.")

        if expression[0][1] != 1:
          reject = True
          error_message = "(Answer is not an integer.)"
          if isPrint: print("Answer is not an integer: ", expression)

      #if True:
      if False:
        expression_original = ""
        for i in range(0,len(expression_index)):
          expression_original += letter[expression_index[i]]

        if not reject:
          print(expression_original, "=" , expression[0][0], error_message)
        else:
          #print(expression_original + " " + error_message)
          pass

      #Save all valid expression
      if not reject:
        expression_original = ""
        for i in range(0, len(expression_index)):
          expression_original += letter[expression_index[i]]

        all_expression[length-1].append((expression[0][0], expression_original))
        if isNormal: normal_expression[length-1].append((expression[0][0], expression_original))
        if isAnswer: all_answer[length-1].append((expression[0][0], expression_original))
        if isNormal and isAnswer: normal_answer[length-1].append((expression[0][0], expression_original))

      #find the next expression_index
      index = expression_last_index
      while True:
        if expression_index[index] != letter_last_index:
          expression_index[index] += 1

          index = index +1
          while index <= expression_last_index:
            expression_index[index] = 0
            index += 1

          break

        elif index == 0:
          isEnd = True
          break

        else: index -= 1

      if isEnd: break

  print("Total of case:", total_case)

  #sorting all_expression
  for i in range(0,len(all_expression)):
    all_expression[i].sort()
    normal_expression[i].sort()
    all_answer[i].sort()
    normal_answer[i].sort()

def create_index(origin, index):
  output = []
  if len(origin) != 0:
    output.append({"value": origin[0][0], "first": 0, "last": 0, "used": False})
    for i in range(0,len(origin)):
      if origin[i][0] == output[-1]["value"]:
        output[-1]["last"] = i
      else:
        output.append({"value": origin[i][0], "first": i, "last": i, "used": False})
  index.append(output)

if not ReadFromFile:
  #Create index for each list of expression
  all_expression_index = []
  normal_expression_index = []
  all_answer_index = []
  normal_answer_index = []

  for i in range(0,len(all_expression)):
    create_index(all_expression[i], all_expression_index)
    create_index(normal_expression[i], normal_expression_index)
    create_index(all_answer[i], all_answer_index)
    create_index(normal_answer[i], normal_answer_index)

  #print index
  #if True:
  if False:
    for i in range(0,len(all_expression)):
      print("length:", i+1)
      print("Index of all expression:")
      for j in range(0,len(all_expression_index[i])):
        print(all_expression_index[i][j])
      print("")

      print("Index of all answer:")
      for j in range(0,len(all_answer_index[i])):
        print(all_answer_index[i][j])
      print("")

      print("Index of normal expression:")
      for j in range(0,len(normal_expression_index[i])):
        print(normal_expression_index[i][j])
      print("")

      print("Index of normal answer:")
      for j in range(0,len(normal_answer_index[i])):
        print(normal_answer_index[i][j])
      print("")

#Create equality
def create_equality(expression, answer, length1, length2, equality):
  #if True:
  if False:
    print("first list")
    for i in range(0,len(expression)):
      print(expression[i])
    print("")

    print("second list")
    for i in range(0,len(answer)):
      print(answer[i])
    print("")

  if len(expression) == 0 or len(answer) == 0: return

  index1 = 0
  index2 = 0
  while True:
    if expression[index1]["value"] == answer[index2]["value"]:
      equality.append({"value": expression[index1]["value"], "length1": length1, "first1": expression[index1]["first"], "last1": expression[index1]["last"], "length2": length2, "first2": answer[index2]["first"], "last2": answer[index2]["last"]})

      expression[index1]["used"] = True
      answer[index2]["used"] = True

      index1 += 1
      index2 += 1
    elif expression[index1]["value"] > answer[index2]["value"]:
      index2 += 1
    elif expression[index1]["value"] < answer[index2]["value"]:
      index1 += 1

    if index1 == len(expression) or index2 == len(answer): break

if not ReadFromFile:
  all_equality = []
  normal_equality = []
  for i in range(0,len(all_expression)):
    create_equality(all_expression_index[i], all_answer_index[size-i-3], i+1, size-i-2, all_equality)
    create_equality(normal_expression_index[i], normal_answer_index[size-i-3], i+1, size-i-2, normal_equality)

  #rebuild expression
  new_expression = []
  for i in range(0,len(all_expression)):
    element = []
    for x in all_expression_index[i]:
      if x["used"]:
        for j in range(x["first"], x["last"]+1):
          element.append(all_expression[i][j])
    new_expression.append(element)
  all_expression = new_expression

  new_expression = []
  for i in range(0,len(all_expression)):
    element = []
    for x in normal_expression_index[i]:
      if x["used"]:
        for j in range(x["first"], x["last"]+1):
          element.append(normal_expression[i][j])
    new_expression.append(element)
  normal_expression = new_expression

  new_expression = []
  for i in range(0,len(all_expression)):
    element = []
    for x in all_answer_index[i]:
      if x["used"]:
        for j in range(x["first"], x["last"]+1):
          element.append(all_answer[i][j])
    new_expression.append(element)
  all_answer = new_expression

  new_expression = []
  for i in range(0,len(all_expression)):
    element = []
    for x in normal_answer_index[i]:
      if x["used"]:
        for j in range(x["first"], x["last"]+1):
          element.append(normal_answer[i][j])
    new_expression.append(element)
  normal_answer = new_expression

  #write to the files
  for i in range(0,len(all_expression)):
    filename = "data/expression/all_expression_" + str(i) + ".txt"
    with open(filename, "w") as f:
      for j in range(0,len(all_expression[i])):
        output = str(all_expression[i][j][0]) + " " + all_expression[i][j][1] + "\n"
        f.write(output)

    filename = "data/expression/normal_expression_" + str(i) + ".txt"
    with open(filename, "w") as f:
      for j in range(0,len(normal_expression[i])):
        output = str(normal_expression[i][j][0]) + " " + normal_expression[i][j][1] + "\n"
        f.write(output)

    filename = "data/expression/all_answer_" + str(i) + ".txt"
    with open(filename, "w") as f:
      for j in range(0,len(all_answer[i])):
        output = str(all_answer[i][j][0]) + " " + all_answer[i][j][1] + "\n"
        f.write(output)

    filename = "data/expression/normal_answer_" + str(i) + ".txt"
    with open(filename, "w") as f:
      for j in range(0,len(normal_answer[i])):
        output = str(normal_answer[i][j][0]) + " " + normal_answer[i][j][1] + "\n"
        f.write(output)

else:
  #Read the files
  for i in range(0,size-2):
    filename = "data/expression/all_expression_" + str(i) + ".txt"
    with open(filename) as f:
      x = []
      line = f.readline()
      while line:
        line = line.rstrip().split()
        x.append((int(line[0]),line[1]))
        line = f.readline()
      all_expression.append(x)

    filename = "data/expression/normal_expression_" + str(i) + ".txt"
    with open(filename) as f:
      x = []
      line = f.readline()
      while line:
        line = line.rstrip().split()
        x.append((int(line[0]),line[1]))
        line = f.readline()
      normal_expression.append(x)

    filename = "data/expression/all_answer_" + str(i) + ".txt"
    with open(filename) as f:
      x = []
      line = f.readline()
      while line:
        line = line.rstrip().split()
        x.append((int(line[0]),line[1]))
        line = f.readline()
      all_answer.append(x)

    filename = "data/expression/normal_answer_" + str(i) + ".txt"
    with open(filename) as f:
      x = []
      line = f.readline()
      while line:
        line = line.rstrip().split()
        x.append((int(line[0]),line[1]))
        line = f.readline()
      normal_answer.append(x)

#print expression
for i in range(0,len(all_expression)):
  #if True:
  if False:
    print("length:", i+1)
    print("All expression:")
    for j in range(0,len(all_expression[i])):
      print(all_expression[i][j])
    print("")

    print("All answer:")
    for j in range(0,len(all_answer[i])):
      print(all_answer[i][j])
    print("")

    print("Normal expression:")
    for j in range(0,len(normal_expression[i])):
      print(normal_expression[i][j])
    print("")

    print("Normal answer:")
    for j in range(0,len(normal_answer[i])):
      print(normal_answer[i][j])
    print("")

#rebuild index
all_expression_index = []
normal_expression_index = []
all_answer_index = []
normal_answer_index = []

for i in range(0,len(all_expression)):
  create_index(all_expression[i], all_expression_index)
  create_index(normal_expression[i], normal_expression_index)
  create_index(all_answer[i], all_answer_index)
  create_index(normal_answer[i], normal_answer_index)

#rebuild equality
all_equality = []
normal_equality = []
for i in range(0,len(all_expression)):
  create_equality(all_expression_index[i], all_answer_index[size-i-3], i+1, size-i-2, all_equality)
  create_equality(normal_expression_index[i], normal_answer_index[size-i-3], i+1, size-i-2, normal_equality)

def get_equality(expression, answer, equality):
  x = []
  length1 = equality["length1"] -1
  for index1 in range(equality["first1"],equality["last1"]+1):
    x.append(expression[length1][index1][1])

  y = []
  length2 = equality["length2"] -1
  for index2 in range(equality["first2"],equality["last2"]+1):
    y.append(answer[length2][index2][1])
  return (x,y)

#print equality
#if True:
if False:
  print("All equality:")
  for i in range(0,len(all_equality)):
    (x,y) = get_equality(all_expression, all_answer, all_equality[i])
    for left in x:
      for right in y:
        equality = left + "=" + right
        print(equality)
  print("")

  print("Normal equality:")
  for i in range(0,len(normal_equality)):
    (x,y) = get_equality(normal_expression, normal_answer, normal_equality[i])
    for left in x:
      for right in y:
        equality = left + "=" + right
        print(equality)
  print("")

answer_aux = []
colour_aux = []
for i in range(0,size):
  answer_aux.append("")
  colour_aux.append("")

def get_colour(guess, answer_original):
  for i in range(0,size):
    answer_aux[i] = answer_original[i]
    colour_aux[i] = ""

  #Fill Green
  for i in range(0,size):
    if guess[i] == answer_aux[i]:
      colour_aux[i] = "G"
      answer_aux[i] = ""

  #Fill Black and Purple
  for i in range(0,size):
    if colour_aux[i] == "G": continue

    if guess[i] not in answer_aux:
      colour_aux[i] = "B"
    else:
      colour_aux[i] = "P"
      index = answer_aux.index(guess[i])
      answer_aux[index] = ""

  output = ""
  for i in range(0, size):
    output += colour_aux[i]

  return output

Total_all_equality = 0
for i in range(0,len(all_equality)):
  (x_all, y_all) = get_equality(all_expression, all_answer, all_equality[i])
  Total_all_equality += len(x_all) * len(y_all)
print("Total of all equality:", Total_all_equality)

new_normal_equality = []
for i in range(0,len(normal_equality)):
  for index1_normal in range(normal_equality[i]["first1"], normal_equality[i]["last1"]+1):
    for index2_normal in range(normal_equality[i]["first2"], normal_equality[i]["last2"]+1):
      answer = normal_expression[normal_equality[i]["length1"] -1][index1_normal][1] + "=" + normal_answer[normal_equality[i]["length2"] -1][index2_normal][1]
      new_normal_equality.append(answer)
normal_equality = new_normal_equality

normal_equality_size = len(normal_equality)
print("Total of normal equality:", normal_equality_size)
print("Total information:", log2(normal_equality_size))
print("Total trial:", Total_all_equality*normal_equality_size)

entropy_record = []
entropy_record_size = 10

count = 0
for i in range(0,len(all_equality)):
  for index1_all in range(all_equality[i]["first1"], all_equality[i]["last1"]+1):
    for index2_all in range(all_equality[i]["first2"], all_equality[i]["last2"]+1):
      count += 1
      if count%10 == 0:
        for (colour, frequency) in entropy_record[0][2].items():
          print(colour, ':', frequency)
        print("count: ", count)
        for record in entropy_record:
          print(record[1], record[0])

      guess = all_expression[all_equality[i]["length1"] -1][index1_all][1] + "=" + all_answer[all_equality[i]["length2"] -1][index2_all][1]
      #print(guess)

      hist = {}
      for answer in normal_equality:
        colour = get_colour(guess, answer)
        #print(guess, answer, colour)

        #if colour not in hist: hist[colour] = []
        #hist[colour].append(answer)

        if colour not in hist: hist[colour] = 0
        hist[colour] += 1

      entropy = 0
      for (colour, frequency) in hist.items():
        #print(colour, ':', frequency))
        entropy += frequency/normal_equality_size * log2(normal_equality_size/frequency)

      #print("entropy:", entropy)
      if len(entropy_record) < entropy_record_size:
        entropy_record.append((entropy, guess, hist))
      elif len(entropy_record) == entropy_record_size:
        entropy_record.append((entropy, guess, hist))
        entropy_record.sort(reverse=True)
      else:
        if entropy > entropy_record[-1][0]:
          del entropy_record[-1]
          entropy_record.append((entropy, guess, hist))
          entropy_record.sort(reverse=True)

for (colour, frequency) in entropy_record[0][2].items():
  print(colour, ':', frequency)
for record in entropy_record:
  print(record[1], record[0])