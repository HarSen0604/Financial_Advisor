# Intelligent Financial Advisor and Optimizer
 
## Overview

The "Intelligent Financial Advisor and Optimizer" project aims to enhance financial empowerment, reduce stress, ensure long-term stability, and promote inclusivity through advanced technology solutions. This platform offers personalized financial advice, investment strategies, budget management, and more, tailored to improve users' overall quality of life.

## Key Features

### Payment Assessment through SMS
- Automatically tracks completed payments via SMS notifications for each transaction.

### Investment Tips
- Delivers personalized investment recommendations based on user profiles and financial goals.

### Investment Tracking
- Provides real-time tracking and analysis of investments to optimize portfolio management.

### Dynamic Monthly Budgeting
- Develops adaptive budget plans with real-time alerts and adjustments.

### Credit Score Tracking
- Monitors credit scores and offers strategies for improvement.

### Tax Tracking and Saving Tips
- Integrates tax tracking with personalized saving strategies.

### Cumulative Suggestim system
- Gets the suggestions both from the algorithm built into the application as well as from the LLM model by feeding the processed data.

## Tech Stack

- **Python**: Core programming language for backend logic, data analysis, and AI tasks.
- **Flask**: Lightweight web framework for building the platform's web interface and personalized profiles.
- **Generative AI**: Potential integration for natural language processing and dynamic budget planning using OpenAI.
- **HTML, CSS, and JS**: Frontend development for creating an intuitive user interface.

## Use Cases

### Small Business Owners
- Manage personal and business finances.
- Track expenses, investments, and improve credit scores.

### Retirees
- Efficiently manage retirement funds and monitor investments.
- Adjust budgets for retirement expenses and safeguard accounts.

### College Students
- Handle finances effectively with part-time earnings and student loans.
- Receive investment advice and prevent fraudulent activity.

### General Public
- Easily manage finances, track investments, and receive personalized financial tips.
- Monitor credit scores, prevent fraud, and optimize tax strategies.

## Execution Steps

Follow these steps to execute the project locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/HarSen0604/Financial_Advisor.git
   ```

2. **Navigate to the Repository**
   ```bash
   cd Financial_Advisor
   ```

3. **Edit Configuration Files**
   - Update `fb.py` to include your OpenAI API key.
   - Edit `index.js` to include Firebase database information.

4. **Run the Application**
   ```bash
   python fb.py
   ```

5. **Access the Application**
   - Open a web browser and navigate to `http://127.0.0.1:5000` or the link shown in the terminal.
