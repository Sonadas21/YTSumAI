# FFmpeg Installation Guide for Windows

## Quick Install (Recommended)

### Option 1: Using winget (Windows 10/11)
```powershell
winget install ffmpeg
```
**Important:** After installation, **restart your terminal completely** for PATH changes to take effect.

### Option 2: Using Chocolatey
```powershell
choco install ffmpeg
```

### Option 3: Manual Installation

1. **Download FFmpeg:**
   - Go to: https://github.com/BtbN/FFmpeg-Builds/releases
   - Download: `ffmpeg-master-latest-win64-gpl.zip`

2. **Extract:**
   - Extract the ZIP file
   - Move the extracted folder to `C:\ffmpeg`

3. **Add to PATH:**
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Go to "Advanced" tab → "Environment Variables"
   - Under "System variables", find and select "Path"
   - Click "Edit" → "New"
   - Add: `C:\ffmpeg\bin`
   - Click OK on all dialogs

4. **Verify Installation:**
   - **Restart your terminal** (important!)
   - Run:
     ```bash
     ffmpeg -version
     ```
   - Should display FFmpeg version information

## Troubleshooting

### "ffmpeg command not found"
- FFmpeg is not in your PATH
- **Solution:** Restart terminal after installation, or manually add to PATH (see above)

### "Postprocessing: ffprobe and ffmpeg not found"
- This appears when downloading YouTube videos
- **Solution:** Install FFmpeg and restart terminal

### Still not working?
- Make sure you restarted your terminal/IDE after adding to PATH
- Verify PATH contains FFmpeg:
  ```powershell
  echo $env:Path
  # Should include C:\ffmpeg\bin or similar
  ```
- Try a fresh PowerShell window (admin mode)

## Verify It's Working

Test FFmpeg:
```bash
ffmpeg -version
ffprobe -version
```

Both commands should show version information without errors.

---

**Need help?** Check the main README.md troubleshooting section.
