from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from immarot.templatetags.dynamic_forms import get_model_form
from users.models import CustomGroup
from django.utils.text import slugify
from .forms import AuthorForm
from django.urls import reverse
from django.contrib import messages
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.apps import apps
from django import forms
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
class Index(LoginRequiredMixin, TemplateView):

    login_url = reverse_lazy('login')
    template_name = "immarot/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        role = getattr(self.request.user, 'roles', None)
        menu_permissions = []

        
        if role:
            processed_models = set()  # To track unique (app_name, model_name) combinations

            for menu in role.menu.all():
                permission_dict = {'add': False, 'change': False, 'delete': False, 'view': False}

                # Loop through all permissions for the current menu
                for perm in menu.permissions.all():
                    # Retrieve the app_label and model name from the content_type
                    content_type = perm.content_type
                    app_name = content_type.app_label
                    model_name = content_type.model

                    # Ensure that only unique (app_name, model_name) combinations are processed
                    if (app_name, model_name) not in processed_models:
                        print("App Name:", app_name)
                        print("Model Name:", model_name)

                        # Get the model class and dynamically retrieve its fields
                        model_class = content_type.model_class()
                        
                        if model_class:
                            field_names = [field.name for field in model_class._meta.fields]
                        else:
                            field_names = []  # Fallback if the model class is not found

                        processed_models.add((app_name, model_name))  # Mark as processed

                    # Update permissions based on codename
                    if 'add' in perm.codename:
                        permission_dict['add'] = True
                    elif 'change' in perm.codename:
                        permission_dict['change'] = True
                    elif 'delete' in perm.codename:
                        permission_dict['delete'] = True
                    elif 'view' in perm.codename:
                        permission_dict['view'] = True

                # Append the menu information for each unique permission set
                menu_permissions.append({
                    'name': menu.title,
                    'slug': slugify(menu.name),  # Assuming you have a 'slug' field
                    'permissions': permission_dict.copy(),  # Use a copy to prevent overwrites
                    'app_name': app_name,
                    'model_name': model_name.capitalize(),
                    'fields': ','.join(field_names)  # Dynamically include field names
                })


        context['menu_permissions'] = menu_permissions
        return context




class MenuDetailView(TemplateView):
    template_name = 'immarot/details.html'
    def get(self, request, *args, **kwargs):
        # Extract query parameters
        record_id = self.request.GET.get('id')
        task = self.request.GET.get('task')
        model_name = self.kwargs.get('model_name')
        app_name = self.kwargs.get('app_name')

        # If task is 'delete' and record_id is provided, process the deletion
        if task == "delete" and record_id:
            # Get the model class dynamically
            model_class = apps.get_model(app_name, model_name)
            # Fetch the object and delete it
            instance = get_object_or_404(model_class, pk=record_id)
            instance.delete()
            messages.success(self.request, f'{model_name} with ID {record_id} has been successfully deleted.')
            
            # After deletion, redirect to the same page or another page as needed
            return HttpResponseRedirect(request.path)

        # Call the parent class get() to render the page
        return super().get(request, *args, **kwargs)








    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_slug = kwargs.get('menu_slug')
        action = kwargs.get('action')
        

        # Dynamically retrieve the menu based on slug
        menu = None
        for group in CustomGroup.objects.all():
            if slugify(group.name) == menu_slug:
                menu = group
                break

        if not menu:
            raise Http404("Menu not found")

        # Retrieve the user's role and permissions
        role = getattr(self.request.user, 'roles', None)
        if not role:
            raise Http404("Role not found")

        permission_dict = {'add': False, 'change': False, 'delete': False, 'view': False}
        for perm in menu.permissions.all():
            if 'add' in perm.codename:
                permission_dict['add'] = True
            elif 'change' in perm.codename:
                permission_dict['change'] = True
            elif 'delete' in perm.codename:
                permission_dict['delete'] = True
            elif 'view' in perm.codename:
                permission_dict['view'] = True

        # Check if the user has permission for the action
        if action == 'view' and not permission_dict['view']:
            raise Http404("Permission Denied")
        if action == 'add' and not permission_dict['add']:
            raise Http404("Permission Denied")
        if action == 'change' and not permission_dict['change']:
            raise Http404("Permission Denied")
        if action == 'delete' and not permission_dict['delete']:
            raise Http404("Permission Denied")
        if action == 'view' and permission_dict.get('view'):
            model_name = self.kwargs.get('model_name')
            app_name = self.kwargs.get('app_name')

            try:
                # Dynamically fetch the model
                model_class = apps.get_model(app_name, model_name)
                data = model_class.objects.all().order_by('-id')  # Fetch all objects from the model
                field_names = []
                if model_class and hasattr(model_class, 'showable_fields'):
                            showable_fields = model_class.showable_fields
                            field_names =showable_fields
                            print("showable_fields",showable_fields)
                # field_names = [field.name for field in model_class._meta.fields]  # Extract field names
                print("showable_fields",field_names)

                # Prepare data as a list of dictionaries
                table_data = [
                    {field: getattr(obj, field, "Field Not Found") for field in field_names}
                    for obj in data
                ]

                context['table_data'] = table_data
                context['field_names'] = field_names
            except Exception as e:
                context['error'] = f"Error loading data: {e}"
                context['table_data'] = []
                context['field_names'] = []

        ######## Menu Permissions ##########
        menu_permissions = []
        if role:
            processed_models = set()  # To track unique (app_name, model_name) combinations

            for menu in role.menu.all():
                permission_dict = {'add': False, 'change': False, 'delete': False, 'view': False}

                # Loop through all permissions for the current menu
                for perm in menu.permissions.all():
                    # Retrieve the app_label and model name from the content_type
                    content_type = perm.content_type
                    app_name = content_type.app_label
                    model_name = content_type.model

                    # Ensure that only unique (app_name, model_name) combinations are processed
                    if (app_name, model_name) not in processed_models:
                        print("App Name:", app_name)
                        print("Model Name:", model_name)

                        # Get the model class and dynamically retrieve its fields
                        model_class = content_type.model_class()
                        if model_class:
                            field_names = [field.name for field in model_class._meta.fields]
                        else:
                            field_names = []  # Fallback if the model class is not found

                        processed_models.add((app_name, model_name))  # Mark as processed

                    # Update permissions based on codename
                    if 'add' in perm.codename:
                        permission_dict['add'] = True
                    elif 'change' in perm.codename:
                        permission_dict['change'] = True
                    elif 'delete' in perm.codename:
                        permission_dict['delete'] = True
                    elif 'view' in perm.codename:
                        permission_dict['view'] = True

                # Append the menu information for each unique permission set
                menu_permissions.append({
                    'name': menu.title,
                    'slug': slugify(menu.name),  # Assuming you have a 'slug' field
                    'permissions': permission_dict.copy(),  # Use a copy to prevent overwrites
                    'app_name': app_name,
                    'model_name': model_name.capitalize(),
                    'fields': ','.join(field_names)  # Dynamically include field names
                })

        context['menu_permissions'] = menu_permissions
        context['slug'] = self.kwargs.get('menu_slug')

        # Dynamically fetch the form using your custom tag and bind it to the context
        form = self.get_form(kwargs.get('app_name'), kwargs.get('model_name'), kwargs.get('fields'))
        context['form'] = form
        
        return context

    def get_form(self, app_name, model_name, fields):
        # Use your custom template tag's form generation logic
        return get_model_form(app_name, model_name, fields)

    def post(self, request, *args, **kwargs):
        menu_slug = kwargs.get('menu_slug')
        action = kwargs.get('action')

        # Check if the action is 'add', otherwise reject the form submission
        if action != 'add':
            messages.error(request, "Invalid action")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        # Initialize the form with POST data
        form = self.get_form(kwargs.get('app_name'), kwargs.get('model_name'), kwargs.get('fields'))
        form = form.__class__(request.POST)  # Bind form to POST data

        if form.is_valid():
            # Save the data or perform the required action
            form.save()  # This will save the Author instance to the database

            # Redirect after successful submission
            messages.success(request, f"Form has been successfully created.")
            return HttpResponseRedirect(request.path)

        # If form is not valid, return the same template with errors
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return TemplateResponse(request, self.template_name, context)


    # def post(self, request, *args, **kwargs):
    #     action = kwargs.get('action')
    #     app_name = kwargs.get('app_name')
    #     model_name = kwargs.get('model_name')
    #     fields = kwargs.get('fields')

    #     # Fetch model class dynamically
    #     try:
    #         model_class = apps.get_model(app_name, model_name)
    #     except LookupError:
    #         messages.error(request, "Model not found")
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    #     if action == 'add':
    #         form = self.get_form(app_name, model_name, fields)
    #         form = form.__class__(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             messages.success(request, "Item successfully added.")
    #         else:
    #             messages.error(request, "Error adding item.")
        
    #     elif action == 'edit':
    #         pk = request.POST.get('id')
    #         obj = get_object_or_404(model_class, pk=pk)
    #         form = self.get_form(app_name, model_name, fields)
    #         form = form.__class__(request.POST, instance=obj)
    #         if form.is_valid():
    #             form.save()
    #             messages.success(request, "Item successfully updated.")
    #         else:
    #             messages.error(request, "Error updating item.")
        
    #     elif action == 'delete':
    #         pk = request.POST.get('id')
    #         obj = get_object_or_404(model_class, pk=pk)
    #         obj.delete()
    #         messages.success(request, "Item successfully deleted.")
        
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    
class Login(TemplateView):
    template_name = "immarot/login.html"
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')  # Redirect to home if already logged in
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        print(password)
        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            return redirect('login')
        

#form handler
def handle_form_submission(request, app_name, model_name):
    try:
        model = apps.get_model(app_name, model_name)
    except LookupError:
        return HttpResponseRedirect("/error/")
    
    class DynamicForm(forms.ModelForm):
        class Meta:
            model = apps.get_model(app_name, model_name)
            fields = '__all__'
    
    if request.method == "POST":
        form = DynamicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/success/")
    return HttpResponseRedirect("/failure/")
##test codes
class Index2(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = "immarot/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        role = getattr(self.request.user, 'roles', None)
        menu_permissions = []

        if role:
            processed_models = set()  # To track unique (app_name, model_name) combinations

            for menu in role.menu.all():
                permission_dict = {'add': False, 'change': False, 'delete': False, 'view': False}

                # Loop through all permissions for the current menu
                for perm in menu.permissions.all():
                    # Retrieve the app_label and model name from the content_type
                    content_type = perm.content_type
                    app_name = content_type.app_label
                    model_name = content_type.model

                    # Ensure that only unique (app_name, model_name) combinations are processed
                    if (app_name, model_name) not in processed_models:
                        print("App Name:", app_name)
                        print("Model Name:", model_name)

                        # Get the model class and dynamically retrieve its fields
                        model_class = content_type.model_class()

                        if model_class:
                            showable_fields = getattr(model_class, 'showable_fields', [])
                            field_names = showable_fields if showable_fields else ['default']  # Ensure field_names is not empty
                        else:
                            showable_fields = []  # Fallback if the model class is not found
                            field_names = showable_fields if showable_fields else ['default']  # Default field names

                        processed_models.add((app_name, model_name))  # Mark as processed

                    # Update permissions based on codename
                    if 'add' in perm.codename:
                        permission_dict['add'] = True
                    elif 'change' in perm.codename:
                        permission_dict['change'] = True
                    elif 'delete' in perm.codename:
                        permission_dict['delete'] = True
                    elif 'view' in perm.codename:
                        permission_dict['view'] = True

                # Append the menu information for each unique permission set
                menu_permissions.append({
                    'name': menu.title,
                    'slug': slugify(menu.name),  # Assuming you have a 'slug' field
                    'permissions': permission_dict.copy(),  # Use a copy to prevent overwrites
                    'app_name': app_name,
                    'model_name': model_name.capitalize(),
                    'fields': ','.join(field_names)  # Dynamically include field_names
                })

        context['menu_permissions'] = menu_permissions
        return context


class MenuDetailView2(TemplateView):
    template_name = 'immarot/details2.html'

    def get(self, request, *args, **kwargs):
        # Extract query parameters
        record_id = self.request.GET.get('id')
        task = self.request.GET.get('task')
        model_name = self.kwargs.get('model_name')
        app_name = self.kwargs.get('app_name')
        action = kwargs.get('action')

        # If task is 'delete' and record_id is provided, process the deletion
        if task == "delete" and record_id:
            model_class = apps.get_model(app_name, model_name)
            instance = get_object_or_404(model_class, pk=record_id)
            instance.delete()
            messages.success(self.request, f'{model_name} with ID {record_id} has been successfully deleted.')
            return HttpResponseRedirect(request.path)

        # Handle the edit action if specified
        if action == 'edit' and record_id:
            model_class = apps.get_model(app_name, model_name)
            instance = get_object_or_404(model_class, pk=record_id)
            form = self.get_form(app_name, model_name, kwargs.get('fields'), instance=instance)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['instance'] = instance
            return TemplateResponse(request, self.template_name, context)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_slug = kwargs.get('menu_slug')
        action = kwargs.get('action')

        # Dynamically retrieve the menu based on slug
        menu = None
        for group in CustomGroup.objects.all():
            if slugify(group.name) == menu_slug:
                menu = group
                break

        if not menu:
            raise Http404("Menu not found")

        role = getattr(self.request.user, 'roles', None)
        if not role:
            raise Http404("Role not found")

        permission_dict = {'add': False, 'change': False, 'delete': False, 'view': False}
        for perm in menu.permissions.all():
            if 'add' in perm.codename:
                permission_dict['add'] = True
            elif 'change' in perm.codename:
                permission_dict['change'] = True
            elif 'delete' in perm.codename:
                permission_dict['delete'] = True
            elif 'view' in perm.codename:
                permission_dict['view'] = True

        # Check if the user has permission for the action
        if action == 'view' and not permission_dict['view']:
            raise Http404("Permission Denied")
        if action == 'add' and not permission_dict['add']:
            raise Http404("Permission Denied")
        if action == 'change' and not permission_dict['change']:
            raise Http404("Permission Denied")
        if action == 'delete' and not permission_dict['delete']:
            raise Http404("Permission Denied")

        # If 'view' action is allowed, fetch the model data
        if action == 'view' and permission_dict.get('view'):
            model_name = self.kwargs.get('model_name')
            app_name = self.kwargs.get('app_name')
            model_class = apps.get_model(app_name, model_name)
            data = model_class.objects.all().order_by('-id')
            field_names = []
            if hasattr(model_class, 'showable_fields'):
                field_names = model_class.showable_fields

            table_data = [
                {field: getattr(obj, field, "Field Not Found") for field in field_names}
                for obj in data
            ]

            context['table_data'] = table_data
            context['field_names'] = field_names
        # If 'view' action is allowed, fetch the model data
        # if action == 'view' and permission_dict.get('view'):
        #     model_name = self.kwargs.get('model_name')
        #     app_name = self.kwargs.get('app_name')
        #     model_class = apps.get_model(app_name, model_name)
        #     data = model_class.objects.all().order_by('-id')
        #     field_names = []
        #     if hasattr(model_class, 'showable_fields'):
        #         field_names = model_class.showable_fields

        #     # Pagination setup
        #     paginator = Paginator(data, 10)  # Show 10 items per page
        #     page_number = self.request.GET.get('page')
        #     page_obj = paginator.get_page(page_number)

        #     table_data = [
        #         {field: getattr(obj, field, "Field Not Found") for field in field_names}
        #         for obj in page_obj.object_list
        #     ]

            # context['table_data'] = table_data
            # context['field_names'] = field_names
            # context['page_obj'] = page_obj  # Pass the page object for pagination controls

        menu_permissions = []
        if role:
            processed_models = set()
            for menu in role.menu.all():
                permission_dict = {'add': False, 'change': False, 'delete': False, 'view': False}
                for perm in menu.permissions.all():
                    content_type = perm.content_type
                    app_name = content_type.app_label
                    model_name = content_type.model
                    if (app_name, model_name) not in processed_models:
                        model_class = content_type.model_class()
                        field_names = getattr(model_class, 'showable_fields', [])
                        processed_models.add((app_name, model_name))
                    if 'add' in perm.codename:
                        permission_dict['add'] = True
                    elif 'change' in perm.codename:
                        permission_dict['change'] = True
                    elif 'delete' in perm.codename:
                        permission_dict['delete'] = True
                    elif 'view' in perm.codename:
                        permission_dict['view'] = True

                menu_permissions.append({
                    'name': menu.title,
                    'slug': slugify(menu.name),
                    'permissions': permission_dict.copy(),
                    'app_name': app_name,
                    'model_name': model_name.capitalize(),
                    'fields': ','.join(field_names)
                })

        context['menu_permissions'] = menu_permissions
        context['slug'] = self.kwargs.get('menu_slug')
        form = self.get_form(kwargs.get('app_name'), kwargs.get('model_name'), kwargs.get('fields'))
        context['form'] = form

        return context

    def get_form(self, app_name, model_name, fields, instance=None):
        return get_model_form(app_name, model_name, fields, instance=instance)

    def post(self, request, *args, **kwargs):
        menu_slug = kwargs.get('menu_slug')
        action = kwargs.get('action')
        record_id = request.GET.get('id')

        if action not in ['add', 'edit']:
            messages.error(request, "Invalid action")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        model_name = kwargs.get('model_name')
        app_name = kwargs.get('app_name')

        model_class = apps.get_model(app_name, model_name)

        if action == 'edit' and record_id:
            instance = get_object_or_404(model_class, pk=record_id)
        else:
            instance = None

        form = self.get_form(app_name, model_name, kwargs.get('fields'), instance=instance)
        form = form.__class__(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, f"Form has been successfully {'updated' if action == 'edit' else 'created'}.")
            current_path = request.path

            # Replace 'edit' or 'add' with 'view'
            updated_path = current_path.replace('edit', 'view').replace('add', 'view')

            # Redirect to the updated path
            return HttpResponseRedirect(updated_path)

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return TemplateResponse(request, self.template_name, context)
    

class MenuDetailView3(TemplateView):
    template_name = 'immarot/details2.html'
    def get(self, request, *args, **kwargs):
        # Extract query parameters
        record_id = self.request.GET.get('id')
        task = self.request.GET.get('task')
        model_name = self.kwargs.get('model_name')
        app_name = self.kwargs.get('app_name')
        action = kwargs.get('action')

        # If task is 'delete' and record_id is provided, process the deletion
        if task == "delete" and record_id:
            model_class = apps.get_model(app_name, model_name)
            instance = get_object_or_404(model_class, pk=record_id)
            instance.delete()
            messages.success(self.request, f'{model_name} with ID {record_id} has been successfully deleted.')
            return HttpResponseRedirect(request.path)

        # Handle the edit action if specified
        if action == 'edit' and record_id:
            model_class = apps.get_model(app_name, model_name)
            instance = get_object_or_404(model_class, pk=record_id)
            form = self.get_form(app_name, model_name, kwargs.get('fields'), instance=instance)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['instance'] = instance
            return TemplateResponse(request, self.template_name, context)

        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_slug = kwargs.get('menu_slug')
        action = kwargs.get('action')

        # Dynamically retrieve the menu based on slug
        menu = None
        for group in CustomGroup.objects.all():
            if slugify(group.name) == menu_slug:
                menu = group
                break

        if not menu:
            raise Http404("Menu not found")

        role = getattr(self.request.user, 'roles', None)
        if not role:
            raise Http404("Role not found")

        permission_dict = {'add': False, 'change': False, 'delete': False, 'view': False}
        for perm in menu.permissions.all():
            if 'add' in perm.codename:
                permission_dict['add'] = True
            elif 'change' in perm.codename:
                permission_dict['change'] = True
            elif 'delete' in perm.codename:
                permission_dict['delete'] = True
            elif 'view' in perm.codename:
                permission_dict['view'] = True

        if action == 'view' and not permission_dict['view']:
            raise Http404("Permission Denied")
        if action == 'add' and not permission_dict['add']:
            raise Http404("Permission Denied")
        if action == 'change' and not permission_dict['change']:
            raise Http404("Permission Denied")
        if action == 'delete' and not permission_dict['delete']:
            raise Http404("Permission Denied")

        # Fetch the model data dynamically based on permissions
        if action == 'view' and permission_dict.get('view'):
            model_name = self.kwargs.get('model_name')
            app_name = self.kwargs.get('app_name')
            model_class = apps.get_model(app_name, model_name)
            field_names = getattr(model_class, 'showable_fields', [])

            search_query = self.request.GET.get('search', '').strip()
            data = model_class.objects.all().order_by('-id')

            # Dynamic search implementation
            if search_query:
                query = Q()
                for field in field_names:
                    field_type = model_class._meta.get_field(field)
                    if field_type.is_relation:  # Handle ForeignKey and ManyToManyField
                        if hasattr(field_type.related_model, 'name'):
                            query |= Q(**{f"{field}__name__icontains": search_query})
                        # Add checks for other related model fields as needed
                    else:
                        query |= Q(**{f"{field}__icontains": search_query})

                data = data.filter(query)

            table_data = [
                {field: getattr(obj, field, "Field Not Found") for field in field_names}
                for obj in data
            ]

            context['table_data'] = table_data
            context['field_names'] = field_names
            print(field_names)

        # Fetch permissions for menus
        menu_permissions = []
        if role:
            processed_models = set()
            for menu in role.menu.all():
                permission_dict = {'add': False, 'change': False, 'delete': False, 'view': False}
                for perm in menu.permissions.all():
                    content_type = perm.content_type
                    app_name = content_type.app_label
                    model_name = content_type.model
                    if (app_name, model_name) not in processed_models:
                        model_class = content_type.model_class()
                        field_names = getattr(model_class, 'showable_fields', [])
                        processed_models.add((app_name, model_name))
                    if 'add' in perm.codename:
                        permission_dict['add'] = True
                    elif 'change' in perm.codename:
                        permission_dict['change'] = True
                    elif 'delete' in perm.codename:
                        permission_dict['delete'] = True
                    elif 'view' in perm.codename:
                        permission_dict['view'] = True

                menu_permissions.append({
                    'name': menu.title,
                    'slug': slugify(menu.name),
                    'permissions': permission_dict.copy(),
                    'app_name': app_name,
                    'model_name': model_name.capitalize(),
                    'fields': ','.join(field_names)
                })

        context['menu_permissions'] = menu_permissions
        context['slug'] = self.kwargs.get('menu_slug')
        form = self.get_form(kwargs.get('app_name'), kwargs.get('model_name'), kwargs.get('fields'))
        context['form'] = form

        return context

    def get_form(self, app_name, model_name, fields, instance=None):
        return get_model_form(app_name, model_name, fields, instance=instance)
    def post(self, request, *args, **kwargs):
        menu_slug = kwargs.get('menu_slug')
        action = kwargs.get('action')
        record_id = request.GET.get('id')

        if action not in ['add', 'edit']:
            messages.error(request, "Invalid action")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        model_name = kwargs.get('model_name')
        app_name = kwargs.get('app_name')

        model_class = apps.get_model(app_name, model_name)

        if action == 'edit' and record_id:
            instance = get_object_or_404(model_class, pk=record_id)
        else:
            instance = None

        form = self.get_form(app_name, model_name, kwargs.get('fields'), instance=instance)
        form = form.__class__(request.POST, instance=instance)
        print("form validity: ",form.is_valid())
        if form.is_valid():
            form.save()
            messages.success(request, f"Form has been successfully {'updated' if action == 'edit' else 'created'}.")
            current_path = request.path
            path_parts = current_path.split('/')  # Split path into components

            # Replace specific parts
            path_parts = [
                part.replace('edit', 'view') if part == 'edit' else part.replace('add', 'view') if part == 'add' else part
                for part in path_parts
            ]

            updated_path = '/'.join(path_parts)  # Join components back into a path
            print("Updated Path:", updated_path)
            print("Request Path:", request.path)

            # Redirect to the updated path
            return HttpResponseRedirect(updated_path)

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return TemplateResponse(request, self.template_name, context)