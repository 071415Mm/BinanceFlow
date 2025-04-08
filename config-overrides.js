const path = require('path');

module.exports = function override(config) {
  config.output.publicPath = path.resolve(__dirname, 'frontend/public');
  return config;
};
