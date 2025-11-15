# Gallery Setup Guide - How to Add FIRE 2025 Photos

## Step-by-Step Instructions

### Step 1: Place Your Images in the Assets Folder
1. Put your FIRE 2025 photos in: `CryptoQWeb/assets/`
   - Example: `CryptoQWeb/assets/FIRE_2025_Photo1.jpg`
   - Example: `CryptoQWeb/assets/FIRE_2025_Photo2.jpg`
   - Example: `CryptoQWeb/assets/FIRE_2025_Presentation.jpg`
   - Example: `CryptoQWeb/assets/FIRE_2025_Demo.jpg`

### Step 2: Copy Images to Static Directory
Run this command in PowerShell (from project root):
```powershell
Copy-Item "CryptoQWeb\assets\FIRE_2025_*.jpg" "CryptoQWeb\static\images\" -Force
```

Or manually copy your images from `CryptoQWeb/assets/` to `CryptoQWeb/static/images/`

### Step 3: Update gallery.html Template
The gallery template will automatically display images using Django's static file system, just like the IIIT Kottayam certificate image.

### Step 4: Run collectstatic (for deployment)
```bash
cd CryptoQWeb
python manage.py collectstatic --noinput
```

## Image Naming Convention
Use descriptive names:
- `FIRE_2025_Conference.jpg`
- `FIRE_2025_Presentation.jpg`
- `FIRE_2025_Demo.jpg`
- `FIRE_2025_Poster.jpg`
- `FIRE_2025_Team.jpg`

## How It Works (Same Pattern as Other Images)

The gallery uses the **exact same pattern** as:
- `IIITKottayam_Summer_Internship.jpg` (in aboutauthor.html)
- `FIRE.jpg` (in aboutus.html)
- `CryptoQ.jpeg` (in home.html)
- `FlowDiagram.jpg` (in visualizations.html)

All images use: `{% static 'images/filename.jpg' %}`

## Template Pattern Example

```html
<picture>
    <source srcset="{% static 'images/FIRE_2025_Photo1.jpg' %}" type="image/jpeg">
    <img src="{% static 'images/FIRE_2025_Photo1.jpg' %}"
         alt="FIRE 2025 Conference Photo" 
         class="img-fluid rounded shadow-lg"
         style="width: 100%; max-width: 100%; height: auto; display: block !important; visibility: visible !important; margin: 0 auto; border-radius: 14px; box-shadow: 0 12px 36px rgba(0,0,0,0.28); object-fit: contain; border: 3px solid #0d6efd; background-color: #ffffff0d;"
         loading="lazy">
</picture>
```

