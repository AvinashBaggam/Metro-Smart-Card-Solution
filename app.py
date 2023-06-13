from flask import Flask, render_template, request

from models import SmartCard

app = Flask(__name__)

cards = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/purchase-card', methods=['GET', 'POST'])
def purchase_card():
    if request.method == 'POST':
        card_id = request.form['card_id']
        if card_id not in cards:
            default_balance = 100  # Set the default amount to be added to the card
            card = SmartCard(card_id, default_balance)
            cards[card_id] = card
            return "Card purchased successfully."
        else:
            return "Card already purchased."
    return render_template('purchase_card.html')


@app.route('/top-up/<card_id>', methods=['GET', 'POST'])
def top_up(card_id):
    card = cards.get(card_id)
    if card:
        if request.method == 'POST':
            amount = int(request.form['amount'])
            card.top_up(amount)
            return "Top-up successful."
        return render_template('top_up.html', card_id=card_id)
    return "Card not found."


@app.route('/fare-deduction/<card_id>', methods=['GET', 'POST'])
def fare_deduction(card_id):
    card = cards.get(card_id)
    if card:
        if request.method == 'POST':
            stations = int(request.form['stations'])
            fare = card.calculate_fare(stations)
            if fare <= card.balance:
                card.deduct_fare(fare)
                if card.balance < 0:
                    return "Insufficient balance."
                return "Fare deducted successfully."
            else:
                return "Insufficient balance."
        return render_template('fare_deduction.html', card_id=card_id)
    return "Card not found."


if __name__ == '__main__':
    app.run(debug=True)