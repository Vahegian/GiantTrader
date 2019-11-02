const {app, BrowserWindow} = require('electron');

function boot(){
	win = new BrowserWindow();
}

app.on('ready', boot);
