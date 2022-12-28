from django.db import models
import uuid
from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Eメールアドレス',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) 
    admin = models.BooleanField(default=False) 
   
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):             
        return self.email

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

# ユーザ情報を格納する
class Task(models.Model):
    task_id = models.UUIDField(verbose_name="タスクID",primary_key=True,default=uuid.uuid4)
    task = models.CharField(verbose_name="タスク",max_length=255)
    # created_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateField(verbose_name="作成日",auto_now_add=True)
    created_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,blank=False,null=False)

    def __str__(self):
        return self.task

class SmallTask(models.Model):
    smalltask_id = models.UUIDField(verbose_name="小タスクID",primary_key=True,default=uuid.uuid4)
    smalltask = models.CharField(verbose_name="小タスク",max_length=255)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.smalltask
