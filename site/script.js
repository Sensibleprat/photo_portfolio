// Global variable to hold all portfolio data
let portfolioData = {};
const tabsContainer = document.getElementById('tabs-container');
const galleryContainer = document.getElementById('gallery-container');

// --- 1. Data Fetching and Initialization ---

async function fetchAndRender() {
    try {
        const response = await fetch('data.json');
        portfolioData = await response.json();

        renderTabs(portfolioData.tabs);

        // Persistence Logic
        const lastTabName = localStorage.getItem('activeTabCategory') || "ALL PHOTOS";
        let initialImages = getAllImages(portfolioData.tabs);

        if (lastTabName !== "ALL PHOTOS") {
            const tab = portfolioData.tabs.find(t => t.category.toUpperCase() === lastTabName);
            if (tab) initialImages = tab.images;
        }

        renderGallery(initialImages);
        setActiveTab(lastTabName);

    } catch (error) {
        console.error("Error loading portfolio data:", error);
        galleryContainer.innerHTML = '<div style="padding: 50px; text-align: center; color: red;">Failed to load portfolio. Make sure data.json exists.</div>';
    }
}

// Helper functions
function getAllImages(tabs) {
    let allImages = [];
    tabs.forEach(tab => {
        allImages = allImages.concat(tab.images);
    });
    return allImages;
}

function setActiveTab(categoryName) {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.textContent === categoryName) {
            item.classList.add('active');
        }
    });
}

// --- 2. Navigation Sidebar Rendering ---

function renderTabs(tabs) {
    tabsContainer.innerHTML = '';

    const allImages = getAllImages(tabs);
    const allTab = createTabElement("ALL PHOTOS", allImages);
    tabsContainer.appendChild(allTab);

    tabs.forEach(tab => {
        const tabElement = createTabElement(tab.category, tab.images);
        tabsContainer.appendChild(tabElement);
    });
}

function createTabElement(categoryName, images) {
    const a = document.createElement('a');
    a.href = "#";
    a.className = 'nav-item';
    a.textContent = categoryName.toUpperCase();

    // Event listener for persistence
    a.addEventListener('click', (e) => {
        e.preventDefault();

        localStorage.setItem('activeTabCategory', categoryName.toUpperCase());
        setActiveTab(categoryName.toUpperCase());
        renderGallery(images);
    });

    return a;
}

// --- 3. Gallery Rendering ---

function renderGallery(images) {
    galleryContainer.innerHTML = '';

    if (images.length === 0) {
        galleryContainer.innerHTML = '<div id="loading-message">No photos found in this category.</div>';
        return;
    }

    images.forEach(image => {
        const item = document.createElement('div');
        item.className = 'gallery-item';

        const img = document.createElement('img');

        // Use local path instead of Google Drive link
        img.src = image.path;
        img.alt = image.name;
        img.loading = 'lazy'; // Enable lazy loading for performance

        // Open Drive link on click if available
        if (image.drive_url) {
            img.style.cursor = 'pointer';
            img.title = "Click to view in Google Drive";
        }

        // Open full-resolution image in new tab (same path for now)
        item.addEventListener('click', () => {
            if (image.drive_url) {
                window.open(image.drive_url, '_blank');
            } else {
                window.open(image.path, '_blank');
            }
        });

        item.appendChild(img);
        galleryContainer.appendChild(item);
    });
}


// Start the process when the page loads
fetchAndRender();