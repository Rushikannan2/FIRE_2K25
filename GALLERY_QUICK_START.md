# Quick Start: Adding Gallery Photos

## Simple 3-Step Process

### Step 1: Add Images to Assets Folder
```
CryptoQWeb/assets/FIRE_2025_Photo1.jpg
CryptoQWeb/assets/FIRE_2025_Photo2.jpg
CryptoQWeb/assets/FIRE_2025_Photo3.jpg
```

### Step 2: Copy to Static Images Folder
```powershell
# From project root (D:\CryptoQ)
Copy-Item "CryptoQWeb\assets\FIRE_2025_*.jpg" "CryptoQWeb\static\images\" -Force
```

### Step 3: Uncomment Image Blocks in gallery.html
Open `CryptoQWeb/sentiment/templates/sentiment/gallery.html` and uncomment the example image blocks, then replace the image names with your actual image filenames.

## Example: Adding Your First Photo

1. **Place photo**: `CryptoQWeb/assets/FIRE_2025_Conference.jpg`

2. **Copy it**: 
   ```powershell
   Copy-Item "CryptoQWeb\assets\FIRE_2025_Conference.jpg" "CryptoQWeb\static\images\" -Force
   ```

3. **In gallery.html**, uncomment and modify:
   ```html
   <div class="col-md-6 col-lg-4 mb-4">
       <div class="gallery-image-container text-center">
           <picture>
               <source srcset="{% static 'images/FIRE_2025_Conference.jpg' %}" type="image/jpeg">
               <img src="{% static 'images/FIRE_2025_Conference.jpg' %}"
                    alt="FIRE 2025 Conference" 
                    class="img-fluid rounded shadow-lg"
                    loading="lazy">
           </picture>
           <p class="gallery-caption">FIRE 2025 Conference - IIT BHU Varanasi</p>
       </div>
   </div>
   ```

4. **Hide placeholder** (optional): Add `style="display: none;"` to the `#galleryPlaceholder` div when you add images.

## That's It! 
Your images will render exactly like the IIIT Kottayam certificate - same styling, same responsive behavior, same Django static file system.

