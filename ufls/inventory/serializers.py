from .models import Asset, AssetLog, Area
from rest_framework import serializers

class AssetPOSTSerializer(serializers.ModelSerializer):
    box = serializers.PrimaryKeyRelatedField(many=False, default=None, allow_null=True, allow_empty=True , read_only=False, queryset=Asset.objects.filter(type='BX'))
    storage_location = serializers.PrimaryKeyRelatedField(many=False, allow_null=True, allow_empty=True ,read_only=False, queryset=Area.objects.all())

    class Meta:
        model = Asset
        fields = ['tag', 'type', 'constructAssetTag', 'company', 'description', 'serial_number', 'owner', 'is_convention_owned', 'cost', 'checked_out_to', 'checked_out_date', 'check_out_department', 'check_out_notes', 'status', 'storage_location', 'getComments', 'box']

class AssetSerializer(serializers.ModelSerializer):
    #box = serializers.PrimaryKeyRelatedField(many=False, allow_null=True, allow_empty=True , read_only=True)
    #storage_location = serializers.PrimaryKeyRelatedField(many=False, allow_null=True, allow_empty=True ,read_only=True)

    class Meta:
        model = Asset
        fields = ['tag', 'type', 'constructAssetTag', 'company', 'description', 'serial_number', 'owner', 'is_convention_owned', 'cost', 'checked_out_to', 'checked_out_date', 'check_out_department', 'check_out_notes', 'status', 'storage_location', 'getComments', 'box']
        depth = 2


    #def to_representation(self, instance):
    #    response = super().to_representation(instance)
    #    response['storage_location'] = AreaSerializer(instance.storage_location).data
    #    response['box'] = AssetSerializer(instance.box).data
    #    return response
        #return super(AssetSerializer, self).to_representation(instance)

class AssetGlimpseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['tag', 'description', 'is_convention_owned', 'constructAssetTag', 'status', 'checked_out_to', 'checked_out_date', 'storage_location', 'box']
        depth = 1

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'