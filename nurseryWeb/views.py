from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from authentication.models import UserProfile
from django.contrib.auth.hashers import make_password, check_password
import re

def home(request):
    return render(request, 'login.html')

def main(request):
    if 'user_id' not in request.session:
        return redirect('userlogin')
    try:
        user = UserProfile.objects.get(mobile=request.session['user_id'])
    except UserProfile.DoesNotExist:
        # If user is not found, redirect to login
        messages.error(request, 'User not found. Please log in again.')
        return redirect('userlogin')
    
    return render(request, 'index.html',{'user': user})


def login_view(request):
    errors = {}
    form_data = {}

    if request.method == 'POST':
        form_data = request.POST
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate that email and password are provided
        if not email:
            errors['email'] = "Email is required."
        if not password:
            errors['password'] = "Password is required."

        if errors:
            return render(request, 'login.html', {
                'active_tab': 'login',
                'errors': errors,
                'form_data': form_data,
                'messages': messages.get_messages(request)
            })

        try:
            user = UserProfile.objects.get(email=email)  # Fetch user profile using email
            if check_password(password, user.password):
                # Successful login
                request.session['user_id'] = user.mobile  # Store user info in session
                return redirect('main')  # Redirect to the main page on successful login
            else:
                messages.error(request, 'Invalid email or password.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'User doesn\'t exist.')

    return render(request, 'login.html', {
        'active_tab': 'login',
        'messages': messages.get_messages(request)
    })

def signup_view(request):
    errors = {}
    form_data = {}

    if request.method == 'POST':
        form_data = request.POST
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Required fields check
        required_fields = ['name', 'email', 'mobile', 'password1', 'password2']
        for field in required_fields:
            if not request.POST.get(field):
                errors[field] = "This field is required."

        # Validate that passwords match
        if password1 != password2:
            errors['password'] = "Passwords do not match."
        else:
            password_regex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    
            if not password_regex.match(password1):
                errors['password'] = ("Password must be at least 8 characters long, "
                                    "and include at least one uppercase letter, "
                                    "one lowercase letter, one digit, and one special character.")

        # Check if email already exists
        if UserProfile.objects.filter(email=email).exists():
            errors['email'] = "Email is already in use."

        # Check if mobile number is valid (assuming 10 digits)
        if not mobile.isdigit() or len(mobile) != 10:
            errors['mobile'] = "Mobile number must be 10 digits long."

        if errors:
            return render(request, 'login.html', {
                'active_tab': 'signup',
                'errors': errors,
                'form_data': form_data,
                'messages': messages.get_messages(request)
            })

        # Create new user
        user = UserProfile(
            mobile=mobile,
            name=name,
            email=email,
            password=make_password(password1)  # Hash the password
        )
        user.save()
        messages.success(request, 'Signup successful. You can now log in.')
        return redirect('userlogin')  # Redirect to login page after successful signup

    return render(request, 'login.html', {
        'active_tab': 'signup',
        'messages': messages.get_messages(request)
    })


def logout_view(request):
    logout(request)
    return redirect('userlogin')


PLANTS = {
    'rose': {
        'name': 'Rose',
        'description': 'A rose is a woody perennial flowering plant. Best grown in sunny areas.',
        'image': 'https://images.unsplash.com/photo-1562025080-79fa68855dfc'
    },
    'lavender': {
        'name': 'Lavender',
        'description': 'Lavender is a flowering plant in the mint family. It prefers well-drained soil.',
        'image': 'https://images.unsplash.com/photo-1592175968026-dabed055f118'
    },
    'aloe-vera': {
        'name': 'Aloe Vera',
        'description': 'Aloe Vera is a succulent plant species known for its medicinal properties.',
        'image': 'https://images.unsplash.com/photo-1592004676757-1f649a7d4e05'
    },
    'snake-plant': {
        'name': 'Snake Plant',
        'description': 'Low light, low maintenance plant. Perfect for indoor spaces.',
        'image': 'https://images.unsplash.com/photo-1580894923947-bd41f1d0038c'
    },
    'fiddle-leaf': {
        'name': 'Fiddle Leaf Fig',
        'description': 'Popular indoor plant with large, glossy leaves. Prefers bright, indirect light.',
        'image': 'https://images.unsplash.com/photo-1563958818-155a7ef07736'
    },
    'pothos': {
        'name': 'Pothos',
        'description': 'Easy care trailing plant with heart-shaped leaves. Ideal for beginners.',
        'image': 'https://images.unsplash.com/photo-1585081357967-e2f5d75e4f9e'
    },
    'philodendron': {
        'name': 'Philodendron',
        'description': 'Heart-shaped leaves, easy to grow. Thrives in low to medium light.',
        'image': 'https://images.unsplash.com/photo-1601580881033-63c5f5b6d4a7'
    }
}

def plant_details(request, plant_name):
    # Get the plant details based on the plant_name parameter
    plant = PLANTS.get(plant_name)
    
    # If the plant does not exist, you could handle it with a 404 page
    if not plant:
        return render(request, '404.html', status=404)
    
    # Pass the plant details to the template
    return render(request, 'plant-details.html', {'plant': plant})


def browse(request):
    category = request.GET.get('category', '')
    plants_data = {
    'flowers': [
        {'name': 'Rose', 'description': 'Beautiful red rose.', 'image': 'img/Rose.jpg'},
        {'name': 'Tulip', 'description': 'Elegant and colorful tulips.', 'image': 'img/Tulip.jpg'},
        {'name': 'Daffodil', 'description': 'Bright yellow daffodils.', 'image': 'https://images.unsplash.com/photo-1600119824013-c08f29c1e60e'},
        {'name': 'Lily', 'description': 'Pure white lilies.', 'image': 'https://images.unsplash.com/photo-1544213456-bd1d6611ab9b'},
        {'name': 'Sunflower', 'description': 'Large and radiant sunflowers.', 'image': 'https://images.unsplash.com/photo-1585996951440-9a87b3a93dd8'},
        {'name': 'Orchid', 'description': 'Exotic orchid flowers.', 'image': 'https://images.unsplash.com/photo-1542596169-cbc45a5b35d5'},
        {'name': 'Jasmine', 'description': 'Fragrant jasmine flowers.', 'image': 'https://images.unsplash.com/photo-1558238883-62c8d4c8c13c'},
        {'name': 'Daisy', 'description': 'White and yellow daisies.', 'image': 'https://images.unsplash.com/photo-1569864584366-1bdf9cd9f6a5'},
        {'name': 'Chrysanthemum', 'description': 'Colorful chrysanthemums.', 'image': 'https://images.unsplash.com/photo-1599932172856-36d1f609f5fe'},
        {'name': 'Lavender', 'description': 'Calming lavender flowers.', 'image': 'https://images.unsplash.com/photo-1560799009-859073672da6'}
    ],
    'succulents': [
        {'name': 'Aloe Vera', 'description': 'Healing aloe vera.', 'image': 'img/Aloe_Vera.jpg'},
        {'name': 'Cactus', 'description': 'A spiky but beautiful succulent.', 'image': 'https://images.unsplash.com/photo-1544476310-5b8c5f80b3a1'},
        {'name': 'Echeveria', 'description': 'Rosette-shaped echeveria.', 'image': 'https://images.unsplash.com/photo-1564869735415-54bdb4fd4763'},
        {'name': 'Jade Plant', 'description': 'Feng Shui friendly jade plant.', 'image': 'https://images.unsplash.com/photo-1586864391653-74cdeafdcfa7'},
        {'name': 'Zebra Plant', 'description': 'Striped zebra succulent.', 'image': 'https://images.unsplash.com/photo-1516925062877-41cbb60c2721'},
        {'name': 'Panda Plant', 'description': 'Soft, furry leaves of the panda plant.', 'image': 'https://images.unsplash.com/photo-1622515823207-2d9506fdbd95'},
        {'name': 'String of Pearls', 'description': 'Unique succulent with pearl-like beads.', 'image': 'https://images.unsplash.com/photo-1621969152213-8b91a5c6bfa4'},
        {'name': 'Snake Plant', 'description': 'Easy to care snake plant.', 'image': 'img/Snake_Plant.jpg'},  # Assuming local image for Snake Plant
        {'name': 'Sedum', 'description': 'Vibrant sedum succulent.', 'image': 'https://images.unsplash.com/photo-1596244642909-79e2d582174f'},
        {'name': 'Agave', 'description': 'Large, striking agave plant.', 'image': 'https://images.unsplash.com/photo-1586015552890-82a1913f1b9f'}
    ],
    'herbs': [
        {'name': 'Basil', 'description': 'Perfect for Italian dishes.', 'image': 'img/Basil.jpg'},
        {'name': 'Mint', 'description': 'Fresh mint for your drinks and meals.', 'image': 'img/Mint.jpg'},
        {'name': 'Cilantro', 'description': 'Cilantro for vibrant flavors.', 'image': 'https://images.unsplash.com/photo-1589884299339-4d6f07a31e9b'},
        {'name': 'Thyme', 'description': 'Aromatic thyme.', 'image': 'https://images.unsplash.com/photo-1600585151948-3d77c5051057'},
        {'name': 'Rosemary', 'description': 'Fragrant rosemary sprigs.', 'image': 'https://images.unsplash.com/photo-1604607447104-0e13c51a702e'},
        {'name': 'Oregano', 'description': 'Mediterranean oregano herb.', 'image': 'https://images.unsplash.com/photo-1596075781086-078110b73fb5'},
        {'name': 'Sage', 'description': 'Sage for culinary and medicinal use.', 'image': 'https://images.unsplash.com/photo-1591801674112-caf01ebf4b14'},
        {'name': 'Chives', 'description': 'Mild onion flavor chives.', 'image': 'https://images.unsplash.com/photo-1592501184331-726b59bc2ebf'},
        {'name': 'Lemongrass', 'description': 'Lemongrass for teas and soups.', 'image': 'https://images.unsplash.com/photo-1561449099-70ca587b6634'},
        {'name': 'Parsley', 'description': 'Fresh parsley leaves.', 'image': 'https://images.unsplash.com/photo-1571707231452-e4e6b9a69bbd'}
    ]
}

    context = {
        'category': category,
        'plants': plants_data.get(category, [])
    }
    return render(request, 'browse.html', context)