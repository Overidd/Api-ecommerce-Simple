from flask import Blueprint, request
from controllers.user_controller import UserController
from utils.jwt_identity_rol import role_required

user_router = Blueprint('user_router', __name__)
controller = UserController()

@user_router.post('/create')
@role_required('ADMIN')
def create():
   json = request.json
   return controller.create(json)

@user_router.get('/get_all')
@role_required('ADMIN')
def get_all_users():
   return controller.get_all()

@user_router.post('/login')
def login():
   json = request.json
   return controller.login(json)


@user_router.put('/update/<int:id>')
@role_required('ADMIN')
def update_user(id):
   json = request.json
   return controller.update(id, json)


@user_router.delete('/delete/<int:id>')
@role_required('ADMIN')
def delete_user(id):
   return controller.delete(id)