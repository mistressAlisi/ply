from .models import PrintJob, ConBadgeLevelMap, RegistrantData, Event, Badge
from rest_framework import serializers

class PrintJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintJob
        fields = ['screenData', 'resolved', 'timeCreated', 'handling']

class RegistrantDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrantData
        fields = ['displayImageUrl','isForwarding','vetoBadgePic','conRegLevel','hasMealPlan','conStaffDepartment',
                  'conIsDealerAssistant','conIsDealer','conIsStaff','conBadgeName','conDOB','conEmail','conLastName',
                  'conFirstName','conBadgeNumber','conRegNotes','conBanFlag','conCreepFlag','conCheckedInDate',
                  'conCheckedIn','dateUpdated','dateCreated','checkedIn','metadata','fieldData','currency',
                  'outstandingAmount','amount','total','status','orderEmail','orderNumber','orderDisplayId','orderId',
                  'customerId','orderCustomerId','formAccRef','formName','formId','displayId','rId','event',
                  'croppedImage','customUploadPicture','isCustomPicture','account','pk','determineTwentyTwoShip',
                  'getBadgeNumber','accessibility', 'a11yPartialAssist','a11yFullAssist','a11yEyesight','a11yChair',
                  'a11yElevator','a11yGroup','a11yNotes','a11yEvents','isCardBadge','determineAge']
        depth = 2

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'
        depth = 2

class RegistrantDataGlimpseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrantData
        fields = ['pk', 'conFirstName', 'determineTwentyTwoShip', 'accessibility', 'conLastName', 'status', 'conEmail', 'mergedName', 'conDOB', 'conBadgeName', 'conRegLevel', 'conCheckedIn', 'conCreepFlag', 'determineAge', 'event', 'displayId', 'isForwarding', 'conBadgeNumber', 'displayImageUrl', 'getBadgeNumber', 'vetoBadgePic', 'conIsDealerAssistant','conIsDealer', 'conIsStaff']

class RegistrantDataSanitizedUserReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrantData
        fields = ['conFirstName', 'conLastName', 'conEmail', 'mergedName', 'conDOB', 'conBadgeName', 'conRegLevel', 'conCheckedIn', 'event', 'displayId', 'orderNumber', 'isForwarding', 'displayImageUrl', 'isCustomPicture', 'conBadgeNumber', 'displayImageUrl', 'vetoBadgePic']
        depth = 2

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
