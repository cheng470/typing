import random
import time

WIDTH = 640
HEIGHT = 400
WHITE_COLOR = (255, 255, 255)
MAX_NUM = 5

balloons = []
balloon_typed = [] # 表示已经命中的气球
score = 0
start_time = time.perf_counter() # 记录游戏开始的时间，返回以秒为单位的小数
left_time = 60 # 游戏时间为60秒
win = False
lost = False

def check_gameover():
    global win, lost
    if score >= 100:
        sounds.win.play()
        win = True
    if left_time <= 0:
        sounds.fail.play()
        lost = True

def count_time():
    global left_time
    if win or lost:
        return
    play_time = int(time.perf_counter()-start_time)
    left_time = 60 - play_time

def add_balloon():
    balloon = Actor("typing_balloon", (WIDTH//2, HEIGHT))
    balloon.char = random_char()
    balloon.x = random_location()
    balloon.vy = random_velocity() # 气球垂直上升的速度
    balloon.typed = False # 表示是否被命中
    balloons.append(balloon)

def update_balloon():
    for balloon in balloons:
        balloon.y += balloon.vy
        if balloon.bottom < 0:
            balloons.remove(balloon)

def random_char():
    charset = set()
    for b in balloons:
        charset.add(b.char)
    ch = chr(random.randint(65, 90))
    while ch in charset:
        ch = chr(random.randint(65, 90))
    return ch

# 随机x坐标，并且要防止和其他气球重叠
def random_location():
    min_dx = 0
    while min_dx < 50:
        min_dx = WIDTH
        x = random.randint(20, WIDTH-20)
        for balloon in balloons:
            dx = abs(balloon.x - x)
            min_dx = min(min_dx, dx)
    return x

def random_velocity():
    n = random.randint(1, 100)
    if n <= 1:
        return -5
    if n <= 4:
        return -4
    if n <= 20:
        return -3
    if n <= 40:
        return -2
    return -1

def remove_balloon():
    sounds.eat.play()
    b = balloon_typed.pop(0)
    if b in balloons:
        balloons.remove(b)

def draw():
    screen.fill(WHITE_COLOR)
    screen.draw.text("Score: " + str(score), bottomleft=(10, HEIGHT-10), color="black")
    screen.draw.text("Time: " + str(left_time), bottomleft=(WIDTH-80, HEIGHT-10), color="black")
    for balloon in balloons:
        balloon.draw()
        if balloon.typed:
            screen.draw.text(balloon.char, center=balloon.center, color="white")
        else:
            screen.draw.text(balloon.char, center=balloon.center, color="black")
    if win:
        screen.draw.text("You Win!", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="red")
    elif lost:
        screen.draw.text("You Lost!", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="red")


def update():
    if len(balloons) < MAX_NUM:
        add_balloon()
    update_balloon()
    check_gameover()
    count_time()

def on_key_down(key):
    global score
    if key < 97 or key > 122:
        return
    char = chr(key-32)
    print("on key down", str(key), char)
    for b in balloons:
        if char == b.char:
            b.typed = True
            balloon_typed.append(b)
            score += 1
            clock.schedule(remove_balloon, 0.3)
            break

