from flask import Blueprint, request, jsonify
from controllers.product_controller import ProductController
from utils.jwt_identity_rol import role_required

product_router = Blueprint('product_router', __name__)
controller = ProductController()

@product_router.post('/create')
@role_required()
def create_product():
   form = request.form
   image = request.files.get('image')
   return controller.create(form, image)

@product_router.get('/get_all')
@role_required()
def get_all_products():
   return controller.get_all()

@product_router.get('/get_all_client')
def get_all_products_for_client():
   return controller.get_all_client()

@product_router.put('/update/<int:id>')
@role_required()
def update_product(id):
   form = request.form
   image = request.files.get('image')
   return controller.update(id, form, image)

@product_router.delete('/delete/<int:id>')
@role_required()
def delete_product(id):
   return controller.delete(id)

@product_router.get('/get_by_id/<int:id>')
def get_by_id(id):
   return controller.get_by_id(id)