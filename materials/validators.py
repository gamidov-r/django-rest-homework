from rest_framework.serializers import ValidationError
import re

youtube_hosts = ["youtube.com", "youtu.be", "m.youtube.com", "m.youtube.ru", "youtube.ru", "youtubekids.com", "youtubeeducation.com", "youtubegaming.com"]

def get_host_from_url(url):
    pattern = r'^(?:https?://)?([^/:?#\s]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def find_urls_in_description(text):
    pattern = r'''
        (?:https?://)?
        (?:www\.)?
        [a-zA-Z0-9][a-zA-Z0-9-]*
        \.(?:com|ru|cn|org|net)
        (?:/[^\s]*)?
    '''
    urls = re.findall(pattern, text, re.VERBOSE | re.IGNORECASE)
    return urls



def validate_url(value):
    if not value:
        return value

    elif not get_host_from_url(value) in youtube_hosts:
        raise ValidationError(f"{value} isn\'t youtube host")



def validate_description(value):
    if not value:
        return value
    urls = find_urls_in_description(value)
    if not urls:
        return value
    for url in urls:
        if not get_host_from_url(url) in youtube_hosts:
            raise ValidationError(f"{value} isn't youtube host")
    return value

# course = name, description
# lesson = name, description, video_url

