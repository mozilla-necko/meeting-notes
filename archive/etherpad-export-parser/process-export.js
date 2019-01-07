const Changeset = require("./Changeset");

if (process.argv.length != 3) {
  console.error("bad usage: nodejs process-export.js <etherpad-lite-exported-file>\n");
  process.exit(1);
}

let dump = require(process.argv[2]);

// Filter all of the keys that are a revision
let revs = Object.keys(dump).filter(key => key.includes(":revs:"));

// Initial text is always just a newline
let text = "\n";

const fs = require("fs");

for (let i = 0; i < revs.length; i++) {
  // this is the text just after applying revision i
  text = Changeset.applyToText(dump[revs[i]].changeset, text);

  // Filtering logic goes here
  // We dump out all of the "stable" revisions - ie that don't change for at
  // least 24 hours

  if (i == revs.length - 1 || dump[revs[i+1]].meta.timestamp > dump[revs[i]].meta.timestamp + 24*60*60*1000) {
    let date = new Date(dump[revs[i]].meta.timestamp).toISOString().substring(0,10);
    console.log(date);
    fs.writeFileSync(date+".txt", `${date}\n\n${text}`);
  }
}
