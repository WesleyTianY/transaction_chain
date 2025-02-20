import axios from 'axios';
import config from '../config';

const baseURL = config[process.env.NODE_ENV].baseURL;

async function getMarketPriceData(bond_cd) {
  try {
    const response = await axios.get(`${baseURL}/api/BasicData_MarketPrice/${bond_cd}`)
    const mktData = response.data.filtered_json_mkt
    return mktData
  } catch (error) {
    console.error('Error fetching market price data:', error)
    return []
  }
}
async function getTransactionDataTsne(bond_cd) {
  try {
    const response = await axios.get(`${baseURL}/api/BasicData_transaction_tsne/${bond_cd}`)
    const transactionData = response.data.filtered_json_transaction
    return transactionData
  } catch (error) {
    console.error('Error fetching market price data:', error)
    return []
  }
}
async function getYld_to_mrtyTsne(bond_cd) {
  try {
    const response = await axios.get(`${baseURL}/api/BasicData_yld_to_mrty_tsne/${bond_cd}`)
    const transactionData = response.data.filtered_json_transaction
    return transactionData
  } catch (error) {
    console.error('Error fetching market price data:', error)
    return []
  }
}
async function getTransactionData(bond_cd) {
  try {
    const response = await axios.get(`${baseURL}/api/BasicData_transaction/${bond_cd}`)
    const transactionData = response.data.filtered_json_transaction
    return transactionData
  } catch (error) {
    console.error('Error fetching market price data:', error)
    return []
  }
}
async function getYld_to_mrty(bond_cd) {
  try {
    const response = await axios.get(`${baseURL}/api/BasicData_transaction/${bond_cd}`)
    const transactionData = response.data.filtered_json_transaction
    return transactionData
  } catch (error) {
    console.error('Error fetching market price data:', error)
    return []
  }
}
async function getTransactionHistoryData(instn_cd, type, bond_cd) {
  try {
    const response = await axios.get(`${baseURL}/api/transaction_history/${instn_cd}/${type}/${bond_cd}`);
    return response.data.json_transaction;
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
    throw error; // 抛出错误以便调用者处理
  }
}
async function getValuationData(bond_cd) {
  try {
    const response = await axios.get(`${baseURL}/api/BasicData_Valuation/${bond_cd}`)
    const valuationData = response.data.filtered_json_val
    return valuationData
  } catch (error) {
    console.error('Error fetching market price data:', error)
    return []
  }
}

export { getMarketPriceData, getTransactionDataTsne, getTransactionData, getYld_to_mrtyTsne, getYld_to_mrty, getTransactionHistoryData, getValuationData }
