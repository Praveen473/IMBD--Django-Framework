from rest_framework import serializers
from .models import WatchList,StreamPlatform,Review


class Reviewserializers(serializers.ModelSerializer):
    # len_name=serializers.SerializerMethodField()
    review_user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        exclude=('watchlist',)
        # fields="__all__"


class WatchListserializers(serializers.ModelSerializer):
    # len_name=serializers.SerializerMethodField()
    # reviews=Reviewserializers(many=True,read_only=True)
    platform=serializers.CharField(source='platform.name')

    class Meta:
        model=WatchList
        fields="__all__"

class StreamPlatformserializers(serializers.HyperlinkedModelSerializer):
    Watchlist = WatchListserializers(many=True,read_only=True)
    # url = serializers.HyperlinkedIdentityField(view_name="Stream-details")
    #Watchlist =serializers.StringRelatedField(many=True)
    #Watchlist = serializers.HyperlinkedRelatedField(

    class Meta:
        model=StreamPlatform
        fields="__all__"

    #
    # def get_len_name(self,object):
    #     return len(object.name)
    # def validate(self,data):
    #     if data['name']==data['description']:
    #         raise serializers.ValidationError("Name and description are same")
    #     return data
    #
    # def validate_name(self,value):
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is short")
    #     return value

# def dname(value):
#     if len(value)<2:
#         raise serializers.ValidationError("Name is short")
#
# class Movieserializers(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField(validators=[dname])
#     description=serializers.CharField()
#
#     def create(self,validated_data):
#         return kk.objects.create(**validated_data)
#     def update(self, instance, validated_data):
#         instance.name=validated_data.get('name',instance.name)
#         instance.description=validated_data.get('description',instance.description)
#         instance.save()
#         return instance
#
#     def validate(self,data):
#         if data['name']==data['description']:
#             raise serializers.ValidationError("Name and description are same")
#         return data
#
#     # def validate_name(self,value):
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is short")
    #     else:
    #         return value


