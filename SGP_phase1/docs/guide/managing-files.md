# 🗑️ Managing Files

*Page 7 of 16: Learn the Basics → Managing Files*

[← Previous: Downloading](/guide/downloading) | [Next: How It Works →](/architecture)

---

Learn how to organize and delete files in ShareJadPi.

## Viewing Files

All uploaded files appear in the "Uploaded Files" section with:
- 📄 **Filename**
- 📊 **File size**
- 📅 **Upload date**
- 🔽 **Download button**
- 🗑️ **Delete button**

---

## Deleting Files

### From Web Interface

1. Find the file you want to delete
2. Click the **Delete** button (🗑️)
3. Confirm the deletion
4. File removed immediately

### From File System

Files are stored at: `~/ShareJadPi-Dev/uploads/`

You can also:
- Delete files directly from this folder
- Copy files to other locations
- Organize in subfolders (manual)

---

## Storage Management

### Check Storage

```bash
# Mac/Linux
du -sh ~/ShareJadPi-Dev/uploads

# Windows
dir "C:\Users\YourName\ShareJadPi-Dev\uploads"
```

### Clean Up Old Files

Regularly delete files you no longer need to free up space.

---

[Continue to Architecture →](/architecture){.cta-button}
