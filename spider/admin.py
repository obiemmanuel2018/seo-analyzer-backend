from django.contrib import admin
from .models import Project, Result, DuplicateTitle, DuplicateDescription,\
                    MissingH1, MissingCanonical, MissingTitle, MissingViewPort,\
                    MissingDescription, LowMeta, LowTitle, DuplicateH1, CrawlingStatistic, \
                          AuditStatistic, Article, ArticleContent

# Register your models here.

class DuplicateTitleAdmin(admin.TabularInline):
      model = DuplicateTitle
      fields = ('titles',)

class DuplicateH1Admin(admin.TabularInline):
      model = DuplicateH1
      fields = ('titles',)

class DuplicateDescriptionAdmin(admin.TabularInline):
      model = DuplicateDescription
      fields = ('titles',)

class MissingH1Admin(admin.TabularInline):
      model = MissingH1
      fields = ('title',)

class MissingTitleAdmin(admin.TabularInline):
      model = MissingTitle
      fields = ('title',)


class MissingDescriptionAdmin(admin.TabularInline):
      model = MissingDescription
      fields = ('title',)

class MissingCanonicalAdmin(admin.TabularInline):
      model = MissingCanonical
      fields = ('title',)


class MissingDescriptionAdmin(admin.TabularInline):
      model = MissingDescription
      fields = ('title',)

class MissingViewPortAdmin(admin.TabularInline):
      model = MissingViewPort
      fields = ('title',)

class LowTitleAdmin(admin.TabularInline):
      model = LowTitle
      fields = ('title',)


class LowMetaAdmin(admin.TabularInline):
      model = LowMeta
      fields = ('title',)


class CrawlingStatisticAdmin(admin.TabularInline):
      model = CrawlingStatistic
      fields = ('date',)


class AuditStatisticAdmin(admin.TabularInline):
      model = AuditStatistic
      fields = ('date',)
      
@admin.register(Result)
class ResultsAdmin(admin.ModelAdmin):
      list_display = ('project', 'created_at', 'updated_at')
      inlines = [DuplicateTitleAdmin, DuplicateDescriptionAdmin, MissingH1Admin, MissingTitleAdmin,
                 MissingDescriptionAdmin, MissingCanonicalAdmin, MissingViewPortAdmin, LowMetaAdmin, LowTitleAdmin,
                 DuplicateH1Admin
                ]
      

@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
      list_display = ('user', 'name', 'homepage', 'created_at')
      ordering = ('-created_at',)
      inlines = [CrawlingStatisticAdmin, AuditStatisticAdmin]
 


class ArticleContentAdmin(admin.TabularInline):
       model = ArticleContent
       fields = ('title','content',)
      

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
      list_display = ['title']
      inlines = [ArticleContentAdmin, ]






