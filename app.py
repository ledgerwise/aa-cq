from flask import Flask, jsonify, request
from main import accounts_by_number_of_holdings, accounts_by_time_of_holdings, accounts_by_attributes

app = Flask(__name__)


@app.route('/nft/number_of_holdings')
def number_of_holdings():
    """{collection_name, schema_name, minimum_holdings, template_id}"""
    data = request.args
    collection = data.get('collection_name')
    schema = data.get('schema_name')
    hold = data.get('minimum_holdings')
    template_id = data.get('template_id')
    holds = accounts_by_number_of_holdings(collection_name=collection, schema_name=schema, minimum_holding=int(hold),
                                           template_id=template_id)
    return jsonify(holds)

@app.route('/nft/attributes')
def attributes():
    """{collection_name, schema_name, number_of_days, template_id}"""
    data = request.args
    kwarg = {}
    for key, value in data.items():
        orig = ["collection_name", "schema_name"]
        if key not in orig:
            kwarg[key] = value
    collection = data.get('collection_name')
    schema = data.get('schema_name')
    holds = accounts_by_attributes(collection_name=collection, schema_name=schema, kwargs=kwarg)
    return jsonify(holds)

@app.route('/nft/time_of_holdings')
def time_of_holdings():
    """{collection_name, schema_name, number_of_days, template_id}"""
    data = request.args
    collection = data.get('collection_name')
    schema = data.get('schema_name')
    days = data.get('number_of_days')
    template_id = data.get('template_id')
    holds = accounts_by_time_of_holdings(collection_name=collection, schema_name=schema, template_id=template_id, number_of_days=days)
    return jsonify(holds)


if __name__ == '__main__':
    app.run(debug=True)
