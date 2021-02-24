from rest_framework import serializers
from django.db import models
#나중에 role 추가할 수 있게 해주면 좋겠음
role=(
    ("back-dev",0),
    ("front-dev",1),
    ("ui-design",2),
    ("ux-design",3),
    ("project_manager",4),
    ("marketer",5),

)
# Create your models here.
class Group(models.Model):
    group_id=models.CharField(max_length=200)
class Role(models.Model):
    role_id=models.CharField(max_length=200,choices=role)
    group_id=models.ForeignKey(Group)
class Project(models.Model):
    due_date=models.DateTimeField()
class CheckBox(serializers.ListField):
    CHECK_CHOICE=(
        ("FIN",0),
        ("UNFIN",1)
    )
    def __init__(self,role_id,content,is_checked):
        self.role_id=role_id
        self.content=content
        self.is_checked=is_checked

class CheckboxSerializer(serializers.Serializer):
    role_id=serializers.CharField(max_length=200,choices=role) #마음이 아프다
    content=serializers.CharField(max_length=200)
    CHECK=((1,1),(0,0))
    is_checked=serializers.IntegerField(choices=CHECK)
    def create(self,validated_data):
        return CheckBox(**validated_data)
    def update(self,instance,validated_data):
        instance.role_id=validated_data.get('role_id')
        instance.content=validated_data.get('content')
        instance.save()
        return instance
class User(models.Model):

    user_id=models.CharField(max_length=200)
    email=models.EmailField()
    '''passwd=
    firstname
    lastname'''
    role_id=models.ForeignKey(Role)


class TodoList(models.Model):
    #records of the list
    create_date=models.DateTimeField #when is it created
    edit_date=models.DateTimeField #when is it last edited
    author=User() #who made the list
    group_id=models.ForeignKey(Group)
    #list의 소속
    project=models.ForeignKey(Project) #which project is the list relevant with


    #list of check box
    list_title=models.CharField(max_length=100)
    check_box=CheckboxSerializer() #elements of the list
