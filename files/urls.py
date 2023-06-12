from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('upload/', FileUploadView.as_view(), name="file-upload"),
    path('create/folder/', CreateFolder.as_view(), name="folder-create"),
    path('folders/', FolderList.as_view(), name="folder-list"),
    path('download/<int:file_id>/', FileDownloadView.as_view(), name='file-download'),

    # path('files/', FileListView.as_view(), name='file-show'),
    # path('file/<int:file_id>', FileDetailView.as_view(), name='file-show-by-id'),
    
    path('files/', FileList.as_view(), name = 'File_list'),
    path('trash/', TrashList.as_view(), name = 'Trash_list'),
    path('shared/', SharedList.as_view(), name = 'Share_list'),
    path('files/<int:file_id>' , FileDetailView.as_view(), name = 'File_detail'),
    path('memos/<int:id>' , MemoDetail.as_view(), name = 'Memo_Detail'),
    path('memos' , MemoList.as_view(), name = 'Memo_list'), 
    path('files/<int:id>/favorite/', FileFavoriteToggle.as_view(), name='file-favorite-toggle'),
    path('files/<int:id>/view/', FileViewCount.as_view(), name='file-view-count'),
    path('files/<int:id>/remove/', FileRemoveToTrash.as_view(), name='file-remove-trash'),
    path('files/<int:id>/delete/', FileDeleteCompletely.as_view(), name='file-delete-completely'),
    path('files/<int:id>/recover/', FileRecoverFromTrash.as_view(), name='file-recover-trash'),
    path('file-search/<int:sort_id>', FileSearch.as_view(), name='file-search'),
    path('file/share/', ShareFile.as_view(), name='share_file'),
]