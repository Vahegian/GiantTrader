const exp = require('express');
const server = exp();
const { app, BrowserWindow, Menu } = require("electron");


server.listen(9999, () => console.log("serving static files on port '9999'"))
server.use(exp.static('web'))








// Electron stuff

Menu.setApplicationMenu(null);


function boot(){
	let mainWindow = new BrowserWindow({
		width:1200,
		height:800,
		skipTaskbar: true,
		toolbar: false
	});
	
	mainWindow.loadURL('http://0.0.0.0:10003')
	// Uncomment to use developer tools
	mainWindow.webContents.openDevTools({detach:true});

	mainWindow.on('closed', function() {
		mainWindow = null;
	});
}

app.on('ready', boot);
