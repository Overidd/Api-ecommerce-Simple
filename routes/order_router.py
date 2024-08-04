from flask import Blueprint, request
from controllers.order_controller import OrderController
from utils.jwt_identity_rol import role_required

order_router = Blueprint('order_router', __name__)
controller = OrderController()


@order_router.post('/create')
def create_purchase():
   json = request.json
   return controller.create(json)

@order_router.delete('/cancel/<int:id>')
def cancel_order(id):
   return controller.cancel(id)

@order_router.get('/get_all')
@role_required()
def get_all_orders():
   return controller.get_all()
