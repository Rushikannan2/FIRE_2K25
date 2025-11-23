# CryptoQ Project Guide

## 📍 PostgreSQL Database Configuration

### Where is the PostgreSQL Render Link Configured?

The PostgreSQL database connection is **NOT hardcoded** in the project files. Instead, it's configured through **environment variables** on Render.com. This is the secure and recommended approach.

#### Location in Code:
- **File**: `CryptoQWeb/CryptoQWeb/settings.py`
- **Lines**: 97-104
- **Configuration**:
  ```python
  DATABASES = {
      'default': dj_database_url.config(
          default='sqlite:///db.sqlite3',
          conn_max_age=600,
          ssl_require=False,
      )
  }
  ```

#### How It Works:
1. **On Render.com**: The `DATABASE_URL` environment variable is automatically set by Render when you create a PostgreSQL database service
2. **In Production**: Django automatically reads `DATABASE_URL` from environment variables
3. **Local Development**: Falls back to SQLite (`db.sqlite3`) if `DATABASE_URL` is not set

#### Where to Find/Modify the Database URL:
1. **Render Dashboard**:
   - Go to https://render.com
   - Navigate to your PostgreSQL database service
   - Click on "Connections" or "Info" tab
   - Copy the "Internal Database URL" or "External Database URL"
   - Format: `postgresql://username:password@host:port/database_name`

2. **Environment Variables on Render**:
   - Go to your Web Service on Render
   - Navigate to "Environment" tab
   - Look for `DATABASE_URL` variable
   - This is automatically linked if you connected the database to your web service

#### Important Notes:
- ✅ **Never commit** database credentials to Git
- ✅ The database URL is stored securely in Render's environment variables
- ✅ Local development uses SQLite, production uses PostgreSQL automatically
- ✅ No code changes needed when database URL changes

---

## 🔧 How to Make Modifications Safely

### Best Practices for Safe Development

#### 1. **Use Git Branches**
Always create a new branch before making changes:
```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push origin feature/your-feature-name

# Create a Pull Request on GitHub to merge safely
```

#### 2. **Test Locally First**
Always test changes locally before deploying:
```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Run migrations (if database changes)
python manage.py makemigrations
python manage.py migrate

# Start development server
python manage.py runserver

# Test your changes at http://localhost:8000
```

#### 3. **Environment Variables**
Never hardcode sensitive values. Use environment variables:

**In `settings.py`**:
```python
# ✅ GOOD - Uses environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-for-dev-only')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
DATABASE_URL = os.environ.get('DATABASE_URL')  # Auto-configured by Render

# ❌ BAD - Hardcoded values
SECRET_KEY = 'my-secret-key-12345'
DEBUG = True
```

**On Render.com**:
- Go to your Web Service → Environment tab
- Add/modify environment variables there
- Never commit `.env` files with real credentials

#### 4. **Database Migrations**
When modifying models, always create migrations:
```bash
# Create migration files
python manage.py makemigrations

# Review the migration files in sentiment/migrations/
# Make sure they look correct

# Apply migrations locally first
python manage.py migrate

# Test that everything works

# Commit migration files
git add sentiment/migrations/
git commit -m "Add database migrations for [feature]"

# On Render, migrations run automatically during deployment
```

#### 5. **Static Files**
When adding/modifying static files (CSS, JS, images):
```bash
# Add files to CryptoQWeb/static/ directory
# Example: CryptoQWeb/static/images/new-image.jpg

# Collect static files (for production)
python manage.py collectstatic --noinput

# Test locally that files load correctly
# Commit the static files
git add CryptoQWeb/static/
git commit -m "Add new static files"
```

#### 6. **Dependencies**
When adding new Python packages:
```bash
# Install the package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Review requirements.txt to ensure it's correct
# Remove any unnecessary packages

# Commit the updated requirements.txt
git add requirements.txt
git commit -m "Add package-name dependency"
```

#### 7. **Deployment Checklist**
Before pushing to production:
- [ ] All changes tested locally
- [ ] No hardcoded secrets or credentials
- [ ] Database migrations created and tested
- [ ] Static files collected (if modified)
- [ ] Requirements.txt updated (if new packages added)
- [ ] Code follows project style
- [ ] No debug print statements left in code
- [ ] Environment variables set on Render (if new ones needed)

#### 8. **Rollback Plan**
If something goes wrong:
```bash
# Revert to previous commit
git revert HEAD

# Or checkout previous version
git checkout <previous-commit-hash>

# Push the revert
git push origin main
```

On Render, you can also:
- Go to Deploys tab
- Click on a previous successful deployment
- Click "Rollback to this deploy"

---

## 🚀 Deployment Workflow

### Standard Deployment Process:

1. **Make Changes Locally**
   ```bash
   git checkout -b feature/new-feature
   # Make your changes
   ```

2. **Test Locally**
   ```bash
   python manage.py runserver
   # Test all functionality
   ```

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "Clear description of changes"
   ```

4. **Push to GitHub**
   ```bash
   git push origin feature/new-feature
   ```

5. **Create Pull Request** (Optional but recommended)
   - Go to GitHub
   - Create Pull Request
   - Review changes
   - Merge to main branch

6. **Automatic Deployment**
   - Render automatically detects changes to main branch
   - Builds and deploys the new version
   - Runs migrations automatically
   - Collects static files automatically

7. **Verify Deployment**
   - Check Render logs for any errors
   - Visit your app URL
   - Test critical functionality

---

## 🔐 Security Best Practices

1. **Never Commit Secrets**:
   - ✅ Use environment variables
   - ❌ Never commit `.env` files
   - ❌ Never hardcode passwords, API keys, or secrets

2. **Database Security**:
   - Database URL is automatically managed by Render
   - Never expose database credentials in code
   - Use connection pooling (already configured with `conn_max_age=600`)

3. **Debug Mode**:
   - Always set `DEBUG=False` in production (on Render)
   - Only use `DEBUG=True` for local development

4. **Secret Key**:
   - Generate a strong secret key for production
   - Store it in Render environment variables
   - Never commit it to Git

---

## 📝 Common Modification Scenarios

### Adding a New Page/View:
1. Create view in `sentiment/views.py`
2. Add URL pattern in `sentiment/urls.py` or `CryptoQWeb/urls.py`
3. Create template in `sentiment/templates/sentiment/`
4. Test locally
5. Commit and push

### Modifying Models:
1. Edit model in `sentiment/models.py`
2. Create migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`
4. Test locally
5. Commit model and migration files
6. Push (migrations run automatically on Render)

### Adding Static Files:
1. Add files to `CryptoQWeb/static/` directory
2. Reference in templates: `{% load static %}` then `{% static 'path/to/file' %}`
3. Test locally
4. Commit static files
5. Push (collectstatic runs automatically on Render)

### Updating Dependencies:
1. Install package: `pip install package-name`
2. Update requirements.txt: `pip freeze > requirements.txt`
3. Test locally
4. Commit requirements.txt
5. Push (Render installs from requirements.txt automatically)

---

## 🆘 Troubleshooting

### Database Connection Issues:
- Check `DATABASE_URL` environment variable on Render
- Verify database service is running
- Check connection limits

### Static Files Not Loading:
- Run `python manage.py collectstatic` locally to test
- Check `STATIC_ROOT` and `STATIC_URL` in settings.py
- Verify WhiteNoise middleware is enabled

### Migration Errors:
- Check migration files for conflicts
- Try: `python manage.py migrate --fake-initial`
- Review migration history: `python manage.py showmigrations`

### Build Failures on Render:
- Check build logs in Render dashboard
- Verify requirements.txt is correct
- Check Python version in `runtime.txt`
- Ensure all dependencies are listed

---

## 📚 Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Render Documentation**: https://render.com/docs
- **Git Best Practices**: https://git-scm.com/doc
- **Project README**: See `README.md` for project-specific information

---

## ✅ Summary

**PostgreSQL Configuration:**
- Configured via `DATABASE_URL` environment variable on Render
- Automatically handled by `dj_database_url.config()` in `settings.py`
- No hardcoded credentials in code
- Local development uses SQLite automatically

**Safe Modification Process:**
1. Create a branch
2. Make changes
3. Test locally
4. Commit changes
5. Push to GitHub
6. Render auto-deploys
7. Verify deployment

**Key Principles:**
- ✅ Always test locally first
- ✅ Use environment variables for secrets
- ✅ Create migrations for database changes
- ✅ Use Git branches for features
- ✅ Never commit credentials
- ✅ Follow the deployment checklist

---

*Last Updated: [Current Date]*
*Maintained by: CryptoQ Development Team*

