import { app, BrowserWindow, shell } from "electron";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DEV_SERVER_URL = new URL("http://localhost:5173/");
const DEV_SERVER_ORIGIN = DEV_SERVER_URL.origin;
const isMac = process.platform === "darwin";
const isWindows = process.platform === "win32";

let mainWindow = null;

// Windows-specific tuning for a smooth always-on-top overlay experience.
if (isWindows) {
  app.setAppUserModelId("com.gewn.desktop");
  app.commandLine.appendSwitch("disable-backgrounding-occluded-windows", "true");
  app.commandLine.appendSwitch("disable-features", "CalculateNativeWinOcclusion");
}

// Enforce a single running instance for a stable desktop assistant runtime.
const gotLock = app.requestSingleInstanceLock();
if (!gotLock) {
  app.quit();
} else {
  app.on("second-instance", () => {
    if (!mainWindow) {
      return;
    }
    if (mainWindow.isMinimized()) {
      mainWindow.restore();
    }
    mainWindow.show();
    mainWindow.focus();
  });
}

const createWindow = () => {
  // Transparent, frameless overlay window optimized for desktop assistant UX.
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    minWidth: 640,
    minHeight: 360,
    show: false,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    fullscreenable: false,
    resizable: true,
    movable: true,
    skipTaskbar: true,
    backgroundColor: "#00000000",
    autoHideMenuBar: true,
    hasShadow: false,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webviewTag: false,
      safeDialogs: true,
      backgroundThrottling: false,
      devTools: !app.isPackaged,
    },
  });

  // Keep the overlay above other windows, including fullscreen apps.
  mainWindow.setAlwaysOnTop(true, "screen-saver");
  mainWindow.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true });

  // Load the React frontend (Vite dev server).
  mainWindow.loadURL(DEV_SERVER_URL.href);

  // Show only when ready to avoid white flashes with transparent windows.
  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
    mainWindow.focus();
    if (isMac) {
      app.dock.hide();
    }
  });

  // Allow drag regions to be defined in the renderer via CSS:
  // `-webkit-app-region: drag` on the desired overlay handle.

  // Prevent new windows and route external links to the OS browser.
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith(DEV_SERVER_ORIGIN)) {
      return { action: "allow" };
    }
    shell.openExternal(url);
    return { action: "deny" };
  });
  mainWindow.webContents.on("will-navigate", (event, url) => {
    if (!url.startsWith(DEV_SERVER_ORIGIN)) {
      event.preventDefault();
      shell.openExternal(url);
    }
  });

  // Retry if the dev server isn't ready yet.
  mainWindow.webContents.on("did-fail-load", () => {
    if (!mainWindow) {
      return;
    }
    setTimeout(() => {
      if (mainWindow) {
        mainWindow.loadURL(DEV_SERVER_URL.href);
      }
    }, 1000);
  });

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
};

app.whenReady().then(() => {
  createWindow();

  // macOS behavior: re-create a window when the dock icon is clicked.
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    } else if (mainWindow) {
      mainWindow.show();
      mainWindow.focus();
    }
  });
});

app.on("window-all-closed", () => {
  if (!isMac) {
    app.quit();
  }
});
