from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class main_user(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_login = None
    sex = models.BooleanField()
    date_of_birth = models.DateField()

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        managed = False
        db_table = 'user'


class Profession(models.Model):
    id_profession = models.AutoField(primary_key=True)
    name_profession = models.CharField(max_length=255)

    class Meta:
        db_table = 'profession'
        managed = False


class ProfessionSkill(models.Model):
    id_skill = models.AutoField(primary_key=True)
    name_skill = models.CharField(max_length=255)
    for_graph = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'profession_skill'


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('main_user', on_delete=models.CASCADE, db_column='user_id')
    desired_profession = models.ForeignKey('Profession', on_delete=models.CASCADE, related_name='desired_profession', db_column='desired_profession')
    about_me = models.TextField()

    class Meta:
        managed = False
        db_table = 'profile'

class ProfileProfession(models.Model):
    profile_profession_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('main_user', on_delete=models.CASCADE, db_column='user_id')
    start_date_work = models.DateField()
    end_date_work = models.DateField()
    id_profession = models.ForeignKey('Profession', on_delete=models.CASCADE, db_column='id_profession')

    class Meta:
        
        managed = False
        db_table = 'profile_profession'

class ProfileSkills(models.Model):
    id_profile_skills = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('main_user', on_delete=models.CASCADE, db_column='user_id')
    id_skill = models.ForeignKey('ProfessionSkill', on_delete=models.CASCADE, db_column='id_skill')

    class Meta:
        managed = False
        db_table = 'profile_skills'

class Edge(models.Model):
    edge_id = models.AutoField(primary_key=True)
    graph_id = models.ForeignKey('Graph', on_delete=models.CASCADE, db_column='graph_id')
    edge_from_param = models.CharField(max_length=255)
    edge_to_param =  models.CharField(max_length=255)   
    class Meta:
        managed = False
        db_table = 'edge'

class Node(models.Model):
    node_id = models.AutoField(primary_key=True)
    graph_id = models.ForeignKey('Graph', on_delete=models.CASCADE, db_column='graph_id')
    node_color_param = models.CharField(max_length=255)
    node_id_param =  models.IntegerField()
    node_shape_param = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'node'

class Graph(models.Model):
    id_graph = models.AutoField(primary_key=True)
    id_profession = models.ForeignKey('Profession', on_delete=models.CASCADE, db_column='id_profession') 
    class Meta:
        managed = False
        db_table = 'graph'

class FrequencyStatistics(models.Model):
    id_frequency_statistics = models.AutoField(primary_key=True)
    id_profession = models.ForeignKey('Profession', on_delete=models.CASCADE,db_column='id_profession')
    id_skill_professions = models.ForeignKey('ProfessionSkill', on_delete=models.CASCADE,db_column='id_skill_professions')
    count_frequency = models.IntegerField()
    date_operate = models.DateTimeField()
    last_operate = models.BooleanField()
    graph_count = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'frequency_statistics'

class SkillDuration(models.Model):
    id_skill = models.AutoField(primary_key=True)
    duration_for_beginer = models.IntegerField()
    duration_for_advanced = models.IntegerField()
    duration_for_professional = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'skill_duration'

class Hints(models.Model):
    hint_id  = models.AutoField(primary_key=True)
    node_id  = models.ForeignKey('Node', on_delete=models.CASCADE,db_column='node_id')
    hint_text  = models.TextField()
    class Meta:
        managed = False
        db_table = 'hints'