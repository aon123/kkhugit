from rest_framework import serializers
from .models import Files
from django.utils import timezone
import os


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Files
        fields = ('id', 'favorites',  'created_at', 'last_modified', 'memo', 'version', 'removed', 's3key', 'clicked', 'file')

        extra_kwargs = {
            'file_name': {'write_only': True},
            'size': {'write_only': True},
        }

    def create(self, validated_data):
        print(validated_data)
        validated_data['user_id'] = self.context['request'].user

        file = self.context['request'].FILES['file']
        validated_data['file_name'] = file.name
        validated_data['size'] = file.size
        existing_files = Files.objects.filter(file_name=file.name, user_id=validated_data['user_id'])
        if existing_files.exists():
            # Get the latest version
            latest_version = existing_files.latest('version').version
            # Increment the version by 1
            validated_data['version'] = latest_version + 1

        file = validated_data.pop('file')
        print(validated_data)
        return super().create(validated_data)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('id',)
        read_only_fields = ('id', 'favorites',  'created_at', 'last_modified', 'user', 'memo', 'version', 's3key', 'removed')

    def update(self, instance, validated_data):
        instance.removed = True
        instance.save()
        return instance

    def validate(self, attrs):
        user = self.context['request'].user

        if user != attrs['user']:
            raise serializers.ValidationError("You don't have permission to delete this file.")

        return attrs
    
class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files 
        fields = '__all__'
        
    def update(self, instance, validated_data): 
        instance.memo = validated_data.get('memo', instance.memo)
        instance.last_modified = timezone.now()
        instance.save()
        return instance
        
    
# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Files
#         fields = ('__all__')        
        
        
class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('id', 'memo')
        read_only_fields = ('id',)
        
'''    def update(self, instance, validated_data):
        instance.memo = validated_data.get('memo', instance.memo)
        instance.last_modified = timezone.now()
        instance.save()
        return instance
    
    def delete(self, instance, validated_data):
        instance.memo = ""
        return instance
'''
