from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import ChatThread

def support_required(user):
    return user.is_authenticated and (user.is_staff or getattr(user, "is_support", False))

@login_required
def chat_home(request):
    thread, _ = ChatThread.objects.get_or_create(customer=request.user, is_open=True)
    return redirect("chat:thread", thread_id=thread.id)

@login_required
def thread_view(request, thread_id):
    thread = get_object_or_404(ChatThread, id=thread_id)
    if not (request.user == thread.customer or support_required(request.user)):
        return redirect("core:home")
    return render(request, "chat/thread.html", {"thread": thread})

@user_passes_test(support_required)
def support_inbox(request):
    threads = ChatThread.objects.order_by("-created_at")[:50]
    return render(request, "chat/support_inbox.html", {"threads": threads})
