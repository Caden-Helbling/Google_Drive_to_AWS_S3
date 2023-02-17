import subprocess

def download_folder(remote_folder, local_folder):
    cmd = f'rclone copy --checksum --verbose {remote_folder} {local_folder}'
    subprocess.call(cmd, shell=True)

# Example usage: download all files from a remote folder called 'my-remote-folder' to a local folder called 'my-local-folder'
download_folder('GDrive:my-remote-folder', 'S3:rclone-remote-bucket')
