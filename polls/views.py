from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader
from django.utils import timezone

from django.views import generic

from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name ='polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last 5 published questions"""
        return Question.objects.filter( pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        context = {
            'error_message' : "You must select a choice",
            'question':question
    }
        return render(request, 'polls/detail.html' , context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
    # Always return an HttpResponse Redirect after successfully dealing with post data
    # this prevents the data from being counted twice by accident if user hits back button
        return HttpResponseRedirect(reverse('polls:results', args= (question.id, )))
    #     reverse function helps us so we don't have to hardcode URL


    # return HttpResponse("You're voting on question %s." %question_id)
    # return render(request, "polls/vote.html", context)


