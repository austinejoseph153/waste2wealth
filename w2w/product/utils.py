from decimal import Decimal

def get_cartitem_total_cost(cart_items):
    sub_total = Decimal(0.0)
    quantity = 0
    for cart_item in cart_items:
        sub_total+= cart_item.calculate_amount()
        quantity+=cart_item.quantity
    
    return{
        "quantity":quantity,
        "sub_total":sub_total 
    }

def delete_cart_items(cart_items, cart):
    for cart_item in cart_items:
        cart_item.delete()
    cart.delete()