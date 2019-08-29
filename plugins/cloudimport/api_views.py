import importlib
import requests
import os
from os import path

from app import models, pending_actions
from app.plugins.views import TaskView
from app.plugins.worker import task
from app.plugins import logger

from worker.celery import app
from rest_framework.response import Response
from rest_framework import status

from .platform_helper import get_all_platforms, get_platform_by_name

platforms = None
class ImportFolderTaskView(TaskView):
    def post(self, request, project_pk=None, pk=None):
        task = self.get_and_check_task(request, pk)
        
        folder_url = request.data.get('selectedFolderUrl', None)
        platform_name = request.data.get('platform', None)
        
        if folder_url == None or platform_name == None:
            return Response({'error': 'Folder URL and platform name must be set.'}, status=status.HTTP_400_BAD_REQUEST)
            
        platform = get_platform_by_name(platform_name)
        
        if platform == None:
            return Response({'error': 'Failed to find a platform with the name \'{}\''.format(platform_name)}, status=status.HTTP_400_BAD_REQUEST)
            
        if platform.verify_folder_url(folder_url) == None:
            return Response({'error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)
            
        files = platform.import_from_folder(folder_url)
        
        task.console_output += "Importing images...\n"
        task.images_count = len(files)
        task.pending_action=pending_actions.IMPORT
        task.save()
        
        serialized = [file.serialize() for file in files]
        logger.error(serialized)
        import_files.delay(task.id, serialized)
        
        return Response({}, status=status.HTTP_200_OK)

class PlatformsVerifyTaskView(TaskView):
    def get(self, request, platform_name):
        folder_url = request.GET.get('folderUrl', None)
        platform = get_platform_by_name(platform_name)
        
        if platform == None:
            return Response({'error': 'Failed to find a platform with the name \'{}\''.format(platform_name)}, status=status.HTTP_400_BAD_REQUEST)
            
        folder = platform.verify_folder_url(folder_url)
        
        if folder == None:
            return Response({'error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'folder': folder.serialize()}, status=status.HTTP_200_OK)


class PlatformsTaskView(TaskView):
    def get(self, request):
        platforms = get_all_platforms()
        return Response({'platforms': [platform.serialize(user = request.user) for platform in platforms]}, status=status.HTTP_200_OK)


###                        ###
#       CELERY TASK(S)       #
###                        ###
@task
def import_files(task_id, files):
    logger.info("Will import {} files".format(len(files)))
    task = models.Task.objects.get(pk=task_id)
    task.create_task_directories()
    task.save()
    
    try:
        downloaded_total = 0
        for file in files: 
            download_file(task, file)
            task.check_if_canceled()
            models.Task.objects.filter(pk=task.id).update(upload_progress=(float(downloaded_total) / float(len(files))))
            downloaded_total += 1

    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        raise NodeServerError(e)

    task.refresh_from_db()
    task.pending_action = None
    task.processing_time = 0
    task.partial = False
    task.save()

def download_file(task, file):
    path = task.task_path(file['name'])
    download_stream = requests.get(file['url'], stream=True, timeout=60)

    with open(path, 'wb') as fd:
        for chunk in download_stream.iter_content(4096):
            fd.write(chunk)
    
    models.ImageUpload.objects.create(task=task, image=path)
