import os
import zipfile
import time

SOURCE_DIR = r"c:\Users\aabir\OneDrive\Desktop\website"
DESKTOP_DIR = r"c:\Users\aabir\OneDrive\Desktop"
ZIP_NAME = "imtechboss-active-dev-backup-2026-10-03.zip"
TARGET_ZIP = os.path.join(DESKTOP_DIR, ZIP_NAME)

start_time = time.time()

# Exclude old Blogger archive and zip files
exclude_extensions = {'.zip', '.tmp'}
exclude_dirs = {'Blogger'}

total_files = 0
total_uncompressed_bytes = 0

with zipfile.ZipFile(TARGET_ZIP, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
    for root, dirs, files in os.walk(SOURCE_DIR):
        # Exclude Blogger folder
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in exclude_extensions):
                continue
                
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, SOURCE_DIR)
            
            try:
                zipf.write(file_path, arcname)
                total_files += 1
                total_uncompressed_bytes += os.path.getsize(file_path)
            except Exception as e:
                print(f"Warning: Could not add {file_path}: {e}")

elapsed = time.time() - start_time
compressed_size = os.path.getsize(TARGET_ZIP) / (1024 * 1024)
uncompressed_size = total_uncompressed_bytes / (1024 * 1024)

print("\n" + "="*60)
print("ACTIVE DEV BACKUP COMPLETED!")
print("="*60)
print(f"Total files archived:    {total_files:,}")
print(f"Uncompressed size:       {uncompressed_size:.2f} MB")
print(f"Compressed ZIP size:     {compressed_size:.2f} MB")
print(f"Time taken:              {elapsed:.2f} seconds")
print(f"Saved at:                {TARGET_ZIP}")
print("="*60)
