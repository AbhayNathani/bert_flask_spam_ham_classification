from crypt import methods
from flask import Flask, render_template, redirect, request
import tensorflow_text as text
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.models import load_model
debug, port = True, 9000

app = Flask(__name__)

model = tf.keras.models.load_model(
    ("static/model_trained.h5"),
    custom_objects={'KerasLayer': hub.KerasLayer}
)
print("Model Loaded")


def predict(q):
    x = model.predict(q)[0][0]

    print("Query", q, round(x*100, 2))
    return f"Spam : {round(x*100,2)}%" if x > 0.5 else f"Ham : {round(x*100,2)}%"


@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""

    if request.method == 'POST':

        q_text = request.form['q_text']
        result = predict([q_text])

    return render_template('index.html', result=result)


@app.route('/history')
def history():
    return render_template('history.html')


# running app
if __name__ == '__main__':
    app.run(debug=debug, port=port)
