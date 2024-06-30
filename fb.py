from flask import Flask, render_template, request, redirect, url_for
from firebase import firebase
from openai import OpenAI

app = Flask(__name__)

global expenditure
global risk_tolerance
global experience_level
global assets
global liabilities
global time_horizon
global loss_reaction
global allocation_percentage
global volatility_comfort
global budgeting_plan

global essentials_budget
global non_essentials_budget
global savings_budget
global debt_budget
global available_budget
global net_worth
global investment_options

api_key = "YOUR_OPENAI_API_KEY"
client = OpenAI(api_key=api_key)
income = 0
expenditure = 0
risk_tolerance = ""
experience_level = ""
assets = 0
liabilities = 0
time_horizon = 0
loss_reaction = 0
allocation_percentage = 0
volatility_comfort = 0
budgeting_plan = 0
financial_goals = ""

#OUTPUT global variables
gpt_response = 'Yet to be generated'
essentials_budget = 0
non_essentials_budget = 0
savings_budget = 0
debt_budget = 0
available_budget = 0
net_worth = 0
investment_options = []

#MISSCELLANEOUS global variables
username = ""
password = ""
dob = ""
name = ""
phone = 0
email = ""
placeOfLiving = ""

def extract(s):
  l = s.splitlines()
  expenses = 0
  for i in l:  # each message pasted is considered as a single string , where seperations between messages is \n
    #Expense Messages will only be of two forms
    if (
        "DEBITED" in i
    ):  # message is of form "An amount of INR 365.00 has been DEBITED to your account XXXXXXXX on ........ Total Avail.bal INR ..... - Bank"
      endpos = i.index("has")
      startpos = i.index(
          "INR"
      )  # will find find occurence of INR , so second occurence of INR will not be mistook
      expenses = expenses + float(i[startpos + 3:endpos])
    if (
        "paid" in i
    ):  # message is of form "Rs.500 paid thru A/C XXXXX on ...... to ......., UPI Ref ........... If not done SMS BLOCKUPI to 324324234. - Bank"
      endpos = i.index("paid")
      startpos = i.index("Rs")
      expenses = expenses + float(i[startpos + 3:endpos])
  return expenses


#example^
#messages ="An amount of INR 365.00 has been DEBITED to your account XXXXXXXX on 2023-10-01. Total Avail.bal INR 1000.00 - Bank\nRs.500 paid thru A/C XXXXX on 2023-10-02 to John Doe, UPI Ref 123456. If not done SMS BLOCKUPI to 324324234. - Bank"


def budget_and_invest():
  global income
  print("INSIDE ALGO")
  # Check if the income is within a valid range
  if income < 0:
    return "Invalid income input. Please provide a positive income."

  # Calculate the budget allocations based on the specified plan

  global expenditure
  global risk_tolerance
  global experience_level
  global assets
  global liabilities
  global time_horizon
  global loss_reaction
  global allocation_percentage
  global volatility_comfort
  global budgeting_plan

  global essentials_budget
  global non_essentials_budget
  global savings_budget
  global debt_budget
  global available_budget
  global net_worth
  global investment_options

  if budgeting_plan == "50-30-20":
    essentials_budget = 0.5 * income
    non_essentials_budget = 0.3 * income

    savings_budget = 0.2 * income
    if savings_budget <= 0: savings_budget = 1

  elif budgeting_plan == "50-30-15-5":
    essentials_budget = 0.5 * income
    non_essentials_budget = 0.3 * income
    savings_budget = 0.15 * income
    debt_budget = 0.05 * income
  elif budgeting_plan == "Zero-Based Budgeting":
    # In Zero-Based Budgeting, user specifies expenses, so no predefined allocations following is dummy formula
    essentials_budget = 0.5 * income
    non_essentials_budget = 0.3 * income

    savings_budget = 0.2 * income
    if savings_budget <= 0: savings_budget = 1
  elif budgeting_plan == "Debt Avalanche":
    # In Debt Avalanche, user specifies debt payments, so no predefined allocations the following is dummy formula
    essentials_budget = 0.5 * income
    non_essentials_budget = 0.3 * income
    savings_budget = 0.15 * income
    debt_budget = 0.05 * income

  # Calculate the available budget after accounting for expenditures and debt payments
  available_budget = income - expenditure - debt_budget

  # Calculate the net worth (assets - liabilities)
  net_worth = assets - liabilities

  if essentials_budget <= 0: essentials_budget = 1
  if non_essentials_budget <= 0: non_essentials_budget = 1
  if savings_budget <= 0: savings_budget = 1
  if debt_budget <= 0: debt_budget = 1
  if available_budget <= 0: available_budget = 1
  if net_worth <= 0: net_worth = 1

  # Determine investment suggestions based on user responses, risk tolerance, budgeting details, risk category, and experience category
  if risk_tolerance == "Very Low":
    investment_options = ["Savings Account", "Certificate of Deposit (CD)"]
    print(investment_options)
  elif risk_tolerance == "Low":
    if experience_level == "Beginner":
      investment_options = ["Savings Account", "Certificate of Deposit (CD)"]
    elif experience_level == "Intermediate":
      if time_horizon >= 3 and loss_reaction >= 3 and allocation_percentage >= 10 and volatility_comfort >= 3:
        investment_options = ["Mutual Funds", "ETFs", "Bonds", "Stocks"]
      else:
        investment_options = ["Mutual Funds", "ETFs", "Bonds"]
    elif experience_level == "Advanced":
      investment_options = ["Mutual Funds", "ETFs", "Bonds", "Stocks"]
  elif risk_tolerance == "Medium":
    if experience_level == "Beginner":
      investment_options = ["Savings Account", "Certificate of Deposit (CD)"]
    elif experience_level == "Intermediate":
      investment_options = ["Mutual Funds", "ETFs", "Bonds", "Stocks"]
    elif experience_level == "Advanced":
      investment_options = ["Mutual Funds", "ETFs", "Bonds", "Stocks"]
  elif risk_tolerance == "High":
    if experience_level == "Beginner":
      investment_options = ["Savings Account", "Certificate of Deposit (CD)"]
    elif experience_level == "Intermediate":
      investment_options = ["Mutual Funds", "ETFs", "Bonds", "Stocks"]
    elif experience_level == "Advanced":
      if allocation_percentage >= 20:
        investment_options = ["Stocks", "Real Estate", "Cryptocurrencies"]
      else:
        investment_options = ["Mutual Funds", "ETFs", "Bonds", "Stocks"]
  elif risk_tolerance == "Very High":
    if experience_level == "Beginner":
      investment_options = ["Savings Account", "Certificate of Deposit (CD)"]
    elif experience_level == "Intermediate":
      investment_options = ["Stocks", "Real Estate"]
    elif experience_level == "Advanced":
      investment_options = ["Stocks", "Real Estate", "Cryptocurrencies"]

# Initialize Firebase
firebase_config = {
    'apiKey': "AIzaSyDwItPgW1h8_oNucAhbFWokvGnd-LyVjx8",
    'authDomain': "app-review-7b0be.firebaseapp.com",
    'projectId': "app-review-7b0be",
    'storageBucket': "app-review-7b0be.appspot.com",
    'messagingSenderId': "898521022978",
    'appId': "1:898521022978:web:38eb004f3cc0d81ba11d1b",
    'measurementId': "G-94WGSYLXDP",
}

firebase_db_url = 'https://app-review-7b0be-default-rtdb.firebaseio.com/'

firebase_app = firebase.FirebaseApplication(firebase_db_url, None)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetching form data
        entered_username = request.form.get('username-input')
        entered_password = request.form.get('password-input')

        # Retrieve user data from Firebase based on the entered username
        user_data = firebase_app.get('/user_data', None)

        # Check if the entered username exists in Firebase
        if user_data and any(data.get('Email') == entered_username for data in user_data.values()):
            # Find the user data based on the entered username
            user_data_match = next(data for data in user_data.values() if data.get('Email') == entered_username)

            # Check if the entered password matches the stored password
            if user_data_match['Password'] == entered_password:
                # Authentication successful
                return redirect('/dashboard')
            else:
                # Password incorrect, redirect to login page
                return redirect(url_for('index'))
        else:
            # Username not found, redirect to login page
            return redirect(url_for('index'))

    # Render the login page
    return render_template('IICpage1.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        global gpt_response

        global name
        name = request.form.get('sample2')

        global email
        email = request.form.get('sample6')

        global phone
        phone = request.form.get('sample3')

        global password
        password = request.form.get('sample4')

        global dob
        dob = request.form.get('sample1')

        global placeOfLiving
        placeOfLiving = request.form.get('sample7')

        global experience_level
        exp = request.form.get('sample5')
        if (exp == "2"):
            experience_level = "Intermediate"
        elif (exp == "3"):
            experience_level = "Advanced"
        else:
            experience_level = "Beginner"
        
        global expenditure
        expense = request.form.get('expense-details')
        expenditure = int(extract(expense))
        
        global income
        temp_income = request.form.get('financial-goals')
        income = int(temp_income)

        global assets
        global liabilities
        temp = request.form.get('assets-liabilities')
        tt = temp.split(" ")
        assets = int(tt[0])
        liabilities = int(tt[1])
        
        global financial_goals
        financial_goals = request.form.get('income-details')

        # Access checkbox data
        global risk_tolerance
        c1 = request.form.get('list-checkbox-very-low')
        c2 = request.form.get('list-checkbox-low')
        c3 = request.form.get('list-checkbox-medium')
        c4 = request.form.get('list-checkbox-high')
        c5 = request.form.get('list-checkbox-very-high')
        if (c1 == "on"):
            risk_tolerance = "Very Low"
        elif (c2 == "on"):
            risk_tolerance = "Low"
        elif (c3 == "on"):
            risk_tolerance = "Medium"
        elif (c4 == "on"):
            risk_tolerance = "High"
        elif (c5 == "on"):
            risk_tolerance = "Very High"

        # Push data to Firebase
        data = {
            'Name': name,
            'Email': email,
            'Phone': phone,
            'Password': password,
            'DateOfBirth': dob,
            'Location': placeOfLiving,
            'InvestmentExperience': exp,
            'ExpenseDetails': expenditure,
            'IncomeDetails': income,
            'AssetsLiabilities': temp,
            'FinancialGoals': financial_goals,
            'RiskTolerance': risk_tolerance,
        }

        result = firebase_app.post('/user_data', data)
        print(result)
        return redirect(url_for('dashboard'))

    return render_template('IICpage2.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global target_budget
    if request.method == 'POST':
        tb = request.form.get('sample3')
        target_budget=int(tb)
        print(target_budget)
    return render_template('IICpage4.html',
                         essentials_budget=essentials_budget,
                         non_essentials_budget=non_essentials_budget,
                         savings_budget=savings_budget,
                         debt_budget=debt_budget,
                         available_budget=available_budget,
                         net_worth=net_worth,
                         investment_options=investment_options,
                        gpt_response=gpt_response)

@app.route('/budget_plan', methods=['GET', 'POST'])
def budget_plan():
    global budgeting_plan
    if request.method == 'POST':
        # Retrieve data from radiobuttons
        r = request.form.get('options')
        print("Radio Button selected:", r)
        if (r == "one"):
            budgeting_plan = "50-30-20"
            print(budgeting_plan)
        elif (r == "two"):
            budgeting_plan = "50-30-15-5"
        elif (r == "three"):
            budgeting_plan = "Zero-Based Budgeting"
        elif (r == "four"):
            budgeting_plan = "Debt Avalanche"
        return redirect(url_for('dashboard'))
    return render_template('IICpage5.html')

@app.route('/risk_sense', methods=['GET', 'POST'])
def risk_sense():
    if request.method == 'POST':
        # Retrieve form data
        list_checkbox_1 = request.form.get('list-checkbox-1')
        list_checkbox_2 = request.form.get('list-checkbox-2')
        list_checkbox_3 = request.form.get('list-checkbox-3')
        list_checkbox_4 = request.form.get('list-checkbox-4')
        list_checkbox_5 = request.form.get('list-checkbox-5')

        loss_reaction = None

        if list_checkbox_1 == 'on':
            loss_reaction = 1
        elif list_checkbox_2 == 'on':
            loss_reaction = 2
        elif list_checkbox_3 == 'on':
            loss_reaction = 3
        elif list_checkbox_4 == 'on':
            loss_reaction = 4
        elif list_checkbox_5 == 'on':
            loss_reaction = 5
        
        print("Loss Reaction: " + str(loss_reaction))

        risk_slider = request.form.get('risk-slider')
        allocation_percentage = int(risk_slider)
        print("Risk Slider: " + str(risk_slider))

        scale_very_low = request.form.get('list-checkbox-very-low')
        scale_low = request.form.get('list-checkbox-low')
        scale_medium = request.form.get('list-checkbox-medium')
        scale_high = request.form.get('list-checkbox-high')
        scale_very_high = request.form.get('list-checkbox-very-high')

        volatility_comfort = None

        if scale_very_low == 'on':
            volatility_comfort = 1
        elif scale_low == 'on':
            volatility_comfort = 2
        elif scale_medium == 'on':
            volatility_comfort = 3
        elif scale_high == 'on':
            volatility_comfort = 4
        elif scale_very_high == 'on':
            volatility_comfort = 5

        print("Volatility Comfort: " + str(volatility_comfort))

        list_checkbox_less_than_1_year = request.form.get('list-checkbox-less_than_1_year')
        list_checkbox_1_3_years = request.form.get('list-checkbox-1-3-years')
        list_checkbox_3_5_years = request.form.get('list-checkbox-3-5-years')
        list_checkbox_5years = request.form.get('list-checkbox-5years')

        time_horizon = None

        if list_checkbox_less_than_1_year == 'on':
            time_horizon = 1
        elif list_checkbox_1_3_years == 'on':
            time_horizon = 2
        elif list_checkbox_3_5_years == 'on':
            time_horizon = 3
        elif list_checkbox_5years == 'on':
            time_horizon = 4
        
        print("Time Horizon: " + str(time_horizon))

        budget_and_invest()

        prompt = f"""You are an investment broker with a client who has the following financial profile:
        - Income: ${income}
        - Expenditure: ${expenditure}
        - Risk Tolerance: {risk_tolerance}
        - Experience Level: {experience_level}
        - Assets: ${assets}
        - Liabilities: ${liabilities}

        Based on this information, recommend the most optimal investment plan for the client and provide a one-liner explaining the reason for your recommendation. Keep the response concise and appealing.
        """

        response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
            model="gpt-3.5-turbo",
            max_tokens=100,
            temperature=0.3,
            top_p=0.5
        )
        global gpt_response
        gpt_response = response.choices[0].message.content
        print("FINALLLLLL")
        print(gpt_response)
        print(essentials_budget, non_essentials_budget, savings_budget,
            debt_budget, available_budget, net_worth, investment_options)

        return render_template('IICpage4.html',
                         essentials_budget=essentials_budget,
                         non_essentials_budget=non_essentials_budget,
                         savings_budget=savings_budget,
                         debt_budget=debt_budget,
                         available_budget=available_budget,
                         net_worth=net_worth,
                         investment_options=investment_options,
                        gpt_response=gpt_response)
    return render_template('IICpage7.html', username="")

@app.route('/cibil_score', methods=['GET', 'POST'])
def cibil_score():
    # You can add any necessary logic here before rendering the template
    return render_template('IICpage8.html', username="")

if __name__ == '__main__':
    app.run(debug=True)
