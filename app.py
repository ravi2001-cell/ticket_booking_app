import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey_change_me'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'
db = SQLAlchemy(app)

# Database Models
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    total_tickets = db.Column(db.Integer, nullable=False)
    tickets_sold = db.Column(db.Integer, default=0)

    @property
    def tickets_left(self):
        return self.total_tickets - self.tickets_sold

# Routes
@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/book/<int:event_id>', methods=['GET', 'POST'])
def book_ticket(event_id):
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        ticket_quantity = int(request.form.get('quantity', 1))
        
        # --- Logic Branching System ---
        # Branch A: Negative or zero validation
        if ticket_quantity <= 0:
            flash("Please select a valid number of tickets.", "error")
            return redirect(url_for('book_ticket', event_id=event.id))
            
        # Branch B: Sold out logic
        elif event.tickets_left == 0:
            flash("Sorry, this event is completely sold out!", "error")
            return redirect(url_for('index'))
            
        # Branch C: Not enough tickets left logic
        elif ticket_quantity > event.tickets_left:
            flash(f"Error! Only {event.tickets_left} tickets left.", "error")
            return redirect(url_for('book_ticket', event_id=event.id))
            
        # Branch D: Successful booking logic
        else:
            event.tickets_sold += ticket_quantity
            db.session.commit()
            flash(f"Success! Successfully booked {ticket_quantity} tickets for {event.title}.", "success")
            return redirect(url_for('index'))

    return render_template('booking.html', event=event)

# Initialize Database with Seed Data
def init_db():
    if not os.path.exists('instance/booking.db'):
        with app.app_context():
            db.create_all()
            # Adding sample data for demonstration
            if not Event.query.first():
                db.session.add(Event(title="Music Festival 2026", total_tickets=100, tickets_sold=95))
                db.session.add(Event(title="Tech Conference", total_tickets=50, tickets_sold=10))
                db.session.add(Event(title="Local Standup Comedy", total_tickets=30, tickets_sold=30))
                db.session.commit()

if __name__ == '__main__':
    init_db()
    # Force Flask to listen to outside traffic on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

