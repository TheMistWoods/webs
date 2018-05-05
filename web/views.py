from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from . models import Topic,Entry
from . forms import TopicForm,EntryForm

from . check_owner import check_topic_owner


# 创建视图
def index(request):
	"""主页"""
	return render(request,'web/index.html')

@login_required #限制访问
def topics(request):
	"""显示所有的主题"""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	content = {'topics':topics}
	return render(request,'web/topics.html',content)

@login_required
def topic(request,topic_id):
	"""显示单个主题及其所有条目"""
	# topic = Topic.objects.get(id=topic_id)
	topic = get_object_or_404(Topic,id=topic_id)

	#确认请求的主题属于当前用户	
	check_topic_owner(request,topic)

	entries = topic.entry_set.order_by('-date_added')
	content = {'topic':topic,'entries':entries}
	return render(request,'web/topic.html',content)

@login_required
def new_topic(request):
	"""添加新主题"""
	if request.method !='POST':
		#为提价数据，创建一个新表单
		form = TopicForm()
	else:
		#POST提交的数据，对数据进行处理
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('web:topics'))

	content = {'form':form}
	return render(request,'web/new_topic.html',content)

@login_required
def new_entry(request,topic_id):
	"""在特定主题中添加新条目"""
	topic = Topic.objects.get(id=topic_id)
	#确认请求的主题属于当前用户	
	check_topic_owner(request,topic)

	if request.method != 'POST':
		#未提交数据，创建一个新表单
		form = EntryForm()
	else:
		#POST提交的数据，对数据进行处理
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)#注意细节！！关键字commit 拼错为 mommit
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('web:topic',args=[topic_id]))

	content = {'topic':topic,'form':form}
	return render(request,'web/new_entry.html',content)

@login_required
def edit_entry(request,entry_id):
	"""编辑既有条目"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	#确认请求的主题属于当前用户	
	check_topic_owner(request,topic)

	if request.method != 'POST':
		#初次请求，使用当前条目填充表单
		form = EntryForm(instance=entry)
	else:
		#POST提交的数据，对数据进行处理
		form = EntryForm(instance=entry,data=request.POST)
		if form.is_valid():
			# form.save()
			edit_entry = form.save(commit=False)
			edit_entry.topic = topic
			edit_entry.save()
			return HttpResponseRedirect(reverse('web:topic',args=[topic.id]))
	
	content = {'entry':entry,'topic':topic,'form':form}
	return render(request,'web/edit_entry.html',content)