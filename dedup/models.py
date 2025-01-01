from django.db import models

# Define constants
BLOCK_SIZE = 4096  # Size of each block in bytes
HASH_SIZE = 64     # Size of each hash in characters

class Hash(models.Model):
    hash_value = models.CharField(max_length=64, unique=True)
    content = models.BinaryField()
    frequency = models.IntegerField(default=1)

    def __str__(self):
        return self.hash_value
    
class StorageStats(models.Model): # KB
    total_uploaded_size = models.BigIntegerField(default=0)  # Total size of uploaded files
    total_hash_size = models.BigIntegerField(default=0)
    total_unique_data_size = models.BigIntegerField(default=0)

    def get_total_dedup_size(self):
        return self.total_hash_size + self.total_unique_data_size

class FileRecord(models.Model):
    filename = models.CharField(max_length=255)
    hash_string = models.TextField(null=True, blank=True)  # Store concatenated hashes
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
    
    def get_hash_size(self): # KB
        return len(self.hash_string) / 1024
    
    def get_original_size(self): # KB
        return self.get_hash_size() * (BLOCK_SIZE / HASH_SIZE)
    
