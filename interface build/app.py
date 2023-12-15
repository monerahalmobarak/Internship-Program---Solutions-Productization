from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Database configuration 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/sqldatabase'

@app.route('/')
def index():
    # Render the HTML form to update prices.
    return render_template('update.html')

@app.route('/update_price', methods=['GET', 'POST'])
def update_price():
    if request.method == 'POST':
        # Extract data from form submission.
        old_date = request.form.get('old_date')
        old_area_product = request.form.get('old_area_product')
        old_price = request.form.get('old_price') 
        new_date = request.form.get('new_date')
        new_area_product = request.form.get('new_area_product')
        new_price = request.form.get('new_price')

        # Validate that none of the fields are empty.
        if not all([old_date, old_area_product, new_date, new_area_product, new_price]):
            return jsonify({'error': 'Missing data'}), 400

        try:
            # Create a new database engine.
            engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

            # Define the SQL UPDATE statement without considering old_price.
            update_query = text("""
                UPDATE oil_prices
                SET "Date" = :new_date, 
                    "Area/Product" = :new_area_product, 
                    "Price" = :new_price
                WHERE "Date" = :old_date AND "Area/Product" = :old_area_product
            """)

            # Execute the update operation.
            with engine.connect() as connection:
                result = connection.execute(update_query, {
                    'new_date': new_date,
                    'new_area_product': new_area_product,
                    'new_price': new_price,
                    'old_date': old_date,
                    'old_area_product': old_area_product
                })

            # Check if any row was updated.
            if result.rowcount == 0:
                return jsonify({'message': 'No record updated'}), 404

            # If the update was successful, send a confirmation message.
            return jsonify({'message': 'Record updated successfully'}), 200

        except Exception as e:
            # If an error occurs, return the error message.
            return jsonify({'error': str(e)}), 500
    else:
        # Render the HTML form for update_price on GET request.
        return render_template('update.html')

if __name__ == '__main__':
    # Run the Flask application.
    app.run(debug=True)
