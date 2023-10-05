from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

class UflsModelViewSet(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        instance = obj
        try:
            if request.GET['depth']:
                self.get_serializer().Meta.depth = int(request.GET['depth'])
        except:
            pass
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        try:
            if request.GET['depth']:
                self.get_serializer().Meta.depth = int(request.GET['depth'])
        except:
            pass
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)