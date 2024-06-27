from django.db.models import Q
from main.models import Movie


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Movie.objects.filter(id=int(query))

    keywords = [word for word in query.split() if len(word) > 2]

    q_objects = Q()

    for token in keywords:
        q_objects |= Q(description__icontains=token)
        q_objects |= Q(title__icontains=token)

    return Movie.objects.filter(q_objects)
