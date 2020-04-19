from django.db import models
from user.models import User

# Create your models here.


class Problem(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    full_score = models.IntegerField(default=100)
    testcases_amount = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class ProblemInOut(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    inp = models.TextField(blank=True)
    out = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super(ProblemInOut, self).save(*args, **kwargs)
        print(ProblemInOut.objects.all())
        self.problem.testcases_amount = ProblemInOut.objects.filter(
            problem=self.problem).count()
        self.problem.save()


class ProblemResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    result = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.problem.title} - {self.user.username}'

    @property
    def score(self):
        score_per_testcase = self.problem.full_score/100
        ret = 0
        for res in self.result:
            if res == 'P':
                ret += score_per_testcase

        return int(ret)
