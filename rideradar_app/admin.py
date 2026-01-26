from django.contrib import admin
from .models import (
    UserProfile, Vehicle, Route, RouteStop, Ticket, Trip,
    Payment, Notification, VehicleRating, TrafficAlert, SafetyAlert
)


# ===== USER ADMIN =====

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'is_verified', 'preferred_payment_method', 'created_at']
    list_filter = ['is_verified', 'preferred_payment_method', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'phone', 'is_verified')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'profile_picture', 'bio')
        }),
        ('Addresses', {
            'fields': ('home_address', 'work_address', 'default_latitude', 'default_longitude')
        }),
        ('Preferences', {
            'fields': ('preferred_payment_method', 'notification_enabled', 'smart_alerts_enabled', 'alert_notification_minutes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ===== VEHICLE ADMIN =====

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'vehicle_type', 'status', 'current_occupancy', 'total_seats', 'is_live', 'last_updated']
    list_filter = ['vehicle_type', 'status', 'is_live', 'created_at']
    search_fields = ['registration_number', 'make_model']
    readonly_fields = ['created_at', 'last_updated']
    
    fieldsets = (
        ('Vehicle Details', {
            'fields': ('registration_number', 'vehicle_type', 'make_model', 'year_manufactured')
        }),
        ('Capacity', {
            'fields': ('total_seats', 'current_occupancy')
        }),
        ('Location & Status', {
            'fields': ('current_latitude', 'current_longitude', 'status', 'is_live')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_updated'),
            'classes': ('collapse',)
        }),
    )


# ===== ROUTE ADMIN =====

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['route_number', 'route_name', 'starting_point', 'ending_point', 'base_fare', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['route_number', 'route_name', 'starting_point', 'ending_point']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Route Details', {
            'fields': ('route_number', 'route_name', 'starting_point', 'ending_point', 'description')
        }),
        ('Route Metrics', {
            'fields': ('distance_km', 'estimated_duration_minutes', 'base_fare')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ['route', 'stop_number', 'stop_name', 'estimated_arrival_from_start']
    list_filter = ['route', 'stop_number']
    search_fields = ['stop_name', 'route__route_number']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Stop Details', {
            'fields': ('route', 'stop_name', 'stop_number')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Timing', {
            'fields': ('estimated_arrival_from_start',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# ===== TICKET & TRIP ADMIN =====

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'user', 'route', 'journey_date', 'status', 'payment_status', 'fare']
    list_filter = ['status', 'payment_status', 'payment_method', 'journey_date', 'created_at']
    search_fields = ['reference_number', 'qr_code', 'user__username', 'route__route_number']
    readonly_fields = ['qr_code', 'reference_number', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Ticket Info', {
            'fields': ('reference_number', 'qr_code', 'user', 'status')
        }),
        ('Route & Journey', {
            'fields': ('route', 'vehicle', 'boarding_stop', 'destination_stop', 'journey_date', 'journey_time')
        }),
        ('Passenger Details', {
            'fields': ('passenger_count', 'special_requests')
        }),
        ('Payment', {
            'fields': ('fare', 'payment_method', 'payment_status')
        }),
        ('Timing', {
            'fields': ('booked_at', 'estimated_arrival', 'actual_arrival', 'completed_at', 'cancelled_at', 'cancellation_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['user', 'route', 'vehicle', 'status', 'start_time', 'eta_minutes', 'rating']
    list_filter = ['status', 'start_time', 'rating']
    search_fields = ['user__username', 'route__route_number', 'vehicle__registration_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Trip Info', {
            'fields': ('user', 'ticket', 'vehicle', 'route', 'status')
        }),
        ('Route Details', {
            'fields': ('boarding_stop', 'destination_stop', 'start_time', 'end_time')
        }),
        ('Real-time Data', {
            'fields': ('current_latitude', 'current_longitude', 'eta_minutes', 'distance_remaining_km')
        }),
        ('Feedback', {
            'fields': ('rating', 'review')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ===== PAYMENT ADMIN =====

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'user', 'amount', 'currency', 'payment_method', 'status', 'initiated_at']
    list_filter = ['payment_method', 'status', 'initiated_at']
    search_fields = ['transaction_id', 'user__username', 'mpesa_reference', 'phone_number']
    readonly_fields = ['initiated_at', 'completed_at']
    
    fieldsets = (
        ('Payment Info', {
            'fields': ('ticket', 'user', 'transaction_id', 'status')
        }),
        ('Amount', {
            'fields': ('amount', 'currency')
        }),
        ('Method', {
            'fields': ('payment_method', 'mpesa_reference', 'phone_number')
        }),
        ('Details', {
            'fields': ('description', 'metadata')
        }),
        ('Timestamps', {
            'fields': ('initiated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


# ===== NOTIFICATION ADMIN =====

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at', 'read_at']
    
    fieldsets = (
        ('Notification Info', {
            'fields': ('user', 'title', 'notification_type', 'is_read')
        }),
        ('Content', {
            'fields': ('message',)
        }),
        ('Relations', {
            'fields': ('trip', 'ticket'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'read_at'),
            'classes': ('collapse',)
        }),
    )


# ===== RATING ADMIN =====

@admin.register(VehicleRating)
class VehicleRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle', 'overall', 'cleanliness', 'driver_behavior', 'safety', 'is_verified_trip', 'created_at']
    list_filter = ['overall', 'is_verified_trip', 'created_at']
    search_fields = ['user__username', 'vehicle__registration_number', 'review']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Rating Info', {
            'fields': ('user', 'vehicle', 'trip', 'is_verified_trip')
        }),
        ('Ratings', {
            'fields': ('cleanliness', 'driver_behavior', 'safety', 'overall')
        }),
        ('Review', {
            'fields': ('review',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# ===== ALERTS ADMIN =====

@admin.register(TrafficAlert)
class TrafficAlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'alert_type', 'alert_level', 'affected_area', 'is_active', 'expected_delay_minutes', 'created_at']
    list_filter = ['alert_type', 'alert_level', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'affected_area']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Alert Details', {
            'fields': ('title', 'description', 'alert_type', 'alert_level')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'affected_area')
        }),
        ('Impact', {
            'fields': ('expected_delay_minutes', 'is_active', 'routes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SafetyAlert)
class SafetyAlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'severity', 'affected_area', 'is_active', 'created_at']
    list_filter = ['severity', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'affected_area', 'recommended_action']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Alert Details', {
            'fields': ('title', 'description', 'severity')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'affected_area')
        }),
        ('Action', {
            'fields': ('recommended_action', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )


# Customize Admin Site
admin.site.site_header = "RideRadar Admin"
admin.site.site_title = "RideRadar Administration"
admin.site.index_title = "Welcome to RideRadar Admin Dashboard"
