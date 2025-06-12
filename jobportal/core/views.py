from django.views import generic
from .models import Job, Application
from .forms import JobForm, ApplicationForm, ProfileForm
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import  render
from .models import Job,Profile
from django.contrib.auth import logout
from django.contrib import messages



class HomeView(generic.ListView):
    model = Job
    paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(location__icontains=q)
        return qs

class JobCreateView(LoginRequiredMixin, generic.CreateView):
    model = Job
    form_class = JobForm
    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

class JobDetailView(generic.DetailView):
    model = Job

class ApplyView(LoginRequiredMixin, generic.View):
    def get(self, request, pk):
        form = ApplicationForm()
        return render(request, 'core/apply.html', {'form': form})

    def post(self, request, pk):
        job = Job.objects.get(pk=pk)
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            send_mail(
                subject=f"New Application for {job.title}",
                message=f"{request.user} applied. Cover letter:\n\n{app.cover_letter}",
                from_email='noreply@jobportal.com',
                recipient_list=[job.posted_by.email],
            )
            return redirect('job_detail', pk=pk)
        return render(request, 'core/apply.html', {'form': form})


@login_required
def job_list(request):
    profile = Profile.objects.filter(user=request.user).first()
    if not profile or not profile.resume or not profile.full_name:
        return redirect('create_or_update_profile')

    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'core/job_list.html', {'jobs': jobs})



@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('job_list')  # Make sure 'job_list' is defined in your urls and views
    else:
        form = JobForm()
    return render(request, 'core/add_job.html', {'form': form})

class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = 'jobs'

@login_required
def apply_job(request, pk):
    profile = Profile.objects.filter(user=request.user).first()
    if not profile or not profile.resume or not profile.full_name:
        request.session['next_after_profile'] = request.get_full_path()
        messages.warning(request, "Please complete your profile before applying.")
        return redirect('create_or_update_profile')

    job = get_object_or_404(Job, pk=pk)

    if Application.objects.filter(job=job, applicant=request.user).exists():
        return render(request, 'core/already_applied.html', {'job': job})

    if request.method == 'POST':
        Application.objects.create(job=job, applicant=request.user)
        return render(request, 'core/application_success.html', {'job': job})

    return render(request, 'core/apply_confirm.html', {'job': job})




def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'core/job_detail.html', {'job': job})


@login_required
def create_or_update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # ⏪ Redirect to original job page if stored in session
            next_url = request.session.pop('next_after_profile', None)
            if next_url:
                return redirect(next_url)
            return redirect('job_list')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'core/profile_form.html', {'form': form})


def custom_logout(request):
    logout(request)
    messages.success(request, "You’ve been logged out.")
    return redirect('login')


def logout_confirm_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # ✅ Delete the user's profile
            Profile.objects.filter(user=request.user).delete()
            logout(request)
            messages.success(request, "You have been logged out and your profile has been removed.")
        return redirect('home')  # redirect to homepage
    return render(request, 'core/logout_confirm.html')

