// Prism Local Server 测试脚本

// 记录页面加载开始时间
const startTime = performance.now();

// 页面加载完成后执行
window.addEventListener('DOMContentLoaded', () => {
    // 更新CSS测试状态
    const cssTest = document.getElementById('css-test');
    if (cssTest) {
        cssTest.textContent = '✅ CSS样式加载';
        cssTest.style.color = 'green';
    }
    
    // 更新JS测试状态
    const jsTest = document.getElementById('js-test');
    if (jsTest) {
        jsTest.textContent = '✅ JavaScript加载';
        jsTest.style.color = 'green';
    }
    
    // 显示当前时间
    const updateTime = () => {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('zh-CN');
        const timeElement = document.getElementById('time');
        if (timeElement) {
            timeElement.textContent = timeStr;
        }
    };
    
    updateTime();
    setInterval(updateTime, 1000);
    
    // 显示页面加载时间
    const loadTime = performance.now() - startTime;
    const loadTimeElement = document.getElementById('load-time');
    if (loadTimeElement) {
        loadTimeElement.textContent = `${loadTime.toFixed(2)}ms`;
    }
    
    console.log('✅ Prism Local Server 测试页面加载完成');
    console.log(`⏱️ 加载时间: ${loadTime.toFixed(2)}ms`);
});
