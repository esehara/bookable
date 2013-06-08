# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ScrapeQue'
        db.create_table(u'scrape_scrapeque', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True)),
            ('via', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'scrape', ['ScrapeQue'])


    def backwards(self, orm):
        # Deleting model 'ScrapeQue'
        db.delete_table(u'scrape_scrapeque')


    models = {
        u'scrape.scrapeque': {
            'Meta': {'object_name': 'ScrapeQue'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'via': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['scrape']