# Fix CORS_ORIGINS Error

## Problem
You're getting this error:
```
pydantic_settings.exceptions.SettingsError: error parsing value for field "CORS_ORIGINS" from source "DotEnvSettingsSource"
```

This happens because there's an **empty or invalid `CORS_ORIGINS`** entry in your `backend/.env` file.

## Quick Fix

**Option 1: Remove CORS_ORIGINS from .env (Recommended)**

1. Open `backend/.env` file
2. Find the line that says `CORS_ORIGINS=` (might be empty)
3. **Delete that line** or comment it out with `#`
4. The app will use default values: `http://localhost:3000,http://localhost:5173`

**Option 2: Set a valid value**

If you want to customize CORS origins, set it in your `backend/.env` file as:

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

Or as JSON:
```env
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

## After Fixing

1. Try running the backend again:
   ```bash
   cd backend
   python run.py
   ```

2. The error should be gone!

## Also: Install Missing Dependencies

You also need to install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

The error `ModuleNotFoundError: No module named 'motor'` means dependencies aren't installed.

