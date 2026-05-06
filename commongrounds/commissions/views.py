from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Commission, Job, JobApplication  
from .forms import CommissionForm, JobFormSet, JobApplicationForm
from django.db.models import Case, When, Value, IntegerField
# Create your views here.

def commission_list(request):
    sort_logic = Case(
        When(status='Open', then=Value(1)),
        When(status='Full', then=Value(2)),
        When(status='Completed', then=Value(3)),
        When(status='Discontinued', then=Value(4)),
        output_field=IntegerField(),
    )

    all_commissions = Commission.objects.annotate(
        custom_order=sort_logic
    ).order_by('custom_order', '-created_on')

    created_commissions = []
    applied_commissions = []
    other_commissions = all_commissions 

    if request.user.is_authenticated:
        profile = request.user.profile
        created_commissions = all_commissions.filter(maker=profile)
        applied_commissions = all_commissions.filter(jobs__applications__applicant=profile).distinct()
        other_commissions = all_commissions.exclude(maker=profile).exclude(jobs__applications__applicant=profile)

    context = {
        'created_commissions': created_commissions,
        'applied_commissions': applied_commissions,
        'other_commissions': other_commissions,
    }
    return render(request, 'commissions/commission_list.html', context)


def commission_detail(request, pk):
    commission = get_object_or_404(Commission, pk=pk)

    total_manpower = 0
    accepted_signees = 0
    jobs = []

    for job in commission.jobs.all():
        total_manpower += job.manpower_required
        accepted_apps = job.applications.filter(status='Accepted').count()
        accepted_signees += accepted_apps
        job.is_full = accepted_apps >= job.manpower_required
        jobs.append(job)

    open_manpower = total_manpower - accepted_signees

    job_application_form = JobApplicationForm()
    if request.method == "POST" and request.user.is_authenticated:
        if request.user.profile == commission.maker:
            return redirect('commissions:commission_detail', pk=commission.pk)

        job_application_form = JobApplicationForm(request.POST)
        if job_application_form.is_valid():
            job_id = request.POST.get('job_id')
            job_to_apply = get_object_or_404(Job, pk=job_id)

            JobApplication.objects.get_or_create(
                job=job_to_apply,
                applicant=request.user.profile,
                defaults={'status': 'Pending'}
            )
        return redirect('commissions:commission_detail', pk=commission.pk)

    context = {
        'commission': commission,
        'total_manpower': total_manpower,
        'open_manpower': open_manpower,
        'jobs': jobs,
        'job_application_form': job_application_form,
    }
    return render(request, 'commissions/commission_detail.html', context)


@login_required
def commission_create(request):
    if request.user.profile.role != "Commission Maker":
        return redirect('commissions:commission_list')

    if request.method == "POST":
        form = CommissionForm(request.POST)
        job_formset = JobFormSet(request.POST)

        if form.is_valid() and job_formset.is_valid():
            commission = form.save(commit=False)
            commission.maker = request.user.profile
            commission.save()

            job_formset.instance = commission
            job_formset.save()

            return redirect('commissions:commission_detail', pk=commission.pk)
    else:
        form = CommissionForm()
        job_formset = JobFormSet()

    context = {
        'form': form,
        'job_formset': job_formset
    }
    return render(request, 'commissions/commission_form.html', context)


@login_required
def commission_update(request, pk):
    commission = get_object_or_404(Commission, pk=pk)

    if request.user.profile.role != "Commission Maker" or request.user.profile != commission.maker:
        return redirect('commissions:commission_list')

    if request.method == "POST":
        form = CommissionForm(request.POST, instance=commission)
        job_formset = JobFormSet(request.POST, instance=commission)

        if form.is_valid() and job_formset.is_valid():
            commission = form.save()
            job_formset.save()

            all_full = True
            for job in commission.jobs.all():
                if job.status != 'Full':
                    all_full = False
                    break

            if all_full and commission.jobs.count() > 0:
                commission.status = 'Full'
                commission.save()

            return redirect('commissions:commission_detail', pk=commission.pk)
    else:
        form = CommissionForm(instance=commission)
        job_formset = JobFormSet(instance=commission)

    context = {
        'form': form,
        'job_formset': job_formset
    }
    return render(request, 'commissions/commission_form.html', context)