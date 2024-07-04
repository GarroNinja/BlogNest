from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        "author": "Rithvik A",
        "title": "Blog Post 1",
        "content": "First Post Content",
        "date_posted": "1 July, 2024"
    },
    {
        "author": "Garro",
        "title": "Blog Post 2",
        "content": "Second Post Content",
        "date_posted": "2 July, 2024"
    }
]
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)
@app.route("/about")
def about():
    return render_template("about.html", title='About')

if __name__ == '__main__':
    app.run(debug=True)
