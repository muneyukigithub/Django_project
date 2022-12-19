from rest_framework import serializers
from .models import CustomUser,Task,SmallTask
from rest_framework.serializers import SerializerMethodField

class SmallTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmallTask
        fields = ('smalltask_id', 'smalltask','task_id')

class TaskSerializer(serializers.ModelSerializer):
    smalltask = SerializerMethodField()
    class Meta:
        model = Task
        fields = [
            'task_id', 
            'task',
            'created_at',
            'smalltask',
            ]

    def get_smalltask(self,obj):
        try:
            s = SmallTaskSerializer(SmallTask.objects.all().filter(task_id=Task.objects.get(task_id=obj.task_id)),many=True).data
            return s
        except:
            s = None
            return s