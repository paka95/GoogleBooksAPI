from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
import requests
import math
from .models import Book
from .serializers import BookSerializer


class ApiSpec(APIView):
    def get(self, request, format=None):
        api_spec = {
            "info": {
                "version": "2022.05.16"
            }
        }
        return Response(api_spec)
    

class ImportBooks(APIView):
    def post(self, request):
        author = request.data['author']

        ### getting the total number of books to be imported, needed for iterations
        url_import = f'https://www.googleapis.com/books/v1/volumes?q=+inauthor:{author}'
        r = requests.get(url = url_import)
        data = r.json()
        books_count = data["totalItems"]

        ### calculating number of iterations to import every single book - limited to 40 per iteration
        iterations = int(math.ceil(books_count / 40))
        startIndex = 0
        books = []

        for iteration in range(iterations):
            url_import = f'https://www.googleapis.com/books/v1/volumes?q=+inauthor:{author}&startIndex={startIndex}&maxResults=40'
            startIndex += 40
            r = requests.get(url = url_import)
            data = r.json()

            for item in data["items"]:
                external_id = item.get('id')
                item_volume_info = item['volumeInfo']
                data = {
                    'external_id': external_id,
                    'title': item_volume_info.get('title'),
                    'authors': item_volume_info.get("authors"),
                    'published_year': item_volume_info["publishedDate"][:4] if "publishedDate" in  item_volume_info.keys() else None,
                    'thumbnail': item_volume_info.get('imageLinks', {}).get('thumbnail')
                }

                try:
                    book = Book.objects.get(external_id=external_id)    # checking if an entry already exists in the database, if so, update its values with provided data
                    serializer = BookSerializer(instance=book, data=data)
                    if serializer.is_valid():
                        serializer.update(book, serializer.validated_data)
                except Book.DoesNotExist:
                    books.append(data)

        serializer = BookSerializer(data = books, many = True)
        if serializer.is_valid():
            serializer.save()

        return Response(
            {"imported": books_count}
        )
    

class Books(ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        filters = {
            'from': 'published_year__gte',
            'to': 'published_year__lte',
            'acquired': 'acquired',
        }
        # Loop over the filters and apply any that are present in the request
        for param, field in filters.items():
            value = self.request.query_params.get(param)
            if value:
                if param == 'acquired':
                    value = True if value.lower() == 'true' else False
                queryset = queryset.filter(**{field: value})
        return queryset


class BookDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

