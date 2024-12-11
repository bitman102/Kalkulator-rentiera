import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Funkcja do obliczeń i generowania wykresów
def calculate_and_plot(initial_amount, monthly_withdrawal, annual_interest_rate,
                       one_time_contribution, year_of_contribution, tax_rate, annual_withdrawal_change):

    monthly_interest_rate = annual_interest_rate / 12
    balance = initial_amount
    months = 0
    balances = [balance]
    withdrawals = [monthly_withdrawal]
    inflations = [0]  # Inflacja usunięta, ale zachowujemy to dla kompatybilności z funkcją wykresu
    max_months = 100 * 12  # Limit do 100 lat

    current_withdrawal = monthly_withdrawal

    while balance > 0 and months < max_months:
        if months % 12 == 0:  # Zastosowanie rocznej zmiany raz w roku
            current_withdrawal *= (1 + annual_withdrawal_change)
        # Zastosowanie jednorazowej wpłaty w określonym roku (upewnij się, że czas jest poprawny)
        if months // 12 == year_of_contribution and months % 12 == 0:
            balance += one_time_contribution

        balance += balance * monthly_interest_rate * (1 - tax_rate)
        balance -= current_withdrawal
        balances.append(balance)
        withdrawals.append(current_withdrawal)
        inflations.append(0)
        months += 1

    years = months // 12
    remaining_months = months % 12

    if balance <= 0:
        result_text = f"Oszczędności wystarczą na {years} lat i {remaining_months} miesięcy."
    else:
        result_text = "Oszczędności nigdy się nie wyczerpią."

    fig = make_subplots(rows=2, cols=1, subplot_titles=("Stan Konta w Czasie", "Kwota Wypłaty w Czasie"))

    fig.add_trace(
        go.Scatter(x=[month / 12 for month in range(len(balances))], y=balances, mode='lines', name='Stan Konta (PLN)'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=[month / 12 for month in range(len(withdrawals))], y=withdrawals, mode='lines', name='Wypłata (PLN)'),
        row=2, col=1
    )

    fig.update_xaxes(title_text="Lata", row=2, col=1)
    fig.update_yaxes(title_text="Saldo (PLN)", row=1, col=1)
    fig.update_yaxes(title_text="Kwota Wypłaty (PLN)", row=2, col=1)
    fig.update_layout(height=600, width=800)

    return result_text, fig

# Ustawienia interfejsu Streamlit
st.title('Kalkulator rentiera')

initial_amount = st.number_input('Kapitał początkowy (PLN):', value=0)
monthly_withdrawal = st.number_input('Miesięczna wypłata (PLN):', value=0)
annual_interest_rate = st.number_input('Roczna stopa oprocentowania aktywów (PLN):', value=0) / 100
annual_withdrawal_change = st.number_input('Roczna stopa inflacji (%) o jaki jest indeksowana miesięczna wypłata:', value=0) / 100
one_time_contribution = st.number_input('Jednorazowa dodatkowa wpłata (PLN) (opcjonalne):', value=0)
year_of_contribution = st.number_input('Rok jednorazowej wpłaty:', value=0)
tax_rate = st.number_input('Stopa podatku od zysków kapitałowych (%) (opcjonalne):', value=0.0) / 100

if st.button('Oblicz'):
    result_text, fig = calculate_and_plot(initial_amount, monthly_withdrawal, annual_interest_rate,
                                          one_time_contribution, year_of_contribution, tax_rate, annual_withdrawal_change)
    st.write(result_text)
    st.plotly_chart(fig)
