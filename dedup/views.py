from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Hash, StorageStats, FileRecord
import hashlib
from django.db import transaction

# Define constants
BLOCK_SIZE = 4096  # Size of each block in bytes
HASH_SIZE = 64     # Size of each hash in characters


def get_file_hash(data):
    """Generate the SHA256 hash of the given data block."""
    return hashlib.sha256(data).hexdigest()


def get_total_unique_data_size():
    total_unique_hash_blocks = Hash.objects.count()
    return 4*total_unique_hash_blocks  # KB

def handle_uploaded_file(f):
    """Handle the uploaded file, process it block by block."""
   
    filename = f.name  
    hash_string = ""  # To store the concatenated hashes

    while True:
        block = f.read(BLOCK_SIZE)
        if not block:
            break

        # Generate hash for the current block
        block_hash = get_file_hash(block)

        # Check if hash exists in the database
        hash_record = Hash.objects.filter(hash_value=block_hash).first()
        if not hash_record:
            # Save the block if the hash is not in the database
            Hash.objects.create(hash_value=block_hash, content=block)
        else: 
            hash_record.frequency += 1
            hash_record.save()
            
        # Append hash to the final hash string
        hash_string += block_hash

    # Save file record
    file_instance = FileRecord.objects.create(
        filename=filename,
        hash_string=hash_string
    )

    # Update StorageStats
    stats, _ = StorageStats.objects.get_or_create(id=1)
    stats.total_uploaded_size += file_instance.get_original_size()
    stats.total_hash_size += file_instance.get_hash_size()
    stats.total_unique_data_size = get_total_unique_data_size()
    stats.save()

    return hash_string


def upload_file(request):

    """Handle file upload and display storage statistics."""
    stats, _ = StorageStats.objects.get_or_create(id=1)

    # Current storage sizes (KB)
    total_dedup_size = stats.get_total_dedup_size()
    total_uploaded_size = stats.total_uploaded_size
    space_saved = total_uploaded_size - total_dedup_size # KB
    files = FileRecord.objects.all()

    message=""
    download_link=""

    """Handle file upload and return the hash values."""
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        hashes = handle_uploaded_file(uploaded_file)

        total_dedup_size = stats.get_total_dedup_size()
        total_uploaded_size = stats.total_uploaded_size
        space_saved = total_uploaded_size - total_dedup_size # KB
        message = f"File successfully deduplicated. First few hashes: {hashes[:HASH_SIZE * 3]}..."
        download_link = f"/download/{uploaded_file.name}"
        return redirect('upload_file')

    return render(request, 'index.html', {
        'message': message,
        'download_link': download_link,
        'total_uploaded_size': total_uploaded_size,  # KB
        'total_dedup_size': total_dedup_size,  # KB
        'space_saved': space_saved,  # KB
        'files': files,
    })


def reconstruct_file_from_hashes(hash_string):
    """Reconstruct the file from the hash_string stored in the database."""
    reconstructed_content = bytearray()

    for i in range(0, len(hash_string), HASH_SIZE):
        hash_value = hash_string[i:i + HASH_SIZE]
        hash_record = Hash.objects.filter(hash_value=hash_value).first()

        if hash_record:
            reconstructed_content.extend(hash_record.content)
        else:
            raise ValueError(f"Hash {hash_value} not found in the database.")

    return reconstructed_content


def download_file(request, file_id):
    """Handle file download by reconstructing it from its hashes."""
    file_record = FileRecord.objects.get(id=file_id)
    hash_string = file_record.hash_string

    reconstructed_content = reconstruct_file_from_hashes(hash_string)
    reconstructed_content_bytes = bytes(reconstructed_content)
    # Return the reconstructed file
    response = HttpResponse(reconstructed_content_bytes, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={file_record.filename}'

    return response


def delete_file(request, file_id):
    """Handle file deletion."""
    file_record = FileRecord.objects.get(id=file_id)
    hash_string = file_record.hash_string

    # Process the hash_string in chunks of hash_size
    for i in range(0, len(hash_string), HASH_SIZE):
        hash_chunk = hash_string[i:i + HASH_SIZE]

        # Check if the hash_chunk exists in the Hash model
        try:
            hash_record = Hash.objects.get(hash_value=hash_chunk)
            # Reduce the frequency by one
            with transaction.atomic():
                if(hash_record.frequency > 1):
                    hash_record.frequency -= 1  # Directly reduce frequency
                    hash_record.save()
                else:
                    hash_record.delete()
        except Hash.DoesNotExist:
            # If the hash does not exist, you can choose to log this or handle it as needed
            pass

    # Update storage stats
    stats, _ = StorageStats.objects.get_or_create(id=1)
    stats.total_uploaded_size -= file_record.get_original_size()  # Approx size
    stats.total_hash_size -= file_record.get_hash_size()
    stats.total_unique_data_size = get_total_unique_data_size()

    stats.total_hash_size = max(0, stats.total_hash_size) # Ensuring doesnt go below zero
    stats.save()

    # Delete from database
    file_record.delete()

    return redirect('upload_file')