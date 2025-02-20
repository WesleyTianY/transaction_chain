import axios from 'axios';
import config from '../config';

const baseURL = config[process.env.NODE_ENV].baseURL;

async function fetchTransactionChains(query_date) {
  const response = await axios.get(`${baseURL}/api/get_transaction_chains`, {
    params: {
      query_date: query_date
    }
  });
  console.log('response.data.bondSummaryData', response.data);
  return response;
}

export { fetchTransactionChains };
