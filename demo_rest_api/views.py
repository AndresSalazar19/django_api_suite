from django.shortcuts import render
from django.http import JsonResponse

# API REST demo: operaciones CRUD sobre una lista en memoria
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

data_list = []  # Simula una base de datos en memoria

# Datos de ejemplo para pruebas iniciales
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False})  # Usuario inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"
    def get(self, request):
        # GET: Devuelve todos los elementos activos
        active_items = [item for item in data_list if item["is_active"]==True]
        return Response(active_items, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data

        # POST: Valida campos requeridos y agrega un nuevo elemento
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    name = "Demo REST API Item"
    
    def _find_item_by_id(self, item_id):
        # Busca un elemento por su ID en la lista
        for item in data_list:
            if item['id'] == item_id:
                return item
        return None
    
    def get(self, request, item_id):
        # GET: Devuelve el elemento con el ID indicado
        item = self._find_item_by_id(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(item, status=status.HTTP_200_OK)
    
    def put(self, request, item_id):
        # PUT: Reemplaza todos los datos del elemento (menos el ID)
        item = self._find_item_by_id(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Los campos "name" y "email" son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)
        original_id = item['id']
        item.clear()
        item.update(data)
        item['id'] = original_id
        if 'is_active' not in item:
            item['is_active'] = True
        return Response({'message': 'Elemento reemplazado exitosamente.', 'data': item}, status=status.HTTP_200_OK)
    
    def patch(self, request, item_id):
        # PATCH: Actualiza solo los campos enviados (menos el ID)
        item = self._find_item_by_id(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        updated_fields = []
        for key, value in data.items():
            if key != 'id':
                item[key] = value
                updated_fields.append(key)
        if not updated_fields:
            return Response({'message': 'No se proporcionaron campos para actualizar.'}, status=status.HTTP_200_OK)
        return Response({
            'message': 'Elemento actualizado parcialmente.',
            'updated_fields': updated_fields,
            'data': item
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, item_id):
        # DELETE: Marca el elemento como inactivo (eliminación lógica)
        item = self._find_item_by_id(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        if item.get('is_active', True) == False:
            return Response({'error': 'El elemento ya está eliminado.'}, status=status.HTTP_400_BAD_REQUEST)
        item['is_active'] = False
        return Response({
            'message': 'Elemento eliminado lógicamente.',
            'data': item
        }, status=status.HTTP_200_OK)
    