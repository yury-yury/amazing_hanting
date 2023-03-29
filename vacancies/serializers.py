from rest_framework import serializers

from vacancies.models import Vacancy, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


# class VacancySerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     text = serializers.CharField(max_length=2000)
#     slug = serializers.CharField(max_length=50)
#     status = serializers.CharField(max_length=6)
#     created = serializers.DateField()
#     username = serializers.CharField(max_length=100)


class VacancyListSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = ["id", "text", "slug", "status", "created", "username", "skills"]


class VacancyDetailSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        # exclude = ['skills']
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._skills = self.initial_data.pop("skills")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        vacancy = Vacancy.objects.create(**validated_data)

        for skill in self._skills:
            skill_object, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_object)

        vacancy.save()
        return vacancy


class VacancyUpdateSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field="name"
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateField(read_only=True)

    class Meta:
        model = Vacancy
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._skills = self.initial_data.pop("skills")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        vacancy = super().save()

        for skill in self._skills:
            skill_object, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_object)

        vacancy.save()
        return vacancy


class VacancyDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ["id"]



