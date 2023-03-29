import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from amazing_hinting import settings
from vacancies.models import Vacancy, Skill
from vacancies.serializers import VacancyDetailSerializer, VacancyListSerializer, VacancyCreateSerializer, \
    VacancyDeleteSerializer, VacancyUpdateSerializer, SkillSerializer


def hello(request):
    return HttpResponse("Hello, world!")


class SkillsViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


# @csrf_exempt   # Декоратор отменяющий проверку токена
# def index(request):
#     if request.method == 'GET':
#         vacancies = Vacancy.objects.all()
#
#         search_text = request.GET.get('text', None)
#         if search_text:
#             vacancies = vacancies.filter(text=search_text)
#
#         response = []
#         for vacancy in vacancies:
#             response.append({
#                 "id": vacancy.id,
#                 "text": vacancy.text,
#             })
#         return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})
#
#     elif request.method == 'POST':
#         vacancy_data = json.loads(request.body)
#         vacancy = Vacancy()
#         vacancy.text = vacancy_data["text"]
#
#         vacancy.save()
#
#         return JsonResponse({
#             "id": vacancy.id,
#             "text": vacancy.text,
#         })


# @method_decorator(csrf_exempt, name='dispatch')
# class VacancyView(View):
#     def get(self, request):
#         vacancies = Vacancy.objects.all()
#
#         search_text = request.GET.get('text', None)
#         if search_text:
#             vacancies = vacancies.filter(text=search_text)
#
#         response = []
#         for vacancy in vacancies:
#             response.append({
#                         "id": vacancy.id,
#                         "text": vacancy.text,
#                     })
#         return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})
#
#     def post(self, request):
#         vacancy_data = json.loads(request.body)
#         vacancy = Vacancy()
#         vacancy.text = vacancy_data["text"]
#
#         vacancy.save()
#
#         return JsonResponse({
#             "id": vacancy.id,
#             "text": vacancy.text,
#         })


# class VacancyListView(ListView):
#     model = Vacancy
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#
#         search_text = request.GET.get('text', None)
#         if search_text:
#             self.object_list = self.object_list.filter(text=search_text)
#             self.object_list = self.object_list.order_by("text")
#
#
#
#         response = []
#         for vacancy in self.object_list:
#             response.append({
#                         "id": vacancy.id,
#                         "text": vacancy.text,
#                     })
#         return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})

class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    def get(self, request, *args, **kwargs):
        vacancy_text = request.GET.get('text', None)
        if vacancy_text:
            self.queryset = self.queryset.filter(
                text__icontains=vacancy_text
            )

        # skill_name = request.GET.get('skill', None)
        # if skill_name:
        #     self.queryset = self.queryset.filter(
        #         skills__name__icontains=skill_name
        #     )

        skills_name = request.GET.getlist('skill', None)
        skill_q = None
        for skill in skills_name:
            if skill_q is None:
                skill_q = Q(skills__name__icontains=skill)
            else:
                skill_q |= Q(skills__name__icontains=skill)
            if skill_q:
                self.queryset = self.queryset.filter(skill_q)

        return super().get(request, *args, **kwargs)

   # class VacancyListView(ListView):
#     model = Vacancy
#
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#
#         search_text = request.GET.get('text', None)
#         if search_text:
#             self.object_list = self.object_list.filter(text=search_text)
#             self.object_list = self.object_list.order_by("text")


        # total = self.object_list.count() # общее число записей
        # page_number = int(request.GET.get("page", 1)) # получаем № запрош. стр. из запроса
        # offset = (page_number - 1) * settings.TOTAL_ON_PAGE # определяем смещение начала списка
        # if offset < total:
        #     self.object_list = self.object_list[offset:offset+settings.TOTAL_ON_PAGE]
        # else:
        #     self.object_list = self.object_list[offset: ]


        # paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        # page_number = int(request.GET.get("page", 1))
        # page_object = paginator.get_page(page_number)


        # vacancies = []
        # for vacancy in page_object:
        #     vacancies.append({
        #         "id": vacancy.id,
        #         "text": vacancy.text,
        #     })

        # list(map(lambda x: setattr(x, "username", x.user.username if x.user else None), page_object))
        #
        # response = {
        #     "items": VacancyListSerializer(page_object, many=True).data,
        #     "num_pages": paginator.num_pages,
        #     "total": paginator.count
        # }
        #
        # return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


# class VacancyDetailView(DetailView):
#     model = Vacancy
#
#     def get(self, request, *args, **kwargs):
#         vacancy = self.get_object()

        # response = {"id": vacancy.id,
        #     "user": vacancy.user_id,
        #     "slug": vacancy.slug,
        #     "text": vacancy.text,
        #     "status": vacancy.status,
        #     "created": vacancy.created,
        #     "skills": list(vacancy.skills.all().values_list("name", flat=True))}

        # return JsonResponse(VacancyDetailSerializer(vacancy).data, json_dumps_params={"ensure_ascii": False})


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer


class UserVacancyDetailView(View):
    def get(self, request):
        user_query_set = User.objects.annotate(vacancies=Count('vacancy'))

        paginator = Paginator(user_query_set, settings.TOTAL_ON_PAGE)
        page_number = int(request.GET.get("page", 1))
        page_object = paginator.get_page(page_number)

        users = []
        for user in page_object:
            users.append({
                "id": user.id,
                "name": user.username,
                "vacancies": user.vacancies
            })

        response = {
            "items": users,
            "total": paginator.count,
            "num_page": paginator.num_pages
        }

        return JsonResponse(response)


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer

# @method_decorator(csrf_exempt, name='dispatch')
# class VacancyCreateView(CreateView):
#     model = Vacancy
#     fields = ['user', 'slug', 'text', 'status', 'created', 'skills']
#
#     def post(self, request, *args, **kwargs):
#         # vacancy_data = json.loads(request.body)
#         vacancy_data = VacancyCreateSerializer(data=json.loads(request.body))
#         if vacancy_data.is_valid():
#             vacancy_data.save()
#         else:
#             return JsonResponse(vacancy_data.errors)

        # vacancy = Vacancy.objects.create(
        #     user_id=vacancy_data['user_id'],
        #     slug=vacancy_data['slug'],
        #     text=vacancy_data['text'],
        #     status=vacancy_data['status'],
        # )
        #
        # for skill in vacancy_data['skills']:
        #     try:
        #         skill_object = Skill.objects.get(name=skill)
        #     except Skill.DoesNotExist:
        #         return JsonResponse({'error': "Skill not found"}, status=404)
        #     vacancy.skills.add(skill_object)
        #
        # return JsonResponse({
        #     "id": vacancy.id,
        #     "text": vacancy.text,
        # })
        # return JsonResponse(vacancy_data.data)


# @method_decorator(csrf_exempt, name='dispatch')
# class VacancyUpdateView(UpdateView):
#     model = Vacancy
#     fields = ['slug', 'text', 'status', 'skills']
#
#     def patch(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#
#         # vacancy_data = (json.loads(request.body))
#
#         vacancy_data = VacancyDetailSerializer(data=json.loads(request.body))
#
#         self.object.slug=vacancy_data['slug']
#         self.object.text=vacancy_data['text']
#         self.object.status=vacancy_data['status']
#
#         for skill in vacancy_data['skills']:
#             try:
#                 skill_object = Skill.objects.get(name=skill)
#             except Skill.DoesNotExist:
#                 return JsonResponse({'error': "Skill not found"}, status=404)
#             self.object.skills.add(skill_object)
#
#         self.object.save()
#
#         return JsonResponse({
#             "id": self.object.id,
#             "user": self.object.user_id,
#             "slug": self.object.slug,
#             "text": self.object.text,
#             "status": self.object.status,
#             "created": self.object.created,
#             "skills": list(self.object.skills.all().values_list("name", flat=True))
#         })


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer


# @method_decorator(csrf_exempt, name='dispatch')
# class VacancyDeleteView(DeleteView):
#     model = Vacancy
#     success_url = '/'
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({"status": "OK"}, status=200)


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDeleteSerializer


# def get(request, vacancy_id):
#     if request.method == 'GET':
#         try:
#             vacancy = Vacancy.objects.get(pk=vacancy_id)
#         except Vacancy.DoesNotExist:
#             return  JsonResponse({"error": "Not found"}, status=404)
#         response = {"id": vacancy.id, "text": vacancy.text,}
#         return JsonResponse(response, json_dumps_params={"ensure_ascii": False})


class VacancyLikeView(UpdateAPIView):
    model = Vacancy
    serializer_class = VacancyDetailSerializer

    def put(self, request, *args, **kwargs):
        Vacancy.objects.filter(pk__in=request.data).update(likes = F('likes') + 1)

        return JsonResponse(
            VacancyDetailSerializer(Vacancy.objects.filter(pk__in=request.data), many=True).data,
            safe=False
        )
