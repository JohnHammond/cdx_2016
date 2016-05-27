from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode

from nano import comments
from nano.comments.models import * 

register = template.Library()

@register.inclusion_tag('nano/comments/comment_list_frag.html')
def show_comments(obj):
    contenttype = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(object_pk=str(obj.pk), content_type=contenttype)
    return {'comments': comments}

@register.inclusion_tag('nano/comments/comment_tree_frag.html')
def show_comments_tree(obj):
    contenttype = ContentType.objects.get_for_model(obj)
    comments = Comment.tree.roots().filter(object_pk=str(obj.pk), content_type=contenttype)
    return {'comments': comments}

@register.inclusion_tag('nano/comments/comment_tree_node_frag.html')
def show_comments_subtree(subtree):
    comments = subtree.children()
    return {'comments': comments}

@register.simple_tag
def show_comment_count(obj):
    contenttype = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(object_pk=str(obj.pk), content_type=contenttype).count()
    return comments

@register.filter
def comment_count(obj):
    contenttype = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(object_pk=str(obj.pk), content_type=contenttype).count()
    return comments
