from app.plugins import PluginBase, Menu, MountPoint
from django.shortcuts import render
from django.utils.translation import gettext as _

class Plugin(PluginBase):

    def main_menu(self):
        return ["<span class=\"masked\">GCP Interface</span>"]

    def app_mount_points(self):
        return [
            MountPoint('$', lambda request: render(request, self.template_path("app.html"), {'title': 'GCP Editor'}))
        ]


