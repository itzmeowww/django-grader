from problem.models import ProblemResult, ProblemInOut
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import threading
import time
import os
import grader
import subprocess as sp
import filecmp
import difflib


class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            print('Thread started')
            self.process = sp.Popen(self.cmd, shell=True)
            self.process.communicate()
            print('Thread finished')

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print('Terminating process')
            self.process.terminate()
            thread.join()
        print(self.process.returncode)


def gradingSystem(file, problem, user, problemResult):
    print(f'>Grading : {problem.title} for {user}')

    temp_file = os.path.join(grader.settings.BASE_DIR,
                             f'temp_file\\{problemResult.pk}')
    print(temp_file)
    path = default_storage.save(f'{temp_file}.cpp', ContentFile(file.read()))

    compile = ['g++', '-o', f'{temp_file}-sol.exe', '-std=c++14', path]
    print('Compiling')

    compile_process = sp.Popen(
        compile, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    compile_message = compile_process.communicate()
    print(compile_message)
    inputoutputList = ProblemInOut.objects.filter(problem=problem)

    result = ""
    num = 0
    for inputoutput in inputoutputList:
        num += 1
        if compile_message[1] != b'':
            result += "X"
            continue

        run0 = f'echo {inputoutput.inp} > {temp_file}-{num}.in'
        run0_process = sp.Popen(
            run0, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)

        run = f'{temp_file}-sol.exe < {temp_file}-{num}.in > {temp_file}-{num}.out timeout /t 3'
        run2 = f'echo {inputoutput.out} > {temp_file}-{num}.cout'
        run2_process = sp.Popen(
            run2, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)

        start_time = time.time()

        command = Command(run)
        command.run(timeout=3)

        print(f'Time {time.time() - start_time}')
        if (time.time() - start_time > 2.5):
            result += "T"
            continue
        # test = f"FC /B {temp_file}-{num}.out {temp_file}-{num}.cout"
        # test_process = sp.Popen(
        #       test, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        # print(test_process.communicate())
        res = True
        f1 = open(f"{temp_file}-{num}.out", "r")
        f2 = open(f"{temp_file}-{num}.cout", "r")
        if(len(f1.readlines()) < len(f2.readlines())):
            res = False
        for line1 in f1:
            for line2 in f2:
                if line1 == line2:
                    print("SAME\n")
                else:
                    res = False
                    print(line1 + line2)
                    break
        f1.close()
        f2.close()

        if res:
            result += 'P'
        else:
            result += '-'

    print(f'+Graded : {problem.title} for {user} : {result}')

    problemResult.result = result
    problemResult.save()


def grade(file, problem, user):
    result = 'Grading'
    problemResult = ProblemResult(user=user, problem=problem, result=result)
    problemResult.save()
    thread = threading.Thread(target=gradingSystem, args=(
        file, problem, user, problemResult))
    thread.start()
