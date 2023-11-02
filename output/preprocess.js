const fs = require('fs');
const file_path = process.argv[2];
// const path = './bluepie.ad_silence.apk/utg.js';
const utg = require(file_path);
// 将对象转换为JSON字符串
const jsonString = JSON.stringify(utg, null, 2);

// 将JSON字符串保存到文件中
fs.writeFile('info.json', jsonString, 'utf8', (err) => {
    if (err) {
        console.error('Error writing JSON file:', err);
    } else {
        console.log('JSON file has been saved as info.json.');
    }
});