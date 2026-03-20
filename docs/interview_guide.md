# 🎓 Project Interview Guide

> **Project Name**: Serverless Photography Portfolio
> **Tech Stack**: Python (Build Scripts, CLI Wizard), Google Drive API, HTML/CSS/JS (Frontend), Cloudflare Pages (Hosting).

This guide is designed to help you explain this project confidently in technical interviews. It covers the **Architecture**, **Data Flow**, and **Key Engineering Decisions**.

---

## 🏗 High-Level Architecture

**"I built a static site generator (SSG) that turns a Google Drive folder into a high-performance portfolio website with zero server maintenance."**

### The Pipeline
1.  **Data Source (CMS)**: Google Drive acts as the Content Management System. You drag-and-drop folders ("Nature", "Travel") and photos there.
2.  **Ingestion (`scripts/sync_from_drive.py`)**: A Python script authenticates via a Service Account, scans the Drive structure, and downloads new photos locally. It also records "Deep Links" (Google Drive web view links) for high-res access.
3.  **Optimization (`scripts/optimize_images.py`)**: A processing pipeline converts raw images (like Apple's HEIC format) into web-optimized JPGs using the `Pillow` library, ensuring fast load times.
4.  **Build (`scripts/generate_site.py`)**: Generates the static assets. It builds a `data.json` index of all photos, performs **build-time randomization** for variety, and injects user config into the HTML templates.
5.  **Deployment**: The final `site/` folder is pushed to GitHub, triggering an automatic Cloudflare Pages deployment.

---

## ⚔️ Technical Challenges & Solutions (Interview Gold)

**Q: Why didn't you just fetch images from Google Drive API directly in the browser?**
> **A:** "I initially considered Client-Side Rendering (CSR). However, Google Drive's API has strict rate limits. If 100 people visited the site at once, the API would return `429 Too Many Requests`. Also, the images on Drive are full-resolution (5MB+), which would make the site extremely slow.
>
> **My Solution**: I moved the fetching to **Build Time** (Static Site Generation approach). We download and optimize once on the local machine. The users only download tiny, static JPGs from Cloudflare's CDN. It scales infinitely, is completely free, and gets 100/100 on Lighthouse performance scores."

**Q: How do you handle large numbers of photos on the frontend?**
> **A:** "To prevent enormous DOM trees and massive initial network payloads, I implemented **Client-Side Pagination**. The JavaScript fetches the `data.json` index, but only renders the first 12 images. A 'Load More' button progressively injects the next chunk into the DOM. This keeps the initial render virtually instant."

**Q: How did you handle randomizing the 'All Photos' gallery?**
> **A:** "I had to decide between *Client-Side* vs *Build-Time* randomization. If I shuffled the array in JavaScript on page load, the layout would jump around during rendering, and it adds CPU overhead to the client device. I chose **Build-Time Randomization** in Python. The `generate_site.py` script shuffles the master list and bakes it into `data.json`. The order remains stable for a given deployment but refreshes every time the site is built."

**Q: How do you handle configuration for other users?**
> **A:** "I decoupled the code from the data to make the project an open-source template. I built an **Interactive Python Setup Wizard** (`scripts/setup_wizard.py`) with a CLI interface. It safely guides non-technical users through connecting their Drive ID and automatically moves their sensitive `credentials.json` into a `.gitignore`'d directory, preventing disastrous secret leaks to GitHub."

---

## 🗣️ Mock Interview Q&A

**Interviewer**: Tell me about this project.
**You**: "It's a serverless portfolio engine. I wanted to build something that combines the ease of storing photos on Google Drive with the performance of a static website. I built a Python ETL (Extract, Transform, Load) pipeline that syncs photos from Drive, converts Apple's HEIC format to optimized JPGs, and deploys a paginated static site to Cloudflare."

**Interviewer**: What was the hardest bug?
**You**: "Handling relative paths in the build scripts. When moving scripts to a `scripts/` subfolder, file references broke (`FileNotFoundError`) depending on where the terminal command was run. I refactored the scripts to use `os.path.abspath(__file__)` to programmatically determine the root directory, making the tooling robust regardless of the user's current working directory."

**Interviewer**: How would you scale this?
**You**: "Right now, the build is local. To scale, I would move the build scripts to **GitHub Actions**. I would store the Google Drive credentials securely in GitHub Secrets, and set up a cron job (scheduled task) to run the sync script every night. This way, the site updates automatically entirely in the cloud, closing the automation loop."
