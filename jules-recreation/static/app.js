const ws = new WebSocket(`ws://${window.location.host}/ws`);
const terminal = document.getElementById('terminal');
const taskInput = document.getElementById('task-input');
const runBtn = document.getElementById('run-btn');
const fileList = document.getElementById('file-list');
const codeViewer = document.getElementById('file-content');
const status = document.getElementById('status');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const div = document.createElement('div');
    div.classList.add(data.type);
    div.innerText = `[${data.type.toUpperCase()}] ${data.message}`;
    terminal.appendChild(div);
    terminal.scrollTop = terminal.scrollHeight;

    if (data.type === 'info' && data.message.includes('Task complete.')) {
        status.innerText = 'Ready';
        refreshFileList();
    }
};

runBtn.addEventListener('click', () => {
    const task = taskInput.value;
    if (task && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ task }));
        taskInput.value = '';
        status.innerText = 'Working...';
    }
});

async function refreshFileList() {
    const response = await fetch('/api/files');
    const data = await response.json();
    fileList.innerHTML = '';
    data.files.forEach(file => {
        const item = document.createElement('div');
        item.classList.add('file-item');
        item.innerText = file;
        item.onclick = () => viewFile(file);
        fileList.appendChild(item);
    });
}

async function viewFile(path) {
    const response = await fetch(`/api/read?path=${encodeURIComponent(path)}`);
    const data = await response.json();
    if (data.content) {
        codeViewer.innerText = data.content;
    } else {
        codeViewer.innerText = `Error: ${data.error}`;
    }
}

refreshFileList();
setInterval(refreshFileList, 5000); // Poll for file changes
