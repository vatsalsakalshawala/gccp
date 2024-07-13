from django.contrib import admin
from .models import (
    CustomUser, Tip, News, Guide, ProductReview, Recipe,
    BlogPost, ProjectIdea, ForumDiscussion, UserFile,
    Comment, Rating, ContactMessage, TeamMember
)

admin.site.register(CustomUser)
admin.site.register(Tip)
admin.site.register(News)
admin.site.register(Guide)
admin.site.register(ProductReview)
admin.site.register(Recipe)
admin.site.register(BlogPost)
admin.site.register(ProjectIdea)
admin.site.register(ForumDiscussion)
admin.site.register(UserFile)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(ContactMessage)
admin.site.register(TeamMember)
