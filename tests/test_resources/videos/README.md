# 测试视频资源说明

## 需要准备的测试视频

请在此目录下放置以下测试视频：

1. **test-video.mp4** - 用于测试 HTTP Range Request 功能（建议大小：50MB 以上）

## 如何准备测试视频

### 方法 1：下载免费测试视频
访问以下网站下载免费测试视频：
- https://sample-videos.com/
- https://test-videos.co.uk/
- https://filesamples.com/formats/mp4

推荐下载：
- Big Buck Bunny (60MB+)
- Sintel (100MB+)

### 方法 2：使用 FFmpeg 生成测试视频
```powershell
# 生成 60 秒的测试视频（约 50MB）
ffmpeg -f lavfi -i testsrc=duration=60:size=1920x1080:rate=30 -pix_fmt yuv420p test-video.mp4
```

### 方法 3：使用现有视频
- 找任意 MP4 视频文件（建议 > 50MB）
- 重命名为 `test-video.mp4`
- 确保视频时长 > 30 秒（方便测试拖拽）

## 测试目的

测试 HTTP Range Request 功能：
- 视频能否正常播放
- 拖拽进度条时是否发送 Range 请求
- 服务器是否返回 206 Partial Content
- 拖拽后是否能立即播放（无需重新加载整个文件）

## 验证方法

1. 在浏览器中打开测试页面
2. 打开开发者工具（F12）→ Network 标签
3. 播放视频并拖拽进度条
4. 查看网络请求：
   - 请求头应包含：`Range: bytes=xxx-xxx`
   - 响应状态码应为：`206 Partial Content`
   - 响应头应包含：`Content-Range: bytes xxx-xxx/total`
