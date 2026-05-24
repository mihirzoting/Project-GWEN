import { contextBridge } from "electron";

// Expose a minimal, read-only surface for the renderer.
const api = Object.freeze({
  platform: process.platform,
  versions: Object.freeze({
    electron: process.versions.electron,
    chrome: process.versions.chrome,
    node: process.versions.node,
  }),
});

contextBridge.exposeInMainWorld("gewn", api);