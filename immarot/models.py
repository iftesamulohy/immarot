from django.db import models
from datetime import datetime

from users.models import Users

# Create your models here.
class BaseModel(models.Model):
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    active = models.CharField(
        max_length=3,  # Length of "Yes" or "No"
        choices=YES_NO_CHOICES,
        default='Yes',  # Default value
        verbose_name="Active?"
    )
    class Meta:
        abstract = True  # Marks this as an abstract base class

class ProjectLocation(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="Location Name")
    showable_fields = ['id','name', 'active']

    class Meta:
        verbose_name = "Project Location"
        verbose_name_plural = "Project Locations"

    def __str__(self):
        return self.name
class Project(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    project_location = models.ForeignKey(ProjectLocation, verbose_name="Project Location",on_delete=models.CASCADE)
    address = models.CharField(max_length=255, verbose_name="Address")
    facing = models.CharField(max_length=255, blank=True, null=True, verbose_name="Facing")
    building_height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Building Height (m)")
    land_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Land Area (sq.m)")
    project_launching_date = models.DateField(blank=True, null=True, verbose_name="Project Launching Date")
    project_hand_over_date = models.DateField(blank=True, null=True, verbose_name="Project Hand Over Date")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    showable_fields = ['id','name', 'project_location', 'address', 'facing', 'building_height', 'land_area', 'project_launching_date', 'project_hand_over_date', 'description', 'active']

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name
    
##Leads model
class LeadStatus(BaseModel):
    name = models.CharField(max_length=255)

    showable_fields = ['id', 'name']  # Add showable fields here

    def __str__(self):
        return self.name


class LeadSource(BaseModel):
    name = models.CharField(max_length=255)

    showable_fields = ['id', 'name','active']  # Add showable fields here

    def __str__(self):
        return self.name

class Lead(BaseModel):
    title = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    lead_status = models.ForeignKey(LeadStatus, on_delete=models.CASCADE, related_name="leads")
    lead_source = models.ForeignKey(LeadSource, on_delete=models.CASCADE, related_name="leads")
    phone = models.CharField(max_length=15)
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="leads")
    description = models.TextField(blank=True, null=True)
    organization_name = models.CharField(max_length=255)
    email = models.EmailField()
    assign_to_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="assigned_leads")
    

    showable_fields = ['id', 'title', 'customer_name', 'lead_status', 'lead_source', 'phone', 'project_name', 'description', 'organization_name', 'email', 'assign_to_user', 'active']

    def __str__(self):
        return self.title
    
class Product(BaseModel):
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="products", verbose_name="Project Name")
    flat_type = models.CharField(max_length=255, verbose_name="Flat Type")
    floor_number = models.IntegerField(verbose_name="Floor Number")
    flat_size = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Flat Size (sq.m)")
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Unit Price")
    total_flat_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Total Flat Price")
    car_parking_charge = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Car Parking Charge")
    utility_charge = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Utility Charge")
    additional_work_charge = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Additional Work Charge")
    other_charge = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Other Charge")
    deduction_discount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Deduction/Discount")
    refund_additional_work_charge = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Refund Additional Work Charge")
    net_sales_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Net Sales (Flat) Price")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    product_image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Product Image")
    

    showable_fields = ['id', 'project_name', 'flat_type', 'floor_number', 'flat_size', 'unit_price', 'total_flat_price', 
                        'car_parking_charge', 'utility_charge', 'additional_work_charge', 'other_charge', 'deduction_discount',
                        'refund_additional_work_charge', 'net_sales_price', 'description', 'product_image', 'active']

    def __str__(self):
        return f"{self.project_name.name} - {self.flat_type} ({self.floor_number})"
    

class Customer(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Customer Name")
    father_or_husband_name = models.CharField(max_length=255, verbose_name="Father's or Husband's Name")
    phone = models.CharField(max_length=15, verbose_name="Phone")
    email = models.EmailField(verbose_name="Customer Email")
    mailing_address = models.TextField(verbose_name="Mailing Address")
    nid = models.CharField(max_length=50, verbose_name="National ID (NID)")
    

    showable_fields = ['id', 'name', 'father_or_husband_name', 'phone', 'email', 'mailing_address', 'nid', 'active']

    def __str__(self):
        return self.name
class Seller(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")


    showable_fields = ['id', 'name', 'description', 'active']

    def __str__(self):
        return self.name  
    
class Sell(BaseModel):
    customer_name = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name="sales", 
        verbose_name="Customer Name"
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name="sales", 
        verbose_name="Project"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="sales", 
        verbose_name="Product"
    )
    seller_name = models.ForeignKey(
        Seller, 
        on_delete=models.CASCADE, 
        related_name="sales", 
        verbose_name="Seller Name"
    )
    date = models.DateField(verbose_name="Date")

    showable_fields = ['id', 'customer_name', 'project', 'product', 'seller_name', 'date', 'active']

    def __str__(self):
        return f"Sell to {self.customer_name} on {self.date}"

class Vendor(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")
    mailing_address = models.TextField(verbose_name="Mailing Address")
    date = models.DateField(verbose_name="Date")
    website = models.URLField(blank=True, null=True, verbose_name="Website")
    phone = models.CharField(max_length=15, verbose_name="Phone")
    email = models.EmailField(verbose_name="Email")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    showable_fields = [
        'id', 'name', 'mailing_address', 'date', 'website', 'phone', 
        'email', 'description', 'active'
    ]

    def __str__(self):
        return self.name
    
class Contractor(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")
    mailing_address = models.TextField(verbose_name="Mailing Address")
    date = models.DateField(verbose_name="Date")
    website = models.URLField(blank=True, null=True, verbose_name="Website")
    phone = models.CharField(max_length=15, verbose_name="Phone")
    email = models.EmailField(verbose_name="Email")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
   

    showable_fields = [
        'id', 'name', 'mailing_address', 'date', 'website', 'phone', 
        'email', 'description', 'active'
    ]

    def __str__(self):
        return self.name