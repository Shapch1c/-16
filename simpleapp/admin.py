# from django.contrib import admin
# from .models import Category, New
#
# admin.site.register(Category)
# admin.site.register(New)


from django.contrib import admin
from .models import Post, Category, Author, PostCategory

class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1  # Количество пустых строк для добавления новых связей


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Поля для отображения в форме редактирования
    fields = ('author', 'post_type', 'title', 'text', 'rating')
    readonly_fields = ('post_time',)  # Поле, доступное только для чтения
    list_display = ('title', 'text', 'author', 'post_type', 'rating')  # Поля для отображения в списке объектов
    inlines = [PostCategoryInline]  # Связь через промежуточную модель

admin.site.register(Author)
admin.site.register(Category)