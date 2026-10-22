from django.db.models import (
    Model,
    CharField,
    TextField,
    DateTimeField,
    ForeignKey,
    CASCADE,
    ManyToManyField,
)



class Author(Model):
    name = CharField(max_length=100, null=False)
    bio = TextField(blank=True)

    def __str__(self):
        return self.name


class Category(Model):
    name = CharField(max_length=40, null=False)

    def __str__(self):
        return self.name



class Tag(Model):
    name = CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class Article(Model):
    title = CharField(max_length=100)
    content = TextField(blank=True, null=True)
    pub_date = DateTimeField(auto_now_add=True, blank=True, null=True)
    author = ForeignKey(Author, on_delete=CASCADE)
    category = ForeignKey(Category, on_delete=CASCADE)
    tags = ManyToManyField(Tag, related_name='articles')


