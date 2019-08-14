require("dotenv").config();
const AWS = require("aws-sdk");
const fs = require("fs");

// Configure client for use with Spaces
const spacesEndpoint = new AWS.Endpoint(process.env.SPACES_ROOT);
const s3 = new AWS.S3({
    endpoint: spacesEndpoint,
    accessKeyId: process.env.AWS_ACCESS_KEY,
    secretAccessKey: process.env.AWS_SECRET_KEY
});

fs.readFile("../webpack-stats-prod.json", (err, data) => {
    if (err) {
        console.error(err);
        return;
    }
    const parsed = JSON.parse(data);
    for (const chunkName in parsed.chunks) {
        parsed.chunks[chunkName].forEach(chunk => {
            fs.readFile(chunk.path, (err, data) => {
                if (err) {
                    console.error(err);
                    return;
                }
                const params = {
                    Body: data,
                    Bucket: "feedzerto",
                    Key: chunk.name
                };
                s3.putObject(params, (err, data) => {
                    if (err) {
                        console.error(err);
                        return;
                    }
                    console.log(data);
                });
            });
        });
    }
});
