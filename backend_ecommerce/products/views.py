from rest_framework import views
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth.models import User
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, ProductCommentSerializer
from .models import Category, Product, ProductImage, ProductComment
from .helpers import custom_response, parse_request
from rest_framework.parsers import JSONParser
from json import JSONDecodeError

class CategoryAPIView(views.APIView):
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response({
        'status': 200,
        'message': 'Get all categories successfully!',
        'data': serializer.data
        }, status=200)
        except Exception as e:
       # nếu query lỗi hay parse lỗi thì trả về error thôi
            return Response({
        'status': 400,
        'message': 'Get all categories failed!',
        'error': [str(e)]
        }, status=400)
    def post(self, request):
        try:
            data = JSONParser().parse(request)
        except JSONDecodeError:
        # nếu parse error thì trả về lỗi
            return Response({
        'status': 400,
        'message': 'JSON decode error!',
        'error': None
        }, status=400)
    # nếu parse thành công thì cho data vào serializer để mapping với model
        serializer = CategorySerializer(data=data)
    # Kiểm tra xem có mapping thành công không
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 201,'message': 'Create category successfully!','data': serializer.data}, status=201)
        else:
            return Response({
            'status': 400,
            'message': 'Get all categories failed!',
            'error': serializer.errors
            }, status=400)
        
class CategoryDetailAPIView(views.APIView):
 def get_object(self, id_slug):
    try:
        return Category.objects.get(id=id_slug)
    except:
        raise Http404
 def get(self, request, id_slug, format=None):
    try:
        category = self.get_object(id_slug)
        serializer = CategorySerializer(category)
        return custom_response('Get category successfully!', 'Success', serializer.data, 200)
    except:
        return custom_response('Get category failed!', 'Error', "Category not found!", 400)
 def put(self, request, id_slug):
    try:
        data = parse_request(request)
        category = self.get_object(id_slug)
        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
             serializer.save()
             return custom_response('Update category successfully!', 'Success', serializer.data, 200)
        else:
            return custom_response('Update category failed', 'Error', serializer.errors, 400)
    except:
        return custom_response('Update category failed', 'Error', "Category not found!", 400)
 def delete(self, request, id_slug):
    try:
        category = self.get_object(id_slug)
        category.delete()
        return custom_response('Delete category successfully!', 'Success', {"category_id": id_slug}, 
204)
    except:
            return custom_response('Delete category failed!', 'Error', "Category not found!", 400)
    

class ProductViewAPI(views.APIView):
 def get(self, request):
    try:
        products = Product.objects.all()
        serializers = ProductSerializer(products, many=True)
        return custom_response('Get all products successfully!', 'Success', serializers.data, 200)
    except:
        return custom_response('Get all products failed!', 'Error', None, 400)
 def post(self, request):
    try:
        data = parse_request(request)
        # product có ràng buộc phải có một category_id nên phải query tìm category đó trước
        category = Category.objects.get(id=data['category_id'])
        product = Product(
        name=data['name'],
        unit=data['unit'],
        price=data['price'],
        discount=data['discount'],
        amount=data['amount'],
        thumbnail=data['thumbnail'],
        # gán category đã tìm được vào field category_id
        category_id=category
        )
        product.save()
        serializer = ProductSerializer(product)
        return custom_response('Create product successfully!', 'Success', serializer.data, 201)
    except Exception as e:
        return custom_response('Create product failed', 'Error', {"error": str(e)}, 400)
class ProductDetailAPIView(views.APIView):
    def get_object(self, id_slug):
        try:
            return Product.objects.get(id=id_slug)
        except:
            raise Http404
    def get(self, request, id_slug, format=None):
        try:
            product = self.get_object(id_slug)
            serializer = ProductSerializer(product)
            return custom_response('Get product successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product failed!', 'Error', "Product not found!", 400)
    def put(self, request, id_slug):
        try:
            data = parse_request(request)
            product = self.get_object(id_slug)
            serializer = ProductSerializer(product, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product failed', 'Error', "Category not found!", 400)
    def delete(self, request, id_slug):
        try:
            product = self.get_object(id_slug)
            product.delete()
            return custom_response('Delete product successfully!', 'Success', {"product_id": id_slug}, 204)
        except:
            return custom_response('Delete product failed!', 'Error', "Product not found!", 400)
class ProductImageAPIView(views.APIView):
    def get(self, request, product_id_slug):
        try:
            product_images = ProductImage.objects.filter(product_id=product_id_slug).all()
            serializers = ProductImageSerializer(product_images, many=True)
            return custom_response('Get all product images successfully!', 'Success', serializers.data, 200)
        except:
            return custom_response('Get all product images failed!', 'Error', 'Product images not found', 
400)
    def post(self, request, product_id_slug):
        try:
            data = parse_request(request)
            product = Product.objects.get(id=data['product_id'])
            product_image = ProductImage(
            product_id=product,
            image_url=data['image_url']
            )
            product_image.save()
            serializer = ProductImageSerializer(product_image)
            return custom_response('Create product image successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            return custom_response('Create product image failed', 'Error', {"error": str(e)}, 400)
class ProductImageDetailAPIView(views.APIView):
    def get_object(self, id_slug):
        try:
            return ProductImage.objects.get(id=id_slug)
        except:
            raise Http404
    def get_object_with_product_id(self, product_id_slug, id_slug):
        try:
            return ProductImage.objects.get(product_id=product_id_slug, id=id_slug)
        except:
            raise Http404
    def get(self, request, product_id_slug, id_slug, format=None):
        try:
            product_image = self.get_object(id_slug)
            serializer = ProductImageSerializer(product_image)
            return custom_response('Get product image successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product image failed!', 'Error', "Product image not found!", 400)
    def put(self, request, product_id_slug, id_slug):
        try:
            data = parse_request(request)
            product_image = self.get_object_with_product_id(product_id_slug, id_slug)
            serializer = ProductImageSerializer(product_image, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product image successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product image failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product image failed', 'Error', "Product image not found!", 400)
    def delete(self, request, product_id_slug, id_slug):
        try:
            product_image = self.get_object_with_product_id(product_id_slug, id_slug)
            product_image.delete()
            return custom_response('Delete product image successfully!', 'Success', {"product_image_id": id_slug}, 204)
        except:
            return custom_response('Delete product image failed!', 'Error', "Product image not found!", 
400)
class ProductCommentAPIView(views.APIView):
    def get(self, request, product_id_slug):
        try:
            product_comments = ProductComment.objects.filter(product_id=product_id_slug).all()
            serializers = ProductCommentSerializer(product_comments, many=True)
            return custom_response('Get all product comments successfully!', 'Success', serializers.data, 200)
        except:
            return custom_response('Get all product comments failed!', 'Error', None, 400)
    def post(self, request, product_id_slug):
        try:
            data = parse_request(request)
            product = Product.objects.get(id=data['product_id'])
            user = User.objects.get(id=data['user_id'])
            product_comment = ProductComment(
            product_id=product,
            rating=data['rating'],
            comment=data['comment'],
            user_id=user,
            parent_id=data['parent_id']
            )
            product_comment.save()
            serializer = ProductCommentSerializer(product_comment)
            return custom_response('Create product comment successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            return custom_response('Create product comment failed', 'Error', {"error": str(e)}, 400)
class ProductCommentDetailAPIView(views.APIView):
    def get_object(self, id_slug):
        try:
            return ProductComment.objects.get(id=id_slug)
        except:
         raise Http404
    def get_object_with_product_id(self, product_id_slug, id_slug):
        try:
            return ProductComment.objects.get(product_id=product_id_slug, id=id_slug)
        except:
            raise Http404
    def get(self, request, product_id_slug, id_slug, format=None):
        try:
            product_comment = self.get_object(id_slug)
            serializer = ProductCommentSerializer(product_comment)
            return custom_response('Get product comment successfully!', 'Success', serializer.data, 200)
        except:
         return custom_response('Get product comment failed!', 'Error', "Product comment not found!", 
400)
    def put(self, request, product_id_slug, id_slug):
        try:
            data = parse_request(request)
            product_comment = self.get_object_with_product_id(product_id_slug, id_slug)
            serializer = ProductCommentSerializer(product_comment, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product comment successfully!', 'Success', serializer.data,200)
            else:
                return custom_response('Update product comment failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product comment failed', 'Error', "Product comment not found!", 400)
    def delete(self, request, product_id_slug, id_slug):
        try:
            product_comment = self.get_object_with_product_id(product_id_slug, id_slug)
            product_comment.delete()
            return custom_response('Delete product comment successfully!', 'Success', {"product_comment_id": id_slug},204)
        except:
            return custom_response('Delete product comment failed!', 'Error', "Product comment not found!", 400)
