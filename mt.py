import tkinter as tk
from tkinter import messagebox

class MovieTicketBooking:
    def __init__(self, rows, seats_per_row):
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.total_seats = rows * seats_per_row
        self.available_seats = {(row, seat) for row in range(1, rows + 1) for seat in range(1, seats_per_row + 1)}
        self.booked_seats = set()

    def book_tickets(self, selected_seats):
        available_seats = self.available_seats - self.booked_seats
        if len(selected_seats) <= len(available_seats):
            if any(seat in self.booked_seats for seat in selected_seats):
                return False  # Some seats are already booked
            else:
                self.booked_seats.update(selected_seats)
                return True
        else:
            return False

    def get_available_seats(self):
        return self.available_seats - self.booked_seats

    def get_booked_seats(self):
        return self.booked_seats

class MovieTicketBookingApp:
    def __init__(self, root, booking_system):
        self.root = root
        self.root.title("Movie Ticket Booking")

        self.booking_system = booking_system
        self.selected_seats = set()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Labels
        tk.Label(self.root, text="Welcome to Movie Ticket Booking", font=('Helvetica', 16)).pack(pady=10)

        # Display Screen
        self.screen_frame = tk.Frame(self.root)
        self.screen_frame.pack()

        # Buttons
        tk.Button(self.root, text="Book Selected Seats", command=self.book_selected_seats, font=('Helvetica', 12)).pack(pady=5)
        tk.Button(self.root, text="Show Booked Seats", command=self.show_booked_seats, font=('Helvetica', 12)).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.destroy, font=('Helvetica', 12), fg='red').pack(pady=10)

        # Initialize and display screen
        self.display_screen()

    def display_screen(self):
        for row in range(1, self.booking_system.rows + 1):
            for seat in range(1, self.booking_system.seats_per_row + 1):
                button_text = f"{row}-{seat}"
                button = tk.Button(self.screen_frame, text=button_text, width=4, height=2,
                                   command=lambda r=row, s=seat: self.toggle_seat(r, s),
                                   font=('Helvetica', 10))

                if (row, seat) in self.booking_system.get_booked_seats():
                    button.config(state=tk.DISABLED, bg='red')  # Change color of booked seats

                button.grid(row=row - 1, column=seat - 1, padx=5, pady=5)

    def toggle_seat(self, row, seat):
        seat = (row, seat)
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
        else:
            self.selected_seats.add(seat)

    def book_selected_seats(self):
        if not self.selected_seats:
            messagebox.showwarning("No Seats Selected", "Please select seats to book.")
            return

        success = self.booking_system.book_tickets(self.selected_seats)
        if success:
            messagebox.showinfo("Booking Successful", "Tickets booked successfully!")
            self.update_seat_colors()  # Update color after booking
        else:
            messagebox.showwarning("Booking Failed", "Some seats are already booked or not enough available seats.")
        self.selected_seats.clear()

    def show_booked_seats(self):
        booked_seats = self.booking_system.get_booked_seats()
        if booked_seats:
            message = f"Booked Seats: {booked_seats}"
        else:
            message = "No seats have been booked yet."
        messagebox.showinfo("Booked Seats", message)

    def update_seat_colors(self):
        for widget in self.screen_frame.winfo_children():
            if widget.cget("text") in [f"{row}-{seat}" for row, seat in self.booking_system.get_booked_seats()]:
                widget.config(state=tk.DISABLED, bg='red')

# Example usage
rows = 5
seats_per_row = 10

root = tk.Tk()
app = MovieTicketBookingApp(root, MovieTicketBooking(rows, seats_per_row))
root.mainloop()
