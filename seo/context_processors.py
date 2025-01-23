from django.conf import settings
'''
let the following informations in settings to be accessible in all pages 
'''
def all_pages(request):
	
	return {
	'author' : settings.AUTHOR,
	'site_name':settings.SITE_NAME,
	'keywords':settings.META_KEYWORDS,
	'page_description':settings.META_DESCRIPTION,
	'tagline':settings.SITE_TAGLINE,
	#----------- start social media -------------------------#
	#----------- end social media -------------------------#
	'page_type' : settings.PAGE_TYPE,
	'page_title' : settings.PAGE_TITLE,
	'page_url' : settings.PAGE_URL,
	'page_image' : settings.PAGE_IMAGE,
	'video_url' : settings.VIDEO_URL,
	'request':request,
}