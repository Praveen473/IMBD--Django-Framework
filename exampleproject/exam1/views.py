from django.shortcuts import render
from rest_framework.response import Response
from exam1.serializers import WatchListserializers,StreamPlatformserializers,Reviewserializers
from exam1.models import WatchList,StreamPlatform,Review
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework import generics
from rest_framework import viewsets
from .permission import AdminOrReadOnly,ReviewUserReadOnly
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from exam1.throttling import ReviewCreateThrottle,ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from exam1.pagination import WatchListPagination,WatchListLOPagination,WatchListCPagination
from django.shortcuts import get_object_or_404
# from rest_framework import mixins



class UserReview(generics.ListAPIView):
    serializer_class = Reviewserializers
    # def get_queryset(self):
    #     username=self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    def get_queryset(self):
        username=self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)
# overwriting Queryset
class ReviewCreate(generics.CreateAPIView):

    serializer_class = Reviewserializers
    permission_classes = [IsAuthenticated]
    throttle_classes=[ReviewCreateThrottle]
    def get_queryset(self):
        return WatchList.objects.all()
    def perform_create(self,serializer):
        pk=self.kwargs.get('pk')
        watchlist=WatchList.objects.get(pk=pk)
        review_user=self.request.user
        review_queryset=Review.objects.filter(watchlist=watchlist,review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("you have already reviewed this Watch")
        # custom calculation
        if watchlist.avg_rating == 0:
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(watchlist.avg_rating + serializer.validated_data['rating'])/2
        watchlist.number_rating= watchlist.number_rating+1
        watchlist.save()
        # custom end
        serializer.save(watchlist=watchlist,review_user=review_user)
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = Reviewserializers
    throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    # becuase the review_user is foreign_key we must use __username
    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [ReviewUserReadOnly]
    # full
    queryset = Review.objects.all()
    serializer_class = Reviewserializers
    throttle_classes = [ScopedRateThrottle]
    throttle_scope= 'review-details'

#concreateView
# class ReviewList(generics.ListCreateAPIView):
#     queryset = Review.objects.all()
#     serializer_class = Reviewserializers
#
# class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Review.objects.all()
#     serializer_class = Reviewserializers


# from line no12 having the function line no 19 with the help of concreate view class
# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class =Reviewserializers
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#
# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class =Reviewserializers
#
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
class StreamPlatformVs(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class= StreamPlatformserializers

# class StreamPlatformVs(viewsets.ViewSet):
    # def list(self, request):
    #     queryset = StreamPlatform.objects.all()
    #     serializer = StreamPlatformserializers(queryset, many=True,context={'request':request})
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = StreamPlatform.objects.all()
    #     watchlist = get_object_or_404(queryset, pk=pk)
    #     serializer = StreamPlatformserializers(watchlist,context={'request':request})
    #     return Response(serializer.data)

class StreamPlatformAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request):
        m =StreamPlatform.objects.all()
        serial= StreamPlatformserializers(m,many=True,context={'request':request})
        return Response(serial.data)

    def post(self,request):
        serial= StreamPlatformserializers(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        else:
            return Response(serial.errors)

class StreamDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request,pk):
        try:
            m =StreamPlatform.objects.filter(pk=pk)
        except StreamDetailAV.DoesNotExist:
            return Response({'error': 'Movie Not Found'},status=status.HTTP_400_BAD_REQUEST)
        serial= StreamPlatformserializers(m,many=True)
        return Response(serial.data)

    def put(self,request,pk):
        m=StreamPlatform.objects.filter(pk=pk)
        serial=StreamPlatformserializers(m,data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        else:
            return Response(serial.errors)

    def delete(self,request,pk):
        m=StreamPlatform.objects.filter(pk=pk)
        m.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#

class WatchListGv(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListserializers
    pagination_class = WatchListCPagination
    # filter_backends = [filters.SearchFilter]
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields  = ['avg_rating']

class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request):
        m =WatchList.objects.all()
        serial= WatchListserializers(m,many=True)
        return Response(serial.data)

    def post(self,request):
        serial= WatchListserializers(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        else:
            return Response(serial.errors)

class WatchDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request,pk):
        try:
            m =WatchList.objects.filter(pk=pk)
        except WatchDetailAV.DoesNotExist:
            return Response({'error': 'Movie Not Found'},status=status.HTTP_400_BAD_REQUEST)
        serial= WatchListserializers(m,many=True)
        return Response(serial.data)

    def put(self,request,pk):
        m=WatchList.objects.filter(pk=pk)
        serial= WatchListserializers(m,data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        else:
            return Response(serial.errors)

    def delete(self,request,pk):
        m=WatchList.objects.filter(pk=pk)
        m.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)








# Create your views here.
# @api_view(['GET', 'POST'])
# def movi(request):
#     if request.method =='GET':
#         m =kk.objects.all()
#         serial= Movieserializers(m,many=True)
#         return Response(serial.data)
#     else:
#         serial= Movieserializers(data=request.data)
#         if serial.is_valid():
#             serial.save()
#             return Response(serial.data)
#         else:
#             return Response(serial.errors)
# @api_view(['GET', 'PUT','DELETE'])
# def movielist(request,pk):
#     if request.method == 'GET':
#         m=kk.objects.get(pk=pk)
#         s =Movieserializers(m)
#         return Response(s.data)
#     if request.method == 'PUT':
#         m=kk.objects.get(pk=pk)
#         serial= Movieserializers(m,data=request.data)
#         if serial.is_valid():
#             serial.save()
#             return Response(serial.data)
#         else:
#             return Response(serial.errors)
#     if request.method == 'DELETE':
#          m=kk.objects.get(pk=pk)
#          m.delete()
#
#          return Response(status=status.HTTP_400_BAD_REQUEST)
