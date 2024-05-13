
# YouTube Video Uploader

This Python script automates the uploading of videos from a local directory to a YouTube channel. It sets the video title based on the date the video was recorded and uploads the video as private. This feature is particularly useful for users who regularly upload videos and want to streamline the process, while keeping the uploaded content hidden from the public view until ready for release.

## Description

The `youtube_video_uploader.py` script is designed to help users automatically upload videos stored in a specified local directory to their YouTube channel. The script authenticates with Google's YouTube Data API v3, retrieves video files from the local storage, and uploads them with titles based on their creation date.

### Privacy Setting: Private Videos
When videos are uploaded as "Private", they are not visible to the public or other users of YouTube. Only the account that uploaded the video and those to whom the uploader grants explicit access can view the video. This setting is ideal for users who are preparing content that is not yet ready to be published publicly or who wish to keep their videos confidential until a certain event or time.

## Disclaimer

This script is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.

## Setup Instructions

### Step 1: Google API Configuration
1. **Create a project** in the [Google Developers Console](https://console.developers.google.com/).
2. **Enable the YouTube Data API v3** for your project.
3. **Create credentials**:
   - Go to "Credentials" and choose "Create Credentials" > "OAuth client ID".
   - Application type should be "Desktop app".
   - Name your client ID and click "Create".
4. **Download the client secret JSON file** and save it to your local machine.

### Step 2: OAuth Consent Screen
1. Configure the OAuth consent screen in the Google Developers Console.
2. Set the Application Name, User Support Email, and add the necessary Scopes (`https://www.googleapis.com/auth/youtube.upload`).
3. Include a link to a Privacy Policy and specify any authorized domains if applicable.

### Step 3: Python Environment Setup
1. Ensure Python is installed on your machine.
2. Install required libraries using pip:
   ```
   pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```
3. Place the downloaded client secret JSON file in the same directory as the script or specify its path in the script.

### Step 4: Running the Script
1. Modify the `CLIENT_SECRETS_FILE` and `VIDEO_DIR` in the script to point to your client secrets file and your video directory.
2. Run the script from your terminal:
   ```
   python youtube_video_uploader.py
   ```
3. Authenticate via the browser when prompted and allow the necessary permissions.

## Author

**aviado1**
- GitHub: [aviado1](https://github.com/aviado1)

Thank you for using or contributing to this project. For any questions or issues, please open an issue on GitHub.
