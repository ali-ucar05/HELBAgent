from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from agentAI.models import AIAgent
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def collect_agent_data_for_user(user):
    agents = AIAgent.objects.all()
    chartData = {}
    dailyMessages = {}

    for agent in agents:
        messageNbr = 0
        discussion = agent.discussion.split("|||")

        for i in range(0, len(discussion), 5):
            if i + 4 < len(discussion) and discussion[i] == user.username:
                messageNbr += 1
                message_date_str = discussion[i + 4]
                date_only = message_date_str.split(" ")[0].split("T")[0]

                if date_only not in dailyMessages:
                    dailyMessages[date_only] = 1
                else:
                    dailyMessages[date_only] += 1

        chartData[agent.name] = messageNbr

    return chartData, dailyMessages

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    chartData, dailyMessages = collect_agent_data_for_user(request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'chartData': chartData,
        'dailyMessages': dailyMessages,
    }

    return render(request, 'users/profile.html', context)


def user_profile(request, username):
    target_user = get_object_or_404(User, username=username)
    chartData, _ = collect_agent_data_for_user(target_user)  

    context = {
        "target_user": target_user,
        "chartData": chartData,
    }

    return render(request, 'users/user_profile.html', context)

