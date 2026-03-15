// 测试JavaScript是否加载成功
document.addEventListener('DOMContentLoaded', function() {
    const jsTest = document.getElementById('js-test');
    if (jsTest) {
        jsTest.textContent = '✓ JavaScript加载成功！';
        jsTest.style.color = 'green';
        jsTest.style.fontWeight = 'bold';
    }
    
    console.log('✓ JavaScript运行正常');
    console.log('✓ 资源加载测试成功');
});
