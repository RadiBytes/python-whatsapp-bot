import queue

q = queue.Queue()

for i in range(9):
    q.put({i: f"data {i}"})

for i in range(4):
    print("hi", q.get())

while not q.empty():
    print(q.get())
