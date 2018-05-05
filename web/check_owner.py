"""我的模块"""

from django.http import Http404

#确认请求的主题属于当前用户
def check_topic_owner(request,topic):
	if topic.owner != request.user:
		raise Http404