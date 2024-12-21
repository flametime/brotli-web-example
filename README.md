# Brotli-Wasm Decompression for Godot Game Files

This guide demonstrates how to modify `.html` and `.js` files after exporting a Godot game to enable Brotli-Wasm decompression for game files.

---

## Quick Start

To jump right in, follow these steps:

1. Go to brotli_export folder.
2. Start a local server to test:
   ```bash
   python -m http.server 8000
   ```
   Visit [http://localhost:8000](http://localhost:8000) in your browser.

3. Game engine must start with *.br files.

For detailed instructions, see below. Example images are provided in the `changes_in_*` folders, and a complete demo is available in the `brotli_export` folder.

---

## Changes in HTML

1. **Add `type="module` to the `<script>` tag**:
   ```html
   <script type="module" src="{project_name}.js"></script>
   ```

2. **Add `type="module` to the inline `<script>` tag**:
   ```html
   <script type="module"></script>
   ```

3. **Insert `await load_b();` before the engine creation line**:
   ```html
   <script>
       await load_b();
       // Your engine initialization code
   </script>
   ```

For reference, see the images in the `changes_in_html` folder.

---

## Changes in `{project_name}.js`

1. **Add the Brotli loader function**:
   At the top of your `.js` file, include:
   ```javascript
   var brotli = null;

   window.load_b = async function () {
       brotli = await import("./brotli.js").then(m => m.default);
   };
   ```

2. **Modify the `loadFetch` function**:
   Add this at the beginning of the function:
   ```javascript
   if (file === "index.pck") {
       file += ".br";
   }
   ```

3. **Update WebAssembly instantiation**:
   Replace this block:
   ```javascript
   if (typeof (WebAssembly.instantiateStreaming) !== 'undefined') {
       // Replace this
   }
   ```
   With:
   ```javascript
   var decompressed = await brotli.decompress(new Uint8Array(await r.arrayBuffer()));
   WebAssembly.instantiateStreaming(Promise.resolve(new Response(decompressed, { 'headers': [['content-type', 'application/wasm']] })), imports).then(done);
   ```

4. **Update preloader path**:
   Find this line:
   ```javascript
   loadPromise = preloader.loadPromise(`${loadPath}.wasm`, size, true);
   ```
   Add `.br`:
   ```javascript
   loadPromise = preloader.loadPromise(`${loadPath}.wasm.br`, size, true);
   ```

5. **Replace the block in `Promise` function**:
   Locate this block:
   ```javascript
   return new Promise(async function (resolve, reject) {
       for (const file of preloader.preloadedFiles) {
        me.rtenv['copyToFS'](file.path, file.buffer);
        }
   });
   ```
   Replace it with:
   ```javascript
   for (const file of preloader.preloadedFiles) {
       var b = await file.buffer.arrayBuffer();
       me.rtenv['copyToFS'](file.path, b);
   }
   ```

For more clarity, refer to the `changes_in_js` folder.

---

## Compression Script

After applying the changes:

1. Run the Python compression script:
   ```bash
   python compress.py
   ```

2. Remove the original `.wasm` and `.pck` files.

3. Start the local server:
   ```bash
   python -m http.server 8000
   ```
   Test the changes at [http://localhost:8000](http://localhost:8000).

---

## Troubleshooting

If you encounter any issues, inspect the demo files and refer to the images provided in the `changes_in_*` folders.

---

## Have Fun!
Enjoy a more efficient, Brotli-compressed game loading experience!
