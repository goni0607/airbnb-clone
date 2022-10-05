from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView
from users import models as user_models
from . import models
from core import views as core_views


def go_conversation(request, a_pk, b_pk):
    try:
        user_one = user_models.User.objects.get(pk=a_pk)
        user_two = user_models.User.objects.get(pk=b_pk)
    except user_models.User.DoesNotExist:
        return core_views.go_home()

    try:
        conversation = models.Conversation.objects.get(
            Q(participants=user_one) & Q(participants=user_two)
        )
    except models.Conversation.DoesNotExist:
        conversation = models.Conversation.objects.create()
        conversation.participants.add(user_one, user_two)
    return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(DetailView):

    model = models.Conversation
