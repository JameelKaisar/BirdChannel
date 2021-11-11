from django.shortcuts import render, redirect
from .models import ConservationCategory, ConservationContent, BirdingCategory, BirdingContent
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import MyRegistrationForm, MyLoginForm, ChangePasswordForm, AddConservationCategory, AddConservationContent, EditConservationCategory, EditConservationContent, AddBirdingCategory, AddBirdingContent, EditBirdingCategory, EditBirdingContent
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.core.management import call_command
from django.utils import timezone
from pathlib import Path
from shutil import copytree

# Create your views here.

def is_birder(user):
    if user.is_authenticated:
        if user.is_superuser or "birder" in [g.name for g in user.groups.all()]:
            return True
    return False

def homepage(request):
    return render(
        request=request,
        template_name="main/home.html",
        context={"title": "Home"}
        )

def aboutpage(request):
    return render(
        request=request,
        template_name="main/about.html",
        context={"title": "About"}
        )

def contactpage(request):
    return render(
        request=request,
        template_name="main/contact.html",
        context={"title": "Contact"}
        )

def helppage(request):
    return render(
        request=request,
        template_name="main/help.html",
        context={"title": "Help"}
        )

def register(request):
    if request.user.is_authenticated:
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        else:
            messages.info(request, "You are already logged in!")
            return redirect("main:homepage")
    else:
        if request.method == "POST":
            form = MyRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get("username")
                messages.info(request, f"New Account Created: {username}")
                login(request, user)
                messages.info(request, f"You are now logged in as {username}!")
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect("main:homepage")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
            return redirect(request.get_full_path())

        form = MyRegistrationForm
        return render(
            request=request,
            template_name="main/register.html",
            context={"title": "Register", "form": form, "next": request.GET.get('next')})

def login_request(request):
    if request.user.is_authenticated:
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        else:
            messages.info(request, "You are already logged in!")
            return redirect("main:homepage")
    else:
        if request.method == "POST":
            form = MyLoginForm(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password  = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}!")
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect("main:homepage")
                else:
                    messages.error(request, "Invalid username or password!")
            else:
                messages.error(request, "Invalid username or password!")
            return redirect(request.get_full_path())

        form = MyLoginForm()
        return render(
            request=request,
            template_name="main/login.html",
            context={"title": "Login", "form": form, "next": request.GET.get('next')})

def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.info(request, "Your password was changed successfully!")
                return redirect("main:profile")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
            return redirect(request.get_full_path())

        form = ChangePasswordForm(request.user)
        return render(
            request=request,
            template_name="main/change_password.html",
            context={"title": "Change Password", "form": form})
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Logged out successfully!")
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    else:
        return redirect("main:homepage")

def profile(request):
    if request.user.is_authenticated:
        return render(
            request=request,
            template_name="main/profile.html",
            context={"title": "Profile"}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

def admin_section(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                if request.POST.get('data_type') == "mb":
                    try:
                        if request.POST.get('data_act') == "0":
                            user_obj = User.objects.get(id=request.POST.get('data_id'))
                            group_obj = Group.objects.get(name='birder')
                            group_obj.user_set.remove(user_obj)
                            messages.info(request, f"{user_obj.username} demoted as birder!")
                            return redirect(f"/admin/?open=mb&page={request.POST.get('data_page')}")
                        else:
                            return redirect("main:homepage")
                    except:
                        return redirect("main:homepage")
                elif request.POST.get('data_type') == "mu":
                    try:
                        if request.POST.get('data_act') == "0":
                            user_obj = User.objects.get(id=request.POST.get('data_id'))
                            group_obj = Group.objects.get(name='birder')
                            group_obj.user_set.remove(user_obj)
                            messages.info(request, f"{user_obj.username} demoted as birder!")
                            return redirect(f"/admin/?open=mu&page={request.POST.get('data_page')}")
                        elif request.POST.get('data_act') == "1":
                            user_obj = User.objects.get(id=request.POST.get('data_id'))
                            group_obj = Group.objects.get(name='birder')
                            group_obj.user_set.add(user_obj)
                            messages.info(request, f"{user_obj.username} promoted to birder!")
                            return redirect(f"/admin/?open=mu&page={request.POST.get('data_page')}")
                        elif request.POST.get('data_act') == "2":
                            user_obj = User.objects.get(id=request.POST.get('data_id'))
                            user_obj_username = user_obj.username
                            user_obj.delete()
                            messages.info(request, f"{user_obj_username} deleted successfully!")
                            return redirect(f"/admin/?open=mu&page={request.POST.get('data_page')}")
                        else:
                            return redirect("main:homepage")
                    except:
                        return redirect("main:homepage")
                elif request.POST.get('data_type') == "md":
                    if request.POST.get('data_act') == "1":
                        try:
                            backup_time = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
                            backup_folder = "database_backup_" + backup_time + "/"
                            backup_file = "database_backup_" + backup_time + ".json"
                            backup_folder_path = "backup/full/" + backup_folder
                            backup_file_path = backup_folder_path + backup_file
                            Path("backup/full/").mkdir(parents=True, exist_ok=True)
                            Path("media/").mkdir(parents=True, exist_ok=True)
                            copytree("media/", backup_folder_path)
                            call_command("dumpdata_utf8", output=backup_file_path)
                            # Using Default dumpdata Command
                            # with open(backup_file_path, mode="w", encoding='utf-8') as f:
                            #     call_command("dumpdata", stdout=f)
                            messages.info(request, "Backup taken successfully!")
                            return redirect("/admin/?open=md")
                        except:
                            messages.error(request, "Unable to take the backup!")
                            return redirect("/admin/?open=md")
                    elif request.POST.get('data_act') == "2":
                        try:
                            backup_time = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
                            backup_file_name = "database_backup_" + backup_time + ".json"
                            backup_file_path = "backup/partial/" + backup_file_name
                            Path("backup/partial/").mkdir(parents=True, exist_ok=True)
                            call_command("dumpdata_utf8", output=backup_file_path)
                            # Using Default dumpdata Command
                            # with open(backup_file_path, mode="w", encoding='utf-8') as f:
                            #     call_command("dumpdata", stdout=f)
                            # download_file = open(backup_file_path, "rb")
                            # response_file = HttpResponse(download_file)
                            # response_file['Content-Type'] = 'application/file'
                            # response_file['Content-Disposition'] = f'attachment; filename="{backup_file_name}"'
                            messages.info(request, "Backup taken successfully!")
                            # return response_file
                            return redirect("/admin/?open=md")
                        except:
                            messages.error(request, "Unable to take the backup!")
                            return redirect("/admin/?open=md")
                    elif request.POST.get('data_act') == "3":
                        # Restore Backup
                        messages.info(request, "This feature is under construction!")
                        return redirect("/admin/?open=md")
                    elif request.POST.get('data_act') == "4":
                        try:
                            if request.user.check_password(request.POST.get('data_pass')):
                                super_username = request.user.username
                                super_password = request.POST.get('data_pass')
                                call_command("flush", "--no-input")
                                call_command("app_init", username=super_username, password=super_password)
                                # User.objects.create_superuser(username=super_username, password=super_password)
                                super_user = authenticate(username=super_username, password=super_password)
                                if super_user is not None:
                                    login(request, super_user)
                                    messages.info(request, "Data erased successfully!")
                                else:
                                    messages.error(request, "Unknown Error!")
                                return redirect("/admin/?open=md")
                            else:
                                messages.error(request, "Incorrect Password!")
                                return redirect("/admin/?open=md")
                        except:
                            messages.error(request, "Unknown Error!")
                            return redirect("/admin/?open=md")
                    else:
                        return redirect("main:homepage")
                else:
                    return redirect("main:homepage")
                return redirect(request.get_full_path())

            birder_group = Group.objects.get(name='birder')
            birders = birder_group.user_set.order_by('username')
            page_birders = Paginator(birders, 20)
            if request.GET.get('open') == "mt":
                page_number = request.GET.get('page')
                page_obj_birders = page_birders.get_page(page_number)
            else:
                page_obj_birders = page_birders.get_page(1)

            users = User.objects.order_by('username')
            page_users = Paginator(users, 20)
            if request.GET.get('open') == "mu":
                page_number = request.GET.get('page')
                page_obj_users = page_users.get_page(page_number)
            else:
                page_obj_users = page_users.get_page(1)

            return render(
                request=request,
                template_name="main/admin.html",
                context={"title": "Admin Section", "birder_group": birder_group, "page_obj_birders": page_obj_birders, "page_obj_users": page_obj_users, "open": request.GET.get('open')}
                )
        else:
            messages.error(request, "You need to have superuser privileges to view this page!")
            return redirect("main:homepage")
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

def birds_section(request):
    return HttpResponse("Birds Section")

def conservation_categories(request):
    if request.method == "POST" and is_birder(request.user):
        form = AddConservationCategory(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Category Added Successfully!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
        return redirect(request.get_full_path())

    form = AddConservationCategory()
    return render(
        request=request,
        template_name="main/conservation-categories.html",
        context={"title": "Conservation", "birder": is_birder(request.user), "conservation_categories": reversed(ConservationCategory.objects.all()), "form": form, "next": request.get_full_path()}
        )

def conservation_content(request, category_slug):
    category_slugs = [c.category_slug for c in ConservationCategory.objects.all()]
    if category_slug in category_slugs:
        category_slug_name = ConservationCategory.objects.filter(category_slug=category_slug)[0].conservation_category
        matching_content = ConservationContent.objects.filter(content_category__category_slug=category_slug)

        if request.method == "POST" and request.user.is_authenticated:
            form = AddConservationContent(request.POST, request.FILES)
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.content_user = request.user
                form.save()
                messages.info(request, "Content Added Successfully!")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
            return redirect(request.get_full_path())

        form = AddConservationContent(initial={"content_category": ConservationCategory.objects.filter(category_slug=category_slug)[0]})
        content = matching_content.order_by('-content_time')
        page_content = Paginator(content, 12)
        page_number = request.GET.get('page')
        page_obj = page_content.get_page(page_number)
        return render(
            request=request,
            template_name="main/conservation-content.html",
            context={"title": category_slug_name, "birder": is_birder(request.user), "page_obj": page_obj, "category_slug": category_slug, "category_slug_name": category_slug_name, "form": form, "next": request.get_full_path()}
            )
    else:
        messages.error(request, f"{category_slug} category is not present!")
        return redirect("main:conservation_categories")

def birding_categories(request):
    if request.method == "POST" and is_birder(request.user):
        form = AddBirdingCategory(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Category Added Successfully!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
        return redirect(request.get_full_path())

    form = AddBirdingCategory()
    return render(
        request=request,
        template_name="main/birding-categories.html",
        context={"title": "Birding", "birder": is_birder(request.user), "birding_categories": reversed(BirdingCategory.objects.all()), "form": form, "next": request.get_full_path()}
        )

def birding_content(request, category_slug):
    category_slugs = [c.category_slug for c in BirdingCategory.objects.all()]
    if category_slug in category_slugs:
        category_slug_name = BirdingCategory.objects.filter(category_slug=category_slug)[0].birding_category
        matching_content = BirdingContent.objects.filter(content_category__category_slug=category_slug)

        if request.method == "POST" and request.user.is_authenticated:
            form = AddBirdingContent(request.POST, request.FILES)
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.content_user = request.user
                form.save()
                messages.info(request, "Content Added Successfully!")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
            return redirect(request.get_full_path())

        form = AddBirdingContent(initial={"content_category": BirdingCategory.objects.filter(category_slug=category_slug)[0]})
        content = matching_content.order_by('-content_time')
        page_content = Paginator(content, 12)
        page_number = request.GET.get('page')
        page_obj = page_content.get_page(page_number)
        return render(
            request=request,
            template_name="main/birding-content.html",
            context={"title": category_slug_name, "birder": is_birder(request.user), "page_obj": page_obj, "category_slug": category_slug, "category_slug_name": category_slug_name, "form": form, "next": request.get_full_path()}
            )
    else:
        messages.error(request, f"{category_slug} category is not present!")
        return redirect("main:birding_categories")

def delete_data(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get('data_type') == "conservation-category" and is_birder(request.user):
                try:
                    if ConservationContent.objects.filter(content_category=request.POST.get('data_id')).count():
                        messages.error(request, "Non-empty Categories can't be Deleted!")
                    else:
                        instance = ConservationCategory.objects.get(id=request.POST.get('data_id'))
                        instance.delete()
                        messages.info(request, "Category Deleted Successfully!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "conservation-content":
                try:
                    instance = ConservationContent.objects.get(id=request.POST.get('data_id'))
                    if instance.content_user == request.user or is_birder(request.user):
                        instance.delete()
                        messages.info(request, "Content Deleted Successfully!")
                        if request.POST.get('data_next'):
                            return redirect(request.POST.get('data_next'))
                        else:
                            return redirect("main:homepage")
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "birding-category" and is_birder(request.user):
                try:
                    if BirdingContent.objects.filter(content_category=request.POST.get('data_id')).count():
                        messages.error(request, "Non-empty Categories can't be Deleted!")
                    else:
                        instance = BirdingCategory.objects.get(id=request.POST.get('data_id'))
                        instance.delete()
                        messages.info(request, "Category Deleted Successfully!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "birding-content":
                try:
                    instance = BirdingContent.objects.get(id=request.POST.get('data_id'))
                    if instance.content_user == request.user or is_birder(request.user):
                        instance.delete()
                        messages.info(request, "Content Deleted Successfully!")
                        if request.POST.get('data_next'):
                            return redirect(request.POST.get('data_next'))
                        else:
                            return redirect("main:homepage")
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            else:
                return redirect("main:homepage")
        else:
            return redirect("main:homepage")
    else:
        return redirect("main:homepage")

def edit_data(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get('data_type') == "conservation-category" and is_birder(request.user):
                try:
                    instance = ConservationCategory.objects.get(id=request.POST.get('data_id'))
                    form = EditConservationCategory(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "conservation_category": instance.conservation_category, "category_summary": instance.category_summary})
                    return render(
                        request=request,
                        template_name="main/edit-data.html",
                        context={"title": "Edit Category", "form": form}
                        )
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-conservation-category" and is_birder(request.user):
                try:
                    instance = ConservationCategory.objects.get(id=request.POST.get('data_id'))
                    instance.conservation_category = request.POST.get('conservation_category')
                    instance.category_summary = request.POST.get('category_summary')
                    if instance.category_slug == slugify(instance.conservation_category):
                        try:
                            instance.save()
                            messages.info(request, "Category Edited Successfully!")
                        except:
                            messages.error(request, "Error while saving the category!")
                    else:
                        current_categories = ConservationCategory.objects.all()
                        for current_category in current_categories:
                            if current_category.category_slug == slugify(instance.conservation_category):
                                messages.error(request, f'Category with name \"{instance.conservation_category}\" already exists.')
                                break
                        else:
                            instance.category_slug = slugify(instance.conservation_category)
                            try:
                                instance.save()
                                messages.info(request, "Category Edited Successfully!")
                            except:
                                messages.error(request, "Error while saving the category!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "conservation-content":
                try:
                    instance = ConservationContent.objects.get(id=request.POST.get('data_id'))
                    if instance.content_user == request.user:
                        form = EditConservationContent(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "conservation_content": instance.conservation_content, "content_text": instance.content_text})
                        return render(
                            request=request,
                            template_name="main/edit-data.html",
                            context={"title": "Edit Content", "form": form}
                            )
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-conservation-content":
                try:
                    instance = ConservationContent.objects.get(id=request.POST.get('data_id'))
                    if instance.content_user == request.user:
                        instance.conservation_content = request.POST.get('conservation_content')
                        instance.content_text = request.POST.get('content_text')
                        try:
                            instance.save()
                            messages.info(request, "Content Edited Successfully!")
                        except:
                            messages.error(request, "Error while saving the content!")
                        if request.POST.get('data_next'):
                            return redirect(request.POST.get('data_next'))
                        else:
                            return redirect("main:homepage")
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "birding-category" and is_birder(request.user):
                try:
                    instance = BirdingCategory.objects.get(id=request.POST.get('data_id'))
                    form = EditBirdingCategory(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "birding_category": instance.birding_category, "category_summary": instance.category_summary})
                    return render(
                        request=request,
                        template_name="main/edit-data.html",
                        context={"title": "Edit Category", "form": form}
                        )
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-birding-category" and is_birder(request.user):
                try:
                    instance = BirdingCategory.objects.get(id=request.POST.get('data_id'))
                    instance.birding_category = request.POST.get('birding_category')
                    instance.category_summary = request.POST.get('category_summary')
                    if instance.category_slug == slugify(instance.birding_category):
                        try:
                            instance.save()
                            messages.info(request, "Category Edited Successfully!")
                        except:
                            messages.error(request, "Error while saving the category!")
                    else:
                        current_categories = BirdingCategory.objects.all()
                        for current_category in current_categories:
                            if current_category.category_slug == slugify(instance.birding_category):
                                messages.error(request, f'Category with name \"{instance.birding_category}\" already exists.')
                                break
                        else:
                            instance.category_slug = slugify(instance.birding_category)
                            try:
                                instance.save()
                                messages.info(request, "Category Edited Successfully!")
                            except:
                                messages.error(request, "Error while saving the category!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "birding-content":
                try:
                    instance = BirdingContent.objects.get(id=request.POST.get('data_id'))
                    if instance.content_user == request.user:
                        form = EditBirdingContent(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "birding_content": instance.birding_content, "content_text": instance.content_text})
                        return render(
                            request=request,
                            template_name="main/edit-data.html",
                            context={"title": "Edit Content", "form": form}
                            )
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-birding-content":
                try:
                    instance = BirdingContent.objects.get(id=request.POST.get('data_id'))
                    if instance.content_user == request.user:
                        instance.birding_content = request.POST.get('birding_content')
                        instance.content_text = request.POST.get('content_text')
                        try:
                            instance.save()
                            messages.info(request, "Content Edited Successfully!")
                        except:
                            messages.error(request, "Error while saving the content!")
                        if request.POST.get('data_next'):
                            return redirect(request.POST.get('data_next'))
                        else:
                            return redirect("main:homepage")
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            else:
                return redirect("main:homepage")
        else:
            return redirect("main:homepage")
    else:
        return redirect("main:homepage")
