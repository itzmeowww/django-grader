from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from problem.models import Problem, ProblemResult
from problem.forms import Submission
from .grade import grade

# Create your views here.


class HomeView(ListView):
    template_name = 'problem/home.html'

    context_object_name = 'problems'
    queryset = Problem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = ProblemResult.objects.all()
        return context


def ProblemDetail(request, pk):

    try:
        problem = Problem.objects.get(pk=pk)
    except:
        problem = None

    if request.method == "POST" and request.user.is_authenticated:
        form = Submission(request.POST, request.FILES)

        if form.is_valid():
            code = request.FILES['file']

            grade(code, problem, request.user)

            return redirect('problem', pk)

    results = ProblemResult.objects.filter(problem=problem)

    form = Submission()

    return render(request, 'problem/problem_detail.html', {
        'problem': problem,
        'results': results,
        'form': form
    })
