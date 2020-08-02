import random
from tensorflow import keras
import numpy

#CHANGE ME:
changeScoreThreshold = 900

adjustedMoves = {'UP': ["LEFT", "UP", "RIGHT"], 'LEFT': ["DOWN", "LEFT", "UP"], 'RIGHT': ['UP', 'RIGHT', 'DOWN'], 'DOWN': ['RIGHT', 'DOWN', 'LEFT']} #0, 1, 2 become Left, Forward, Righ
moves = ["LEFT", "RIGHT", "DOWN", "UP"]
current_pool = []
total_models = 40
best_score = 0
scores = []

def createModel():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape = (2,3)),
        keras.layers.Dense(12, activation = 'relu'),
        keras.layers.Dense(3, activation = "softmax")
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def createInput(head, body, snack, rows, direction):
    input = []
    moves = adjustedMoves[direction] #Using current direction, make available moves the three directions (left, up, right)

    #Creates collision input
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

    #Direction towards food input
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
    foodInput[moveToFood] = 1

    input.append(collisionInput)
    input.append(foodInput)
    return input

def predict(model, input, direction):
    neurons = numpy.atleast_2d(numpy.asarray([input]))
    guess = model.predict(neurons).tolist()[0] #Predicts [Left, Forward, Right]
    move = adjustedMoves[direction][guess.index(max(guess))]
    return move

def selectMove(head, body, snack, rows, id1, direction):
    input = createInput(head,body,snack,rows,direction) #[Left, Forward, Right]
    if len(current_pool)<total_models: #Creates a model for every snake only if they don't exist
        model = createModel()
        current_pool.append(model)
    move = predict(current_pool[id1], input, direction)
    return move

def reproduce(parent1, parent2):
    global current_pool
    weight1 = current_pool[parent1].get_weights()
    weight2 = current_pool[parent2].get_weights()

    new_weight1 = weight1
    new_weight2 = weight2

    gene = random.randint(0, len(new_weight1) - 1)

    new_weight1[gene] = weight2[gene]
    new_weight2[gene] = weight1[gene]

    return numpy.asarray([new_weight1, new_weight2])

def mutate(weights, mutation):#,generation): for decaying mutation
    # mutate each models weights
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if( random.uniform(0,1) > mutation):
                change = random.uniform(-.5,.5)
                weights[i][j] += change
    return weights

def gameIsOver(snakes):
    global current_pool
    global best_score
    new_weights = []
    highScore = [0,0]
    secondHighScore = [0,0]

    #Determine highest and second highest scoring snake
    for s in snakes:
        s.score = s.length*50
        if s.score>highScore[0]:
            highScore = [s.score, snakes.index(s)]
        elif s.score>secondHighScore[0]:
            secondHighScore = [s.score, snakes.index(s)]
    scores.append(highScore[0])

    #If we got a good model, save it
    if highScore[0] > changeScoreThreshold:
        current_pool[highScore[1]].save(f"snakeScore{highScore[0]}.h5")

    #If we had a new high score, reproduce with the high scorers, otherwise mutate everything just a little
    if best_score<=highScore[0]:
        print("Reproduced using new high scorers")
        for babies in range(total_models // 2):
            cross_over_weights = reproduce(highScore[1], secondHighScore[1])
            mutated1 = mutate(cross_over_weights[0], .95)
            mutated2 = mutate(cross_over_weights[0], .85)
            new_weights.append(mutated1)
            new_weights.append(mutated2)
        for modelID in range(len(current_pool)):
            current_pool[modelID].set_weights(new_weights[modelID])
        best_score = highScore[0]
    else: #If there was no high score, just mutate at a higher rate
        for modelID in range(len(current_pool)):
            current_pool[modelID].set_weights(mutate(current_pool[modelID].get_weights(), .85))

    #in case of catastrophic failure, kill everything and start over
    if highScore[0] <= 200:
        current_pool = []
        best_score = 300
    print(f"Generation: {len(scores)}")
    print(f'Score History: {scores}')