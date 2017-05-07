from django.contrib.auth.models import User
from django.db import models
from customers.models import Account
from product.models import Product
from decimal import Decimal

from django.db.models.signals import pre_save, post_save, post_delete


FLAT_SHIPPING_COST = Decimal('9.90')
TAX_PERCENTAGE = Decimal('12.50')





class CartItem(models.Model):
    """
    A single product in a Cart, having a quantity.
    """
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,  on_delete=models.CASCADE,help_text='Product in a cart')
    quantity = models.PositiveIntegerField(default=1, help_text='Quantity of this product.')
    date_added = models.DateTimeField(auto_now_add=True, help_text='Date that this product was added to the cart.')
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['date_added']

    def __unicode__(self):
        return u'%i of %s' % (self.quantity, self.product.name)
    def __str__(self):
        return '%s : %d : %s' % (self.cart,self.id,self.product.sku)
    

    @property
    def total_price(self):
        return self.quantity * self.product.selling_price

def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = int(instance.quantity)
    if qty >= 1:
        price = instance.product.get_price()
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total
    instance.cart.update_subtotal()

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()
    instance.cart.update_cart_items()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


       

class Cart(models.Model):
    """
    Shopping cart belonging to a Customer, and containing CartItems.
    """
    # TODO - Do we need to store a status field for carts?
    # TODO - Do we want to allow carts to be owned by anonymous users?
    # TODO - Add Voucher support
    # TODO - Is a customer allowed to have multiple carts?
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    #items = models.ManyToManyField(Product, through=CartItem)
    cart_items = models.TextField(max_length=2500)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    items_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    #tax_percentage  = models.DecimalField(max_digits=10, decimal_places=5, default=0.085)
    tax = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    shipping = models.DecimalField(max_digits=50, decimal_places=2, default=0.00) 
    total_price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['date_created']

    def __unicode__(self):
        return u'%s\'s Cart' % self.id
    
    def __str__(self):
        return '%s' % (self.customer.user)


    def update_subtotal(self):
        subtotal = 0
        #items = self.items.all()
        items=CartItem.objects.filter(cart=self)

        #print(items)
        for item in items:
            subtotal += item.line_item_total
        self.items_total=subtotal
        #print(self.items_total)
        self.save()
    
    def get_items(self):
        items=CartItem.objects.filter(cart=self)
        return items

    def get_items_count(self):
        count=CartItem.objects.filter(cart=self).count()
        return count

    
    def update_cart_items(self):
        itemlist=CartItem.objects.filter(cart=self)
        item_details=[]
        for item in itemlist:
            item_details.append((item.product.sku + " " + str(item.quantity) +
                "  " + str(item.line_item_total)))
        self.cart_items = item_details
        #print(self.cart_items)
        self.save()    
        #return item_details        
        

    
    # TODO - Add ability to merge with any existing quantities of the product.
    def add_product(self, product, quantity=1):
        for cartitem in self.cartitems.all():
            if cartitem.product == product:
                cartitem.quantity += quantity
                
            
        cart_item = CartItem(product=product, quantity=quantity, cart=self)
        cart_item.save()



def do_tax_and_total_receiver(sender, instance, *args, **kwargs):
    items_total = Decimal(instance.items_total)
    tax_total = round(items_total * Decimal(TAX_PERCENTAGE), 2)/100 #8.5%
    ##print (instance.tax_percentage)
    total = round(items_total + Decimal(tax_total), 2)
    instance.tax = tax_total
    instance.total_price = total
    #instance.save()



pre_save.connect(do_tax_and_total_receiver, sender=Cart)
'''
    NW: New
    DD: Dispatched
    PR: Payment Received
    CT: Complete

'''
ORDER_STATUS=(
    ("NW","New Order"),
    ("PP", "Payment Pending"), 
    ("PP", "Payment Received"),
    ("OC", "Order Complete"),
    )
PAYMENT_MODE=(
    ("POD","Payment On Delivery"),
    ("ONLINE", "On-line Banking"), 
    ("CARD", "Card Payment"),
    )

class Order(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email=    models.EmailField(max_length=100)
    phone=    models.CharField(max_length=100)
    pincode =  models.CharField(max_length=100)
    house=  models.CharField(max_length=250)
    street=  models.CharField(max_length=250)
    place =  models.CharField(max_length=150)
    city =  models.CharField(max_length=150)
    state =  models.CharField(max_length=150)
    
    order_items = models.TextField(max_length=2500)
    tax = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    shipping = models.DecimalField(max_digits=50, decimal_places=2, default=0.00) 
    order_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    payment_mode = models.CharField(max_length=100,choices=PAYMENT_MODE,default="POD")
    order_status = models.CharField(max_length=100,choices=ORDER_STATUS,default="NW")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%d : %s' % (self.id,self.customer.user)


