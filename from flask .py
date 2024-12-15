from flask import Flask, request
import time

app = Flask(__name__)

# Simulated database
users = {}
loans = {}

@app.route('/ussd', methods=['POST'])
def ussd():
    session_id = request.form.get("sessionId")
    service_code = request.form.get("serviceCode")
    phone_number = request.form.get("phoneNumber")
    text = request.form.get("text", "")

    response = ""

    # Parse user input
    inputs = text.split("*")

    if text == "":
        response = "CON Welcome to SikaLoan.\n1. Register\n2. Get a Loan\n3. Loan Balance\n4. Notices"

    elif inputs[0] == "1":  # Register
        if len(inputs) == 1:
            response = "CON Enter your Ghana Card number:"
        elif len(inputs) == 2:
            response = "CON Enter your Voter's ID:"
        elif len(inputs) == 3:
            response = "CON Enter your full name:"
        elif len(inputs) == 4:
            response = "CON Enter your telephone number (must match registration name):"
        elif len(inputs) == 5:
            gh_card = inputs[1]
            voters_id = inputs[2]
            full_name = inputs[3]
            tel_number = inputs[4]

            # Validate phone number matches registration
            if tel_number != phone_number:
                response = "END The telephone number must match your registration number."
            else:
                # Save user data
                users[phone_number] = {
                    "ghana_card": gh_card,
                    "voters_id": voters_id,
                    "full_name": full_name,
                    "telephone": tel_number,
                }

                response = "END Congratulations, you have successfully registered with SikaLoan!"

    elif inputs[0] == "2":  # Get a Loan
        if phone_number not in users:
            response = "END You need to register first. Dial again and select option 1 to register."
        elif len(inputs) == 1:
            response = "CON Enter loan amount (100 - 3000 GHS):"
        elif len(inputs) == 2:
            try:
                loan_amount = int(inputs[1])
                if 100 <= loan_amount <= 3000:
                    response = "CON Choose payback duration:\n1. 3 months\n2. 6 months"
                else:
                    response = "END Invalid amount. Enter an amount between 100 and 3000 GHS."
            except ValueError:
                response = "END Invalid input. Please enter a numeric value for the loan amount."
        elif len(inputs) == 3:
            duration = "3 months" if inputs[2] == "1" else "6 months"
            loan_amount = int(inputs[1])

            # Save loan details
            loans[phone_number] = {
                "amount": loan_amount,
                "duration": duration,
                "date_taken": time.strftime("%Y-%m-%d"),
            }

            response = f"END Loan of {loan_amount} GHS approved for {duration}. Terms and conditions apply."

    elif inputs[0] == "3":  # Loan Balance
        if phone_number in loans:
            loan = loans[phone_number]
            response = f"END Loan Balance:\nAmount: {loan['amount']} GHS\nDuration: {loan['duration']}\nDate Taken: {loan['date_taken']}"
        else:
            response = "END You have no active loans."

    elif inputs[0] == "4":  # Notices
        if phone_number in loans:
            loan = loans[phone_number]
            response = f"END Notice:\nRepayment Deadline: {loan['duration']} from {loan['date_taken']}"
        else:
            response = "END You have no active loans."

    else:
        response = "END Invalid option."

    return response

if __name__ == "__main__":
    app.run(debug=True)
