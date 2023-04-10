from new_row import Row
from new_place import NewPlace
from old_place import OldPlace

# r = NewPlace(2)
# r.insert(1, 2)
# r.insert(2, 3)
# # r.delete(1)
# # f_id = r.search(1)
# r.insert(3, 1)
# # f_id = r.search(1)
# r.insert(4, 1)
# r.insert(6, 3)
# r.delete(3)
# r.delete(1)
# r.insert(5, 10)
# r.insert(7, 3)
# r.display()
r = Row(1)
f_id = r.search(5)
r.insert(5, 5, f_id[0])
r.generate_module_image()

# s = OldPlace(4)
# s.insert(1, 3)
# s.insert(2, 4)
# s.insert(3, 5)
# s.delete(2)
# s.display()