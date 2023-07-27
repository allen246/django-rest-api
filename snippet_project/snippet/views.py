from rest_framework.views import APIView
from .serializers import SnippetSerializer, TagSerializer
from .models import Snippet, Tag
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, action

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_user=self.request.user)

    def list(self, request, *args, **kwargs):
        snippets = self.get_queryset()
        serializer = self.get_serializer(snippets, many=True)
        total_snippets = snippets.count()
        data = {
            'total_snippets': total_snippets,
            'snippets': [data.get('snippet_url') for data in serializer.data]
        }
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def batch_delete(self, request):
        snippet_ids = request.data.get('snippet_ids', [])
        snippets = Snippet.objects.filter(id__in=snippet_ids)
        if not snippets.exists():
            return Response({"error": "No snippets found with the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        snippets_serializer = SnippetSerializer(snippets, many=True, context={'request': request})
        snippets_data = snippets_serializer.data  # Serialize the snippets data before deletion
        snippets.delete()
        return Response(snippets_data, status=status.HTTP_204_NO_CONTENT)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        snippets = Snippet.objects.filter(tag=instance)
        snipperts_serializer = SnippetSerializer(snippets, many=True, context={'request': request})
        serializer = self.get_serializer(instance)
        response=serializer.data
        response['snippets'] = snipperts_serializer.data
        return Response(response)


# class SnippetView(APIView):
# 	def get(self, request):
# 		data = Snippet.objects.all()
# 		serializer = SnippetSerializer(data, many=True)
# 		return Response(serializer.data)

# 	def post(self, request):
# 		serializer = SnippetSerializer(data = request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=201)
# 		return Response(serializer.errors, status=400)

# 	def put(self, request):
# 			try:
# 				snippet_obj = Snippet.objects.get(id=request.data.get('id'))
# 			except Snippet.DoesNotExist:
# 				return Response({"id": [
# 	        		"This field is required or valid"
# 	    		]}, status=400)
# 			serializer = SnippetSerializer(snippet_obj, data=request.data)
# 			if serializer.is_valid():
# 				serializer.save()
# 				return Response(serializer.data, status=201)
# 			return Response(serializer.errors, status=400)

# 	def patch(self, request):
# 			try:
# 				snippet_obj = Snippet.objects.get(id=request.data.get('id'))
# 			except Snippet.DoesNotExist:
# 				return Response({"id": [
# 	        		"This field is required or valid"
# 	    		]}, status=400)
# 			serializer = SnippetSerializer(snippet_obj, data=request.data, partial=True)
# 			if serializer.is_valid():
# 				serializer.save()
# 				return Response(serializer.data, status=201)
# 			return Response(serializer.errors, status=400)

# 	def delete(self, request):
# 		try:
# 			snippet_obj = Snippet.objects.get(id=request.data.get('id'))
# 		except Snippet.DoesNotExist:
# 			return Response({"id": [
#         		"This field is required or valid"
#     		]}, status=400)
# 		serializer = SnippetSerializer(snippet_obj)
# 		return Response(serializer.data, status=202)

# class TagView(APIView):

# 	def get(self, request):
# 		data = Tag.objects.all()
# 		serializer = TagSerializer(data, many=True)
# 		return Response(serializer.data)