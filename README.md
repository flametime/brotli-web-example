This example show how to modify *.html and *.js files AFTER export the game to use Brotli-Wasm to decompress game files

if you want to jump-in - go to export demo and type in cmd :
python -m http.server 8000 
Go to http://localhost:8000 and test it

First of all - drop all files from "include_to_export" folder, to your folder with game files (icon, js, html etc.)

All instructions have images, in "changes_in_*" folders and demo with all changes in "brotli_export" folder

CHANGES IN HTML:

1. Open {project_name}.html and and add type="module" to {project_name}.js and script (Look at changes in html folder image)
2. Add "await load_b();" before engine creation

CHANGES IN {project_name}.js (in demo its "index.js"):
1. Add this to top of your *.js file 

var brotli = null;

window.load_b = async function () {
	brotli = await import("./brotli.js").then(m => m.default)
}

2. Find "loadFetch" func and add inside it (in top of func):

    if (file === "index.pck")
    {
        file += ".br"
    }

3. Find "if (typeof (WebAssembly.instantiateStreaming) !== 'undefined')"
and replace to :
var decompressed = await brotli.decompress(new Uint8Array(await r.arrayBuffer()));
WebAssembly.instantiateStreaming(Promise.resolve(new Response(decompressed, { 'headers': [['content-type', 'application/wasm']] })), imports).then(done);

4. Find "loadPromise = preloader.loadPromise(`${loadPath}.wasm`, size, true)" and add ".br" after ".wasm"

5. Find "return new Promise(async function (resolve, reject) {" and replace fucn block inside to :
for (const file of preloader.preloadedFiles) {
    //Push new data to engine
    var b = await file.buffer.arrayBuffer()
    me.rtenv['copyToFS'](file.path, b);
}

After everything is done - launch python compression script:
python compress.py

After compression you can remove original *.wasm and *.pck and launch :
python -m http.server 8000 
Go to http://localhost:8000 and test it

If you not sure about something - you can inspect example and look images

Have fun!