from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200, help_text="Name or description of the product")
    sku = models.CharField(max_length=50, unique=True, help_text="Unique Product Code (Stock Keeping Unit, barcode)")
    manufacturer = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Product's selling price")
    
    current_stock = models.PositiveIntegerField(default=0, help_text="Current quantity in stock")
    minimum_stock = models.PositiveIntegerField(default=5, help_text="Minimum level for low stock alert")
    
    # Specific fields for product specifications
    processor = models.CharField(max_length=100, blank=True)
    ram = models.CharField(max_length=50, blank=True, help_text="e.g., 8GB, 16GB")
    storage = models.CharField(max_length=100, blank=True, help_text="e.g., 256GB SSD, 1TB HDD")
    screen_size = models.CharField(max_length=50, blank=True, help_text="e.g., 6.1 inches, 27-inch")
    camera_resolution = models.CharField(max_length=50, blank=True, help_text="e.g., 12MP, 108MP")
    operating_system = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)
    power_supply = models.CharField(max_length=50, blank=True, help_text="e.g., 127V, 220V, Bivolt")
    connectivity = models.TextField(blank=True, help_text="e.g., Wi-Fi, Bluetooth, Ethernet")
    ports = models.TextField(blank=True, help_text="e.g., USB-C, HDMI, P2")
    build_material = models.CharField(max_length=100, blank=True)
    weight = models.CharField(max_length=50, blank=True, help_text="e.g., 1.2kg, 220g")

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.sku})"

class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = 'IN', 'In'
        OUT = 'OUT', 'Out'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
    quantity = models.PositiveIntegerField()
    movement_type = models.CharField(max_length=3, choices=MovementType.choices)
    
    # The user who performed the movement
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="stock_movements")
    
    # The date reported by the user, not the system timestamp
    movement_date = models.DateTimeField(help_text="Date of the movement, as reported by the user")
    
    notes = models.TextField(blank=True, help_text="Additional notes (e.g., reason for movement, invoice number)")

    def __str__(self):
        return f"{self.get_movement_type_display()} of {self.quantity}x {self.product.name}"
