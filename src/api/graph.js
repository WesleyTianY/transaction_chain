import axios from 'axios';
import config from '../config';

const baseURL = config[process.env.NODE_ENV].baseURL;

export async function sheetdata2Graphdata(csvdata) {
  const dataToSend = {
    graph: csvdata
  };

  try {
    const response = await fetch(`${baseURL}/api/instnRelationGraph`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dataToSend)
    });

    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }

    const data = await response.json();
    return data.received_data; // 返回处理后的数据
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
    throw error; // 抛出错误以便调用者处理
  }
}
