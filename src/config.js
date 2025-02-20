// src/config.js
const config = {
  development: {
    baseURL: 'http://localhost:5003'
  },
  production: {
    baseURL: '//200.31.175.88:5003'
    // baseURL: 'http://localhost:5003'
  }
};

const environment = process.env.NODE_ENV || 'development';
console.log(`Current baseURL is: ${config[environment].baseURL}`);

export default config;
