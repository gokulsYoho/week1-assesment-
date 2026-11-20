import numpy as np

# 4 students x 3 subjects marks
marks = np.array([ 
(85, 90, 78),
(65,70, 72),
(88, 92, 85), 
(70, 68, 74)
])

print("Shape:", marks.shape)
print("Student averages:", np.round(marks.mean(axis=1), 2))
print("Subject averages:", np.round(marks.mean(axis=0), 2))

# add 5 grace marks using broadcasting
grace_marks = marks + 5
print("With grace marks:\n", grace_marks)

# weighted scores using np.dot
weights = np.array([0.3, 0.3, 0.4])
weighted = np.dot(marks, weights)
print("Weighted scores:", np.round(weighted, 2))