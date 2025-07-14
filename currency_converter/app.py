from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount'))
            from_currency = request.form.get('from_currency')
            to_currency = request.form.get('to_currency')

            url = f"https://open.er-api.com/v6/latest/{from_currency}"
            response = requests.get(url, timeout=5)
            data = response.json()

            print("API Data:", data)

            if data.get("result") == "success":
                rates = data.get("rates", {})
                if to_currency in rates:
                    converted = round(amount * rates[to_currency], 2)
                    result = f"{amount} {from_currency} = {converted} {to_currency}"
                else:
                    result = "❌ Target currency not found."
            else:
                result = "❌ Conversion failed. Try again!"
        except Exception as e:
            result = f"⚠️ Error: {str(e)}"

    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
