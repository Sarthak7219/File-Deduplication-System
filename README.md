# File Deduplication System Using Python

## Description

This system optimizes storage by eliminating data redundancy across various file types, including text documents, PDFs, images, and audio files. It breaks files into 4KB data blocks, hashes each block, and stores only unique blocks in a database, thus reducing storage consumption. The system is capable of handling different file types and can be used to develop a deduplication file system in operating systems using FUSE.

## Features

- **Block-level Deduplication**: Files are divided into 4KB blocks, and only unique blocks are stored, ensuring efficient storage usage.
- **Support for Multiple File Types**: Handles various file formats, including text, PDFs, images, and audio files.
- **SHA-256 Hashing**: Ensures data integrity and uniqueness by generating SHA-256 hashes for each block.
- **Storage Metrics**: Tracks total space used before and after deduplication, showing space savings.
- **User Interface**: Web-based interface built with Django for easy file upload and management.
- **Database**: Uses MySQL to store hashes and metadata, ensuring data integrity and quick lookups.

## Setup

### Requirements

- Python
- Django
- MySQL

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Sarthak7219/File-Deduplication-System.git
   cd File-Deduplication-System
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up MySQL database and configure in `.env`:
   ```bash
   DB_NAME="your_database_name"
   DB_PASSWORD="password"
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the server:
   ```bash
   python manage.py runserver
   ```

6. Access the web interface via `http://127.0.0.1:8000/`.

## Usage

- Upload files via the web interface.
- The system will automatically calculate and display:
  - Total space used by uploaded files.
  - Total space used after deduplication.
  - Space saved through deduplication.

## Future Enhancements

- Implement deduplication at the filesystem level using FUSE.
- Optimize hashing algorithms for different file types.
- Add additional file formats for deduplication.
