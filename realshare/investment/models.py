from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="property_images/")
    price_per_percent = models.FloatField()
    percentage_sold = models.FloatField(default=0)
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="investment_properties"
    )
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Investment(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="investments"
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="buyer_investments"
    )
    amount = models.FloatField()

    def __str__(self):
        return f"Investment by {self.buyer} in {self.property}"


class SellerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="real_estate_sellerprofile"
    )
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction by {self.buyer} on {self.date}"


class RealEstateInvestment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'investment_real_estate_investment'
