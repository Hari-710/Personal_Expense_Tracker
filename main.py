import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from decimal import Decimal
import time
import db


st.set_page_config("Personal Expenses Tracker", layout="wide", page_icon="https://img.icons8.com/?size=100&id=eYaVJ9Nbqqbw&format=png&color=000000")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.month = None


with st.sidebar:
    st.write("Use drop down to login and register")
    choice = st.sidebar.selectbox("Registrations:", ["Login", "Register"])
    if choice == "Login":
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password",type="password", key="login_password")

        if st.button("Login", type="primary"):
            if db.login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}")
                st.subheader(f"Logged in as: {st.session_state.username}")
            else:
                st.warning("Register first...")

    elif choice == "Register":
        username = st.text_input("Username", key="reg_username")
        password = st.text_input("Password",type="password", key="reg_password")
        if st.button("Register",type="primary"):
            if db.register(username, password):
                st.success("Registered Successfully! Please Login")
            else:
                st.error("Username already taken")

if not st.session_state.logged_in:
    st.title("SpendWise: A Personal Expenses Tracker")
elif st.session_state.logged_in:
    col8, col9, col10, col11, col12 = st.columns(5)
    with col12:
        if st.button("Logout", type="primary"):
            for key in ["login_username", "login_password","reg_username","reg_password"]:
                if key in st.session_state:
                    del st.session_state[key]

            st.session_state.logged_in = False
            st.session_state.username = None

            st.success("Logged out Successfully")
            st.rerun()
            time.sleep(2)

    st.title("Personal Finance Expenses Tracker")
    st.text("Managing your money is the first step towards financial freedom. This app helps you track, analyze, and control your expenses in a simple and effective way.")
    action = st.selectbox("Action",["Set budget", "View Budgets", "Add Expenses", "View Expenses", "Delete Expenses"])

    if action == "Set budget":
        st.subheader("Setting up budget..")
        st.info("Sample for view expenses input.. (2025-09)")
        year_month = st.text_input("YYYY-MM")
        amount = st.number_input("Amount")
        limit_amount = st.number_input("Amount Limit")
        if st.button("Add Budget",type="primary"):
            if '-' in year_month:
                if db.insert_budget(st.session_state.username, year_month, amount, limit_amount):
                    st.success("Budget added successfully")
                else:
                    st.warning("Fill all the details")
            else:
                st.warning("Enter in the correct format")
    
    elif action == "View Budgets":
        st.subheader(f"Budget of {st.session_state.username}")
        if st.button("View Budget", type="primary"):
            budgets = db.fetch_budgets(st.session_state.username)
            if budgets:
                df = pd.DataFrame(budgets)
                st.dataframe(df)
            else:
                st.info("No budgets yet..")
    
    elif action == "Add Expenses":
        st.subheader("Adding Expenses..")
        date = st.date_input("Date")
        category = st.selectbox("Category",["Food","Travel","Bills","Entertainment","Medical","Groceries","Savings","Personal care", "School/college Fees"])
        amount = st.number_input("Amount")
        payment_mode = st.selectbox("Payment_Type",["Cash","Card","UPI"])
        year_month = date.strftime("%Y-%m")

        if db.check_month(st.session_state.username, year_month):
            bud, limit = db.fetch_month_budget(st.session_state.username, year_month)
            if bud:
                bud = float(bud)
                exp = db.fetch_expenses(st.session_state.username, year_month)
                c_p = sum(float(e["amount"]) for e in exp) if exp else 0

                p_s = c_p + amount

                if p_s == limit:
                    st.warning(f"Adding this expense will reach your monthly limit amount Rs.{limit}!")
                    st.info(f"You will still have Rs.{bud - p_s:,.0f} left after this expense.")
                elif p_s > limit:
                    st.error(f"Adding this expense will exceed your monthly limit amount Rs.{limit}!")
                    st.info(f"You will still have Rs.{bud - p_s:,.0f} left after this expense.")
                elif p_s < limit:
                    st.info(f"You will still have Rs.{bud - p_s:,.0f} left after this expense.")
                elif p_s == bud:
                    st.warning(f"Adding this expense will reach your monthly budget Rs.{bud}!")
                elif p_s > bud:
                    st.error(f"Adding this expense will exceed your monthly budget Rs.{bud}")

            if st.button("Add Expenses", type="primary"):
                if db.insert_expenses(st.session_state.username, date, category, amount, payment_mode):
                    st.success("Expenses Added Successfullly")
                else:
                    st.warning("Please fill all the fields")
        else:
            st.info(f"Set budget for {year_month}") 

    elif action == "View Expenses":
        st.subheader(f"Expenses of {st.session_state.username}")
        exp_option = st.radio("Choose",["Category-Wise Expenses","Month-Wise Expenses"])
        if exp_option == "Month-Wise Expenses":
            st.info("Sample for view expenses input.. (2025-09)")
            selected_month = st.text_input("Enter Year-MM(YYYY-MM)")
            if st.button("View Expenses", type="primary"):
                if '-' in selected_month:
                    expenses = db.fetch_expenses(st.session_state.username, selected_month)
                    if expenses:
                        df1 = pd.DataFrame(expenses)
                        st.dataframe(df1)

                        st.divider()

                        t_amount, lim_amount = db.fetch_month_budget(st.session_state.username, selected_month)
                        sp_amount = df1["amount"].sum()

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric(label = f"Budget for {selected_month}", value = f"Rs. {t_amount:,.0f}")

                        with col2:
                            st.metric(label = "Remaining Amount", value = f"Rs. {t_amount-sp_amount:,.0f}")

                        with col3:
                            st.metric(label = "Total Amount spent..",value = f"Rs. {sp_amount:,.0f}")

                        st.divider()

                        st.subheader("Expense Insights")

                        df1['date'] = pd.to_datetime(df1['date'])
                        daily_spending = df1.groupby("date")["amount"].sum().reset_index()

                        avg_daily_spend = daily_spending['amount'].mean()

                        max_spend_row = daily_spending.loc[daily_spending['amount'].idxmax()]

                        col4, col5 = st.columns(2)
                        with col4:
                            st.metric(
                                label="Average Daily Spend",
                                value=f"Rs. {avg_daily_spend:,.0f}"
                            )                    

                        with col5:
                            st.metric(
                                label="Highest Spending Day",
                                value=max_spend_row['date'].strftime("%Y-%m-%d"),
                                delta=f"Rs. {max_spend_row['amount']:,.0f}"
                            )

                        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Category percentage", "Payment-type comparison", "Top Categories", "Monthly Trends", "Month comparison"])

                        with tab1:
                            st.subheader("Category wise percentage")
                            category_data = df1.groupby("category")["amount"].sum()
                            fig, ax = plt.subplots(figsize=(3,3))
                            ax.pie(
                                category_data,
                                autopct='%1.1f%%',
                                startangle=90,
                                pctdistance=0.8
                            )
                            ax.legend(
                                category_data.index,
                                title="Categories",
                                loc="center left",
                                bbox_to_anchor=(1, 0.5)
                            )
                            ax.axis('equal')
                            st.pyplot(fig)

                        with tab2:
                            payment_data = df1.groupby("payment_mode")["amount"].sum().reset_index().head(3)
                            fig, ax = plt.subplots(figsize=(16,3))
                            ax.bar(payment_data["payment_mode"],payment_data["amount"], color="black", edgecolor="red")
                            ax.set_xlabel("Payment Mode")
                            ax.set_ylabel("Total Amount")
                            ax.set_title("Expense comparison by Payment Mode")

                            st.pyplot(fig)         
                        
                        with tab3:
                            cat_data = df1.groupby("category")['amount'].sum().reset_index().head(3)
                            fig,ax = plt.subplots(figsize=(16,3))
                            ax.bar(cat_data["category"],cat_data["amount"],color="black",edgecolor="red")
                            ax.set_xlabel("Category")
                            ax.set_ylabel("Amount")
                            ax.set_title("Top 3 Category")
                            st.pyplot(fig)  

                        with tab4:
                            st.subheader("Monthtly Expense Trend")
                            eu1 = db.fetch_expenses_user(st.session_state.username)
                            if eu1:
                                df3 = pd.DataFrame(eu1)
                                df3['month_year'] = pd.to_datetime(df3['date']).dt.to_period('M').astype(str)
                                monthly_trend = df3.groupby('month_year')['amount'].sum().reset_index()

                                max_val = float(monthly_trend['amount'].max())

                                fig, ax = plt.subplots(figsize=(8, 4))
                                ax.plot(monthly_trend['month_year'], monthly_trend['amount'], marker='o', linestyle='-',linewidth=2, markerfacecolor="black", markeredgecolor="black",color="red")

                                for i, val in enumerate(monthly_trend['amount']):
                                    v = float(val)

                                    if v >= 0.8 * max_val:
                                        ax.text(i, v - (v * 0.03), f"{v:.0f}", ha="center", va = 'top', fontsize=9, color="black")
                                    else:
                                        ax.text(i, v + (v * 0.03), f"{v:.0f}", ha="center", va = 'bottom', fontsize=9, color="black")

                                ax.set_title("Monthly Expenses Trend")
                                ax.set_xlabel("Month")
                                ax.set_ylabel("Total Expenses")
                                st.pyplot(fig)

                        with tab5:
                            st.subheader("Category Growth Percentage from Last Month")
                            eu = db.fetch_expenses_user(st.session_state.username)
                            if eu:
                                df2 = pd.DataFrame(eu)

                                df2['date'] = pd.to_datetime(df2['date'], errors="coerce")
                                df2['amount'] = pd.to_numeric(df2['amount'], errors='coerce').fillna(0)

                                df2['month_year1'] = df2['date'].dt.to_period('M').astype(str)
                                category_month = (
                                    df2.groupby(['month_year1','category'])['amount']
                                    .sum()
                                    .unstack(fill_value=0)
                                    .sort_index()
                                )

                            if len(category_month) > 1:
                                prev = category_month.shift(1)
                                g = category_month.pct_change()*100

                                g = g.replace([np.inf, -np.inf], np.nan)

                                def format_growth(val, prev_val, curr_val):
                                    if pd.isna(val):
                                        if prev_val == 0 and curr_val > 0:
                                            return "🟢 New"
                                        else:
                                            return "0.00%"
                                    try:
                                        if val > 0:
                                            return f"🟢 {val:.2f}% ↑"
                                        elif val < 0:
                                            return f"🔴 {val:.2f}% ↓"
                                        else:
                                            return f"{val:.2f}%"
                                    except Exception:
                                        return "-"
                                    
                                s_g = g.copy().astype(object)
                                for r in g.index:
                                    for c in g.columns:
                                        s_g.loc[r, c] = format_growth(
                                            g.loc[r, c],
                                            prev.loc[r, c],
                                            category_month.loc[r, c]
                                        )
                                st.dataframe(s_g)
                            else:
                                st.info("Not enough months of data to calculate growth.")
                            
                        st.sidebar.subheader("Click below to download report..")
                        with st.sidebar:
                            csv = df3.to_csv(index=True).encode('utf-8')
                            st.download_button(
                                label="Download CSV Report",
                                data=csv,
                                file_name=f"Expenses report of{st.session_state.username}.csv",
                                mime="text/csv",
                                type="primary"
                            )

                    else:
                        st.info(f"No Expenses Yet.. Add Expenses for {selected_month}..")
                else:
                    st.warning("Check the input format")

        elif exp_option == "Category-Wise Expenses":
            cat = st.selectbox("Choose", ["Food","Travel","Bills","Entertainment","Medical","Groceries","Savings","Personal care", "School/college Fees"])
            cate = db.fetch_categories(st.session_state.username, cat)
            if cate:
                df4 = pd.DataFrame(cate, columns=['Date', 'Category', 'Amount', 'Payment_Mode'])
                df4
            else:
                st.info(f"No Expenses for this {cat} category!!")

    elif action == "Delete Expenses":
        expenses = db.fetch_expense_for_delete(st.session_state.username)

        if not expenses.empty:
            df = pd.DataFrame(expenses)
            df['label'] = df.apply(
                lambda row: f"{row['category']} - Rs.{row['amount']} on {row['date']}", axis=1
            )

            selected_label = st.selectbox("Select Expense to Delete", df['label'])
            selected_id = df.loc[df['label'] == selected_label, "expense_id"].values[0]

            if st.button("Delete Expense", type="primary"):
                st.session_state.show_confirm_box = True

            if st.session_state.get("show_confirm_box",False):
                st.warning(f"Are you sure want to delete this expense?\n\n {selected_label}")
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Yes, Delete", key="confirm_delete"):
                        if db.delete_expense(st.session_state.username, int(selected_id)):
                            st.success(f"Deleted: {selected_label}")
                            st.session_state.show_confirm_box = False
                        else:
                            st.error("Expense Not Found")
                    
                with col2:
                    if st.button("Cancel", key="cancel_delete"):
                        st.info("Deletion Cancelled")
                        st.session_state.show_confirm_box = False
        else:
            st.info("No expenses found to Delete.")

              
