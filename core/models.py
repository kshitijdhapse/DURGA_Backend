from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    branch = models.CharField(max_length=50)
    REQUIRED_FIELDS = ['branch']
    def __str__(self):
        return self.username
    
class FoodItem(models.Model):
    name = models.CharField("Name", max_length=50)
    image = models.ImageField(blank=True,null=True, upload_to='images/')
    description = models.CharField("Description", max_length=200,null=True)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    
    foodchoices=(
        ('Breakfast','Breakfast'),
        ('Sandwich','Sandwich'),
        ('Misal Pav','Misal Pav'),
        ('Dosa','Dosa'),
        ('Pav Bhaji','Pav Bhaji'),
        ('Bhurji','Bhurji'),
        ('Cold Coffee','Cold Coffee'),
        ('Shakes','Shakes'),
        ('Pizza','Pizza'),
        ('Cold Drink','Cold Drink'),
        ('Ice Cream','Ice Cream'),
        ('Mastani','Mastani'),
        )
    category = models.CharField("Category",choices=foodchoices, max_length=50)
    hide = models.BooleanField("Hide", default=False)
    topping = models.CharField("Topping", max_length=50, blank=True, null=True)
    topping_price = models.DecimalField("Topping Price", max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Branch(models.Model):
    branch = models.CharField("Branch",max_length=50)
    owner = models.CharField(max_length=50,null=True,blank=True)
    contact = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit contact number')],
        null=True,blank=True
    )
    def __str__(self):
        return self.branch
    
class BranchMenu(models.Model):
    branch = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.foodname.price
        
        if not self.branch:
            self.branch = self._get_current_user_branch()
        
        super().save(*args, **kwargs)
        
    foodname = models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2,null=True)
    
    def _get_current_user_branch(self):
        # Custom method to retrieve the branch of the logged-in user
        # This is a placeholder; actual implementation will depend on where you are calling save()
        from django.contrib.auth import get_user
        user = get_user()
        return user.branch
        
    def __str__(self):
        return f"{self.foodname} at {self.branch}"
