# How do get a performance profile from an xpcshell run

```bash
MOZ_PROFILER_STARTUP='1' MOZ_PROFILER_STARTUP_INTERVAL='1' \
MOZ_PROFILER_STARTUP_ENTRIES='134217728' \
MOZ_PROFILER_STARTUP_FEATURES='markersallthreads,flows,screenshots,js,stackwalk,cpu,processcpu,bandwidth,memory' \
MOZ_PROFILER_STARTUP_FILTERS='Cache2 I/O,Compositor,DNS Resolver,DOM Worker,GeckoMain,Renderer,Socket Thread,StreamTrans,SwComposite,TRR Background' \
MOZ_PROFILER_SHUTDOWN=/tmp/profile.json MOZ_PROFILER_SYMBOLICATE=1 \
./mach test network/test/unit/test_trr.js
```

You'll get an unsymbolicated profile.
In order to add C++ symbols for your obj folder, you can use samply.

```bash
# install samply
cargo install --locked samply
# load the profile generated from the xpcshell run
samply load /tmp/profile.json
```

Now load http://127.0.0.1:3000 - if page doesn't load in a minute or so, a page refresh might fix it.
The loaded profile will now contain the local symbols, and can be uploaded.

# Flows

Copy the path of the profiler URL. For example for https://profiler.firefox.com/public/bjts21vnqdn1xnvqtjy0dg6bcyab5eq2yabr4y8/ the path would be `/public/bjts...`

Load https://deploy-preview-5190--perf-html.netlify.app + path above
