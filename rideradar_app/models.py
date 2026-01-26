from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

# ===== CORE USER MODELS =====

class UserProfile(models.Model):
    """Extended user profile for commuters"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # Address & Location
    home_address = models.CharField(max_length=255, blank=True)
    work_address = models.CharField(max_length=255, blank=True)
    default_latitude = models.FloatField(null=True, blank=True)
    default_longitude = models.FloatField(null=True, blank=True)
    
    # Preferences
    preferred_payment_method = models.CharField(
        max_length=20,
        choices=[('onapp', 'On App'), ('cash', 'Cash'), ('mpesa', 'M-Pesa'), ('card', 'Card')],
        default='cash'
    )
    notification_enabled = models.BooleanField(default=True)
    smart_alerts_enabled = models.BooleanField(default=True)
    alert_notification_minutes = models.IntegerField(default=2)
    
    # Account Info
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"


# ===== VEHICLE & FLEET MODELS =====

class Vehicle(models.Model):
    """Public transport vehicle (matatu/bus)"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
        ('offline', 'Offline'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50, choices=[('matatu', 'Matatu'), ('bus', 'Bus'), ('shuttle', 'Shuttle')])
    make_model = models.CharField(max_length=100)
    year_manufactured = models.IntegerField()
    
    # Capacity
    total_seats = models.IntegerField(validators=[MinValueValidator(1)])
    current_occupancy = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Location & Status
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    is_live = models.BooleanField(default=False)
    
    # Tracking
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.registration_number} - {self.vehicle_type}"


class Route(models.Model):
    """Public transport routes"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route_number = models.CharField(max_length=20, unique=True)
    route_name = models.CharField(max_length=255)
    starting_point = models.CharField(max_length=255)
    ending_point = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Route Details
    distance_km = models.FloatField(validators=[MinValueValidator(0.1)])
    estimated_duration_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    base_fare = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['route_number']
    
    def __str__(self):
        return f"Route {self.route_number} - {self.route_name}"


class RouteStop(models.Model):
    """Bus stops along a route"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    stop_name = models.CharField(max_length=255)
    stop_number = models.IntegerField()  # Order in the route
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    # Timing
    estimated_arrival_from_start = models.IntegerField(help_text="Minutes from route start")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['route', 'stop_number']
        unique_together = ['route', 'stop_number']
    
    def __str__(self):
        return f"{self.route.route_number} - Stop {self.stop_number}: {self.stop_name}"


# ===== BOOKING & TICKET MODELS =====

class Ticket(models.Model):
    """Booking/Ticket for a trip"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active/In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='tickets')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    
    # Trip Details
    boarding_stop = models.ForeignKey(RouteStop, on_delete=models.SET_NULL, null=True, related_name='boarding_tickets')
    destination_stop = models.ForeignKey(RouteStop, on_delete=models.SET_NULL, null=True, related_name='destination_tickets')
    journey_date = models.DateField()
    journey_time = models.TimeField()
    
    # Passenger Info
    passenger_count = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    special_requests = models.TextField(blank=True)
    
    # Pricing
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=[('cash', 'Cash'), ('mpesa', 'M-Pesa'), ('card', 'Card')]
    )
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # QR Code & Reference
    qr_code = models.CharField(max_length=100, unique=True)
    reference_number = models.CharField(max_length=50, unique=True)
    
    # Booking Info
    booked_at = models.DateTimeField(auto_now_add=True)
    estimated_arrival = models.DateTimeField(null=True, blank=True)
    actual_arrival = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['route', 'journey_date']),
        ]
    
    def __str__(self):
        return f"Ticket {self.reference_number} - {self.user.get_full_name()}"


class Trip(models.Model):
    """Completed trip record"""
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='trip')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, related_name='trips')
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, related_name='trips')
    
    # Trip Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Route taken
    boarding_stop = models.ForeignKey(RouteStop, on_delete=models.SET_NULL, null=True, related_name='boarding_trips')
    destination_stop = models.ForeignKey(RouteStop, on_delete=models.SET_NULL, null=True, related_name='destination_trips')
    
    # Real-time Data
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)
    eta_minutes = models.IntegerField(default=0)
    distance_remaining_km = models.FloatField(default=0)
    
    # Feedback
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"Trip {self.id} - {self.user.get_full_name()}"


# ===== PAYMENT MODELS =====

class Payment(models.Model):
    """Payment transactions"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('mpesa', 'M-Pesa'),
        ('card', 'Card'),
        ('wallet', 'Wallet'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='KES')
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    
    # Payment Details
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # M-Pesa specific
    mpesa_reference = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Metadata
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timing
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-initiated_at']
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.amount} {self.currency}"


# ===== NOTIFICATION MODELS =====

class Notification(models.Model):
    """User notifications"""
    TYPE_CHOICES = [
        ('trip_alert', 'Trip Alert'),
        ('trip_reminder', 'Trip Reminder'),
        ('driver_message', 'Driver Message'),
        ('system_message', 'System Message'),
        ('promotion', 'Promotion'),
        ('safety_alert', 'Safety Alert'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Relationship
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"


# ===== RATING & REVIEW MODELS =====

class VehicleRating(models.Model):
    """Ratings for vehicles/routes"""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicle_ratings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='ratings')
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, related_name='vehicle_rating', null=True, blank=True)
    
    cleanliness = models.IntegerField(choices=RATING_CHOICES)
    driver_behavior = models.IntegerField(choices=RATING_CHOICES)
    safety = models.IntegerField(choices=RATING_CHOICES)
    overall = models.IntegerField(choices=RATING_CHOICES)
    
    review = models.TextField(blank=True)
    is_verified_trip = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'vehicle', 'trip']
    
    def __str__(self):
        return f"Rating by {self.user.get_full_name()} for {self.vehicle.registration_number}"


# ===== ALERT & INCIDENT MODELS =====

class TrafficAlert(models.Model):
    """Traffic and incident alerts"""
    ALERT_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    ALERT_TYPE_CHOICES = [
        ('congestion', 'Congestion'),
        ('accident', 'Accident'),
        ('roadwork', 'Road Work'),
        ('weather', 'Weather'),
        ('strike', 'Strike'),
        ('police_operation', 'Police Operation'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    routes = models.ManyToManyField(Route, related_name='alerts', blank=True)
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    alert_level = models.CharField(max_length=20, choices=ALERT_LEVEL_CHOICES, default='medium')
    
    # Location
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    affected_area = models.CharField(max_length=255, blank=True)
    
    # Impact
    expected_delay_minutes = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.alert_type}: {self.title}"


class SafetyAlert(models.Model):
    """Safety incidents and warnings"""
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    affected_area = models.CharField(max_length=255)
    
    # Action Items
    recommended_action = models.TextField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Safety Alert: {self.title}"
