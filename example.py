from tensorflow_chatbots.ttb.callback import TelegramBotCallback
# tensorflow와 tf.keras를 임포트합니다
import tensorflow as tf
from tensorflow import keras

token = "1045007850:AAEp0L3UN12EswG5O7cRzR7foZQmsuEXNHs"
if token == "your token":
  print("read instructions in the https://github.com/Yeachan-Heo/Tensorflow-Chatbots.git, you have to use your token")
# 헬퍼(helper) 라이브러리를 임포트합니다

print(tf.__version__)

fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

train_images = train_images / 255.0

test_images = test_images / 255.0

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

if __name__ == "__main__":
    model.fit(train_images, train_labels, validation_data=(test_images, test_labels), epochs=1100, callbacks=[TelegramBotCallback(token)])
