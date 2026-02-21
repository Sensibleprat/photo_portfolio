# Part 1: Google Cloud & Service Account Setup

To allow your portfolio to automatically sync photos from Google Drive, we need a way for the script to authenticate. We achieve this using a **Google Cloud Service Account**—essentially a "bot user" that can access specific files you share with it.

> [!NOTE]
> **Architect's Insight:** Why use a Service Account instead of OAuth? 
> OAuth requires a human to click "Allow" in a web browser. A Service Account uses a key file, allowing our build scripts (`sync_from_drive.py`) to run in the background seamlessly without human intervention.

## Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Log in with your standard Google account.
3. Click the project dropdown in the top navigation bar and select **New Project**.
4. Name your project (e.g., `Photography-Portfolio-API`) and click **Create**.
5. Wait a few moments, then ensure your new project is selected in the top dropdown.

## Step 2: Enable the Google Drive API
1. In the Cloud Console search bar (top), type **Google Drive API** and select it.
2. Click the blue **Enable** button.
3. This tells Google Cloud that this specific project is allowed to interact with Google Drive.

## Step 3: Create a Service Account
1. Using the left-hand navigation menu (hamburger icon), navigate to **IAM & Admin** > **Service Accounts**.
2. Click **+ Create Service Account** at the top.
3. Provide a name (e.g., `portfolio-bot`) and a description. Click **Create and Continue**.
4. *Optional*: You can skip the "Grant this service account access to project" steps. Just click **Done**.

## Step 4: Generate the Credentials Key
This key is the "password" your script will use. **Treat it like a real password.**

1. On the Service Accounts page, click the **Email address** of the account you just created.
2. Go to the **KEYS** tab.
3. Click **Add Key** > **Create new key**.
4. Choose **JSON** format and click **Create**.
5. A `.json` file will automatically download to your computer.
6. **Rename this file** to exactly `credentials.json`.
7. **Move this file** into the root directory of your cloned repository (next to `README.md`).

> [!CAUTION]
> **Security Warning:** NEVER commit `credentials.json` to GitHub or share it publicly. If someone gets this file, they can access any Google Drive folders you have shared with the Service Account. This repository is pre-configured to ignore this file via `.gitignore`, but you must never force-add it.

## Next Steps
Now that you have your "bot user" (the Service Account email address) and its keys (`credentials.json`), you are ready to set up your Google Drive folders.

➡️ Proceed to **[Part 2: Google Drive Setup](2_google_drive_setup.md)**
