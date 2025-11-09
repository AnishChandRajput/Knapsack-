from flask import Flask, render_template, request

app = Flask(__name__)

def knapsack(weights, values, capacity):
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Build DP table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    # Trace selected items
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i)
            w -= weights[i - 1]

    selected_items.reverse()
    return dp[n][capacity], selected_items


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    selected = []
    if request.method == "POST":
        try:
            values = list(map(int, request.form["values"].split(",")))
            weights = list(map(int, request.form["weights"].split(",")))
            capacity = int(request.form["capacity"])

            max_profit, selected = knapsack(weights, values, capacity)
            result = f"Maximum Profit: {max_profit}"
        except:
            result = "⚠️ Please enter valid numbers separated by commas."

    return render_template("index.html", result=result, selected=selected)

if __name__ == "__main__":
    app.run(debug=True)
