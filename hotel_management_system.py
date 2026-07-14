"""
Hotel Management System
Comprehensive hotel management system with room booking, guest management, and billing
"""
from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import os

class RoomType(Enum):
    """Types of rooms in the hotel"""
    SINGLE = "Single"
    DOUBLE = "Double"
    SUITE = "Suite"
    DELUXE = "Deluxe"
    PENTHOUSE = "Penthouse"

class RoomStatus(Enum):
    """Status of a room"""
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"
    CLEANING = "Cleaning"

class BookingStatus(Enum):
    """Status of a booking"""
    CONFIRMED = "Confirmed"
    CHECKED_IN = "Checked In"
    CHECKED_OUT = "Checked Out"
    CANCELLED = "Cancelled"

class PaymentMethod(Enum):
    """Payment methods"""
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    ONLINE = "Online Transfer"
    CHEQUE = "Cheque"

class Room:
    """Represents a hotel room"""
    
    def __init__(self, room_number: int, room_type: RoomType, price_per_night: float, capacity: int):
        """
        Initialize a room
        
        Args:
            room_number (int): Unique room number
            room_type (RoomType): Type of room
            price_per_night (float): Price per night in currency
            capacity (int): Guest capacity
        """
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.capacity = capacity
        self.status = RoomStatus.AVAILABLE
        self.amenities = []
        self.floor = (room_number // 100) if room_number >= 100 else 1
        self.last_cleaned = datetime.now()
    
    def add_amenity(self, amenity: str):
        """Add an amenity to the room"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
    
    def set_status(self, status: RoomStatus):
        """Set room status"""
        self.status = status
    
    def to_dict(self) -> Dict:
        """Convert room to dictionary"""
        return {
            'room_number': self.room_number,
            'room_type': self.room_type.value,
            'price_per_night': self.price_per_night,
            'capacity': self.capacity,
            'status': self.status.value,
            'amenities': self.amenities,
            'floor': self.floor,
            'last_cleaned': self.last_cleaned.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def __str__(self) -> str:
        """String representation of room"""
        status_symbol = {
            RoomStatus.AVAILABLE: "✓",
            RoomStatus.OCCUPIED: "●",
            RoomStatus.MAINTENANCE: "⚠",
            RoomStatus.CLEANING: "🧹"
        }[self.status]
        
        return (f"{status_symbol} Room {self.room_number} | {self.room_type.value} | "
                f"${self.price_per_night}/night | Capacity: {self.capacity}")


class Guest:
    """Represents a hotel guest"""
    
    def __init__(self, guest_id: int, name: str, email: str, phone: str, address: str = ""):
        """
        Initialize a guest
        
        Args:
            guest_id (int): Unique guest ID
            name (str): Guest name
            email (str): Email address
            phone (str): Phone number
            address (str): Physical address
        """
        self.guest_id = guest_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.registration_date = datetime.now()
        self.total_stays = 0
        self.loyalty_points = 0
    
    def add_loyalty_points(self, points: int):
        """Add loyalty points"""
        self.loyalty_points += points
    
    def to_dict(self) -> Dict:
        """Convert guest to dictionary"""
        return {
            'guest_id': self.guest_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'registration_date': self.registration_date.strftime("%Y-%m-%d %H:%M:%S"),
            'total_stays': self.total_stays,
            'loyalty_points': self.loyalty_points
        }
    
    def __str__(self) -> str:
        """String representation of guest"""
        return f"Guest {self.guest_id}: {self.name} | {self.email} | {self.phone}"


class Booking:
    """Represents a room booking"""
    
    def __init__(self, booking_id: int, guest: Guest, room: Room, 
                 check_in_date: str, check_out_date: str):
        """
        Initialize a booking
        
        Args:
            booking_id (int): Unique booking ID
            guest (Guest): Guest object
            room (Room): Room object
            check_in_date (str): Check-in date (YYYY-MM-DD)
            check_out_date (str): Check-out date (YYYY-MM-DD)
        """
        self.booking_id = booking_id
        self.guest = guest
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.status = BookingStatus.CONFIRMED
        self.booking_date = datetime.now()
        self.number_of_guests = 1
        self.special_requests = ""
        self.total_price = self.calculate_total_price()
    
    def calculate_total_price(self) -> float:
        """Calculate total booking price"""
        try:
            check_in = datetime.strptime(self.check_in_date, "%Y-%m-%d")
            check_out = datetime.strptime(self.check_out_date, "%Y-%m-%d")
            nights = (check_out - check_in).days
            return nights * self.room.price_per_night
        except ValueError:
            return 0
    
    def check_in(self) -> bool:
        """Process check-in"""
        self.status = BookingStatus.CHECKED_IN
        self.room.set_status(RoomStatus.OCCUPIED)
        return True
    
    def check_out(self) -> bool:
        """Process check-out"""
        self.status = BookingStatus.CHECKED_OUT
        self.room.set_status(RoomStatus.CLEANING)
        self.guest.total_stays += 1
        # Award 1 loyalty point per dollar spent
        self.guest.add_loyalty_points(int(self.total_price))
        return True
    
    def cancel_booking(self) -> bool:
        """Cancel the booking"""
        self.status = BookingStatus.CANCELLED
        self.room.set_status(RoomStatus.AVAILABLE)
        return True
    
    def to_dict(self) -> Dict:
        """Convert booking to dictionary"""
        return {
            'booking_id': self.booking_id,
            'guest_id': self.guest.guest_id,
            'room_number': self.room.room_number,
            'check_in_date': self.check_in_date,
            'check_out_date': self.check_out_date,
            'status': self.status.value,
            'booking_date': self.booking_date.strftime("%Y-%m-%d %H:%M:%S"),
            'number_of_guests': self.number_of_guests,
            'special_requests': self.special_requests,
            'total_price': self.total_price
        }
    
    def __str__(self) -> str:
        """String representation of booking"""
        return (f"Booking {self.booking_id} | Guest: {self.guest.name} | "
                f"Room: {self.room.room_number} | {self.check_in_date} to {self.check_out_date} | "
                f"Status: {self.status.value} | ${self.total_price:.2f}")


class Invoice:
    """Represents a hotel invoice/bill"""
    
    def __init__(self, invoice_id: int, booking: Booking):
        """
        Initialize an invoice
        
        Args:
            invoice_id (int): Unique invoice ID
            booking (Booking): Associated booking
        """
        self.invoice_id = invoice_id
        self.booking = booking
        self.room_charges = booking.total_price
        self.additional_charges = 0
        self.services = {}
        self.tax_rate = 0.10  # 10% tax
        self.discount = 0
        self.paid = False
        self.payment_method = None
        self.payment_date = None
        self.invoice_date = datetime.now()
    
    def add_service_charge(self, service_name: str, amount: float):
        """Add a service charge"""
        self.services[service_name] = amount
        self.additional_charges += amount
    
    def calculate_subtotal(self) -> float:
        """Calculate subtotal"""
        return self.room_charges + self.additional_charges
    
    def calculate_tax(self) -> float:
        """Calculate tax"""
        return self.calculate_subtotal() * self.tax_rate
    
    def calculate_total(self) -> float:
        """Calculate total amount due"""
        subtotal = self.calculate_subtotal()
        tax = self.calculate_tax()
        return subtotal + tax - self.discount
    
    def apply_discount(self, discount_amount: float):
        """Apply discount"""
        self.discount = min(discount_amount, self.calculate_subtotal())
    
    def process_payment(self, method: PaymentMethod) -> bool:
        """Process payment"""
        self.paid = True
        self.payment_method = method
        self.payment_date = datetime.now()
        return True
    
    def display_invoice(self):
        """Display invoice details"""
        print("\n" + "="*70)
        print(f"INVOICE #{self.invoice_id}")
        print("="*70)
        print(f"Guest: {self.booking.guest.name}")
        print(f"Room: {self.booking.room.room_number} ({self.booking.room.room_type.value})")
        print(f"Check-in: {self.booking.check_in_date} | Check-out: {self.booking.check_out_date}")
        print("-"*70)
        print(f"Room Charges:       ${self.room_charges:>12.2f}")
        
        if self.services:
            for service, amount in self.services.items():
                print(f"  {service}:          ${amount:>12.2f}")
        
        if self.additional_charges > sum(self.services.values()):
            print(f"Other Charges:      ${self.additional_charges - sum(self.services.values()):>12.2f}")
        
        print("-"*70)
        print(f"Subtotal:           ${self.calculate_subtotal():>12.2f}")
        print(f"Tax (10%):          ${self.calculate_tax():>12.2f}")
        
        if self.discount > 0:
            print(f"Discount:          -${self.discount:>12.2f}")
        
        print("-"*70)
        print(f"TOTAL DUE:          ${self.calculate_total():>12.2f}")
        
        if self.paid:
            print(f"Status: PAID (via {self.payment_method.value})")
        else:
            print("Status: PENDING")
        
        print("="*70 + "\n")
    
    def to_dict(self) -> Dict:
        """Convert invoice to dictionary"""
        return {
            'invoice_id': self.invoice_id,
            'booking_id': self.booking.booking_id,
            'room_charges': self.room_charges,
            'additional_charges': self.additional_charges,
            'services': self.services,
            'tax_rate': self.tax_rate,
            'discount': self.discount,
            'total': self.calculate_total(),
            'paid': self.paid,
            'payment_method': self.payment_method.value if self.payment_method else None,
            'payment_date': self.payment_date.strftime("%Y-%m-%d %H:%M:%S") if self.payment_date else None
        }


class HotelManagementSystem:
    """Main hotel management system"""
    
    def __init__(self, hotel_name: str, storage_file: str = "hotel_data.json"):
        """
        Initialize the hotel management system
        
        Args:
            hotel_name (str): Name of the hotel
            storage_file (str): Path to storage file
        """
        self.hotel_name = hotel_name
        self.storage_file = storage_file
        self.rooms: List[Room] = []
        self.guests: List[Guest] = []
        self.bookings: List[Booking] = []
        self.invoices: List[Invoice] = []
        
        self.next_guest_id = 1
        self.next_booking_id = 1
        self.next_invoice_id = 1
        
        self.load_data()
    
    def add_room(self, room_number: int, room_type: RoomType, 
                 price_per_night: float, capacity: int) -> Optional[Room]:
        """Add a room to the hotel"""
        if self.find_room(room_number):
            print(f"✗ Room {room_number} already exists")
            return None
        
        room = Room(room_number, room_type, price_per_night, capacity)
        self.rooms.append(room)
        print(f"✓ Room {room_number} added: {room_type.value} - ${price_per_night}/night")
        return room
    
    def find_room(self, room_number: int) -> Optional[Room]:
        """Find a room by number"""
        for room in self.rooms:
            if room.room_number == room_number:
                return room
        return None
    
    def find_guest(self, guest_id: int) -> Optional[Guest]:
        """Find a guest by ID"""
        for guest in self.guests:
            if guest.guest_id == guest_id:
                return guest
        return None
    
    def register_guest(self, name: str, email: str, phone: str, address: str = "") -> Optional[Guest]:
        """Register a new guest"""
        guest = Guest(self.next_guest_id, name, email, phone, address)
        self.guests.append(guest)
        self.next_guest_id += 1
        print(f"✓ Guest registered: {guest}")
        return guest
    
    def get_available_rooms(self, check_in: str, check_out: str) -> List[Room]:
        """Get available rooms for a date range"""
        available = []
        
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        except ValueError:
            print("✗ Invalid date format")
            return available
        
        for room in self.rooms:
            if room.status == RoomStatus.AVAILABLE:
                # Check if room is booked during this period
                is_available = True
                for booking in self.bookings:
                    if booking.room.room_number == room.room_number:
                        if booking.status != BookingStatus.CANCELLED:
                            booking_in = datetime.strptime(booking.check_in_date, "%Y-%m-%d")
                            booking_out = datetime.strptime(booking.check_out_date, "%Y-%m-%d")
                            
                            # Check for overlap
                            if not (check_out_date <= booking_in or check_in_date >= booking_out):
                                is_available = False
                                break
                
                if is_available:
                    available.append(room)
        
        return available
    
    def create_booking(self, guest_id: int, room_number: int, 
                      check_in: str, check_out: str) -> Optional[Booking]:
        """Create a new booking"""
        guest = self.find_guest(guest_id)
        if not guest:
            print(f"✗ Guest {guest_id} not found")
            return None
        
        room = self.find_room(room_number)
        if not room:
            print(f"✗ Room {room_number} not found")
            return None
        
        available = self.get_available_rooms(check_in, check_out)
        if room not in available:
            print(f"✗ Room {room_number} is not available for this date range")
            return None
        
        booking = Booking(self.next_booking_id, guest, room, check_in, check_out)
        self.bookings.append(booking)
        self.next_booking_id += 1
        print(f"✓ Booking created: {booking}")
        return booking
    
    def check_in_guest(self, booking_id: int) -> bool:
        """Check in a guest"""
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                if booking.check_in():
                    print(f"✓ Guest {booking.guest.name} checked in to Room {booking.room.room_number}")
                    return True
        print(f"✗ Booking {booking_id} not found")
        return False
    
    def check_out_guest(self, booking_id: int) -> bool:
        """Check out a guest"""
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                if booking.status == BookingStatus.CHECKED_IN:
                    booking.check_out()
                    print(f"✓ Guest {booking.guest.name} checked out from Room {booking.room.room_number}")
                    return True
        print(f"✗ Booking {booking_id} not found or not checked in")
        return False
    
    def generate_invoice(self, booking_id: int) -> Optional[Invoice]:
        """Generate invoice for a booking"""
        booking = None
        for b in self.bookings:
            if b.booking_id == booking_id:
                booking = b
                break
        
        if not booking:
            print(f"✗ Booking {booking_id} not found")
            return None
        
        invoice = Invoice(self.next_invoice_id, booking)
        self.invoices.append(invoice)
        self.next_invoice_id += 1
        print(f"✓ Invoice generated: Invoice #{invoice.invoice_id}")
        return invoice
    
    def process_payment(self, invoice_id: int, method: PaymentMethod) -> bool:
        """Process payment for an invoice"""
        for invoice in self.invoices:
            if invoice.invoice_id == invoice_id:
                invoice.process_payment(method)
                print(f"✓ Payment processed for Invoice #{invoice_id}")
                print(f"  Amount: ${invoice.calculate_total():.2f}")
                print(f"  Method: {method.value}")
                return True
        print(f"✗ Invoice {invoice_id} not found")
        return False
    
    def clean_room(self, room_number: int) -> bool:
        """Mark room as cleaned and available"""
        room = self.find_room(room_number)
        if room:
            room.set_status(RoomStatus.AVAILABLE)
            room.last_cleaned = datetime.now()
            print(f"✓ Room {room_number} cleaned and ready")
            return True
        return False
    
    def get_occupancy_rate(self) -> float:
        """Calculate current occupancy rate"""
        occupied = sum(1 for room in self.rooms if room.status == RoomStatus.OCCUPIED)
        total = len(self.rooms)
        return (occupied / total * 100) if total > 0 else 0
    
    def get_revenue(self, start_date: str = None, end_date: str = None) -> float:
        """Calculate total revenue"""
        revenue = 0
        for invoice in self.invoices:
            if invoice.paid:
                if start_date and end_date:
                    payment_date = datetime.strptime(invoice.payment_date, "%Y-%m-%d %H:%M:%S")
                    start = datetime.strptime(start_date, "%Y-%m-%d")
                    end = datetime.strptime(end_date, "%Y-%m-%d")
                    if start <= payment_date <= end:
                        revenue += invoice.calculate_total()
                else:
                    revenue += invoice.calculate_total()
        return revenue
    
    def display_rooms(self):
        """Display all rooms"""
        print("\n" + "="*90)
        print("🛏️ ROOMS INVENTORY")
        print("="*90)
        for room in sorted(self.rooms, key=lambda r: r.room_number):
            print(room)
        print("="*90 + "\n")
    
    def display_bookings(self, status: BookingStatus = None):
        """Display bookings"""
        bookings_to_show = self.bookings
        if status:
            bookings_to_show = [b for b in self.bookings if b.status == status]
        
        print("\n" + "="*90)
        print(f"📋 BOOKINGS")
        print("="*90)
        for booking in bookings_to_show:
            print(booking)
        print("="*90 + "\n")
    
    def display_dashboard(self):
        """Display hotel dashboard"""
        occupied = sum(1 for room in self.rooms if room.status == RoomStatus.OCCUPIED)
        available = sum(1 for room in self.rooms if room.status == RoomStatus.AVAILABLE)
        maintenance = sum(1 for room in self.rooms if room.status == RoomStatus.MAINTENANCE)
        cleaning = sum(1 for room in self.rooms if room.status == RoomStatus.CLEANING)
        
        total_revenue = self.get_revenue()
        avg_occupancy = self.get_occupancy_rate()
        
        print("\n" + "="*80)
        print(f"🏨 {self.hotel_name.upper()} - DASHBOARD")
        print("="*80)
        
        print("\n📊 ROOM STATUS:")
        print(f"  Total Rooms:    {len(self.rooms)}")
        print(f"  Occupied:       {occupied} ({'●' * occupied}{'○' * available})")
        print(f"  Available:      {available}")
        print(f"  Maintenance:    {maintenance}")
        print(f"  Cleaning:       {cleaning}")
        print(f"  Occupancy Rate: {avg_occupancy:.1f}%")
        
        print("\n👥 GUESTS & BOOKINGS:")
        print(f"  Total Guests:   {len(self.guests)}")
        print(f"  Total Bookings: {len(self.bookings)}")
        print(f"  Confirmed:      {sum(1 for b in self.bookings if b.status == BookingStatus.CONFIRMED)}")
        print(f"  Checked In:     {sum(1 for b in self.bookings if b.status == BookingStatus.CHECKED_IN)}")
        print(f"  Checked Out:    {sum(1 for b in self.bookings if b.status == BookingStatus.CHECKED_OUT)}")
        print(f"  Cancelled:      {sum(1 for b in self.bookings if b.status == BookingStatus.CANCELLED)}")
        
        print("\n💰 FINANCIAL:")
        print(f"  Total Revenue:  ${total_revenue:,.2f}")
        print(f"  Total Invoices: {len(self.invoices)}")
        print(f"  Paid:           {sum(1 for i in self.invoices if i.paid)}")
        print(f"  Pending:        {sum(1 for i in self.invoices if not i.paid)}")
        
        print("="*80 + "\n")
    
    def save_data(self) -> bool:
        """Save all data to file"""
        try:
            data = {
                'hotel_name': self.hotel_name,
                'rooms': [room.to_dict() for room in self.rooms],
                'guests': [guest.to_dict() for guest in self.guests],
                'bookings': [booking.to_dict() for booking in self.bookings],
                'invoices': [invoice.to_dict() for invoice in self.invoices],
                'next_guest_id': self.next_guest_id,
                'next_booking_id': self.next_booking_id,
                'next_invoice_id': self.next_invoice_id,
                'last_saved': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"✗ Error saving data: {str(e)}")
            return False
    
    def load_data(self) -> bool:
        """Load data from file"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.next_guest_id = data.get('next_guest_id', 1)
                    self.next_booking_id = data.get('next_booking_id', 1)
                    self.next_invoice_id = data.get('next_invoice_id', 1)
                return True
            return True
        except Exception as e:
            print(f"✗ Error loading data: {str(e)}")
            return False


# Example usage and demo
if __name__ == "__main__":
    print("\n" + "="*80)
    print("🏨 HOTEL MANAGEMENT SYSTEM - DEMO MODE")
    print("="*80 + "\n")
    
    # Initialize hotel
    hotel = HotelManagementSystem("Grand Plaza Hotel")
    
    # Add rooms
    print("➕ Adding rooms...\n")
    hotel.add_room(101, RoomType.SINGLE, 100, 1)
    hotel.add_room(102, RoomType.DOUBLE, 150, 2)
    hotel.add_room(103, RoomType.SUITE, 250, 4)
    hotel.add_room(201, RoomType.SINGLE, 100, 1)
    hotel.add_room(202, RoomType.DOUBLE, 150, 2)
    hotel.add_room(301, RoomType.DELUXE, 300, 3)
    hotel.add_room(401, RoomType.PENTHOUSE, 500, 6)
    
    # Display rooms
    hotel.display_rooms()
    
    # Register guests
    print("👥 Registering guests...\n")
    guest1 = hotel.register_guest("John Smith", "john@email.com", "555-0001", "123 Main St")
    guest2 = hotel.register_guest("Sarah Johnson", "sarah@email.com", "555-0002", "456 Oak Ave")
    guest3 = hotel.register_guest("Mike Brown", "mike@email.com", "555-0003", "789 Pine Rd")
    
    # Create bookings
    print("\n📅 Creating bookings...\n")
    booking1 = hotel.create_booking(guest1.guest_id, 101, "2026-07-15", "2026-07-18")
    booking2 = hotel.create_booking(guest2.guest_id, 102, "2026-07-16", "2026-07-19")
    booking3 = hotel.create_booking(guest3.guest_id, 301, "2026-07-20", "2026-07-25")
    
    # Display bookings
    hotel.display_bookings()
    
    # Check in guests
    print("✓ Checking in guests...\n")
    hotel.check_in_guest(booking1.booking_id)
    hotel.check_in_guest(booking2.booking_id)
    
    # Generate invoices
    print("\n💳 Generating invoices...\n")
    invoice1 = hotel.generate_invoice(booking1.booking_id)
    invoice1.add_service_charge("Room Service", 50)
    invoice1.add_service_charge("Laundry", 20)
    invoice1.display_invoice()
    
    invoice2 = hotel.generate_invoice(booking2.booking_id)
    invoice2.display_invoice()
    
    # Process payments
    print("💰 Processing payments...\n")
    hotel.process_payment(invoice1.invoice_id, PaymentMethod.CREDIT_CARD)
    hotel.process_payment(invoice2.invoice_id, PaymentMethod.ONLINE)
    
    # Check out guests
    print("\n🚪 Checking out guests...\n")
    hotel.check_out_guest(booking1.booking_id)
    hotel.check_out_guest(booking2.booking_id)
    
    # Clean rooms
    print("🧹 Cleaning rooms...\n")
    hotel.clean_room(101)
    hotel.clean_room(102)
    
    # Display dashboard
    hotel.display_dashboard()
    
    # Save data
    print("💾 Saving data...\n")
    hotel.save_data()
    
    print("✓ Demo completed successfully!")
