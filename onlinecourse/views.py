from django.shortcuts import render
from django.http import HttpResponseRedirect
# <HINT> Import any new Models here
from .models import Course, Enrollment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging
from .models import Course, Enrollment, Question, Choice, Submission
# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(
            user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled


# CourseListView
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


# <HINT> A example method to collect the selected choices from the exam form from the request object


def extract_answers(request):
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_answers.append(choice_id)
    return submitted_answers

# <HINT> Create an exam result view to check if learner passed exam and show their question results and result for each question,
# you may implement it based on the following logic:
    # Get course and submission based on their ids
    # Get the selected choice ids from the submission record
    # For each selected choice, check if it is a correct answer or not
    # Calculate the total sselected choicesxam_result(request, course_id, submission_id):


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    submitted_answers = extract_answers(request)
    question = get_object_or_404(Question, pk=course_id)
    user = request.user
    # questions = course.question_set.all()
    questions = []
    # choices = question.choice_set.all()
    choices = []
    correct_choices = []
    correct_choices_ids = []
    submitted_responses = []
    # selected_choices = submission.choices
    selected_choices = submission.choices.all()
    # selected_choices_ids = []
    grade = 0
    
    sel_choices = []
    cor_choices = []
    
    for i in submission.choices.all():
        sel_choices.append(i)
    
    
    
    for i in course.question_set.all():
        questions.append(i)
        
    for i in question.choice_set.all():
        choices.append(i)
    
    for j in course.question_set.all():
        for i in j.choice_set.all():
            if i.is_correct == True:
                correct_choices.append(i)
                correct_choices_ids.append(i.id)       
    
    for i in correct_choices:
        cor_choices.append(i)

    for i in selected_choices:
        submitted_responses.append(i)
        
    for i in sel_choices:
        if i in cor_choices:
        # if sel_choices.index(i) == cor_choices.index(i):
            grade += 100 / len(correct_choices)
        # else: grade -= 100 / len(correct_choices)
                                          
    count = 0
    score = 0
    total_score = grade
    question_results = [] 
    
    question_and_choices = []
    
    for x in questions:
        question_and_choices.append(question)
        
    questionsandanswers = {}
    count = 0  
    
    
    for q in questions:
        questionsandanswers['Option_'+str(count)] = {}
        questionsandanswers['Option_'+str(count)]['Question_'+str(count)] =  q 
        count += 1        
    
    count = 0
    
    for i in cor_choices:
        questionsandanswers['Option_'+str(count)]['Correct_choice_'+str(count)] = i
        count += 1
        
    count = 0
    
    for j in selected_choices:
        questionsandanswers['Option_'+str(count)]['Selected_choice_'+str(count)] = j
        count += 1
        
    
    
    # for q in questions:
        
    #     questionsandanswers['Option_'+str(count)]['question_'+str(count)] = q 
    #     count += 1        
    
    # count = 0
    
    # for i in correct_choices:
    #     questionsandanswers['correct_choice_'+str(count)] = i
    #     count += 1
        
    # count = 0
    
    # for j in selected_choices:
    #     questionsandanswers['selected_choice_'+str(count)] = j
    #     count += 1
        
        
        
        # for i in correct_choices:
        #     questionsandanswers[count][count1] = i
        #     count1 += 1
        #     for j in selected_choices:
        #         questionsandanswers[count][count1] = j
        #         count += 1
        #         count1 = 0
                
    displayresponses = ['Question', 'Your Answer', 'Correct Answer']          
       
        
    context = {
        'course': course,
        'submission': submission,
        'total_score': total_score,
        'question_results': question_results,
        'selected_choices': selected_choices,        
        # 'selected_choices_ids': selected_choices_ids,        
        'displayresponses': displayresponses,
        'correct_choices': correct_choices,
        'questions': questions,
        'question': question,
        'choices': choices,
        # 'request_submitted': request_submitted,
        'correct_choices_ids': correct_choices_ids,
        'submitted_answers': submitted_answers,
        'submitted_responses': submitted_responses,
        'sel_choices': sel_choices,
        'cor_choices': cor_choices,
        'grade': grade,
        'user': user,
        'count': count,
        'questionsandanswers': questionsandanswers
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

# <HINT> Create a submit view to create an exam submission record for a course enrollment,
# you may implement it based on following logic:
    # Get user and course object, then get the associated enrollment object created when the user enrolled the course
    # Create a submission object referring to the enrollment
    # Collect the selected choices from exam form
    # Add each selected choice object to the submission object
    # Redirect to show_exam_result with the submission id
def submit(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    # selected_choices = request.POST.getlist('choice')
    selected_choices = submission.choices.all()
    selected_choices_ids = []
    
    if request.method == 'POST':
        # Get the list of selected choice IDs from the POST dictionary
        # selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                # selected_choices_ids.append(key)
                # selected_choices_ids.append(value)  
                # selected_choices.append(value)  
                submission.choices.add(value) 
                
    
    # for choice in selected_choices:
    #     choice = get_object_or_404(Choice, id=choice_id)
    #     submission.choices.add(choice)
    
    # for i in selected_choices_ids:
    #     choice = get_object_or_404(Choice, id=selected_choices_ids[i])
    #     submission.choices.append(choice)        
        
    for i in selected_choices_ids:
        choice = get_object_or_404(Choice, id=i)
        submission.choices.add(choice)     
    
    # for i in selected_choices:
    #     choice = get_object_or_404(Choice, id=i)
    #     submission.choices.add(choice)        
        
    # context = {
    #         'selected_choices': selected_choices
    #     }

    return redirect('onlinecourse:show_exam_result', course_id=course_id, submission_id=submission.id)

