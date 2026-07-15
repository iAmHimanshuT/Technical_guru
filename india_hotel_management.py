"""
India Lead Role Hotel Management System
Specialized hotel management system for India-based hotels with multi-language support,
GST compliance, Indian payment methods, and localized features
"""
from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import os

class RoomType(Enum):
    """Types of rooms in Indian hotels"""
    ECONOMY = "Economy"
    STANDARD = "Standard"
    DELUXE = "Deluxe"
    SUPER_DELUXE = "Super Deluxe"
    SUITE = "Suite"
    LUXURY_SUITE = "Luxury Suite"
    PRESIDENTIAL = "Presidential"

class RoomStatus(Enum):
    """Status of a room"""
    AVAILABLE = "उपलब्ध"  # Available in Hindi
    OCCUPIED = "कब्जे में"  # Occupied in Hindi
    MAINTENANCE = "रखरखाव"  # Maintenance in Hindi
    CLEANING = "सफाई"  # Cleaning in Hindi
    RESERVED = "आरक्षित"  # Reserved in Hindi

class BookingStatus(Enum):
    """Status of a booking"""
    CONFIRMED = "Confirmed"
    CHECKED_IN = "Checked In"
    CHECKED_OUT = "Checked Out"
    CANCELLED = "Cancelled"
    NO_SHOW = "No Show"

class PaymentMethod(Enum):
    """Indian payment methods"""
    CASH = "नकद (Cash)"
    UPI = "UPI (Google Pay, PhonePe, Paytm)"
    CREDIT_CARD = "क्रेडिट कार्ड (Credit Card)"
    DEBIT_CARD = "डेबिट कार्ड (Debit Card)"
    NET_BANKING = "नेट बैंकिंग (Net Banking)"
    RTGS_NEFT = "RTGS/NEFT"
    CHEQUE = "चेक (Cheque)"
    CORPORATE = "कॉर्पोरेट (Corporate)"

class Language(Enum):
    """Supported languages"""
    ENGLISH = "English"
    HINDI = "Hindi"
    REGIONAL = "Regional"

class GuestCategory(Enum):
    """Guest categories for Indian hotels"""
    DOMESTIC = "Domestic"
    FOREIGN = "Foreign"
    CORPORATE = "Corporate"
    GOVERNMENT = "Government"
    STUDENT = "Student"
    SENIOR_CITIZEN = "Senior Citizen"
    VIP = "VIP"

class Room:
    """Represents a hotel room with Indian specifications"""
    
    def __init__(self, room_number: int, room_type: RoomType, price_per_night: float, 
                 capacity: int, ac_type: str = "Window AC"):
        """
        Initialize a room for Indian hotel
        
        Args:
            room_number (int): Unique room number
            room_type (RoomType): Type of room
            price_per_night (float): Price per night in INR
            capacity (int): Guest capacity
            ac_type (str): Type of air conditioning
        """
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.capacity = capacity
        self.ac_type = ac_type
        self.status = RoomStatus.AVAILABLE
        self.amenities = [
            "HD TV",
            "WiFi",
            "24/7 Hot Water",
            "Room Service",
            "Work Desk"
        ]
        self.floor = (room_number // 100) if room_number >= 100 else 1
        self.last_cleaned = datetime.now()
        self.housekeeping_status = "Clean"
    
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
            'ac_type': self.ac_type,
            'status': self.status.value,
            'amenities': self.amenities,
            'floor': self.floor,
            'housekeeping_status': self.housekeeping_status,
            'last_cleaned': self.last_cleaned.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def __str__(self) -> str:
        """String representation of room"""
        return (f"कक्ष {self.room_number} | {self.room_type.value} | "
                f"₹{self.price_per_night}/रात | क्षमता: {self.capacity}")


class Guest:
    """Represents a hotel guest in India"""
    
    def __init__(self, guest_id: int, name: str, email: str, phone: str, 
                 category: GuestCategory, id_type: str = "Aadhar", id_number: str = ""):
        """
        Initialize a guest
        
        Args:
            guest_id (int): Unique guest ID
            name (str): Guest name
            email (str): Email address
            phone (str): Indian phone number
            category (GuestCategory): Guest category
            id_type (str): ID type (Aadhar, PAN, Passport, etc.)
            id_number (str): Government ID number
        """
        self.guest_id = guest_id
        self.name = name
        self.email = email
        self.phone = phone
        self.category = category
        self.id_type = id_type
        self.id_number = id_number
        self.registration_date = datetime.now()
        self.total_stays = 0
        self.loyalty_points = 0
        self.membership_tier = "Bronze"  # Bronze, Silver, Gold, Platinum
    
    def add_loyalty_points(self, points: int):
        """Add loyalty points"""
        self.loyalty_points += points
        self.update_membership_tier()
    
    def update_membership_tier(self):
        """Update membership tier based on loyalty points"""
        if self.loyalty_points >= 50000:
            self.membership_tier = "Platinum"
        elif self.loyalty_points >= 20000:
            self.membership_tier = "Gold"
        elif self.loyalty_points >= 5000:
            self.membership_tier = "Silver"
        else:
            self.membership_tier = "Bronze"
    
    def get_discount_percentage(self) -> float:
        """Get discount based on membership tier"""
        discounts = {
            "Platinum": 20,
            "Gold": 15,
            "Silver": 10,
            "Bronze": 0
        }
        return discounts.get(self.membership_tier, 0)
    
    def to_dict(self) -> Dict:
        """Convert guest to dictionary"""
        return {
            'guest_id': self.guest_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'category': self.category.value,
            'id_type': self.id_type,
            'id_number': self.id_number,
            'registration_date': self.registration_date.strftime("%Y-%m-%d %H:%M:%S"),
            'total_stays': self.total_stays,
            'loyalty_points': self.loyalty_points,
            'membership_tier': self.membership_tier
        }
    
    def __str__(self) -> str:
        """String representation of guest"""
        return (f"अतिथि {self.guest_id}: {self.name} | {self.category.value} | "
                f"{self.membership_tier} | ₹{self.loyalty_points}")


class Booking:
    """Represents a room booking in India"""
    
    def __init__(self, booking_id: int, guest: Guest, room: Room, 
                 check_in_date: str, check_out_date: str):
        """
        Initialize a booking
        
        Args:
            booking_id (int): Unique booking ID
            guest (Guest): Guest object
            room (Room): Room object
            check_in_date (str): Check-in date (DD-MM-YYYY)
            check_out_date (str): Check-out date (DD-MM-YYYY)
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
        self.advance_paid = 0
        self.total_price = self.calculate_total_price()
    
    def calculate_total_price(self) -> float:
        """Calculate total booking price"""
        try:
            check_in = datetime.strptime(self.check_in_date, "%d-%m-%Y")
            check_out = datetime.strptime(self.check_out_date, "%d-%m-%Y")
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
        # Award loyalty points: 1 point per rupee
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
            'advance_paid': self.advance_paid,
            'total_price': self.total_price
        }
    
    def __str__(self) -> str:
        """String representation of booking"""
        return (f"बुकिंग {self.booking_id} | अतिथि: {self.guest.name} | "
                f"कक्ष: {self.room.room_number} | {self.check_in_date} से {self.check_out_date} | "
                f"₹{self.total_price:.2f}")


class Invoice:
    """Indian hotel invoice with GST compliance"""
    
    def __init__(self, invoice_id: int, invoice_number: str, booking: Booking):
        """
        Initialize an invoice with GST
        
        Args:
            invoice_id (int): Unique invoice ID
            invoice_number (str): GST-compliant invoice number (STATE-HOTEL-SERIES)
            booking (Booking): Associated booking
        """
        self.invoice_id = invoice_id
        self.invoice_number = invoice_number  # e.g., MH-HOTEL-001
        self.booking = booking
        self.room_charges = booking.total_price
        self.additional_charges = 0
        self.services = {}
        
        # GST Rates in India
        self.gst_rate = 0.12  # 12% GST for room rent in India
        self.service_tax_rate = 0.18  # 18% for services
        
        self.discount = 0
        self.paid = False
        self.payment_method = None
        self.payment_date = None
        self.invoice_date = datetime.now()
        self.invoice_month = datetime.now().strftime("%B %Y")
    
    def add_service_charge(self, service_name: str, amount: float):
        """Add a service charge"""
        self.services[service_name] = amount
        self.additional_charges += amount
    
    def calculate_subtotal(self) -> float:
        """Calculate subtotal (before tax)"""
        return self.room_charges + self.additional_charges
    
    def calculate_gst(self) -> float:
        """Calculate GST (12% on room charges)"""
        return self.room_charges * self.gst_rate
    
    def calculate_service_tax(self) -> float:
        """Calculate service tax (18% on additional charges)"""
        return self.additional_charges * self.service_tax_rate
    
    def calculate_total_tax(self) -> float:
        """Calculate total tax"""
        return self.calculate_gst() + self.calculate_service_tax()
    
    def calculate_total(self) -> float:
        """Calculate total amount due"""
        subtotal = self.calculate_subtotal()
        total_tax = self.calculate_total_tax()
        return subtotal + total_tax - self.discount
    
    def apply_discount(self, discount_amount: float):
        """Apply discount (membership or corporate)"""
        self.discount = min(discount_amount, self.calculate_subtotal())
    
    def process_payment(self, method: PaymentMethod) -> bool:
        """Process payment"""
        self.paid = True
        self.payment_method = method
        self.payment_date = datetime.now()
        return True
    
    def display_invoice(self):
        """Display GST-compliant invoice"""
        print("\n" + "="*80)
        print("TAX INVOICE (कर चालान)")
        print("="*80)
        print(f"Invoice No.: {self.invoice_number}")
        print(f"Invoice Date: {self.invoice_date.strftime('%d-%m-%Y')}")
        print(f"Invoice Month: {self.invoice_month}")
        print("-"*80)
        print(f"Guest Name: {self.booking.guest.name}")
        print(f"Guest ID Type: {self.booking.guest.id_type}")
        print(f"Guest ID Number: {self.booking.guest.id_number}")
        print(f"Room Number: {self.booking.room.room_number} ({self.booking.room.room_type.value})")
        print(f"Check-in: {self.booking.check_in_date} | Check-out: {self.booking.check_out_date}")
        print("-"*80)
        print(f"Room Rent (₹):                          {self.room_charges:>15,.2f}")
        
        if self.services:
            for service, amount in self.services.items():
                print(f"  {service} (₹):                      {amount:>15,.2f}")
        
        print("-"*80)
        print(f"Subtotal (₹):                           {self.calculate_subtotal():>15,.2f}")
        print()
        print("TAX BREAKDOWN:")
        print(f"  GST @ 12% on Room Rent (₹):          {self.calculate_gst():>15,.2f}")
        print(f"  Service Tax @ 18% on Services (₹):   {self.calculate_service_tax():>15,.2f}")
        
        if self.discount > 0:
            print(f"  Membership Discount (₹):            -{self.discount:>15,.2f}")
        
        print("-"*80)
        print(f"TOTAL AMOUNT DUE (₹):                   {self.calculate_total():>15,.2f}")
        print()
        print(f"Payment Status: {'PAID' if self.paid else 'PENDING'}")
        if self.paid:
            print(f"Payment Method: {self.payment_method.value}")
            print(f"Payment Date: {self.payment_date.strftime('%d-%m-%Y %H:%M:%S')}")
        
        print("="*80)
        print("धन्यवाद! (Thank you!)")
        print("="*80 + "\n")
    
    def to_dict(self) -> Dict:
        """Convert invoice to dictionary"""
        return {
            'invoice_id': self.invoice_id,
            'invoice_number': self.invoice_number,
            'booking_id': self.booking.booking_id,
            'room_charges': self.room_charges,
            'gst': self.calculate_gst(),
            'service_tax': self.calculate_service_tax(),
            'additional_charges': self.additional_charges,
            'services': self.services,
            'discount': self.discount,
            'total': self.calculate_total(),
            'paid': self.paid,
            'payment_method': self.payment_method.value if self.payment_method else None,
            'payment_date': self.payment_date.strftime("%Y-%m-%d %H:%M:%S") if self.payment_date else None
        }


class IndiaLeadHotelManagement:
    """Hotel Management System with India-specific features"""
    
    def __init__(self, hotel_name: str, state_code: str, hotel_gstin: str, 
                 storage_file: str = "india_hotel_data.json"):
        """
        Initialize India-specific hotel management
        
        Args:
            hotel_name (str): Name of the hotel
            state_code (str): Indian state code (MH, DL, KA, etc.)
            hotel_gstin (str): Hotel's GST Identification Number
            storage_file (str): Path to storage file
        """
        self.hotel_name = hotel_name
        self.state_code = state_code
        self.hotel_gstin = hotel_gstin
        self.storage_file = storage_file
        
        self.rooms: List[Room] = []
        self.guests: List[Guest] = []
        self.bookings: List[Booking] = []
        self.invoices: List[Invoice] = []
        
        self.next_guest_id = 1001
        self.next_booking_id = 5001
        self.next_invoice_id = 1
        self.invoice_series = f"{state_code}-{hotel_name[:3].upper()}"
        
        self.load_data()
    
    def add_room(self, room_number: int, room_type: RoomType, 
                 price_per_night: float, capacity: int, ac_type: str = "Window AC") -> Optional[Room]:
        """Add a room to the hotel"""
        if self.find_room(room_number):
            print(f"✗ कक्ष {room_number} पहले से मौजूद है")
            return None
        
        room = Room(room_number, room_type, price_per_night, capacity, ac_type)
        self.rooms.append(room)
        print(f"✓ कक्ष {room_number} जोड़ा गया: {room_type.value} - ₹{price_per_night}/रात")
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
    
    def register_guest(self, name: str, email: str, phone: str, 
                      category: GuestCategory, id_type: str = "Aadhar", 
                      id_number: str = "") -> Optional[Guest]:
        """Register a new guest"""
        guest = Guest(self.next_guest_id, name, email, phone, category, id_type, id_number)
        self.guests.append(guest)
        self.next_guest_id += 1
        print(f"✓ अतिथि पंजीकृत: {guest.name} ({category.value})")
        return guest
    
    def get_available_rooms(self, check_in: str, check_out: str) -> List[Room]:
        """Get available rooms for a date range"""
        available = []
        
        try:
            check_in_date = datetime.strptime(check_in, "%d-%m-%Y")
            check_out_date = datetime.strptime(check_out, "%d-%m-%Y")
        except ValueError:
            print("✗ गलत तारीख प्रारूप (उपयोग करें: DD-MM-YYYY)")
            return available
        
        for room in self.rooms:
            if room.status == RoomStatus.AVAILABLE:
                is_available = True
                for booking in self.bookings:
                    if booking.room.room_number == room.room_number:
                        if booking.status != BookingStatus.CANCELLED:
                            booking_in = datetime.strptime(booking.check_in_date, "%d-%m-%Y")
                            booking_out = datetime.strptime(booking.check_out_date, "%d-%m-%Y")
                            
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
            print(f"✗ अतिथि {guest_id} नहीं मिला")
            return None
        
        room = self.find_room(room_number)
        if not room:
            print(f"✗ कक्ष {room_number} नहीं मिला")
            return None
        
        available = self.get_available_rooms(check_in, check_out)
        if room not in available:
            print(f"✗ कक्ष {room_number} इस तारीख के लिए उपलब्ध नहीं है")
            return None
        
        booking = Booking(self.next_booking_id, guest, room, check_in, check_out)
        self.bookings.append(booking)
        self.next_booking_id += 1
        print(f"✓ बुकिंग बनाई गई: {booking}")
        return booking
    
    def check_in_guest(self, booking_id: int) -> bool:
        """Check in a guest"""
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                if booking.check_in():
                    print(f"✓ अतिथि {booking.guest.name} कक्ष {booking.room.room_number} में चेक-इन हुए")
                    return True
        print(f"✗ बुकिंग {booking_id} नहीं मिली")
        return False
    
    def check_out_guest(self, booking_id: int) -> bool:
        """Check out a guest"""
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                if booking.status == BookingStatus.CHECKED_IN:
                    booking.check_out()
                    print(f"✓ अतिथि {booking.guest.name} कक्ष {booking.room.room_number} से चेक-आउट हुए")
                    return True
        print(f"✗ बुकिंग {booking_id} नहीं मिली या चेक-इन नहीं है")
        return False
    
    def generate_invoice(self, booking_id: int) -> Optional[Invoice]:
        """Generate GST-compliant invoice"""
        booking = None
        for b in self.bookings:
            if b.booking_id == booking_id:
                booking = b
                break
        
        if not booking:
            print(f"✗ बुकिंग {booking_id} नहीं मिली")
            return None
        
        invoice_number = f"{self.invoice_series}-{self.next_invoice_id:06d}"
        invoice = Invoice(self.next_invoice_id, invoice_number, booking)
        
        # Apply membership discount
        discount = booking.guest.get_discount_percentage()
        if discount > 0:
            discount_amount = (booking.total_price * discount) / 100
            invoice.apply_discount(discount_amount)
        
        self.invoices.append(invoice)
        self.next_invoice_id += 1
        print(f"✓ चालान बनाया गया: {invoice_number}")
        return invoice
    
    def process_payment(self, invoice_id: int, method: PaymentMethod, amount: float) -> bool:
        """Process payment in INR"""
        for invoice in self.invoices:
            if invoice.invoice_id == invoice_id:
                invoice.process_payment(method)
                print(f"✓ भुगतान प्रसंस्कृत: चालान #{invoice.invoice_number}")
                print(f"  राशि: ₹{amount:,.2f}")
                print(f"  विधि: {method.value}")
                return True
        print(f"✗ चालान {invoice_id} नहीं मिला")
        return False
    
    def clean_room(self, room_number: int) -> bool:
        """Mark room as cleaned and available"""
        room = self.find_room(room_number)
        if room:
            room.set_status(RoomStatus.AVAILABLE)
            room.housekeeping_status = "Clean"
            room.last_cleaned = datetime.now()
            print(f"✓ कक्ष {room_number} सफाई के बाद तैयार है")
            return True
        return False
    
    def get_occupancy_rate(self) -> float:
        """Calculate current occupancy rate"""
        occupied = sum(1 for room in self.rooms if room.status == RoomStatus.OCCUPIED)
        total = len(self.rooms)
        return (occupied / total * 100) if total > 0 else 0
    
    def get_revenue(self, start_date: str = None, end_date: str = None) -> float:
        """Calculate total revenue in INR"""
        revenue = 0
        for invoice in self.invoices:
            if invoice.paid:
                if start_date and end_date:
                    payment_date = datetime.strptime(invoice.payment_date, "%Y-%m-%d %H:%M:%S")
                    start = datetime.strptime(start_date, "%d-%m-%Y")
                    end = datetime.strptime(end_date, "%d-%m-%Y")
                    if start <= payment_date <= end:
                        revenue += invoice.calculate_total()
                else:
                    revenue += invoice.calculate_total()
        return revenue
    
    def get_gst_collected(self) -> float:
        """Calculate total GST collected"""
        gst = 0
        for invoice in self.invoices:
            if invoice.paid:
                gst += invoice.calculate_gst()
        return gst
    
    def display_dashboard(self):
        """Display comprehensive hotel dashboard"""
        occupied = sum(1 for room in self.rooms if room.status == RoomStatus.OCCUPIED)
        available = sum(1 for room in self.rooms if room.status == RoomStatus.AVAILABLE)
        maintenance = sum(1 for room in self.rooms if room.status == RoomStatus.MAINTENANCE)
        cleaning = sum(1 for room in self.rooms if room.status == RoomStatus.CLEANING)
        
        total_revenue = self.get_revenue()
        gst_collected = self.get_gst_collected()
        occupancy = self.get_occupancy_rate()
        
        print("\n" + "="*90)
        print(f"🏨 {self.hotel_name.upper()} - प्रबंधन डैशबोर्ड (DASHBOARD)")
        print(f"राज्य: {self.state_code} | GSTIN: {self.hotel_gstin}")
        print("="*90)
        
        print("\n📊 कक्ष स्थिति (ROOM STATUS):")
        print(f"  कुल कक्ष (Total):      {len(self.rooms)}")
        print(f"  कब्जे में (Occupied):  {occupied}")
        print(f"  उपलब्ध (Available):    {available}")
        print(f"  रखरखाव (Maintenance):  {maintenance}")
        print(f"  सफाई (Cleaning):       {cleaning}")
        print(f"  अधिभोग दर (Occupancy): {occupancy:.1f}%")
        
        print("\n👥 अतिथि और बुकिंग (GUESTS & BOOKINGS):")
        print(f"  कुल अतिथि (Total Guests):     {len(self.guests)}")
        print(f"  कुल बुकिंग (Total Bookings):   {len(self.bookings)}")
        print(f"  पुष्टि (Confirmed):            {sum(1 for b in self.bookings if b.status == BookingStatus.CONFIRMED)}")
        print(f"  चेक-इन (Checked In):          {sum(1 for b in self.bookings if b.status == BookingStatus.CHECKED_IN)}")
        print(f"  चेक-आउट (Checked Out):        {sum(1 for b in self.bookings if b.status == BookingStatus.CHECKED_OUT)}")
        
        print("\n💰 वित्तीय (FINANCIAL):")
        print(f"  कुल राजस्व (Total Revenue):     ₹{total_revenue:,.2f}")
        print(f"  एकत्रित जीएसटी (GST Collected): ₹{gst_collected:,.2f}")
        print(f"  कुल चालान (Total Invoices):    {len(self.invoices)}")
        print(f"  भुगतान (Paid):                ₹{sum(i.calculate_total() for i in self.invoices if i.paid):,.2f}")
        print(f"  लंबित (Pending):              ₹{sum(i.calculate_total() for i in self.invoices if not i.paid):,.2f}")
        
        print("\n🎖️ अतिथि श्रेणी (GUEST CATEGORIES):")
        domestic = sum(1 for g in self.guests if g.category == GuestCategory.DOMESTIC)
        foreign = sum(1 for g in self.guests if g.category == GuestCategory.FOREIGN)
        corporate = sum(1 for g in self.guests if g.category == GuestCategory.CORPORATE)
        print(f"  घरेलू (Domestic):    {domestic}")
        print(f"  विदेशी (Foreign):    {foreign}")
        print(f"  कॉर्पोरेट (Corporate): {corporate}")
        
        print("="*90 + "\n")
    
    def save_data(self) -> bool:
        """Save all data to file"""
        try:
            data = {
                'hotel_name': self.hotel_name,
                'state_code': self.state_code,
                'hotel_gstin': self.hotel_gstin,
                'rooms': [room.to_dict() for room in self.rooms],
                'guests': [guest.to_dict() for guest in self.guests],
                'bookings': [booking.to_dict() for booking in self.bookings],
                'invoices': [invoice.to_dict() for invoice in self.invoices],
                'next_guest_id': self.next_guest_id,
                'next_booking_id': self.next_booking_id,
                'next_invoice_id': self.next_invoice_id,
                'last_saved': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"✗ डेटा सहेजने में त्रुटि: {str(e)}")
            return False
    
    def load_data(self) -> bool:
        """Load data from file"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.next_guest_id = data.get('next_guest_id', 1001)
                    self.next_booking_id = data.get('next_booking_id', 5001)
                    self.next_invoice_id = data.get('next_invoice_id', 1)
                return True
            return True
        except Exception as e:
            print(f"✗ डेटा लोड करने में त्रुटि: {str(e)}")
            return False


# Demo and Example Usage
if __name__ == "__main__":
    print("\n" + "="*90)
    print("🏨 भारतीय होटल प्रबंधन प्रणाली (INDIA LEAD ROLE HOTEL MANAGEMENT SYSTEM)")
    print("डेमो मोड (DEMO MODE)")
    print("="*90 + "\n")
    
    # Initialize hotel
    hotel = IndiaLeadHotelManagement(
        "TajView",
        state_code="MH",
        hotel_gstin="27AABCT1234H1Z0"
    )
    
    # Add rooms
    print("➕ कक्ष जोड़े जा रहे हैं (Adding Rooms)...\n")
    hotel.add_room(101, RoomType.ECONOMY, 3000, 1, "Window AC")
    hotel.add_room(102, RoomType.STANDARD, 4500, 2, "Split AC")
    hotel.add_room(103, RoomType.DELUXE, 6500, 2, "Split AC")
    hotel.add_room(201, RoomType.SUPER_DELUXE, 8500, 3, "Central AC")
    hotel.add_room(202, RoomType.SUITE, 12000, 4, "Central AC")
    hotel.add_room(301, RoomType.LUXURY_SUITE, 18000, 4, "Central AC")
    hotel.add_room(401, RoomType.PRESIDENTIAL, 30000, 6, "Central AC")
    
    # Register guests
    print("\n👥 अतिथियों को पंजीकृत किया जा रहा है (Registering Guests)...\n")
    guest1 = hotel.register_guest(
        "राज कुमार",
        "raj@email.com",
        "9876543210",
        GuestCategory.DOMESTIC,
        "Aadhar",
        "1234-5678-9012"
    )
    
    guest2 = hotel.register_guest(
        "प्रिया शर्मा",
        "priya@email.com",
        "9987654321",
        GuestCategory.CORPORATE,
        "PAN",
        "ABCDE1234F"
    )
    
    guest3 = hotel.register_guest(
        "जॉन स्मिथ",
        "john@email.com",
        "9876543211",
        GuestCategory.FOREIGN,
        "Passport",
        "A12345678"
    )
    
    # Create bookings
    print("\n📅 बुकिंग बनाई जा रही है (Creating Bookings)...\n")
    booking1 = hotel.create_booking(guest1.guest_id, 101, "15-07-2026", "18-07-2026")
    booking2 = hotel.create_booking(guest2.guest_id, 202, "16-07-2026", "19-07-2026")
    booking3 = hotel.create_booking(guest3.guest_id, 301, "20-07-2026", "25-07-2026")
    
    # Check in guests
    print("\n✓ अतिथियों का चेक-इन किया जा रहा है (Checking In Guests)...\n")
    hotel.check_in_guest(booking1.booking_id)
    hotel.check_in_guest(booking2.booking_id)
    
    # Generate invoices with services
    print("\n💳 चालान बनाए जा रहे हैं (Generating Invoices)...\n")
    invoice1 = hotel.generate_invoice(booking1.booking_id)
    invoice1.add_service_charge("कमरा सेवा (Room Service)", 500)
    invoice1.add_service_charge("लॉन्ड्री (Laundry)", 300)
    invoice1.display_invoice()
    
    invoice2 = hotel.generate_invoice(booking2.booking_id)
    invoice2.add_service_charge("स्पा (Spa)", 2000)
    invoice2.add_service_charge("डिनर (Dinner)", 1500)
    invoice2.display_invoice()
    
    # Process payments
    print("\n💰 भुगतान प्रसंस्कृत किए जा रहे हैं (Processing Payments)...\n")
    hotel.process_payment(invoice1.invoice_id, PaymentMethod.UPI, invoice1.calculate_total())
    hotel.process_payment(invoice2.invoice_id, PaymentMethod.CREDIT_CARD, invoice2.calculate_total())
    
    # Check out guests
    print("\n🚪 अतिथियों का चेक-आउट किया जा रहा है (Checking Out Guests)...\n")
    hotel.check_out_guest(booking1.booking_id)
    hotel.check_out_guest(booking2.booking_id)
    
    # Clean rooms
    print("🧹 कक्षों की सफाई की जा रही है (Cleaning Rooms)...\n")
    hotel.clean_room(101)
    hotel.clean_room(202)
    
    # Display dashboard
    hotel.display_dashboard()
    
    # Save data
    print("💾 डेटा सहेजा जा रहा है (Saving Data)...\n")
    hotel.save_data()
    
    print("✓ डेमो सफल रहा! (Demo Completed Successfully!)")
