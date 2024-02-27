import requests

def download_file(url, local_filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"File '{local_filename}' downloaded successfully.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def upload_file(url, local_filename):
    with open(local_filename, 'rb') as file:
        files = {'file': (local_filename, file)}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print(f"File '{local_filename}' uploaded successfully.")
        else:
            print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    
    SERVER_URL = "http://localhost:8080"  # Adjust to the server's URL
    DOWNLOAD_PATH = "downloaded_file.txt"
    UPLOAD_PATH = "local_file.txt"

    # Example for downloading a file
    download_file(f"{SERVER_URL}/sds.txt", DOWNLOAD_PATH)

    # Example for uploading a file
    upload_file(f"{SERVER_URL}/uploaded_file.txt", UPLOAD_PATH)
