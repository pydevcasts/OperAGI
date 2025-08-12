from django.db import models
from documents.models import Document




class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    content = models.TextField()
    embedding = models.JSONField()  
    index = models.PositiveIntegerField()

    def __str__(self):
        return f"Chunk {self.index} of {self.document.title}"