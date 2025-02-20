import axios from 'axios';
import config from '../config';

const baseURL = config[process.env.NODE_ENV].baseURL;

// async function setQueryDate(queryDate) {
//   try {
//     const response = await axios.post(`${baseURL}/api/set_query_date`, { query_date: queryDate });
//     return response
//   } catch (error) {
//     console.error('Error setting query date:', error);
//   }
// }

// 新增的 setQueryDate 函数，用于发送 POST 请求以设置 query_date
async function setQueryDate(queryDate) {
  try {
    const response = await axios.post(`${baseURL}/api/set_query_date`, {
      query_date: queryDate
    });
    console.log('Query date set response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error setting query date:', error);
    throw error;
  }
}

async function fetchColorMapping() {
  try {
    const response = await axios.get(`${baseURL}/api/color_mapping`);
    return response.data;
  } catch (error) {
    console.error('Error fetching color mapping:', error);
    throw error;
  }
}

export { fetchColorMapping, setQueryDate };
