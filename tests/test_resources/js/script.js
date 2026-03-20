// Prism Local Server 测试脚本

console.log('✅ JavaScript 文件加载成功！');

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM 加载完成');
    
    // 显示当前 URL
    const currentUrlElement = document.getElementById('currentUrl');
    if (currentUrlElement) {
        currentUrlElement.textContent = window.location.href;
    }
    
    // 显示用户代理
    const userAgentElement = document.getElementById('userAgent');
    if (userAgentElement) {
        userAgentElement.textContent = navigator.userAgent;
    }
    
    // 测试按钮点击事件
    const testButton = document.getElementById('testButton');
    const testResult = document.getElementById('testResult');
    
    if (testButton && testResult) {
        testButton.addEventListener('click', function() {
            const timestamp = new Date().toLocaleString('zh-CN');
            const randomNumber = Math.floor(Math.random() * 1000);
            
            testResult.innerHTML = `
                <div style="color: #28a745; font-weight: bold; margin-bottom: 10px;">
                    ✅ JavaScript 功能正常！
                </div>
                <div style="color: #555;">
                    <p><strong>测试时间：</strong>${timestamp}</p>
                    <p><strong>随机数：</strong>${randomNumber}</p>
                    <p><strong>浏览器：</strong>${getBrowserInfo()}</p>
                </div>
            `;
            
            console.log('✅ 测试按钮点击成功', { timestamp, randomNumber });
        });
    }
    
    // 检测资源加载状态
    checkResourcesLoaded();
    
    // 监听视频事件
    setupVideoMonitoring();
});

// 获取浏览器信息
function getBrowserInfo() {
    const ua = navigator.userAgent;
    let browserName = '未知浏览器';
    
    if (ua.indexOf('Chrome') > -1 && ua.indexOf('Edg') === -1) {
        browserName = 'Google Chrome';
    } else if (ua.indexOf('Edg') > -1) {
        browserName = 'Microsoft Edge';
    } else if (ua.indexOf('Firefox') > -1) {
        browserName = 'Mozilla Firefox';
    } else if (ua.indexOf('Safari') > -1) {
        browserName = 'Apple Safari';
    }
    
    return browserName;
}

// 检查资源加载状态
function checkResourcesLoaded() {
    const images = document.querySelectorAll('img');
    const videos = document.querySelectorAll('video');
    
    console.log(`📊 检测到 ${images.length} 个图片元素`);
    console.log(`📊 检测到 ${videos.length} 个视频元素`);
    
    images.forEach((img, index) => {
        img.addEventListener('load', function() {
            console.log(`✅ 图片 ${index + 1} 加载成功: ${img.src}`);
        });
        
        img.addEventListener('error', function() {
            console.error(`❌ 图片 ${index + 1} 加载失败: ${img.src}`);
        });
    });
    
    videos.forEach((video, index) => {
        video.addEventListener('loadedmetadata', function() {
            console.log(`✅ 视频 ${index + 1} 元数据加载成功: ${video.src}`);
            console.log(`   时长: ${video.duration.toFixed(2)} 秒`);
        });
        
        video.addEventListener('error', function() {
            console.error(`❌ 视频 ${index + 1} 加载失败: ${video.src}`);
        });
    });
}

// 监听视频播放事件（用于测试 Range Request）
function setupVideoMonitoring() {
    const videos = document.querySelectorAll('video');
    
    videos.forEach((video, index) => {
        // 监听 seeking 事件（拖拽进度条）
        video.addEventListener('seeking', function() {
            console.log(`🎬 视频 ${index + 1} 正在跳转到: ${video.currentTime.toFixed(2)} 秒`);
            console.log('   这应该触发 HTTP Range Request');
        });
        
        // 监听 seeked 事件（跳转完成）
        video.addEventListener('seeked', function() {
            console.log(`✅ 视频 ${index + 1} 跳转完成: ${video.currentTime.toFixed(2)} 秒`);
        });
        
        // 监听播放事件
        video.addEventListener('play', function() {
            console.log(`▶️ 视频 ${index + 1} 开始播放`);
        });
        
        // 监听暂停事件
        video.addEventListener('pause', function() {
            console.log(`⏸️ 视频 ${index + 1} 暂停播放`);
        });
    });
}

// 测试 AJAX 请求（可选）
function testAjaxRequest() {
    fetch(window.location.href)
        .then(response => {
            console.log('✅ AJAX 请求成功');
            console.log('   状态码:', response.status);
            console.log('   Content-Type:', response.headers.get('Content-Type'));
            return response.text();
        })
        .then(html => {
            console.log('   响应长度:', html.length, '字符');
        })
        .catch(error => {
            console.error('❌ AJAX 请求失败:', error);
        });
}

// 导出测试函数（供控制台调用）
window.prismTest = {
    testAjax: testAjaxRequest,
    getBrowserInfo: getBrowserInfo,
    checkResources: checkResourcesLoaded
};

console.log('💡 提示：可以在控制台调用 prismTest.testAjax() 测试 AJAX 请求');
