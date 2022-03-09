from django.db import models


class Reviews(models.Model):
    '''
    title_id = models.ForeignKey(
        # Titles, on_delete=models.CASCADE, related_name='review'
    )
    author = models.ForeignKey(
        # Users, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Review publication date', auto_now_add=True
    )
'''

class Comments(models.Model):
    '''
    title_id = models.ForeignKey(
        # Titles, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        # Users, on_delete=models.CASCADE, related_name='comments'
    )
    review_id = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Comment publication date', auto_now_add=True
    )
'''