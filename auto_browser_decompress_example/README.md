# Auto-Decompression Support for Godot Game Files

If your hosting platform or browser supports auto-decompression, you can use this example. In this case, the browser decompresses the file but does not replace the filename.

For example: your browser auto-decompresses `index.wasm.br`, but the filename remains `index.wasm.br` after decompression.

---

## Overview

Only **6 changes** are required, all in the `.js` file.

### 1. Update Preload Promise Block

Find this block:
```javascript
return this.loadPromise(pathOrBuffer, fileSize).then(function (buf) {
    me.preloadedFiles.push({
        path: destPath || pathOrBuffer,
        buffer: buf,
    });
    return Promise.resolve();
});
```

Replace it with:
```javascript
return this.loadPromise(pathOrBuffer, fileSize).then(function (buf) {
    if (pathOrBuffer.endsWith(".br")) {
        pathOrBuffer = pathOrBuffer.replace(".br", "");
    }
    me.preloadedFiles.push({
        path: destPath || pathOrBuffer,
        buffer: buf,
    });
    return Promise.resolve();
});
```

---

### 2. Update `Engine.load` Function

Find this block:
```javascript
Engine.load = function (basePath, size) {
    if (loadPromise == null) {
        loadPath = basePath;
        loadPromise = preloader.loadPromise(`${loadPath}.wasm`, size, true);
        requestAnimationFrame(preloader.animateProgress);
    }
    return loadPromise;
};
```

Replace it with:
```javascript
Engine.load = function (basePath, size) {
    if (loadPromise == null) {
        loadPath = basePath;
        loadPromise = preloader.loadPromise(`${loadPath}.wasm.br`, size, true);
        requestAnimationFrame(preloader.animateProgress);
    }
    return loadPromise;
};
```

---

### 3. Adjust File Paths in Preload Loop

Find this block:
```javascript
for (const file of preloader.preloadedFiles) {
    me.rtenv['copyToFS'](file.path, file.buffer);
}
```

Replace it with:
```javascript
for (const file of preloader.preloadedFiles) {
    file.path = file.path.replace(".br", "");
    me.rtenv['copyToFS'](file.path, file.buffer);
    // console.log(file.path, file.buffer);
}
```

---

### 4. Update Initialization and Preload Calls

Find this block:
```javascript
this.init(exe),
this.preloadFile(pack, pack),
```

Replace it with:
```javascript
this.init(exe),
this.preloadFile(pack + ".br", pack + ".br"),
```

---

## Summary

These changes ensure that:
- Auto-decompressed files are correctly processed without `.br` in their filenames.
- Game initialization and file preloading work seamlessly with Brotli-compressed files.

Test your changes and enjoy improved loading with Brotli support!
