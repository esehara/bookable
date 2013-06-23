# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BookLog'
        db.create_table(u'booklog_booklog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shelf.Book'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'booklog', ['BookLog'])


    def backwards(self, orm):
        # Deleting model 'BookLog'
        db.delete_table(u'booklog_booklog')


    models = {
        u'booklog.booklog': {
            'Meta': {'ordering': "['-updated_at']", 'object_name': 'BookLog'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shelf.Book']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'shelf.book': {
            'Meta': {'ordering': "['-click']", 'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'click': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detail': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'is_mecab': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'users': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'via': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['booklog']