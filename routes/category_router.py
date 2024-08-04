from flask import request, Blueprint
from controllers.category_controller import CategoryController
from utils.jwt_identity_rol import role_required

category_router = Blueprint('category_controller', __name__)
controller = CategoryController()

@category_router.get('/get_all')
@role_required('ADMIN')
def get_all_categories():
   return controller.get_all()

@category_router.get('/get_all_for_clients')
def get_all_categories_for_clients():
   return controller.get_all_for_clients()

@category_router.post('/create')
@role_required('ADMIN')
def create_category():
   json = request.json
   return controller.create(json)   

@category_router.put('/update/<int:id>')
@role_required('ADMIN')
def update_category(id):
   json = request.json
   return controller.update(id, json)

@category_router.delete('/delete/<int:id>')
@role_required('ADMIN')
def delete_category(id):
   return controller.delete(id)