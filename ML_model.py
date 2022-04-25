import tensorflow as tf
from tensorflow import keras
import numpy as np

training_inputs = []
training_outputs = []
testing_inputs = []
testing_outputs = []
with open('stock_sentiment.txt', 'r') as ss_file:
    lines = ss_file.readlines()
    length = int(len(lines) * 0.8)
    for line in lines[1:]:
        line = line.split()
        if length > 0:
            training_inputs.append(float(line[1]))
            training_outputs.append(float(line[0]))
        else:
            testing_inputs.append(float(line[1]))
            testing_outputs.append(float(line[0]))
        length -= 1



training_inputs = np.array(training_inputs)
training_outputs = np.array(training_outputs)
testing_inputs = np.array(testing_inputs)
testing_outputs = np.array(testing_outputs)

    
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(1,)),
    keras.layers.Dense(5, activation=tf.nn.relu),
	keras.layers.Dense(10, activation=tf.nn.relu),
    keras.layers.Dense(1)
])

model.compile(optimizer='adam', 
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(training_inputs, training_outputs, epochs=10, batch_size=5)

test_loss, test_acc = model.evaluate(testing_inputs, testing_outputs)
print('Test accuracy:', test_acc)
model.save("model.h5")
print("Saved model to disk")
# a= np.array([[2000,3000],[4,5]])
# print(model.predict(a))


# train_data = np.array([[1.0,1.0]])
# train_targets = np.array([2.0])
# print(train_data)
# for i in range(3,10000,2):
#     train_data= np.append(train_data,[[i,i]],axis=0)
#     train_targets= np.append(train_targets,[i+i])
# test_data = np.array([[2.0,2.0]])
# test_targets = np.array([4.0])
# for i in range(4,8000,4):
#     test_data = np.append(test_data,[[i,i]],axis=0)
#     test_targets = np.append(test_targets,[i+i])