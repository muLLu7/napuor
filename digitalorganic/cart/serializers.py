from rest_framework import serializers
from cart.models import Cart, CartItem, Order
from customers.models import Account
from customers.views import CustomerDetail
from product.views import ProductDetail
from django.core.mail import send_mail
import datetime


class CartItemSerializer(serializers.ModelSerializer):
    #product = serializers.HyperlinkedRelatedField(view_name='product-detail',read_only=True)
    #total_price = serializers.CharField( read_only=True)
    #line_item_total = serializers.DecimalField(max_digits=10, decimal_places=2,read_only=True)
    #product_id = serializers.IntegerField(source='Product.id')
    #cart = serializers.IntegerField(read_only=True)
    #customer = serializers.CharField(source='cart.customer')
    item_detail=serializers.CharField(source='product.sku', read_only=True)
    cartitem_id = serializers.CharField(read_only=True,source='id')
    
    class Meta:
        model = CartItem
        fields = ('cartitem_id','cart','product','item_detail', 'quantity','line_item_total' ,'date_added')
        read_only_fields = ('cartitem_id','item_detail','line_item_total',)

    def get_item(self,obj):
        return obj.product.id
        
    def get_item_title(self, obj):
        return "%s" %(obj.product.sku)

    def get_price(self, obj):
        return obj.product.price

    def get_cart(self,obj):
        return obj.cart


    def create(self,validated_data):
        cart_item = CartItem.objects.create(
            cart=validated_data['cart'],
            product=validated_data['product'],
            quantity=validated_data['quantity'],
            #line_item_total=validated_data['line_item_total'],
            )
        #cart_item.cart=self.get_cart_id(self.instance)
        cart_item.save()
        return cart_item    
    def __init__(self, *args, **kwargs):
        super(CartItemSerializer, self).__init__(*args, **kwargs)
        #self.cart = 19    


class CartSerializer(serializers.ModelSerializer):
    #customer = serializers.HyperlinkedRelatedField(view_name='CustomerDetail',read_only=True)
    cart_items = serializers.CharField(read_only=True)
    items_total = serializers.DecimalField(max_digits=10, decimal_places=2,read_only=True)
    shipping = serializers.DecimalField(max_digits=10, decimal_places=2,read_only=True)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2,read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2,read_only=True)
    cart_id = serializers.CharField(source='id',read_only=True)
    '''
    customer = serializers.CharField(source='Customer')
    cartitems = CartItemSerializer(required=False)
    total_price = serializers.CharField(read_only=True)
    shipping_cost = serializers.CharField(read_only=True)
    '''
    class Meta:
        model = Cart
        fields = ('cart_id', 'customer', 'date_created', 'date_modified', 'cart_items', 'items_total',
             'shipping','tax','total_price',)
        read_only_fields = ('cart_id',)
    '''
    def validate(self,data):
        """
        Check that the start is before the stop.
        """
        #customer = Customer.objects.get(customer=self.customer)
        ##print(data['customer'])
        if data['customer'] !=  self.customer:
            raise serializers.ValidationError("Enter current user")
        return data    
    '''




    
class OrderSerializer(serializers.ModelSerializer):
    #order_status = serializers.CharField(max_length=100)
    date_created = serializers.SerializerMethodField()
    date_modified = serializers.SerializerMethodField()   
    order_id = serializers.CharField(source='id',read_only=True)
    pincode =  serializers.CharField(max_length=100)
    house=  serializers.CharField(max_length=250)
    street=  serializers.CharField(max_length=250)
    place =  serializers.CharField(max_length=150)
    city =  serializers.CharField(max_length=150)
    state =  serializers.CharField(max_length=150)
    
    class Meta:
        model = Order
        fields = ('order_id','customer','name','phone','email',
                'house','street','place','city','state','pincode',
                'order_items','tax','shipping' ,'order_total','order_status','payment_mode','date_created','date_modified')
        read_only_fields = ('order_id','name','phone','email',
                            'order_items','tax','shipping' ,'order_total','order_status','date_created','date_modified')   
    
    def get_date_created(self, obj):
        request = self.context.get('request')

        datetime_str = obj.date_created
        new_datetime_str = datetime_str.strftime('%d/%m/%Y--%H:%M:%S')  
        return new_datetime_str


    
    def get_date_modified(self, obj):
        request = self.context.get('request')

        datetime_str = obj.date_modified
        new_datetime_str = datetime_str.strftime('%d/%m/%Y--%H:%M:%S')  
        return new_datetime_str
        