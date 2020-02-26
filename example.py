from ttb.callback import TelegramBotCallback

# tensorflow와 tf.keras를 임포트합니다
import tensorflow as tf
from tensorflow import keras

token = "your token"
if token == "your token":
  print("read instructions in the https://github.com/Yeachan-Heo/Tensorflow-Telegram-Bot.git, you have to use your token")
# 헬퍼(helper) 라이브러리를 임포트합니다
import matplotlib.pyplot as plt

print(tf.__version__)

fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

train_images = train_images / 255.0

test_images = test_images / 255.0

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

if __name__ == "__main__":
    model.fit(train_images, train_labels, validation_data=(test_images, test_labels), epochs=1110, callbacks=[TelegramBotCallback(token)])
