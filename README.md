# branded

A repository for creating branded videos.

## Sample Video

This repository includes a sample branded video (`sample_video.mp4`) that demonstrates basic video branding capabilities.

### Video Specifications
- **Duration:** 5 seconds
- **Resolution:** 1280x720 (HD)
- **Format:** MP4 (H.264)
- **Content:** Blue background with "BRANDED" title and "Sample Video" subtitle in white text

### Creating Custom Branded Videos

You can create your own branded videos using ffmpeg. Here's the command used to generate the sample video:

```bash
ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=5 \
  -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='BRANDED':fontsize=120:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-50,\
       drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='Sample Video':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+80" \
  -c:v libx264 -pix_fmt yuv420p -y sample_video.mp4
```

### Customization Options

You can customize:
- **Background color:** Change `color=c=blue` to any color (e.g., `red`, `green`, `#FF5733`)
- **Duration:** Modify `d=5` to change video length in seconds
- **Resolution:** Adjust `s=1280x720` to your desired resolution
- **Text:** Change `text='BRANDED'` and `text='Sample Video'` to your own branding
- **Font size:** Modify `fontsize=120` and `fontsize=48` values
- **Text color:** Change `fontcolor=white` to any color