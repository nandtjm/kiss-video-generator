from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def add_watermark(input_path, output_path):
    clip = VideoFileClip(input_path)
    txt = TextClip("Free KissPreview", fontsize=24, color='white').set_position(("center","bottom")).set_duration(clip.duration)
    result = CompositeVideoClip([clip, txt])
    result.write_videofile(output_path, codec='libx264', fps=clip.fps)
    return output_path
