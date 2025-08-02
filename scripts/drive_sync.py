import os
import io
import json
import argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from tqdm import tqdm

def get_drive_service():
    """Authenticate to Google Drive using service account from environment variable."""
    json_key_str = os.environ.get("GDRIVE_SERVICE_ACCOUNT_JSON")
    if not json_key_str:
        raise ValueError("GDRIVE_SERVICE_ACCOUNT_JSON not found in environment variables.")
    
    service_account_info = json.loads(json_key_str)
    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)

def list_files_in_folder(service, folder_id):
    """List all files in a specific Google Drive folder."""
    files = []
    page_token = None
    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id, name)",
            pageToken=page_token
        ).execute()
        files.extend(response.get("files", []))
        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break
    return files

def download_file(service, file_id, filename, local_root):
    """Download a file from Google Drive."""
    os.makedirs(local_root, exist_ok=True)
    local_path = os.path.join(local_root, filename)

    if os.path.exists(local_path):
        tqdm.write(f"Skipping (exists): {filename}")
        return

    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(local_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            tqdm.write(f"Downloading {filename} — {int(status.progress() * 100)}%")

def main():
    parser = argparse.ArgumentParser(description="Sync Google Drive folder to local storage.")
    parser.add_argument("--folder-id", required=True, help="Google Drive folder ID")
    parser.add_argument("--local-root", default="archive/originals", help="Local folder to save files")
    args = parser.parse_args()

    service = get_drive_service()
    files = list_files_in_folder(service, args.folder_id)

    for f in tqdm(files, desc="Processing files"):
        download_file(service, f["id"], f["name"], args.local_root)

if __name__ == "__main__":
    main()
