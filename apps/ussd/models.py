from django.db import models

from django.db.models.deletion import CASCADE, PROTECT, DO_NOTHING

# Create your models here.


class Menu(models.Model):

    code           = models.CharField(max_length=15,primary_key=True)
    init_tree      = models.ForeignKey('Tree', on_delete=DO_NOTHING)
    output_url     = models.CharField(max_length=255)
    active         = models.BooleanField(default=False)
    test_numbers   = models.TextField(blank=True, null=True)
    
    
       
    def __str__(self):
        return self.code

    class Meta:
        db_table = 'ussd_menu'
        managed = True
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
        
        
class Tree(models.Model):

    title           = models.TextField()
    show_text       = models.BooleanField(default=False)
    argument        = models.TextField()
    var_name        = models.CharField(max_length=50)
    validation      = models.CharField(max_length=150, blank=True, null=True)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'ussd_tree'
        managed = True
        verbose_name = 'Tree'
        verbose_name_plural = 'Trees'

class Node(models.Model):
    
    tree            = models.ForeignKey('Tree',related_name='nodes',on_delete=CASCADE) 
    response        = models.CharField(max_length=50)
    next_id         = models.ForeignKey('Tree',related_name='next_id', on_delete=CASCADE) 

    def __str__(self):
        return str(self.pk)+' - '+self.tree.title

    class Meta:
        db_table = 'ussd_node'
        managed = True
        verbose_name = 'Node'
        verbose_name_plural = 'Nodes'
        
class Session(models.Model):

    session_id          = models.CharField(max_length=150)
    active              = models.BooleanField(default=True)
    msisdn              = models.CharField(max_length=150)
    current_tree        = models.ForeignKey('Tree',related_name='session', on_delete=DO_NOTHING)
    error_count         = models.IntegerField(default=0)
    output_url          = models.CharField(max_length=255)
    data                = models.TextField(blank=True, null=True)
    updated_on          = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        pass

    class Meta:
        db_table = 'ussd_session'
        managed = True
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'