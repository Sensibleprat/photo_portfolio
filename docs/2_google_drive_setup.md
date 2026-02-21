# Part 2: Google Drive Structure & Sharing

The beauty of this architecture is that Google Drive acts as your CMS (Content Management System). You don't need to log into a complex dashboard to manage your portfolio—just drag, drop, and organize folders.

## Step 1: Create Your Master Folder
1. Open [Google Drive](https://drive.google.com/).
2. Create a new master folder for your website (e.g., `My Portfolio Website`).
3. This is the root boundary. The script will *only* look inside this folder.

## Step 2: Create Category Subfolders
The script automatically generates your website's navigation tabs based on the folders you create here.

1. Inside your master folder, create subfolders grouping your work.
   - Example: `Portraits`, `Landscapes`, `Street`, `Weddings`.
2. **Upload your photos** (JPG, PNG, or HEIC) into their respective categories.

> [!TIP]
> **Architect's Insight: Naming Conventions** 
> The names of these folders exactly dictate the names of the tabs on your website. Keep them short and descriptive. The script handles sorting your photos automatically.

## Step 3: Share the Folder with the Service Account
Right now, the Service Account we created in Part 1 is a stranger; it cannot see your personal Drive files. We must explicitly invite it.

1. Open the `credentials.json` file you downloaded in Part 1 using any text editor.
2. Find the `"client_email"` field. It will look something like this:
   `portfolio-bot@your-project-id.iam.gserviceaccount.com`
3. Copy this entire email address.
4. Go back to Google Drive, right-click your master folder (`My Portfolio Website`), and select **Share**.
5. Paste the Service Account email address into the "Add people and groups" field.
6. Uncheck "Notify people" (bots don't read emails).
7. Give it **Viewer** access (it only needs to read the photos, not write them).
8. Click **Share**.

## Step 4: Obtain the Folder ID
The local script needs to know *exactly* which folder to pull from.

1. Double-click to open your master folder (`My Portfolio Website`) in Google Drive.
2. Look at the URL in your browser's address bar. It will look like this:
   `https://drive.google.com/drive/folders/1KtAZreDObnIKpNf-Z-HYMFIjfiejqRp-`
3. Copy the long string of letters, numbers, and hyphens at the end of the URL.
   *(In the example above, the ID is `1KtAZreDObnIKpNf-Z-HYMFIjfiejqRp-`)*.
4. Keep this ID handy; you will paste it into your configuration file in the next setup phase.

## Next Steps
Your cloud infrastructure is fully configured. Now, we will connect the codebase to this folder so it can pull the photos and generate the website.

➡️ Proceed to **[Part 3: Local Configuration & Build](3_local_configuration.md)**
