from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, Investment, SellerProfile, Transaction
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PropertyForm
from .models import SellerProfile

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.groups.filter(name='Seller').exists():
                # Check if the seller is approved by the admin
                if hasattr(user, 'sellerprofile') and user.sellerprofile.is_approved:
                    login(request, user)
                    return redirect('register')
                else:
                    messages.error(request, 'Your seller account is not approved yet. Please contact admin.')
            elif user.groups.filter(name='Buyer').exists():
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'User role not defined.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

@login_required
def add_property(request):
    if not request.user.groups.filter(name='Seller').exists():
        messages.error(request, "You are not authorized to add properties.")
        return redirect('home')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.seller = request.user
            property.save()
            return redirect('seller_dashboard')
    else:
        form = PropertyForm()
    return render(request, 'add_property.html', {'form': form})

@login_required
def home(request):
    # user_name = request.POST['username']  # Assuming the user is logged in
    recent_properties = Property.objects.order_by('-id')[:4]
    return render(request, 'home.html',{'user': request.user,'recent_properties': recent_properties})

def search(request):
    query = request.GET.get('query')
    results = Property.objects.filter(title__icontains=query) | Property.objects.filter(location__icontains=query)
    return render(request, 'search_results.html', {'results': results})

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, password=password)

        if 'is_seller' in request.POST:  # Check if the user is registering as a seller
            # Add user to the "Seller" group
            seller_group, created = Group.objects.get_or_create(name='Seller')
            user.groups.add(seller_group)

            # Create a SellerProfile with `is_approved = False`
            SellerProfile.objects.create(user=user, is_approved=False)
            messages.success(request, "Registration successful. Please wait for admin approval.")
        else:
            # Add user to the "Buyer" group
            buyer_group, created = Group.objects.get_or_create(name='Buyer')
            user.groups.add(buyer_group)
            messages.success(request, "Registration successful. You can now log in.")

        return redirect('login')
    
    return render(request, 'register.html')


def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.method == "POST":
        percentage = float(request.POST.get("percentage"))
        amount = percentage * property.price_per_percent

        if percentage > (100 - property.percentage_sold):
            messages.error(request, f"Only {100 - property.percentage_sold}% is available for purchase.")
            return render(request, "property_detail.html", {"property": property})

        Transaction.objects.create(
            buyer=request.user,
            property=property,
            percentage_bought=percentage,
            amount_paid=amount
        )

        property.percentage_sold += percentage
        property.save()
        messages.success(request, "Transaction successful!")
        return redirect("buyer_dashboard")

    return render(request, "property_detail.html", {"property": property})


@login_required
def user_dashboard(request):
    investments = Investment.objects.filter(user=request.user).select_related('property')
    total_investment = sum(investment.amount_invested for investment in investments)
    return render(request, 'dashboard.html', {
        'investments': investments,
        'total_investment': total_investment,
    })


@login_required
def seller_dashboard(request):
    if not hasattr(request.user, 'sellerprofile') or not request.user.sellerprofile.is_approved:
        return render(request, 'not_approved.html')

    properties = Property.objects.filter(seller=request.user)
    return render(request, 'seller_dashboard.html', {'properties': properties})


@login_required
def superuser_dashboard(request):
    if request.user.is_superuser:
        pending_properties = Property.objects.filter(is_approved=False)
        return render(request, 'superuser_dashboard.html', {'pending_properties': pending_properties})
    return redirect('home')


@login_required
def approve_property(request, property_id):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('home')

    property = get_object_or_404(Property, id=property_id)
    property.is_approved = True
    property.save()
    messages.success(request, "Property approved successfully!")
    return redirect('superuser_dashboard')
