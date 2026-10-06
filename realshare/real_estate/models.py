from django.db import models
from django.contrib.auth.models import User


class Investment(models.Model):
    property = models.ForeignKey("real_estate.Property", on_delete=models.CASCADE)
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Property(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="properties/")
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="real_estate_properties"  # Distinct related_name
    )
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class SellerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="real_estate_seller_profile"  # Distinct related_name
    )
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="real_estate_transactions"  # Distinct related_name
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction by {self.buyer} on {self.date}"
seller = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="investment_properties",
    null=True,  # Field can be null in the database
    blank=True  # Field can be empty in forms
)
