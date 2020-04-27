from bird import Bird
from random import randint

class Problem:
    def __init__(self):
        pass

    def get_best(self, group):
        flag = False
        ans = None
        for item in group:
            if not flag or item.score >= ans.score:
                flag = True
                ans = item
        return ans

    def generate_new_generation(self, best, size):
        ans = []

        br_x = best.random_x
        br_y = best.random_y

        for _ in range(int(size/2)):
            ans.append(Bird(randint(-5, 5), randint(-5, 5), randint(1, 3), randint(50, 150)))

        for _ in range(int(size/2)):
            ans.append(Bird(br_x + randint(-100, 100), br_y + randint(-100, 100), randint(1, 3), randint(50, 150)))

        return ans
