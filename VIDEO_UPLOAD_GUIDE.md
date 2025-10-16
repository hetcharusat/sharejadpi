# How to Add Videos to README on GitHub

GitHub doesn't support direct video file references from your repo. Videos must be uploaded to GitHub's CDN to display inline.

## Steps:

1. **Go to your GitHub repository** on the web: https://github.com/hetcharusat/sharejadpi

2. **Click on README.md** to view it

3. **Click the Edit (pencil) icon** in the top right

4. **Find the video placeholder lines** like:
   ```
   https://github.com/user-attachments/assets/YOUR_VIDEO_ID_HERE
   ```

5. **Drag and drop the video file** from your `vidss/` folder directly into the GitHub editor where the placeholder is

6. **GitHub will upload it and auto-generate a URL** like:
   ```
   https://user-images.githubusercontent.com/YOUR_USER_ID/123456789-abc123def456.mov
   ```

7. **Delete the placeholder line and keep the generated URL**

8. **Repeat for all 3 videos:**
   - `vidss/context-menu-share.mp4`
   - `vidss/open_sharejadpi.mp4`
   - `vidss/settings.mp4`

9. **Commit changes** at the bottom

## Result:

The videos will display as embedded players directly in your README! Users can click play without leaving the page.

## Example:

Before:
```markdown
https://github.com/user-attachments/assets/YOUR_VIDEO_ID_HERE
```

After drag-drop upload:
```markdown
https://user-images.githubusercontent.com/6877923/123006036-64e2e780-d3b7-11eb-922e-018994b32da5.mov
```

The video will automatically render as a player in the README!
