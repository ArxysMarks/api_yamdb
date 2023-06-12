import datetime as dt
from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review, Comment


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'На сайте нельзя публиковать произведения из будущего')
        return value


class ReviewsSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Введите оценку от 0 до 10')
        return value

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            author = self.context['request'].user
            if author.reviews.filter(title_id=title_id).exists():
                raise serializers.ValidationError(
                    'У вас уже есть один отзыв на это произведение'
                )
        return data


class CommentsSerializer(serializers.ModelSerializer):

    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text',
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment
