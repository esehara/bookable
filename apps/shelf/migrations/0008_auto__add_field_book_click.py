# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Book.click'
        db.add_column(u'shelf_book', 'click',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Book.click'
        db.delete_column(u'shelf_book', 'click')


    models = {
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
        },
        u'shelf.keyword': {
            'Meta': {'ordering': "['-times']", 'object_name': 'Keyword'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'times': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'shelf.keywordtobook': {
            'Meta': {'object_name': 'KeywordToBook'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shelf.Book']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shelf.Keyword']"})
        }
    }

    complete_apps = ['shelf']