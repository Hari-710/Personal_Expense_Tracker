📊 Personal Expenses Tracker

A Streamlit-based web application that helps users track their monthly budgets and expenses, visualize spending habits with interactive charts, and manage personal finances effectively.

✨ Features

✅ User Authentication – Register & login securely
✅ Set Monthly Budget – Allocate a budget for each month
✅ Add Expenses – Record expenses with category, amount, date, and payment mode
✅ View Budgets & Expenses – See your monthly budgets and spending history
✅ Interactive Visualizations –

📌 Pie Chart – Category-wise spending percentage

📌 Bar Chart – Payment mode comparison

📌 Top Categories – Highest spending categories

📌 Monthly Trends – Expense growth/decline trends

📌 Category Growth % – Month-over-month category growth/decline
✅ Download Reports – Export monthly reports in CSV format
✅ Delete Expenses – Manage and remove old records

🛠️ Tech Stack

Frontend/UI – Streamlit

Backend/Database – MySQL

Password Security – bcrypt

Data Analysis – pandas, matplotlib

📂 Project Structure
personal-expenses-tracker/
│── app.py             # Main Streamlit app
│── db.py              # Database operations (MySQL queries)
│── requirements.txt   # Project dependencies
│── README.md          # Documentation
│── .streamlit/
    │── config.toml  

⚡ Installation & Setup

### Clone the repository

git clone https://github.com/<your-username>/personal-expenses-tracker.git
cd personal-expenses-tracker


### Install dependencies

pip install -r requirements.txt


### Set up MySQL database
### Run the following SQL in MySQL:

CREATE DATABASE expenses;

USE expenses;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE Budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    month VARCHAR(10),
    amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE,
    category VARCHAR(50),
    amount DECIMAL(10,2),
    payment_mode VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

### Run the application

streamlit run app.py

🚀 Future Enhancements

✅ Add expense forecasting with ML

✅ Integrate email alerts when crossing budget limits

✅ Deploy the app on Streamlit Cloud / Render

👨‍💻 Author

Harish J – Aspiring Data Analyst | Passionate about Data Analytics

🔗 LinkedIn - www.linkedin.com/in/harish-j-056022277  | GitHub - https://github.com/Hari-710

