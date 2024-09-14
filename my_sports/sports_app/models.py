from django.db import models
from django.utils import timezone


class Userlogin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class Enquiry(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    contact_no = models.CharField(max_length=20)
    parent_name = models.CharField(max_length=100)
    parent_mobile_no = models.CharField(max_length=20)
    parent_email = models.EmailField()
    parent_address = models.TextField()
    weekly_sessions = models.CharField(max_length=1)
    how_did_you_know = models.CharField(max_length=50)
    other_details = models.TextField()
    age=models.CharField(max_length=20)



    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Admisssion

class Register(models.Model):
    admission_no=models.CharField(max_length=100,null=True)
    dob = models.DateField()
    gender = models.CharField(max_length=10,null=True)
    phone = models.CharField(max_length=15,null=True)
    adhar = models.CharField(max_length=12,null=True)
    parentName = models.CharField(max_length=100,null=True)
    mobile = models.CharField(max_length=10,null=True)
    email = models.CharField(max_length=100,null=True)
    place = models.CharField(max_length=500,null=True)  # Comma-separated list of kit items
    address = models.CharField(max_length=100,null=True)
    uniformSize = models.CharField(max_length=15,null=True)
    uniformColor = models.CharField(max_length=100,null=True)
    package = models.CharField(max_length=100,null=True)
    sessions = models.CharField(max_length=100,null=True)
    totalAmount = models.CharField(max_length=100,null=True)
    invoice_ID=models.CharField(max_length=100,null=True)
    date = models.DateField()
    blood_group=models.CharField(max_length=100,null=True)
    payment=models.CharField(max_length=100,null=True)
    balance = models.CharField(max_length=100,null=True)
    batchtime=models.CharField(max_length=100,null=True)
    name=models.CharField(max_length=100,null=True)
    first_name=models.CharField(max_length=100,null=True)
    last_name=models.CharField(max_length=100, null=True)
    doj=models.CharField(max_length=100, null=True)


class AddRegister(models.Model):
    admission_no=models.CharField(max_length=100,null=True)
    dob = models.DateField()
    gender = models.CharField(max_length=10,null=True)
    phone = models.CharField(max_length=15,null=True)
    adhar = models.CharField(max_length=12,null=True)
    parentName = models.CharField(max_length=100,null=True)
    mobile = models.CharField(max_length=10,null=True)
    email = models.CharField(max_length=100,null=True)
    place = models.CharField(max_length=500,null=True)  # Comma-separated list of kit items
    address = models.CharField(max_length=100,null=True)
    uniformSize = models.CharField(max_length=15,null=True)
    uniformColor = models.CharField(max_length=100,null=True)
    package = models.CharField(max_length=100,null=True)
    sessions = models.CharField(max_length=100,null=True)
    totalAmount = models.CharField(max_length=100,null=True)
    invoice_ID=models.CharField(max_length=100,null=True)
    date = models.DateField()
    blood_group=models.CharField(max_length=100,null=True)
    payment=models.CharField(max_length=100,null=True)
    balance = models.CharField(max_length=100,null=True)
    batchtime=models.CharField(max_length=100,null=True)
    name=models.CharField(max_length=100,null=True)
    doj = models.CharField(max_length=100, null=True)
    coachname=models.CharField(max_length=100, null=True)
    coachType=models.CharField(max_length=100, null=True)
    age=models.CharField(max_length=100, null=True)
    dateOfBirth = models.CharField(max_length=20)

#sessions
class Duration(models.Model):
    session = models.CharField(max_length=100)
    weekly_sessions = models.CharField(max_length=100)
    payment = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.session} - {self.weekly_sessions}"

class coachReg(models.Model):
    coachname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    coachType = models.CharField(max_length=100)
    adhar=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    document=models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    password=models.CharField(max_length=100)



class Coach_allocation(models.Model):
    session = models.CharField(max_length=10)
    batchtime = models.CharField(max_length=10)
    coachname = models.CharField(max_length=10)
    coachType= models.CharField(max_length=10)




class KitItem(models.Model):
    brand_name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_stock = models.IntegerField()


class Item_entry(models.Model):
    itemname = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pieces = models.IntegerField()
    purpose=models.CharField(max_length=100)
    Purchase=models.CharField(max_length=100)



class kit_distribution(models.Model):
    selectCustomer = models.CharField(max_length=255)
    admission_no = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    adhar = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    package = models.CharField(max_length=255)
    sessions =models.CharField(max_length=255)
    batchtime = models.CharField(max_length=255)
    totalAmount = models.CharField(max_length=255)
    balance=models.CharField(max_length=255)
    brand_name=models.CharField(max_length=255)
    kit_quantity = models.CharField(max_length=255)
    kitTotalAmount = models.CharField(max_length=255)
    itemname = models.CharField(max_length=255)
    item_quantity = models.CharField(max_length=255)
    itemTotalAmount=models.CharField(max_length=255)
    finalAmount = models.CharField(max_length=255)
    kit=models.CharField(max_length=255)
    item=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    unit_price=models.CharField(max_length=255)
    price=models.CharField(max_length=255)
    receipt=models.CharField(max_length=255)



class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50,null=True)
    utype = models.CharField(max_length=50)



class CricketItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name




class SportsKit(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):
    kit = models.ForeignKey(SportsKit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order for {self.kit.name} - Quantity: {self.quantity}"


class Purchase(models.Model):
    item = models.ForeignKey(KitItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Purchase of {self.item.itemname} on {self.purchased_at}'

class KitPurchase(models.Model):
    kit_name = models.CharField(max_length=255)
    quantity =models.CharField(max_length=255)
    price_per_unit = models.CharField(max_length=255)
    total_cost = models.CharField(max_length=255)
    description= models.CharField(max_length=255)
    company_name=models.CharField(max_length=255)
    date=models.CharField(max_length=255)

class Stock(models.Model):
    product_name = models.CharField(max_length=255)
    quantity =models.CharField(max_length=255)
    price_per_unit = models.CharField(max_length=255)
    total_cost = models.CharField(max_length=255)
    description= models.CharField(max_length=255)
    company_name=models.CharField(max_length=255)
    date=models.CharField(max_length=255)

class Store(models.Model):
    kit_name = models.CharField(max_length=255)
    quantity =models.CharField(max_length=255)
    price_per_unit = models.CharField(max_length=255)
    total_cost = models.CharField(max_length=255)
    description= models.CharField(max_length=255)
    company_name=models.CharField(max_length=255)
    date=models.CharField(max_length=255)







class ItemPurchase(models.Model):
    item_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    price_per_unit = models.CharField(max_length=255)
    total_cost = models.CharField(max_length=255)
    company_name=models.CharField(max_length=255)
    date = models.CharField(max_length=255)


class Supliers(models.Model):
    comapny_name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.PositiveIntegerField()
    email = models.DecimalField(max_digits=10, decimal_places=2)
    other_details=models.CharField(max_length=255)

class Company(models.Model):
    comapny_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    other_details=models.CharField(max_length=255)



class Sale(models.Model):
    name = models.CharField(max_length=255)
    admission_no = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    adhar = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    package = models.CharField(max_length=255)
    sessions = models.CharField(max_length=255)
    batchtime = models.CharField(max_length=255)
    quantity=models.CharField(max_length=255)
    price_per_unit=models.CharField(max_length=255)
    updatedBalance = models.CharField(max_length=255)
    totalCost=models.CharField(max_length=255)
    receipt=models.CharField(max_length=255)
    kit_name=models.CharField(max_length=255)
    productname=models.CharField(max_length=255)
    balance=models.CharField(max_length=255)


class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)




class Customer_sale(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    kit_name = models.CharField(max_length=255)
    price_per_unit = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    totalCost = models.CharField(max_length=255)
    updatedBalance = models.CharField(max_length=255)
    receipt=models.CharField(max_length=255)


class Attendence(models.Model):
    coachname= models.CharField(max_length=100)
    coachType = models.CharField(max_length=100)
    current_date = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    sessions = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    batchtime = models.CharField(max_length=100)
    status=models.CharField(max_length=100)



class Coach_Attendence(models.Model):
    coachname= models.CharField(max_length=100)
    coachType = models.CharField(max_length=100)
    current_date = models.DateField()
    address = models.CharField(max_length=100)
    status=models.CharField(max_length=100)

