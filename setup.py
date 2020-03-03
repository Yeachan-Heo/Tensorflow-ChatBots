from setuptools import setup

setup(
    name='Tensorflow-ChatBots',
    version='0.0.10',
    packages=['tensorflow_chatbots', 'tensorflow_chatbots.tsb', 'tensorflow_chatbots.ttb',
              'tensorflow_chatbots.variableholder'],
    url='https://github.com/Yeachan-Heo/Tensorflow-ChatBots',
    license='MIT',
    author='Yeachan-Heo',
    author_email='hurrc04@gmail.com',
    description='ChatBots supporting TensorFlow', install_requires=['tensorflow', 'gym', 'numpy', 'numba', 'matplotlib',
                                                                    'slacker', "python-telegram-bot"]
)
