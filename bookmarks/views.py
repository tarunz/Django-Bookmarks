from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template import Context
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout 
from django.template import RequestContext
from bookmarks.forms import *
from bookmarks.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# main_page view without shortcut
# def main_page(request):
# 	template=get_template('main_page.html')
# 	variables=Context({
# 		'head_title':'Django Bookmarks !!',
# 		'page_title':'Welcome to Django Bookmarks',
# 		# 'page_body':"Where you can store share bookmarks!"
# 		'user':request.user
# 		})
# 	output=template.render(variables)
# 	return HttpResponse(output)

# main_page view with shortcuts
def main_page(request):
	return render_to_response(
		'main_page.html',
		RequestContext(request,
			{
		'head_title':'Django Bookmarks !!',
 		'page_title':'Welcome to Django Bookmarks',
 		# 'user':request.user
 		}
 			)
		)

def user_page(request,username):
	# try:
	# 	user=User.objects.get(username=username)
	# except:
	# 	raise Http404("Requested User not found.")
	# bookmarks=user.bookmark_set.all()
	# # template=get_template('user_page.html')
	user=get_object_or_404(User,username=username)
	bookmarks=user.bookmark_set.order_by('-id')
	variables=RequestContext(request,
		{
		'username':username,
		'bookmarks':bookmarks,
		'show_tags':True
		})
	# output=template.render(variables)
	# return HttpResponse(output)
	return render_to_response('user_page.html',variables)
def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_page(request):
	if request.method=='POST':
		form =RegistrationForm(request.POST)
		if form.is_valid():
			# User.objects.create_user will do the password hashing
			# an instance of User class won't do password hashing
			user=User.objects.create_user(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1'],
				email=form.cleaned_data['email']
				)
			return HttpResponseRedirect('/register/success/')
	else:
		form=RegistrationForm()
		variables=RequestContext(request,{
			'form':form
			})
		return render_to_response(
				'registration/register.html',
				variables
				)

# @login_required
def bookmark_save_page(request):
	if request.method=="POST":
		form = BookmarkSaveForm(request.POST)
		if form.is_valid():
			# Get or Create a link
			link,dummy=Link.objects.get_or_create(
				url=form.cleaned_data['url']
				)
			#Get or Create a Bookmark
			bookmark,created = Bookmark.objects.get_or_create(
				user=request.user,
				link=link
				)
			#Update the bookmark title
			bookmark.title=form.cleaned_data['title']
			#If the bookmark is being updated ,clear the old tag list
			if not created:
				bookmark.tag_set.clear()
			#Create a new tag list
			tag_names=form.cleaned_data['tags'].split()
			for tag_name in tag_names:
				tag,dummy=Tag.objects.get_or_create(name=tag_name)
				bookmark.tag_set.add(tag)
			#Save bookmark to the database
			bookmark.save()
			return HttpResponseRedirect(
				'/user/%s/'%request.user.username
				)
	else:
		form=BookmarkSaveForm()
		variables = RequestContext(request,
			{
			'form':form 
			})
	return render_to_response('bookmark_save.html',variables)

def tag_page(request, tag_name):
     tag = get_object_or_404(Tag, name=tag_name)
     bookmarks = tag.bookmarks.order_by('-id')
     variables = RequestContext(request, {
       'bookmarks': bookmarks,
       'tag_name': tag_name,
       'show_tags': True,
       'show_user': True
     })
     return render_to_response('tag_page.html', variables)
def tag_cloud_page(request):
	MAX_WEIGHT=5
	tags=Tag.objects.order_by('name')
	#Calculate tag,min and max counts
	min_count = max_count = tags[0].bookmarks.count()
	for tag in tags:
		tag.count =tag.bookmarks.count()
		if tag.count<min_count:
			min_count=tag.count
		if max_count < tag.count:
			max_count =tag.count 
	#Calculate the count range. Avoid dividing by zero
	ranges=float(max_count-min_count)
	if ranges==0.0:
		ranges=1.0
	#Calculate tag weights
	for tag in tags:
		tag.weight=int(
			MAX_WEIGHT*(tag.count-min_count)/ranges
			)
	variables = RequestContext(request,
		{
		'tags':tags
		})
	return render_to_response('tag_cloud_page.html',variables)







# Create your views here.
