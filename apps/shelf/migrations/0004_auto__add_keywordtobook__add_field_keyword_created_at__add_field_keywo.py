# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'KeywordToBook'
        db.create_table(u'shelf_keywordtobook', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shelf.Keyword'])),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shelf.Book'])),
        ))
        db.send_create_signal(u'shelf', ['KeywordToBook'])

        # Adding field 'Keyword.created_at'
        db.add_column(u'shelf_keyword', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 6, 2, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Keyword.updated_at'
        db.add_column(u'shelf_keyword', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 6, 2, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'KeywordToBook'
        db.delete_table(u'shelf_keywordtobook')

        # Deleting field 'Keyword.created_at'
        db.delete_column(u'shelf_keyword', 'created_at')

        # Deleting field 'Keyword.updated_at'
        db.delete_column(u'shelf_keyword', 'updated_at')


    models = {
        u'shelf.book': {
            'Meta': {'ordering': "['created_at']", 'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detail': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'users': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'via': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'shelf.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
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