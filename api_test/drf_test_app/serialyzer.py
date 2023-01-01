from rest_framework import serializers
from .models import CustomUser, Task, SmallTask
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

    def create(self, validated_data):
        print("create call is SmallTask(**validate")
        return SmallTask(**validated_data)


class TaskSerializer(serializers.ModelSerializer):
    # SerializerMethodField は get_xxxx ってなっているメソッドをコールする
    smalltask = SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "task_id",
            "task",
            "created_at",
            "smalltask",
        ]

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
