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

        if (lastTabName === "ALL PHOTOS") {
            currentImages = portfolioData.all_images || getAllImages(portfolioData.tabs);
        } else if (lastTabName.includes('/')) {
            // Child tab key format: "PARENT/CHILD"
            const [parentKey, childKey] = lastTabName.split('/');
            const parentTab = portfolioData.tabs.find(t => t.category.toUpperCase() === parentKey);
            const child = parentTab?.children?.find(c => c.category.toUpperCase() === childKey);
            currentImages = child ? child.images : (parentTab ? parentTab.images : []);
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

function setActiveTab(categoryKey) {
    // Clear all active states on both parent nav-items and child nav-child-items
    document.querySelectorAll('.nav-item, .nav-child-item').forEach(item => {
        item.classList.remove('active');
    });
    // Clear active state from parent rows too (controls caret tinting)
    document.querySelectorAll('.nav-parent-row').forEach(row => {
        row.classList.remove('active');
    });

    // Set active on matching item
    document.querySelectorAll('.nav-item, .nav-child-item').forEach(item => {
        if (item.dataset.categoryKey === categoryKey) {
            item.classList.add('active');
            // If this is a child item, mark the parent row active too
            const parentRow = item.closest('.nav-group')?.querySelector('.nav-parent-row');
            if (parentRow) parentRow.classList.add('active');
            // Mobile UX: scroll active tab into view
            item.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        }
    });
}

// --- 2. Navigation Sidebar Rendering ---

function renderTabs(tabs) {
    tabsContainer.innerHTML = '';

    // "All Photos" tab — always first
    const allImages = portfolioData.all_images || getAllImages(tabs);
    const allTab = createFlatTabElement('ALL PHOTOS', 'ALL PHOTOS', allImages);
    tabsContainer.appendChild(allTab);

    tabs.forEach(tab => {
        if (tab.has_children && tab.children && tab.children.length > 0) {
            // Build a collapsible group for this parent category (desktop-only)
            const group = createGroupedTabElement(tab);
            tabsContainer.appendChild(group);
        } else {
            // Standard flat tab
            const tabEl = createFlatTabElement(
                tab.category,
                tab.category.toUpperCase(),
                tab.images
            );
            tabsContainer.appendChild(tabEl);
        }
    });
}

/** Creates a standard flat nav-item anchor */
function createFlatTabElement(categoryKey, displayLabel, images) {
    const a = document.createElement('a');
    a.href = '#';
    a.className = 'nav-item';
    a.textContent = displayLabel.toUpperCase();
    a.dataset.categoryKey = categoryKey.toUpperCase();

    a.addEventListener('click', e => {
        e.preventDefault();
        localStorage.setItem('activeTabCategory', categoryKey.toUpperCase());
        setActiveTab(categoryKey.toUpperCase());
        currentImages = images;
        renderGallery(true);
    });

    return a;
}

/** Creates a collapsible nav group: parent row + caret toggle + child dropdown */
function createGroupedTabElement(tab) {
    const group = document.createElement('div');
    group.className = 'nav-group';

    // --- Parent row ---
    const parentRow = document.createElement('div');
    parentRow.className = 'nav-parent-row';

    const parentLink = document.createElement('a');
    parentLink.href = '#';
    parentLink.className = 'nav-item';
    parentLink.textContent = tab.category.toUpperCase();
    parentLink.dataset.categoryKey = tab.category.toUpperCase();

    // Clicking parent shows ALL its images (own + all children)
    parentLink.addEventListener('click', e => {
        e.preventDefault();
        const key = tab.category.toUpperCase();
        localStorage.setItem('activeTabCategory', key);
        setActiveTab(key);
        currentImages = tab.images;
        renderGallery(true);
        // Auto-expand children when parent is clicked
        toggleChildren(toggleBtn, childrenContainer, true);
    });

    // --- Caret toggle button ---
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'nav-toggle-btn';
    toggleBtn.setAttribute('aria-label', `Expand ${tab.category}`);
    toggleBtn.innerHTML = `<svg width="12" height="12" viewBox="0 0 12 12" fill="none"
        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="4,2 8,6 4,10"></polyline>
    </svg>`;

    // --- Children container ---
    const childrenContainer = document.createElement('div');
    childrenContainer.className = 'nav-children-container';

    tab.children.forEach(child => {
        const childLink = document.createElement('a');
        childLink.href = '#';
        childLink.className = 'nav-child-item';
        childLink.textContent = child.category.toUpperCase();
        childLink.dataset.categoryKey = `${tab.category.toUpperCase()}/${child.category.toUpperCase()}`;

        childLink.addEventListener('click', e => {
            e.preventDefault();
            const key = `${tab.category.toUpperCase()}/${child.category.toUpperCase()}`;
            localStorage.setItem('activeTabCategory', key);
            setActiveTab(key);
            currentImages = child.images;
            renderGallery(true);
        });

        childrenContainer.appendChild(childLink);
    });

    // Toggle logic
    toggleBtn.addEventListener('click', e => {
        e.stopPropagation();
        toggleChildren(toggleBtn, childrenContainer);
    });

    parentRow.appendChild(parentLink);
    parentRow.appendChild(toggleBtn);
    group.appendChild(parentRow);
    group.appendChild(childrenContainer);

    return group;
}

function toggleChildren(btn, container, forceOpen) {
    const shouldOpen = forceOpen !== undefined ? forceOpen : !btn.classList.contains('expanded');
    if (shouldOpen) {
        btn.classList.add('expanded');
        container.classList.add('open');
    } else {
        btn.classList.remove('expanded');
        container.classList.remove('open');
    }
}


// --- 3. Gallery Rendering & Pagination ---

let currentColumnCount = 0;
let columnElements = [];
let columnHeights = [];

function getTargetColumnCount() {
    const width = window.innerWidth;
    if (width <= 480) return 1;
    if (width <= 768) return 2;
    return 3;
}

function createColumnContainers(colCount) {
    galleryContainer.innerHTML = '';
    columnElements = [];
    columnHeights = new Array(colCount).fill(0);
    currentColumnCount = colCount;

    for (let i = 0; i < colCount; i++) {
        const col = document.createElement('div');
        col.className = 'gallery-col';
        galleryContainer.appendChild(col);
        columnElements.push(col);
    }
}

function getAspectHeight(image) {
    if (image.width && image.height) {
        return image.height / image.width;
    }
    return 1.25;
}

// --- Video Playback & Viewport Observer ---
let activeVideoController = null;

const PLAY_ICON_SVG = `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
    <polygon points="5 3 19 12 5 21 5 3"></polygon>
</svg>`;

const PAUSE_ICON_SVG = `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
    <rect x="6" y="4" width="4" height="16"></rect>
    <rect x="14" y="4" width="4" height="16"></rect>
</svg>`;

const MUTE_ICON_SVG = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
    <line x1="23" y1="9" x2="17" y2="15"></line>
    <line x1="17" y1="9" x2="23" y2="15"></line>
</svg>`;

const UNMUTE_ICON_SVG = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
    <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
</svg>`;

const videoViewportObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (!entry.isIntersecting || entry.intersectionRatio < 0.25) {
            const controller = entry.target._videoController;
            if (controller && controller.isPlaying) {
                controller.pause();
            }
        }
    });
}, { threshold: [0, 0.25, 0.5] });

function createGalleryItemElement(image) {
    const item = document.createElement('div');
    item.className = 'gallery-item';

    const safeSrc = encodeURI(image.path);
    const driveUrl = image.drive_url || safeSrc;
    const isVideo = image.media_type === 'video';
    const isGif = image.media_type === 'gif';

    if (isVideo) {
        // Video element
        const video = document.createElement('video');
        video.src = safeSrc;
        video.preload = 'metadata';
        video.loop = true;
        video.muted = true;
        video.playsInline = true;

        if (image.width && image.height) {
            video.style.aspectRatio = `${image.width} / ${image.height}`;
        }

        // Auto-adapt to actual video dimensions once metadata loads
        video.addEventListener('loadedmetadata', () => {
            if (video.videoWidth && video.videoHeight) {
                video.style.aspectRatio = `${video.videoWidth} / ${video.videoHeight}`;
            }
        });

        // Top-Right Idle Media Badge
        const badge = document.createElement('div');
        badge.className = 'gallery-media-badge';
        badge.innerHTML = `<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
        </svg> <span>VIDEO</span>`;
        item.appendChild(badge);

        // Top-Right Action Buttons
        const actions = document.createElement('div');
        actions.className = 'gallery-actions-overlay';

        // 1. Play/Pause button
        const playBtn = document.createElement('button');
        playBtn.className = 'gallery-action-btn gallery-btn-play';
        playBtn.title = "Play video";
        playBtn.setAttribute('aria-label', "Play video");
        playBtn.innerHTML = PLAY_ICON_SVG;

        // 2. Audio Mute/Unmute button
        const audioBtn = document.createElement('button');
        audioBtn.className = 'gallery-action-btn gallery-btn-audio';
        audioBtn.title = "Unmute audio";
        audioBtn.setAttribute('aria-label', "Unmute audio");
        audioBtn.innerHTML = MUTE_ICON_SVG;

        // 3. Drive Link button
        const linkBtn = document.createElement('button');
        linkBtn.className = 'gallery-action-btn gallery-btn-link';
        linkBtn.title = "View in Google Drive";
        linkBtn.setAttribute('aria-label', "View in Google Drive");
        linkBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
            <polyline points="15 3 21 3 21 9"></polyline>
            <line x1="10" y1="14" x2="21" y2="3"></line>
        </svg>`;
        linkBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            window.open(driveUrl, '_blank');
        });

        // Scrubber / Progress Bar
        const scrubber = document.createElement('div');
        scrubber.className = 'gallery-video-scrubber';
        const progressFill = document.createElement('div');
        progressFill.className = 'gallery-video-progress-fill';
        scrubber.appendChild(progressFill);

        // Controller logic
        const controller = {
            isPlaying: false,
            play() {
                // Pause any other currently playing video
                if (activeVideoController && activeVideoController !== controller) {
                    activeVideoController.pause();
                }
                activeVideoController = controller;
                video.play().then(() => {
                    controller.isPlaying = true;
                    item.classList.add('is-playing');
                    playBtn.title = "Pause video";
                    playBtn.setAttribute('aria-label', "Pause video");
                    playBtn.innerHTML = PAUSE_ICON_SVG;
                }).catch(() => {});
            },
            pause() {
                video.pause();
                controller.isPlaying = false;
                item.classList.remove('is-playing');
                playBtn.title = "Play video";
                playBtn.setAttribute('aria-label', "Play video");
                playBtn.innerHTML = PLAY_ICON_SVG;
                if (activeVideoController === controller) {
                    activeVideoController = null;
                }
            },
            toggle() {
                if (controller.isPlaying) {
                    controller.pause();
                } else {
                    controller.play();
                }
            }
        };

        playBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            controller.toggle();
        });

        audioBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            video.muted = !video.muted;
            if (video.muted) {
                audioBtn.title = "Unmute audio";
                audioBtn.setAttribute('aria-label', "Unmute audio");
                audioBtn.innerHTML = MUTE_ICON_SVG;
            } else {
                video.volume = 1.0;
                audioBtn.title = "Mute audio";
                audioBtn.setAttribute('aria-label', "Mute audio");
                audioBtn.innerHTML = UNMUTE_ICON_SVG;
            }
        });

        // Time progress update
        video.addEventListener('timeupdate', () => {
            if (video.duration) {
                const pct = (video.currentTime / video.duration) * 100;
                progressFill.style.width = `${pct}%`;
            }
        });

        // Seeking via scrubber click & scrub
        const seek = (e) => {
            e.stopPropagation();
            const rect = scrubber.getBoundingClientRect();
            const pos = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
            if (video.duration) {
                video.currentTime = pos * video.duration;
            }
        };
        scrubber.addEventListener('click', seek);

        actions.appendChild(playBtn);
        actions.appendChild(audioBtn);
        actions.appendChild(linkBtn);
        item.appendChild(actions);
        item.appendChild(scrubber);

        // Clicking the video item directly also toggles playback
        item.addEventListener('click', () => {
            controller.toggle();
        });

        item.appendChild(video);

        // Register with viewport observer for auto-pause on scroll
        item._videoController = controller;
        videoViewportObserver.observe(item);

    } else {
        // Image / GIF element
        const img = document.createElement('img');
        img.src = safeSrc;
        img.alt = image.name;
        img.loading = 'lazy';

        // Automatic retry if request drops
        let retries = 0;
        img.onerror = () => {
            if (retries < 3) {
                retries++;
                setTimeout(() => {
                    img.src = `${safeSrc}?retry=${Date.now()}`;
                }, 300 * retries);
            }
        };

        if (image.width && image.height) {
            img.style.aspectRatio = `${image.width} / ${image.height}`;
        }

        if (image.drive_url) {
            img.style.cursor = 'pointer';
            img.title = "Click to view in Google Drive";
        }

        if (isGif) {
            const badge = document.createElement('div');
            badge.className = 'gallery-media-badge';
            badge.textContent = 'GIF';
            item.appendChild(badge);
        }

        item.addEventListener('click', () => {
            window.open(driveUrl, '_blank');
        });

        item.appendChild(img);
    }

    if (image.date) {
        const overlay = document.createElement('div');
        overlay.className = 'gallery-date-overlay';
        const dateSpan = document.createElement('span');
        dateSpan.className = 'gallery-date-text';
        dateSpan.textContent = image.date;
        overlay.appendChild(dateSpan);
        item.appendChild(overlay);
    }

    return item;
}

function balanceBatchAcrossColumns(batch, colCount, initialHeights) {
    const colAssignments = Array.from({ length: colCount }, () => []);
    let simulatedHeights = [...initialHeights];

    // Phase 1: Greedy placement based on shortest column
    for (let j = 0; j < batch.length; j++) {
        const img = batch[j];
        let shortestCol = 0;
        for (let c = 1; c < colCount; c++) {
            if (simulatedHeights[c] < simulatedHeights[shortestCol]) {
                shortestCol = c;
            }
        }
        colAssignments[shortestCol].push(img);
        simulatedHeights[shortestCol] += getAspectHeight(img);
    }

    // Phase 2: Local search optimization (swaps & transfers)
    // Iteratively checks all column pairs to minimize (max_height - min_height)
    let improved = true;
    let iterations = 0;
    const maxIterations = 30;

    while (improved && iterations < maxIterations) {
        improved = false;
        iterations++;

        const currentSpread = Math.max(...simulatedHeights) - Math.min(...simulatedHeights);
        let bestMove = null;
        let bestSpread = currentSpread;

        for (let c1 = 0; c1 < colCount; c1++) {
            for (let c2 = c1 + 1; c2 < colCount; c2++) {
                // 1. Try 1-to-1 item swaps between columns c1 and c2
                for (let i = 0; i < colAssignments[c1].length; i++) {
                    for (let j = 0; j < colAssignments[c2].length; j++) {
                        const h1 = getAspectHeight(colAssignments[c1][i]);
                        const h2 = getAspectHeight(colAssignments[c2][j]);
                        const diff = h1 - h2;

                        const testHeights = [...simulatedHeights];
                        testHeights[c1] -= diff;
                        testHeights[c2] += diff;

                        const testSpread = Math.max(...testHeights) - Math.min(...testHeights);
                        if (testSpread < bestSpread - 0.01) {
                            bestSpread = testSpread;
                            bestMove = { type: 'swap', c1, i, c2, j, testHeights };
                        }
                    }
                }

                // 2. Try transferring an item from column with more items to column with fewer
                if (colAssignments[c1].length > colAssignments[c2].length) {
                    for (let i = 0; i < colAssignments[c1].length; i++) {
                        const h = getAspectHeight(colAssignments[c1][i]);
                        const testHeights = [...simulatedHeights];
                        testHeights[c1] -= h;
                        testHeights[c2] += h;
                        const testSpread = Math.max(...testHeights) - Math.min(...testHeights);
                        if (testSpread < bestSpread - 0.01) {
                            bestSpread = testSpread;
                            bestMove = { type: 'move', fromCol: c1, itemIdx: i, toCol: c2, testHeights };
                        }
                    }
                } else if (colAssignments[c2].length > colAssignments[c1].length) {
                    for (let j = 0; j < colAssignments[c2].length; j++) {
                        const h = getAspectHeight(colAssignments[c2][j]);
                        const testHeights = [...simulatedHeights];
                        testHeights[c2] -= h;
                        testHeights[c1] += h;
                        const testSpread = Math.max(...testHeights) - Math.min(...testHeights);
                        if (testSpread < bestSpread - 0.01) {
                            bestSpread = testSpread;
                            bestMove = { type: 'move', fromCol: c2, itemIdx: j, toCol: c1, testHeights };
                        }
                    }
                }
            }
        }

        if (bestMove) {
            if (bestMove.type === 'swap') {
                const temp = colAssignments[bestMove.c1][bestMove.i];
                colAssignments[bestMove.c1][bestMove.i] = colAssignments[bestMove.c2][bestMove.j];
                colAssignments[bestMove.c2][bestMove.j] = temp;
            } else if (bestMove.type === 'move') {
                const [item] = colAssignments[bestMove.fromCol].splice(bestMove.itemIdx, 1);
                colAssignments[bestMove.toCol].push(item);
            }
            simulatedHeights = bestMove.testHeights;
            improved = true;
        }
    }

    // Sort items in each column by their original batch index to preserve natural vertical flow
    for (let c = 0; c < colCount; c++) {
        colAssignments[c].sort((a, b) => a._batchIndex - b._batchIndex);
    }

    return colAssignments;
}

function renderBatch(batch) {
    batch.forEach((img, idx) => {
        img._batchIndex = idx;
    });

    if (currentColumnCount <= 1) {
        batch.forEach(image => {
            const item = createGalleryItemElement(image);
            columnElements[0].appendChild(item);
            columnHeights[0] += getAspectHeight(image);
        });
    } else {
        const assignments = balanceBatchAcrossColumns(batch, currentColumnCount, columnHeights);
        for (let c = 0; c < currentColumnCount; c++) {
            assignments[c].forEach(image => {
                const item = createGalleryItemElement(image);
                columnElements[c].appendChild(item);
                columnHeights[c] += getAspectHeight(image);
            });
        }
    }
}

function renderGallery(reset = false) {
    // If resetting (e.g. switching tabs), clear container and reset columns
    if (reset) {
        renderedCount = 0;
        const targetCols = getTargetColumnCount();
        createColumnContainers(targetCols);

        const existingBtn = document.getElementById('load-more-btn');
        if (existingBtn) existingBtn.remove();
    }

    if (currentImages.length === 0) {
        galleryContainer.innerHTML = '<div id="loading-message">No photos found in this category.</div>';
        updateLoadMoreButton();
        return;
    }

    // Ensure columns exist if not already initialized
    if (columnElements.length === 0) {
        createColumnContainers(getTargetColumnCount());
    }

    // Determine slice range for pagination
    const start = renderedCount;
    const end = Math.min(renderedCount + PAGE_SIZE, currentImages.length);
    const batch = currentImages.slice(start, end);

    renderBatch(batch);

    renderedCount = end;
    updateLoadMoreButton();
}

function updateLoadMoreButton() {
    let btnContainer = document.getElementById('pagination-container');
    if (!btnContainer) {
        btnContainer = document.createElement('div');
        btnContainer.id = 'pagination-container';
        btnContainer.style.textAlign = 'center';
        btnContainer.style.padding = '20px';
        galleryContainer.parentNode.insertBefore(btnContainer, galleryContainer.nextSibling);
    }

    btnContainer.innerHTML = '';

    if (renderedCount < currentImages.length) {
        const btn = document.createElement('button');
        btn.id = 'load-more-btn';
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

// Window resize listener: if the number of columns changes, re-distribute already-rendered images
let resizeDebounceTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeDebounceTimeout);
    resizeDebounceTimeout = setTimeout(() => {
        const targetCols = getTargetColumnCount();
        if (targetCols !== currentColumnCount && renderedCount > 0 && currentImages.length > 0) {
            const countToKeep = renderedCount;
            createColumnContainers(targetCols);

            for (let s = 0; s < countToKeep; s += PAGE_SIZE) {
                const batch = currentImages.slice(s, Math.min(s + PAGE_SIZE, countToKeep));
                renderBatch(batch);
            }
            renderedCount = countToKeep;
            updateLoadMoreButton();
        }
    }, 150);
});

// Start the process when the page loads
fetchAndRender();