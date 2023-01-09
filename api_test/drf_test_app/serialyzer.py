from rest_framework import serializers
from .models import CustomUser, Task, SmallTask,Motivation
from rest_framework.serializers import SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password

# class myTokenObtainPairSerializer:
#     TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class SmallTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmallTask
        fields = ("smalltask_id", "smalltask", "task_id")

    # def create(self, validated_data):
    #     print("create call is SmallTask(**validate")
    #     return SmallTask(**validated_data)

class TaskSerializer(serializers.ModelSerializer):
    # SerializerMethodField は get_xxxx ってなっているメソッドをコールする
    smalltask = SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "task_id",
            "task",
            "created_at",
            "created_user",
            "smalltask",
        ]

    def get_created_user(self,obj):

        print("--",obg)
        return 50

    def get_smalltask(self, obj):
        try:
            s = SmallTaskSerializer(
                SmallTask.objects.all().filter(
                    task_id=Task.objects.get(task_id=obj.task_id)
                ),
                many=True,
            ).data
            return s
        except:
            s = None
            return s

    # def create(self, validated_data):
    #     print("create")
    #     return Task(**validated_data)

class MotivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motivation
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at')

class DetailTaskSerializer(serializers.ModelSerializer):
    motivation = SerializerMethodField()
    smalltask = SerializerMethodField()
    
    class Meta:
        model = Task
        fields = [
            "task",
            "motivation",
            "smalltask",
        ]
        

    def get_smalltask(self, obj):
        return SmallTaskSerializer(SmallTask.objects.all().filter(task_id=Task.objects.get(task_id=obj.task_id)),many=True,).data

    
    def get_motivation(self,obj):
        try:
            s = Motivation.objects.filter(task_id=obj.task_id)
            print(s[0].motivation)
            return s[0].motivation
        except Exception as e:
            print(e)
            return "mot_null"

    #     print(obj)
    #     return 

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = ["email"]
        fields = "__all__"

        # extra_kwargsは読み込みはせず、書き込みだけしたいフィールドを記載
        extra_kwargs = {
            "password": {"write_only": True},
        }

        # 追加

    def validate_password(self, value: str) -> str:
        """
        ハッシュ値に変換する
        """
        return make_password(value)
