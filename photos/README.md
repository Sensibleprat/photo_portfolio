# Photos Directory

This is where you organize your photography portfolio!

## How to Use

1. **Create category folders** - Each folder becomes a navigation tab on your website
   ```
   photos/
   ├── Nature/
   ├── Street/
   ├── Portraits/
   ├── Landscape/
   └── Urban/
   ```

2. **Add your photos** - Place photos inside the category folders
   ```
   photos/
   ├── Nature/
   │   ├── sunset.jpg
   │   ├── forest.jpg
   │   └── mountains.jpg
   └── Street/
       ├── city_life.jpg
       └── people.jpg
   ```

3. **Run the scripts**
   ```bash
   python optimize_images.py  # Optimizes images for web
   python generate_site.py    # Generates website
   ```

## Tips

- **Folder names** become tab names (e.g., "Nature", "Street Photography")
- Use descriptive names for better organization
- Supported formats: JPG, PNG, HEIC, WebP
- **Note**: This folder is `gitignored`. The photos here are downloaded from your Google Drive when you run `./deploy.sh` (or `python scripts/sync_from_drive.py`).
- Original photos stay here; optimized versions go to `optimized/`

## Example Structure

```
photos/
├── Wayanad/
│   ├── IMG_3277.jpg
│   ├── IMG_3024.jpg
│   └── IMG_3045.jpg
├── Ooty/
│   ├── IMG_3900.jpg
│   └── IMG_4192.jpg
└── Pondi/
    ├── beach_sunset.jpg
    └── old_town.jpg
```

Happy organizing! 📸
