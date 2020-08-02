# SnakeAI
## Introduction
Using a pre-build, open-source, but heavily modified game of Snake found on TechWithTim's website, I created a neural network to predict the best move that is trained through intensive training with a genetic algorithm.
## Training
To train the network, simply run the main script (game.py) and set train_snakes at the top to True. You can tinker with the population by changing the variable numOfSnakes.
While training, multiple snakes will run at the same time, which may be a little confusing. Each snake will have a randomized color, and each snake will have its own color-coded food as well. It will look as follows:

 ![Example](https://im7.ezgif.com/tmp/ezgif-7-c80d6908d33b.gif)
 
 After running the program for a while, once the network runs a snake that exceeds a certain score (easily adjustable using the changeScoreThreshold variable at the top of neuralnetwork.py), the program will save a copy of the best performing model. Although the program will continue, you can quit at any time, and your best model will have been saved. 
## Using high-performing models
 To test certain models, change the train_snakes variable at the top of game.py to False. In usemodel.py, simply change the bestModel variable to the name of the model you want to use. This will allow you to run just a single snake on your favorite model!
 
  ![Example](https://im7.ezgif.com/tmp/ezgif-7-484d462b6531.gif)
