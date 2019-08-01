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
  configureWebpack: config => {
    const filename =
      process.env.NODE_ENV === "production"
        ? "../webpack-stats-prod.json"
        : "../webpack-stats-dev.json";

    config.plugins.push(new BundleTracker({ filename }));
  }
};
