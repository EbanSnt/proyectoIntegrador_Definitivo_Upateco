import tkinter as tk
import csv
from datetime import datetime, timedelta

days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

def show_week_events(start_date):
    root = tk.Tk()
    root.title('Agenda Semanal')
    root.geometry('800x300+100+150')
    root.resizable(False, False)
    root.config(background="grey")
    day_frame = tk.Frame(root)
    day_frame.pack(pady=10)

    for day in days:
        tk.Label(day_frame, text=day, width=10, padx=20, pady=5, borderwidth=2, relief='groove',
                 foreground="#000",background="#fff").pack(side=tk.LEFT)

    event_frame = tk.Frame(root,background="grey")
    event_frame.place(x=0,y=40,width=800)

    with open('agenda.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        events = list(reader)

    week_start = start_date - timedelta(days=start_date.weekday())
    week_end = week_start + timedelta(days=6)
    week_events = [event for event in events if
                   datetime.strptime(event['Fecha'], '%d/%m/%Y').date() >= week_start.date() and
                   datetime.strptime(event['Fecha'], '%d/%m/%Y').date() <= week_end.date()]

    day_events = {}
    for event in week_events:
        day = datetime.strptime(event['Fecha'], '%d/%m/%Y').strftime('%A')
        if day == 'Monday':
            day = 'Lunes'
        elif day == 'Tuesday':
            day = 'Martes'
        elif day == 'Wednesday':
            day = 'Miércoles'
        elif day == 'Thursday':
            day = 'Jueves'
        elif day == 'Friday':
            day = 'Viernes'
        elif day == 'Saturday':
            day = 'Sábado'
        elif day == 'Sunday':
            day = 'Domingo'
        if day not in day_events:
            day_events[day] = []
        day_events[day].append(event) 

    def show_prev_week():
        nonlocal week_start, week_end
        week_start -= timedelta(days=7)
        week_end = week_start + timedelta(days=6)
        root.destroy()  # destroy the current window
        show_week_events(week_start)  # call show_week_events with updated start_date

    def show_next_week():
        nonlocal week_start, week_end
        week_start += timedelta(days=7)
        week_end = week_start + timedelta(days=6)
        root.destroy()  # destroy the current window
        show_week_events(week_start)  # call show_week_events with updated start_date

    prev_button = tk.Button(root, text='Semana anterior', command=show_prev_week)
    prev_button.place(x=170,y=250)
    prev_button.config(fg="white",font=("Helvetica",9))
    prev_button.config(bg="#000")

    next_button = tk.Button(root, text='Próxima semana', command=show_next_week)
    next_button.place(x=50,y=250)
    next_button.config(fg="white",font=("Helvetica",9))
    next_button.config(bg="#000")

    for day in days:
        if day in day_events:
            event_list = tk.Listbox(event_frame, width=17, height=10, borderwidth=2, relief='groove')
            for event in day_events[day]:
                event_list.insert(tk.END, event['Titulo'])
                event_list.insert(tk.END, event['Descripcion'])
                event_list.insert(tk.END, event['Fecha'])
                event_list.insert(tk.END, '')
            event_list.pack(side=tk.LEFT, padx=4, pady=10)
        else:
            date_no_events = week_start + timedelta(days=days.index(day))
            tk.Label(event_frame, text=f"{date_no_events.strftime('%d/%m/%Y')}\nSin eventos", width=12, padx=13,
                    pady=10, borderwidth=2, relief='groove',background="#fff",foreground="#000",
                     font=("Helvetica",9)).pack(side=tk.LEFT)

    root.mainloop()

#show_week_events(datetime.today())