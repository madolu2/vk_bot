from dvach import Dvach

dvach = Dvach()

board = 'b'
num = 2
thread = dvach.get_thread(num, board)
# print(thread)
img = dvach.files_in_thread(thread)
print(img)
