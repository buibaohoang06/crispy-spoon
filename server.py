from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')

@app.route('/create-ticket', methods=['GET', 'POST'])
def createTicket():
    if request.method == 'POST':
        content = request.args.get('content')
        position = request.args.get('position')
        time = request.args.get('time')
        name = request.args.get('name')
        if content and position:
            print(f"{content} {position} {time} {name}")
        else:
            pass
    return jsonify({
        "status": "success"
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="80")