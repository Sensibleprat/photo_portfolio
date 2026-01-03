// Global variables
let portfolioData = {};
let currentImages = []; // Images for the currently active tab
let renderedCount = 0;  // How many images are currently shown
const PAGE_SIZE = 12;   // Number of images to load per batch

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

        // Use pre-shuffled "all_images" if available, otherwise fallback
        if (lastTabName === "ALL PHOTOS") {
            currentImages = portfolioData.all_images || getAllImages(portfolioData.tabs);
        } else {
            const tab = portfolioData.tabs.find(t => t.category.toUpperCase() === lastTabName);
            currentImages = tab ? tab.images : [];
        }

        renderGallery(true); // true = reset
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
            // Mobile UX: Scroll active tab into view
            item.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        }
    });
}

// --- 2. Navigation Sidebar Rendering ---

function renderTabs(tabs) {
    tabsContainer.innerHTML = '';

    // "All Photos" uses the pre-shuffled list from data.json if available
    const allImages = portfolioData.all_images || getAllImages(tabs);
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

    a.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.setItem('activeTabCategory', categoryName.toUpperCase());
        setActiveTab(categoryName.toUpperCase());

        // Update current context and reset gallery
        currentImages = images;
        renderGallery(true);
    });

    return a;
}

// --- 3. Gallery Rendering & Pagination ---

function renderGallery(reset = false) {
    // If resetting, clear container and counters
    if (reset) {
        galleryContainer.innerHTML = '';
        renderedCount = 0;

        // Remove existing "Load More" button if any
        const existingBtn = document.getElementById('load-more-btn');
        if (existingBtn) existingBtn.remove();
    }

    if (currentImages.length === 0) {
        galleryContainer.innerHTML = '<div id="loading-message">No photos found in this category.</div>';
        return;
    }

    // Determine slice range
    const start = renderedCount;
    const end = Math.min(renderedCount + PAGE_SIZE, currentImages.length);
    const batch = currentImages.slice(start, end);

    // Render batch
    batch.forEach(image => {
        const item = document.createElement('div');
        item.className = 'gallery-item';

        const img = document.createElement('img');
        img.src = image.path;
        img.alt = image.name;
        img.loading = 'lazy';

        if (image.drive_url) {
            img.style.cursor = 'pointer';
            img.title = "Click to view in Google Drive";
        }

        item.addEventListener('click', () => {
            const url = image.drive_url || image.path;
            window.open(url, '_blank');
        });

        item.appendChild(img);
        galleryContainer.appendChild(item);
    });

    renderedCount = end;

    // Manage "Load More" Button
    updateLoadMoreButton();
}

function updateLoadMoreButton() {
    // Try to find helper container or create one
    let btnContainer = document.getElementById('pagination-container');
    if (!btnContainer) {
        btnContainer = document.createElement('div');
        btnContainer.id = 'pagination-container';
        btnContainer.style.textAlign = 'center';
        btnContainer.style.padding = '20px';
        // Insert after gallery container
        galleryContainer.parentNode.insertBefore(btnContainer, galleryContainer.nextSibling);
    }

    btnContainer.innerHTML = ''; // Clear

    if (renderedCount < currentImages.length) {
        const btn = document.createElement('button');
        btn.textContent = 'LOAD MORE';
        btn.style.padding = '12px 30px';
        btn.style.fontSize = '14px';
        btn.style.letterSpacing = '1px';
        btn.style.cursor = 'pointer';
        btn.style.backgroundColor = '#333';
        btn.style.color = 'white';
        btn.style.border = 'none';
        btn.style.borderRadius = '4px';

        btn.addEventListener('click', () => {
            renderGallery(false);
        });

        btnContainer.appendChild(btn);
    }
}


// Start the process when the page loads
fetchAndRender();