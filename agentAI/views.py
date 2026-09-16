from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ( 
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .forms import InputForm
from groq import Groq
from ollama import chat
from ollama import ChatResponse
from .models import AIAgent
from django.utils import timezone
import datetime
import requests
import base64
import os

def agentAIHome(request):
    context = {
        'aiAgents' : AIAgent.objects.all(),
    }

    return render(request, 'agentAI/home_aiagent.html', context)


# affiche la discussion avec l'agent en question.
# permet d'envoyer des messages en API ou local avec un cool down.
@login_required 
def discussWithAgentAI(request, pk): 
    agent = get_object_or_404(AIAgent, pk=pk) 
    discussion = [item for item in agent.discussion.split("|||") if item] 
    last_message_time = None 
 
    for i in range(0, len(discussion), 5): 
        if i + 4 < len(discussion): 
            user_name = discussion[i] 
            time_stamp = discussion[i + 4] 
 
            if request.user.username == user_name: 
                try: 
                    msg_time = datetime.datetime.fromisoformat(time_stamp)
                    if last_message_time is None or msg_time > last_message_time: 
                        last_message_time = msg_time
                except (ValueError, TypeError): 
                    pass 
 
    d_form = InputForm(request.POST or None) 
 
    # le message a été envoyé 
    if request.method == 'POST' and d_form.is_valid(): 
        can_send = True
 
        # Vérifie la différence de temps entre le temps actuel et le temps du dernier message 
        if last_message_time: 
            time_since_last = (timezone.now() - last_message_time).total_seconds() 
            can_send = time_since_last >= agent.cooldown
 
        # Vérifie si l'utilisateur peut envoyer un message 
        if can_send: 
            prompt = d_form.cleaned_data['prompt'] 
 
            # verifie le modèle de l'agent 
            if agent.model == "API": 
                client = Groq(api_key=os.getenv("GROQ_API_KEY")) 
                completion = client.chat.completions.create( 
                    model="llama-3.1-8b-instant", 
                    messages=[{"role": "user", "content": agent.initial_prompt + " " + prompt}], 
                    temperature=1, 
                    max_completion_tokens=1024, 
                    top_p=1, 
                    stream=True, 
                    stop=None 
                ) 
 
                full_answer = '' 
                for chunk in completion: 
                    content = chunk.choices[0].delta.content 
                    if content: 
                        full_answer += content 
            else: 
                response = chat(model='smollm2:135m', messages=[{'role': 'user', 'content': agent.initial_prompt + " " + prompt}]) 
                full_answer = response.message.content 
 
            # enregistre la discussion 
            timestamp = timezone.now() 
            agent.discussion += f"{request.user.username}|||{prompt}|||{agent.name}|||{full_answer}|||{timestamp.isoformat()}|||" 
            agent.last_activity = timestamp 
            agent.save() 
 
            # rechargement de la page 
            return redirect('aiagent-discuss', pk=agent.pk)
        else:
            # Affiche le message d'erreur du cooldown
            # Django envoie les messages du cooldown au frontend
            time_remaining = int(agent.cooldown - time_since_last)
            messages.error(request, f"Please wait another {time_remaining} seconds before sending a new message.")
 
    context = { 
        'd_form': d_form, 
        'username': request.user.username, 
        'agent': agent, 
    } 
 
    return render(request, 'agentAI/discussion.html', context)

# permet de faire voir les messages en temps réel avec l'ajax construit un tableau qui stockent des
# dictionnaires qui sont manipulable coté scrip du jquery garce a la json reponse
def fetch_chat_data(request, pk):
    agent = get_object_or_404(AIAgent, pk=pk)
    discussion = [item for item in agent.discussion.split("|||") if item]

    messages = []
    for i in range(0, len(discussion), 5):
        if i + 4 < len(discussion):
            user_name = discussion[i]
            user_message = discussion[i+1]
            agent_name = discussion[i+2]
            agent_answer = discussion[i+3]

            try:
                user = User.objects.get(username=user_name)
                user_image = user.profile.image.url
            except User.DoesNotExist:
                user_image = "/media/default.jpg"

            messages.append({
                "user_name": user_name,
                "user_image": user_image,
                "prompt": user_message,
                "answer": agent_answer,
                "agent_name": agent_name,
                "agent_image": agent.image.url,
                "is_current_user": request.user.username == user_name, # utiliser pour afficher les messages de l'utilisateur actuel
            })

    return JsonResponse(messages, safe=False)


# permet d'afficher le chat
def helb_plays2025(request):
    return render(request, 'agentAI/helb_plays2526.html')
# recupere le fichier de la discussion et permet de l'envoyer en réponse 
def get_chat(request):
    url = "https://helbplays2526.alwaysdata.net/chat.txt"
    response = requests.get(url)
    return HttpResponse(response.text, content_type="text/plain")

def send_message_helb_plays2025(request):
    # Récupérer le message envoyé dans la requête GET
    message = request.GET.get('message')
    
    name = "ali"
    key = "kmKOGucarbc4Eg"
    
    # Encodage en base64 des paramètres
    encoded_name = base64.b64encode(name.encode('utf-8')).decode('utf-8')
    encoded_message = base64.b64encode(message.encode('utf-8')).decode('utf-8')
    encoded_key = base64.b64encode(key.encode('utf-8')).decode('utf-8')

    # Construction de l'URL avec les paramètres encodés
    url = f"https://helbplays2526.alwaysdata.net/chat.php?username={encoded_name}&message={encoded_message}&key={encoded_key}"
    
    # Envoi de la requête GET au serveur externe
    response = requests.get(url)
    
    # Retourner la réponse du serveur
    if response.status_code == 200:
        return HttpResponse("Message envoyé avec succès!")
    else:
        return HttpResponse(f"Erreur lors de l'envoi du message: {response.status_code}", status=response.status_code)

class AIAgentListView(ListView):
    model = AIAgent
    template_name = 'agentAI/home_aiagent.html'
    context_object_name = 'aiAgents'
    ordering = ['-last_activity'] # mettre par le recent vers le plus ancien
    paginate_by = 5

class UserAIAgentListView(ListView):
    model = AIAgent
    template_name = 'agentAI/users_aiagent.html'
    context_object_name = 'aiAgents'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return AIAgent.objects.filter(author=user).order_by('-last_activity')

class AIAgentDetailtView(DetailView):
    model = AIAgent

class AIAgentCreateView(LoginRequiredMixin, CreateView):
    model = AIAgent
    fields = ['name', 'description', 'initial_prompt', 'model', 'cooldown', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AIAgentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AIAgent
    fields = ['name', 'description', 'initial_prompt', 'model', 'cooldown', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        aiAgent = self.get_object()
        return self.request.user == aiAgent.author

class AIAgentDeletetView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AIAgent
    success_url = '/'

    def test_func(self):
        aiAgent = self.get_object()
        if self.request.user == aiAgent.author:
            return True
        return False

    