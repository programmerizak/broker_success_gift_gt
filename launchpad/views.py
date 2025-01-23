from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LaunchPad


@login_required
def launchpad_list(request, status=None):
    context = {'page_title': 'Launch Pad'}
    if status:
        launchpads = LaunchPad.objects.filter(status=status)
        context['page_title'] = f"Launch {status}"
    else:
        launchpads = LaunchPad.objects.all()
    context['launchpads'] = launchpads
    return render(request, "launchpad/launchpad_list.html", context)



@login_required
def launchpad_detail(request,status_given,launchpad_id):
    # Retrieve the launchpad object or return a 404 error if not found
    launchpad = get_object_or_404(LaunchPad,status=status_given,pk=launchpad_id)
    
    # Pass the launchpad object to the template
    context = {
        'launchpad': launchpad,
        'page_title': f'{launchpad.coin_name} Launch Pad Details'
    }
    
    # Render the template with the launchpad details
    return render(request, 'launchpad/launchpad_detail.html', context)
