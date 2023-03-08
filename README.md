## About the project
<hr>

My first dive into artificial intelligence starts simple with a path-finding snake 
game. I utilize breath first search to locate the quickest path from the snake to 
the apple, and depth first search to coil the snake and locate the end of its tail. 

### Built with

I use Carnegie Mellon's `cmu_graphics` library to draw my objects. 

### Installation

```
git clone https://github.com/MartinJ45/autoSnake.git 
pip install -r requirements.txt
```


## How to play
<hr>

### Controls

+ `SPACE` to pause the game <br>
- `SHIFT` + `P` to take control of the snake <br>
  + When in control, use `WASD` to move
+ `SHIFT` + `G` to enable and disable grid
- `LEFT` and `RIGHT` arrow keys to decrease and increase game speed
+ `SHIFT` + `I` to print out important information <br>
- `SHIFT` + `E` to end the game <br>

At the end of every game an `appleSeed` will print out if you wish to replicate the 
same game. 
