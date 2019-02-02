import os
import shutil

from rest_framework import generics, serializers
from rest_framework.response import Response

from repository.apis.serializers import RepositorySerializer
from repository.models import Repository


class RepositoryListCreateGenericAPIView(generics.ListCreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer


class RepositoryRetrieveUpdateDestroyGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        repo = Repository.objects.filter(pk=instance.pk)

        source = repo[0].get_repository_dir
        destination = repo[0].get_repository_dir.split(repo[0].name)[0] + request.data.get('name')

        if os.path.isdir(destination):
            raise serializers.ValidationError({'detail': '이미 존재하는 레포지토리가 있습니다.'})

        shutil.move(source, destination)
        repo.update(name=request.data.get('name'))

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
