from tensorflow import keras
import numpy

adjustedMoves = {'UP': ["LEFT", "UP", "RIGHT"], 'LEFT': ["DOWN", "LEFT", "UP"], 'RIGHT': ['UP', 'RIGHT', 'DOWN'], 'DOWN': ['RIGHT', 'DOWN', 'LEFT']} #0, 1, 2 become Left, Forward, Righ
moves = ["LEFT", "RIGHT", "DOWN", "UP"]

def createInput(head, body, snack, rows, direction):
    moves = adjustedMoves[direction]
    input = []

    collisionInput = [] #INPUT IS [left, forward, right]
    for move in moves: #MAKES A COPY OF EACH MOVE TO SEE IF IT PUTS US IN DANGER
        head1 = list(head)
        if move=='LEFT':
            head1[0]-=1
        elif move == 'RIGHT':
            head1[0]+=1
        elif move == 'UP':
            head1[1]-=1
        elif move == 'DOWN':
            head1[1]+=1
        if tuple(head1) in [bod.pos for bod in body[:-1]] or 0 in head1 or rows-1 in head1:
            collisionInput.append(1)
        else:
            collisionInput.append(0)
    moveToFood = 0
    if snack[0]-head[0]>0:
        if "RIGHT" in adjustedMoves[direction]:
            moveToFood = adjustedMoves[direction].index("RIGHT")
    elif snack[0]-head[0]>0:
        if "LEFT" in adjustedMoves[direction]:
            moveToFood = adjustedMoves[direction].index("LEFT")
    if snack[1]-head[1]<0:
        if "UP" in adjustedMoves[direction]:
            moveToFood = adjustedMoves[direction].index("UP")
    elif snack[1]-head[1]>0:
        if "DOWN" in adjustedMoves[direction]:
            moveToFood = adjustedMoves[direction].index("DOWN")
    foodInput = [0,0,0]
    foodInput[moveToFood]=1

    input.append(collisionInput)
    input.append(foodInput)
    return input

def predict(model, input, direction):
    neurons = numpy.atleast_2d(numpy.asarray([input]))
    guess = model.predict(neurons).tolist()[0] #Predicts [Left, Forward, Right]
    move = adjustedMoves[direction][guess.index(max(guess))]
    return move

def selectMove(head, body, snack, rows, id1, direction): #variable id1 isn't necessary but is on the other script, so to avoid being forced to change the input every time just kept it here
    input = createInput(head,body,snack,rows,direction) #[Left, Forward, Right]
    model = keras.models.load_model('snakeScore900.h5')
    move = predict(model, input, direction)
    return move