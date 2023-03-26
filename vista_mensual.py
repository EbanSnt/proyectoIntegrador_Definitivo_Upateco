import tkinter as tk
import pandas as pd
from datetime import datetime
import calendar

def show_calendar(window):
    # Create a tkinter window
    # window = tk.Tk()
    # window.title("Calendario")
    # window.config(bg="#F5F5F5")

    # Create a dataframe from the agenda file
    df = pd.read_csv("agenda.csv")
    df["Fecha"] = pd.to_datetime(df["Fecha"], format='%d/%m/%Y')

    # Get the current month and year
    now = datetime.now()
    year = now.year
    month = now.month

    # Create a label for the current month and year
    month_label = tk.Label(window, text=f"{calendar.month_name[month].capitalize().replace('January', 'Enero').replace('February', 'Febrero').replace('March', 'Marzo').replace('April', 'Abril').replace('May', 'Mayo').replace('June', 'Junio').replace('July', 'Julio').replace('August', 'Agosto').replace('September', 'Septiembre').replace('October', 'Octubre').replace('November', 'Noviembre').replace('December', 'Diciembre')} {year}", font=('Arial', 20, 'bold'), bg="#F5F5F5", fg="#222222")
    month_label.place(x=80,y=50)
    # Create a calendar for the current month
    cal = tk.Frame(window, width=412, height=310, bg="#F5F5F5")
    cal.place(x=50,y=100)

    # Create labels for the days of the week
    days = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    for i in range(7):
        label = tk.Label(cal, text=days[i], font=('Arial', 14, 'bold'), bg="#F5F5F5", fg="#222222")
        label.grid(row=0, column=i)

    # Get the number of days in the current month
    days_in_month = calendar.monthrange(year, month)[1]

    # Create labels for each day in the current month
    day_labels = []
    for i in range(days_in_month):
        day = i + 1
        day_label = tk.Label(cal, text=str(day), font=('Arial', 12), bg="#F5F5F5", fg="#222222")
        day_labels.append(day_label)

    # Place the day labels on the calendar grid
    row = 1
    col = calendar.weekday(year, month, 1)
    for day_label in day_labels:
        day_label.grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col == 7:
            col = 0
            row += 1

    # Highlight the current day on the calendar
    if year == now.year and month == now.month:
        day_labels[now.day-1].configure(bg='#008CBA', fg="#FFFFFF", relief="raised", bd=1)

    # Display events on the calendar
    for index, row in df.iterrows():
        if row["Fecha"].year == year and row["Fecha"].month == month:
            day_labels[row["Fecha"].day-1].configure(bg='#6DB65B')

    # window.mainloop()