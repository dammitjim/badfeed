const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
    pages: {
        reader: {
            entry: "src/reader/main.js",
            template: "public/index.html",
            chunks: ["chunk-vendors", "chunk-common", "reader"]
        },
        globalStyles: {
            entry: "src/styles/entry.js",
            chunks: ["chunk-vendors", "chunk-common", "globalStyles"]
        }
    },

    baseUrl: process.env.NODE_ENV === "production" ? "/static/" : "http://localhost:8080/",

    devServer: {
        publicPath: "http://localhost:8080/",
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
            "Access-Control-Allow-Headers": "X-Requested-With, content-type, Authorization",
            "Access-Control-Allow-Credentials": "true"
        }
    },

    configureWebpack: config => {
        const filename =
            process.env.NODE_ENV === "production"
                ? "../webpack-stats-prod.json"
                : "../webpack-stats-dev.json";

        config.plugins.push(new BundleTracker({ filename }));
    }
};