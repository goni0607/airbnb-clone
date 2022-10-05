from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
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


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            conversation = models.Conversation.objects.get_or_none(pk=pk)
            if conversation is not None:
                return render(
                    self.request,
                    "conversations/conversation_detail.html",
                    {"conversation": conversation},
                )
        return core_views.go_home()

    def post(self, *args, **kwargs):
        pk = kwargs.get("pk")
        message = self.request.POST.get("message", None)
        if message is not None:
            conversation = models.Conversation.objects.get_or_none(pk=pk)
            if conversation is not None:
                models.Message.objects.create(
                    message=message, user=self.request.user, conversation=conversation
                )
                return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
        return core_views.go_home()
