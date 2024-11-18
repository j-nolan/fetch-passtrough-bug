const fs = require("fs");
const { PassThrough } = require("stream");

async function run() {
  const readStream = fs.createReadStream("my-file.txt");

  //   const passThrough = new PassThrough();

  //   passThrough.on("data", (e) => {
  //     console.log("chunk length", e.length);
  //   });

  //   readStream.pipe(passThrough);

  const url = `http://localhost:8000`;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "text/plain",
    },
    // body: passThrough,
    body: readStream,
    duplex: "half",
  });

  console.log("response status:", response.status);
}

run();
